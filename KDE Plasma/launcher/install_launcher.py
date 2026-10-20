#!/usr/bin/env python3
"""Install a guarded, user-local Kickoff contrast adjustment; never edit /usr.

Run again after a Plasma update to rebuild from the installed upstream widget.
Remove ~/.local/share/plasma/plasmoids/org.kde.plasma.kickoff to uninstall.
The copied widget retains its upstream GPL-2.0-or-later license headers.
"""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import shutil
import tempfile

SOURCE = Path('/usr/share/plasma/plasmoids/org.kde.plasma.kickoff')
DEFAULT_DESTINATION = Path.home() / '.local/share/plasma/plasmoids/org.kde.plasma.kickoff'
OLD_SELECTION = 'readonly property bool iconAndLabelsShouldlookSelected: down && !isCategoryListItem'
NEW_SELECTION = '''readonly property bool iconAndLabelsShouldlookSelected: (down && !isCategoryListItem)
        || (PlasmaCore.Theme.themeName === "Wallaby"
            && view !== null && view.currentIndex === index
            && view.highlightItem !== null && view.highlightItem.visible)'''


def build(source, destination):
    """Copy the installed widget, rejecting changed upstream patch anchors."""
    source = Path(source)
    destination = Path(destination)
    delegate = source / 'contents/ui/AbstractKickoffItemDelegate.qml'
    original = delegate.read_text()
    if original.count(OLD_SELECTION) != 1:
        raise ValueError('Upstream Kickoff selection logic changed; inspect before updating')
    shutil.copytree(source, destination, symlinks=True)
    (destination / 'contents/ui/AbstractKickoffItemDelegate.qml').write_text(
        original.replace(OLD_SELECTION, NEW_SELECTION))


def install(destination):
    destination = Path(destination)
    if destination.is_symlink():
        raise ValueError('Refusing to replace a symlink destination')
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Build and validate before touching a prior local copy.
    with tempfile.TemporaryDirectory(prefix='wallaby-kickoff-', dir=destination.parent) as temp:
        candidate = Path(temp) / destination.name
        build(SOURCE, candidate)
        backup = None
        if destination.exists():
            stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
            backup = Path.home() / 'homebrew/wallaby-backups' / ('kickoff-' + stamp) / destination.name
            backup.parent.mkdir(parents=True, exist_ok=True)
            destination.rename(backup)
        try:
            candidate.rename(destination)
        except OSError:
            if backup is not None:
                backup.rename(destination)
            raise
    print('Installed user-local Kickoff contrast fix:', destination)
    print('Log out/in to reload the widget; system KDE files are unchanged.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path, default=DEFAULT_DESTINATION)
    args = parser.parse_args()
    install(args.destination)
