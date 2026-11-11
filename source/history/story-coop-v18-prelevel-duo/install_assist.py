"""Temporary user-requested assistance for the exact new pre-level test."""
import sys
from flow import HERE
sys.path.insert(0,str(HERE.parent/'story-coop-v15-boss-transitions'))
from test_assist import install

if __name__=='__main__':
    install(int(sys.argv[1]),expected_path=HERE.parent/'story-coop-v14-transitions/game/bin/shank2-coop-v18-prelevel-test.exe',
        manifest_path=HERE/'builds.json',report_dir=HERE)
