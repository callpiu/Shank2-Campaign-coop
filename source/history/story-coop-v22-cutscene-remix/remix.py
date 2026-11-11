"""Remix the v0.9 BIK soundtracks using local TIGER-DnR stem estimates."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREVIOUS = ROOT / 'outputs/Shank2-StoryCoop-v0.9-CHS/patch'
SOURCE = PREVIOUS / 'payload/data/movies'
OUTPUT = HERE / 'remixed'
MODEL = HERE / 'tiger-mirror.onnx'
MODEL_SHA = '2189859ac7e89cf4d9d284c6f393e737aaa2b3233ed7ee424ad622012bce7bca'
sys.path[:0] = [str(HERE / 'tools'), str(HERE.parent / 'story-coop-v07-dialogue')]
if '--dml' in sys.argv:
    sys.path.insert(0, str(HERE / 'tools-dml'))
import numpy as np
import onnxruntime as ort
from batch_enhance import FF, decode, delay_and_snr, limit, mux, packets, save, sha

MODEL_RATE = 44100
RATE = 48000
WINDOW_SIZE = 2048
STEP = 512
CHUNK = 12 * MODEL_RATE
HOP = 8 * MODEL_RATE
WINDOW = np.hanning(WINDOW_SIZE + 1)[:-1].astype(np.float32)
PROFILE = {'id': 'tiger-dnr-dialogue180-music30-v1', 'reference': 'v0.9',
           'dialogue_gain': 1.8, 'music_gain': 0.3, 'effects_gain': 1.0,
           'model_sha256': MODEL_SHA, 'peak_ceiling': 0.95, 'ort': ort.__version__}


def resample(signal, before, after):
    channels = signal.shape[1]
    result = subprocess.run([FF, '-v', 'error', '-f', 'f32le', '-ar', str(before), '-ac', str(channels),
                             '-i', 'pipe:0', '-ar', str(after), '-f', 'f32le', 'pipe:1'],
                            input=np.asarray(signal, dtype='<f4').tobytes(), capture_output=True, check=True)
    return np.frombuffer(result.stdout, dtype='<f4').reshape(-1, channels)


def synthesize(spectrum):
    frames = np.fft.irfft(spectrum.T, n=WINDOW_SIZE, axis=-1).astype(np.float32) * WINDOW
    result = np.zeros((len(frames) - 1) * STEP + WINDOW_SIZE, dtype=np.float32)
    weight = np.zeros_like(result)
    squared = WINDOW * WINDOW
    for offset, frame in enumerate(frames):
        start = offset * STEP
        result[start:start + WINDOW_SIZE] += frame
        weight[start:start + WINDOW_SIZE] += squared
    span = slice(WINDOW_SIZE // 2, WINDOW_SIZE // 2 + CHUNK)
    return result[span] / weight[span]


def separate_chunk(session, signal):
    pad = np.pad(signal, WINDOW_SIZE // 2, mode='reflect')
    windows = np.lib.stride_tricks.sliding_window_view(pad, WINDOW_SIZE)[::STEP]
    spectrum = np.fft.rfft(windows * WINDOW, axis=-1).T
    assert spectrum.shape == (1025, 1034)
    mix = np.ascontiguousarray(np.stack((spectrum.real, spectrum.imag))[None], dtype=np.float32)
    stems = session.run(['stems_spec'], {'mix_spec': mix})[0][0]
    assert stems.shape == (6, 1025, 1034) and np.isfinite(stems).all()
    return np.stack([synthesize(stems[index] + 1j * stems[index + 1]) for index in (0, 2)], axis=-1)


def separate(session, source):
    down = resample(source, RATE, MODEL_RATE)
    samples = len(down)
    offsets = list(range(0, max(1, samples - CHUNK + HOP), HOP))
    accumulated = np.zeros((samples, 2, 2), dtype=np.float32)
    denominator = np.zeros(samples, dtype=np.float32)
    fade = np.linspace(0, 1, CHUNK - HOP, dtype=np.float32)
    for index, start in enumerate(offsets):
        count = min(CHUNK, samples - start)
        segment = np.pad(down[start:start + count], ((0, CHUNK - count), (0, 0)))
        weight = np.ones(CHUNK, dtype=np.float32)
        if index:
            weight[:len(fade)] = fade
        if index < len(offsets) - 1:
            weight[-len(fade):] = fade[::-1]
        for channel in range(2):
            estimates = separate_chunk(session, segment[:, channel])
            accumulated[start:start + count, channel] += estimates[:count] * weight[:count, None]
        denominator[start:start + count] += weight[:count]
    assert np.all(denominator > 0)
    accumulated /= denominator[:, None, None]
    up = resample(accumulated.reshape(-1, 4), MODEL_RATE, RATE)
    assert abs(len(up) - len(source)) <= 2
    up = np.pad(up, ((0, max(0, len(source) - len(up))), (0, 0)))[:len(source)].reshape(-1, 2, 2)
    return up[:, :, 0], up[:, :, 1]


def render(session, original, scratch, preview=False):
    target = OUTPUT / original.name
    report = OUTPUT / (original.stem + '.json')
    input_sha = sha(original)
    if not preview and report.exists() and target.exists():
        previous = json.loads(report.read_text(encoding='utf-8'))
        if previous['profile'] == PROFILE and previous['input_sha256'] == input_sha and previous['output_sha256'] == sha(target):
            return previous
    started = time.monotonic()
    source = decode(original, scratch / 'source.f32')
    dialogue, music = separate(session, source)
    mixed = source + 0.8 * dialogue - 0.7 * music
    rendered, limiter = limit(mixed.astype(np.float64))
    pcm = scratch / 'remixed.wav'
    backoff = 1.0
    for attempt in range(3):
        save(pcm, rendered * backoff)
        mux(original, pcm, target)
        decoded = decode(target, scratch / 'decoded.f32')
        peak = float(np.abs(decoded).max())
        if peak < 0.995:
            break
        backoff *= 0.97 / peak
    else:
        raise RuntimeError(f'Encoded peaks exceed headroom: {original.name}')
    source_info = packets(original)
    assert source_info == packets(target), original.name
    assert len(decoded) == len(source), (original.name, len(decoded), len(source))
    delay, snr = delay_and_snr(rendered * backoff, decoded)
    assert delay is None or abs(delay) <= 16, (original.name, delay)
    assert snr is None or snr > 20, (original.name, snr)
    rms = lambda signal: float(np.sqrt(np.mean(np.square(signal), dtype=np.float64)))
    result = {'file': original.name, 'profile': PROFILE, 'input_sha256': input_sha,
              'output_sha256': sha(target), 'bytes': target.stat().st_size,
              'video_frames_unchanged': source_info['frames'], 'samples': len(source),
              'sample_delay': delay, 'decoded_sample_peak': peak, 'clipped_samples': 0,
              'roundtrip_snr_db': snr, 'limiter': limiter, 'codec_backoff': backoff,
              'estimated_input_stem_rms': {'dialogue': rms(dialogue), 'music': rms(music),
                                           'effects_and_residual': rms(source - dialogue - music)},
              'render_seconds': round(time.monotonic() - started, 2)}
    if preview:
        dest = HERE / 'samples'
        dest.mkdir(exist_ok=True)
        excerpt = slice(12 * RATE, 28 * RATE)
        save(dest / 'v0.9.wav', source[excerpt])
        save(dest / 'v0.9.1.wav', decoded[excerpt])
    report.write_text(json.dumps(result, indent=2), encoding='utf-8')
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--preview', action='store_true')
    parser.add_argument('--dml', action='store_true')
    parser.add_argument('--threads', type=int, default=5)
    args = parser.parse_args()
    assert sha(MODEL) == MODEL_SHA
    options = ort.SessionOptions()
    options.intra_op_num_threads = args.threads
    options.inter_op_num_threads = 1
    providers = ['CPUExecutionProvider']
    if args.dml:
        options.enable_mem_pattern = False
        providers.insert(0, 'DmlExecutionProvider')
    session = ort.InferenceSession(str(MODEL), options, providers=providers)
    assert session.get_providers()[0] == providers[0]
    PROFILE['provider'] = providers[0]
    print(f'Local TIGER-DnR model loaded: {providers[0]}', flush=True)
    assert session.get_inputs()[0].name == 'mix_spec'
    OUTPUT.mkdir(exist_ok=True)
    scratch = HERE / 'scratch'
    scratch.mkdir(exist_ok=True)
    files = sorted(SOURCE.glob('*.bik'), key=lambda path: (path.name != '01_INT_003.bik', path.name))
    assert len(files) == 27
    manifest = {entry['file']: entry['output_sha256'] for entry in json.loads((PREVIOUS / 'movie-assets.json').read_text())}
    if args.preview:
        files = files[:1]
    rows = []
    for index, original in enumerate(files, 1):
        assert sha(original) == manifest[original.name], original.name
        row = render(session, original, scratch, args.preview)
        rows.append(row)
        print(f"{index}/{len(files)} {original.name}: {row['render_seconds']} s, peak {row['decoded_sample_peak']:.3f}", flush=True)
    if not args.preview:
        assert sum(row['video_frames_unchanged'] for row in rows) == 18822
        (HERE / 'remix-validation.json').write_text(json.dumps({'profile': PROFILE, 'files': rows}, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
