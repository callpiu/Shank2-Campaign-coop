"""Verify Steam loaded this exact clean dodge extension, without test assists."""
import importlib.util
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
TOOLS=HERE.parent/'story-coop-v29-steam-entry'
sys.path.insert(0,str(TOOLS))
spec=importlib.util.spec_from_file_location('dodge_steam_verifier',TOOLS/'verify_runtime.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

if __name__=='__main__':module.main(int(sys.argv[1]),build_dir=HERE,report_dir=HERE)
