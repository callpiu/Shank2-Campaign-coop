"""User's default temporary assistance for a freshly launched v17 test."""
import sys
from anchor import HERE
from test_assist import install

if __name__=='__main__':
    install(int(sys.argv[1]),expected_path=HERE.parent/'story-coop-v14-transitions/game/bin/shank2-coop-v17-boss-fixes-test.exe',
        manifest_path=HERE/'build-validation.json',report_dir=HERE)
