# Shank 2 Campaign Co-op MOD v0.10.4

This package has two shortcuts:

- Install.cmd: open the manager, select the game folder, then choose Install,
  Verify or Remove. The manager also opens the controls tool.
- Uninstall.cmd: restore the previous files directly.

Extract the full archive and keep the patch folder beside these shortcuts.
Exit the game before installing/removing. Launch normally from Steam afterward.
To update the English MOD, install into the same game folder; original backups,
saves, display settings and custom bindings are retained. Uninstall the previous
profile before switching between MOD-only and localized packages.

Coop-Key-Settings.cmd is installed in the GAME folder. Use it to edit bindings;
settings apply the next time the game starts. All package filenames and text are
English. Technical scripts, manifests and checksums are inside patch.

## Co-op features

- Use Restart Checkpoint in the pause menu. Confirming a different character automatically retries the current checkpoint. Throwables refill on retry and when starting a new level.

- Independent controls, health, equipment, consumables and scores.
- Both players choose character and equipment before each campaign level.
- All 17 characters are available, with applicable Survival health/damage traits.
  Weapons still follow campaign unlocks. Character names, traits and biographies
  now use separate areas in the English selection panel.
- Either player can revive the other; retry only after both players are down.
  Retry retains individual scores. Terrain deaths return downed players nearby.
- Pause-menu equipment selection for each player. Character changes there apply
  on retry or the next level.
- Shared camera with smooth zoom, manual P2 recall, and the previously confirmed
  boss-grab, cutscene-transition, recovery-overlay and selection UI fixes.

## Default keyboard controls

Enable NumLock for P2.

| Action | P1 | P2 |
| --- | --- | --- |
| Move | WASD | Arrow keys |
| Jump / Confirm | Space | Numpad 0 |
| Light attack | J | Numpad 1 |
| Heavy weapon | K | Numpad 2 |
| Ranged attack | L | Numpad 3 |
| Grapple | O | Numpad 6 |
| Dodge left / right | Z / C | Numpad 8 / 9 |

Enter pauses/resumes and confirms menus. F6 recalls P2. F7 toggles the shared
camera. Other actions and custom bindings are available in the controls tool.
Two physical XInput controllers are also supported.

## Requirements and validation

Windows PowerShell 5.1 and a working Steam installation of Shank 2 are required.
Supported original bin/shank2.exe SHA-256:
3cd7aeb0d9f135dc82c4bba491463ecb85fec9aa33b9189ab2cee5160dd045d3

The installer reconstructs the modified executable from your own verified copy.
No complete game EXE/DLL, save, personal settings, invincibility, one-hit-kill
assist or diagnostic tool is distributed. Original Steam and Bink DLLs remain
unchanged. Steam APIs are retained; achievement conditions are not bypassed.

Many co-op features were confirmed by the user in the Chinese edition. The user
also confirmed that Classic, Boogie and Sunshine display complete names, traits
and biographies without overlap in this English update. All 17 English layouts
passed static checks; full-campaign coverage remains incomplete.

Controls shortcut fix: Coop-Key-Settings.cmd directly launches its installed settings script; no legacy Open-Window helper is required.
