# Wallaby contrast adjustment for the standard KDE launcher

The stock Application Launcher (Kickoff) uses its selected text colour only
while an item is pressed or dragged. Wallaby draws a solid gold hover/current
background, so its labels also need the selected dark-teal text colour whenever
the current item's highlight is visible. Normal items remain white.

## Install

From the repository root:

```sh
python3 'KDE Plasma/launcher/install_launcher.py'
```

This copies the **currently installed** system Kickoff package to
`~/.local/share/plasma/plasmoids/org.kde.plasma.kickoff`, then changes one guarded
selection-colour expression. It never edits `/usr` and preserves the upstream
GPL-2.0-or-later headers. The extra condition only activates when the Plasma
theme is named `Wallaby`; other themes retain Kickoff's original behaviour.
Existing user-local copies are moved under `~/homebrew/wallaby-backups` first.

Reload Plasma or log out/in to load the user-local widget. This is still the
standard Kickoff menu, not a replacement launcher with a different UI.

After a Plasma update, rerun the installer to rebuild from the updated system
package. If the upstream expression changes, installation refuses to overwrite
the existing copy rather than guessing at a patch.

## Revert

Remove or move aside the user-local `org.kde.plasma.kickoff` directory and reload
Plasma. KDE falls back to its untouched system copy. The repository installer
and Git history retain the adjustment for later use.

## Tests

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tests/test_launcher_contrast.py
python3 tests/test_palette.py
```

The first command builds a disposable copy and executes its exact selection
expression against real ListView and GridView items in Qt 6's QML test runner.
It checks normal, hover/keyboard-current,
hidden-highlight, category, pressed and non-current states. It also verifies
that changed upstream patch anchors are rejected before a destination is made.
Tests require the Plasma 6 modules, the installed Wallaby desktop theme and
`/usr/lib/qt6/bin/qmltestrunner`.

The accompanying palette changes keep window titles white on teal and make
button/taskbar hover use the same gold as selection. Taskbar SVG transparency,
ordinary text, links, status colours, layouts and Steam styling are unchanged.
