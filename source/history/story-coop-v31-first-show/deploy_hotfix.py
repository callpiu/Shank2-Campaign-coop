"""Install the verified first-show refresh while retaining Steam rollback."""
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
sys.path.insert(0, str(WORK / 'story-coop-v30-trait-table'))
import deploy_hotfix as transaction


def main():
    validation = json.loads((WORK / 'story-coop-v28-trait-descriptions/validation.json').read_text())
    assert validation['passed'] and validation['first_show_cases'] == 17
    assert validation['old_first_show_failure_reproduced']
    assert validation['first_show_without_selection_event']
    # Reuse the transactional updater, but keep this deployment's evidence here.
    (HERE / 'startup-validation.json').write_bytes(
        (WORK / 'story-coop-v30-trait-table/startup-validation.json').read_bytes())
    transaction.HERE = HERE
    transaction.main()
    print('First-show refresh installed; gameplay visual confirmation is pending.')


if __name__ == '__main__':
    main()
