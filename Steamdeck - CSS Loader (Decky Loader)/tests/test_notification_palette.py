"""Check that separate notification windows receive their colour palette."""
import json
from pathlib import Path
import unittest


class NotificationPaletteTests(unittest.TestCase):
    def test_notification_targets_receive_shared_palette(self):
        theme = Path(__file__).resolve().parents[1] / 'Wallaby'
        manifest = json.loads((theme / 'theme.json').read_text())
        notification_targets = set(manifest['inject']['notifications.css'])
        palette_targets = set(manifest['inject']['shared.css'])
        self.assertTrue(notification_targets)
        self.assertFalse(notification_targets - palette_targets,
                         'Notification windows need explicit shared.css injection; '
                         'CSS Loader All only covers Big Picture and its side menus')


if __name__ == '__main__':
    unittest.main()
