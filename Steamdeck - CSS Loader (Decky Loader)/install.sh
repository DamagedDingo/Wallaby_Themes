#!/bin/sh
# Install this theme without changing existing themes or their saved settings.
set -eu
source_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)/Wallaby
themes_dir=${1:-/home/deck/homebrew/themes}
python3 - "$source_dir" "$themes_dir" <<'PY'
from pathlib import Path
import shutil, sys
from datetime import datetime, timezone
source, themes = map(Path, sys.argv[1:])
target = themes / 'Wallaby'
if target.is_symlink():
    raise SystemExit('Refusing to replace a symlink at ' + str(target))
if target.exists():
    backup = themes.parent / 'wallaby-backups' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ') / 'Wallaby'
    shutil.copytree(target, backup)
    print('Previous Wallaby version backed up to', backup)
shutil.copytree(source, target, dirs_exist_ok=True)
print('Installed:', target)
print('Reload CSS Loader, disable overlapping colour themes, then enable Wallaby.')
PY
