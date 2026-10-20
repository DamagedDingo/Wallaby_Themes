"""Palette consistency checks: python3 -m unittest discover -s tests."""
from configparser import ConfigParser
from pathlib import Path
import re
import tarfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ACCENT_RGB = '255,188,3'


class PaletteTests(unittest.TestCase):
    def test_kde_selection_uses_one_gold(self):
        for relative in ('KDE Plasma/color-schemes/Wallaby.colors',
                         'KDE Plasma/desktoptheme/Wallaby/colors'):
            with self.subTest(file=relative):
                config = ConfigParser()
                config.read(ROOT / relative)
                for key in ('BackgroundNormal', 'BackgroundAlternate'):
                    self.assertEqual(config['Colors:Selection'][key], ACCENT_RGB)
                for section in ('Colors:Button', 'Colors:Complementary', 'Colors:Header',
                                'Colors:Tooltip', 'Colors:View', 'Colors:Window'):
                    for key in ('DecorationFocus', 'ForegroundActive'):
                        self.assertEqual(config[section][key], ACCENT_RGB)
                self.assertEqual(config['Colors:Button']['DecorationHover'], ACCENT_RGB)
                self.assertEqual(config['WM']['activeForeground'], '242,242,242')

    def test_launcher_svg_uses_same_gold(self):
        path = ROOT / 'KDE Plasma/desktoptheme/Wallaby/widgets/viewitem.svg'
        tree = ET.parse(path)
        style = tree.find('.//{http://www.w3.org/2000/svg}style')
        assert style is not None
        self.assertIn('#ffbc03', style.text or '')
        self.assertNotIn('#f6df62', style.text or '')

    def test_steam_hover_reuses_shared_gold(self):
        css = (ROOT / 'Steamdeck - CSS Loader (Decky Loader)/Wallaby/shared.css').read_text()
        variables = dict(re.findall(r'(--wallaby-[\w-]+)\s*:\s*([^;]+);', css))
        self.assertEqual(variables['--wallaby-accent'], '#ffbc03')
        self.assertEqual(variables['--wallaby-accent-hover'], 'var(--wallaby-accent)')

    def test_packaged_plasma_selection_matches_source(self):
        with tarfile.open(ROOT / 'KDE Plasma/Wallaby-Plasma-Style.tar.gz') as archive:
            member = archive.extractfile('./colors')
            assert member is not None
            colours = member.read().decode()
        config = ConfigParser()
        config.read_string(colours)
        self.assertEqual(config['Colors:Selection']['BackgroundAlternate'], ACCENT_RGB)


if __name__ == '__main__':
    unittest.main()
