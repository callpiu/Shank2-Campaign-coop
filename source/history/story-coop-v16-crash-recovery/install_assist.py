"""Reapply the user's temporary boss-test assistance to the exact v16 build."""
import sys
from pose3 import HERE
from test_assist import install

if __name__=='__main__':
    install(int(sys.argv[1]),expected_path=HERE.parent/'story-coop-v14-transitions/game/bin/shank2-coop-v16-boss-fixes-test.exe',
        manifest_path=HERE/'build-validation.json',report_dir=HERE)
