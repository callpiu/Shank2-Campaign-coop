"""Install full-width biographies with a reversible Steam/UI transaction."""
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
sys.path.insert(0, str(WORK / 'story-coop-v30-trait-table'))
import deploy_hotfix as transaction


def main():
    assert json.loads((HERE/'layout-validation.json').read_text())['passed']
    (HERE/'startup-validation.json').write_bytes(
        (WORK/'story-coop-v30-trait-table/startup-validation.json').read_bytes())
    transaction.HERE=HERE
    transaction.main()
    print('Full-width character biographies installed; user visual verification pending.')


if __name__ == '__main__': main()
