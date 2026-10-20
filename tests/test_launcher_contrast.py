"""Run generated Kickoff selection logic in the real Qt QML engine."""
import importlib.util
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('wallaby_launcher', ROOT / 'KDE Plasma/launcher/install_launcher.py')
assert spec is not None and spec.loader is not None
launcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(launcher)


class LauncherContrastTests(unittest.TestCase):
    def test_qml_selection_tracks_visible_highlight(self):
        with tempfile.TemporaryDirectory(prefix='wallaby-launcher-test-') as folder:
            folder = Path(folder)
            generated = folder / 'widget'
            launcher.build(launcher.SOURCE, generated)
            text = (generated / 'contents/ui/AbstractKickoffItemDelegate.qml').read_text()
            match = re.search(r'    readonly property bool iconAndLabelsShouldlookSelected:.*?(?=\n\n)', text, re.S)
            self.assertIsNotNone(match)
            assert match is not None
            fixture = '''import QtQuick
import QtTest
import org.kde.plasma.core as PlasmaCore
TestCase {
    name: "WallabyKickoffContrast"
    visible: true
    width: 200
    height: 200
    when: windowShown
    property bool down: false
    property bool isCategoryListItem: false
    property int index: 1
    property alias view: actualView
    ListView {
        id: actualView
        width: 200
        height: 200
        model: 3
        delegate: Rectangle { width: 200; height: 30 }
        highlight: Rectangle { color: "gold" }
    }
PROPERTY
    property color labelColor: iconAndLabelsShouldlookSelected ? "#1a5d6c" : "#f2f2f2"
    function test_states_data() {
        return [
            {tag:"normal", current:false, visible:true, pressed:false, category:false, expected:"#f2f2f2"},
            {tag:"hover_or_keyboard_focus", current:true, visible:true, pressed:false, category:false, expected:"#1a5d6c"},
            {tag:"highlight_hidden", current:true, visible:false, pressed:false, category:false, expected:"#f2f2f2"},
            {tag:"category_highlight", current:true, visible:true, pressed:false, category:true, expected:"#1a5d6c"},
            {tag:"pressed", current:true, visible:true, pressed:true, category:false, expected:"#1a5d6c"},
            {tag:"not_current", current:false, visible:true, pressed:false, category:false, expected:"#f2f2f2"}
        ]
    }
    function test_states(data) {
        down=data.pressed
        isCategoryListItem=data.category
        view.currentIndex=data.current ? index : 0
        tryVerify(function() { return view.highlightItem !== null })
        view.highlightItem.visible=data.visible
        compare(labelColor, Qt.color(data.expected))
    }
}
'''.replace('PROPERTY', match[0])
            for kind in ('ListView', 'GridView'):
                test = folder / ('tst_' + kind.lower() + '.qml')
                test.write_text(fixture.replace('    ListView {', '    ' + kind + ' {')
                                .replace('WallabyKickoffContrast', 'WallabyKickoff' + kind))
            env = dict(os.environ, QT_QPA_PLATFORM='offscreen', QSG_RHI_BACKEND='software',
                       QT_LOGGING_RULES='*.warning=true;*.critical=true')
            runner = '/usr/lib/qt6/bin/qmltestrunner'
            result = subprocess.run([runner, '-input', str(folder), '-o', '-,txt'],
                                    capture_output=True, text=True, env=env, timeout=30)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotIn('QWARN', result.stdout + result.stderr)

    def test_upstream_change_is_rejected_before_copy(self):
        with tempfile.TemporaryDirectory(prefix='wallaby-anchor-test-') as folder:
            source = Path(folder) / 'source'
            destination = Path(folder) / 'output'
            file = source / 'contents/ui/AbstractKickoffItemDelegate.qml'
            file.parent.mkdir(parents=True)
            file.write_text('upstream structure changed')
            with self.assertRaisesRegex(ValueError, 'Upstream'):
                launcher.build(source, destination)
            self.assertFalse(destination.exists())


if __name__ == '__main__':
    unittest.main()
