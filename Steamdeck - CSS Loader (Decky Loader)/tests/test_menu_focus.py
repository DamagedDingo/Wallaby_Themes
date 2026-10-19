"""Computed-colour regression tests against the running Steam CEF renderer.

Requires Python 3 and `websockets` (pip install websockets), Steam CEF debugging
on localhost:8080, CSS Loader's css_translations.json, and a MainMenu tab.
Tests run in an off-screen disposable iframe: no Steam actions are invoked.
Run: python3 tests/test_menu_focus.py
"""
import asyncio
import json
from pathlib import Path
import re
import unittest
import urllib.request

import websockets

THEME = Path(__file__).resolve().parents[1] / 'Wallaby'
TRANSLATIONS = Path.home() / 'homebrew/themes/css_translations.json'


def mappings():
    data = json.loads(TRANSLATIONS.read_text())
    return {old: versions[-1] for versions in data.values() for old in versions[:-1]}


def translated(text):
    table = mappings()
    return re.sub(r'\.([_a-zA-Z][_a-zA-Z0-9-]*)',
                  lambda m: '.' + table.get(m[1], m[1]), text)


async def evaluate(expression, title='MainMenu'):
    with urllib.request.urlopen('http://127.0.0.1:8080/json', timeout=5) as response:
        tabs = json.load(response)
    tab = next(t for t in tabs if t['title'].startswith(title))
    async with websockets.connect(tab['webSocketDebuggerUrl'], max_size=16000000) as ws:
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {
            'expression': expression, 'returnByValue': True, 'awaitPromise': True}}))
        while True:
            result = json.loads(await ws.recv())
            if result.get('id') == 1:
                if 'exceptionDetails' in result.get('result', {}):
                    raise RuntimeError(result['result']['exceptionDetails'])
                return result['result']['result']['value']


def colours(kind):
    css = '\n'.join(translated((THEME / name).read_text()) for name in (
        'shared.css', 'main-menu.css', 'modals/styled-modals.css'))
    table = mappings()
    classes = {key: table.get(value, value) for key, value in {
        'item': 'gamepadcontextmenu_contextMenuItem_1sdvo',
        'focused': 'gamepadcontextmenu_Focused_X813r',
        'destructive': 'gamepadcontextmenu_Destructive_3aIFv',
    }.items()}
    expression = '''(async () => {
      const frame = document.createElement('iframe');
      frame.style.cssText = 'position:fixed;left:-10000px;top:0;width:1280px;height:800px;pointer-events:none';
      document.body.append(frame);
      try {
        const d = frame.contentDocument;
        for (const sheet of document.styleSheets) {
          if (!sheet.href) continue;
          const style = d.createElement('style');
          style.textContent = [...sheet.cssRules].map(r=>r.cssText).join('\\n');
          d.head.append(style);
        }
        const style = d.createElement('style');
        style.textContent = CSS_TEXT;
        d.head.append(style);
        let targets;
        if (KIND === 'main') {
          const source = document.querySelector('[role="menuitem"]');
          if (!source) throw Error('Steam main menu DOM unavailable');
          const root = source.parentElement.parentElement.cloneNode(true);
          d.body.append(root);
          targets = [...root.querySelectorAll('[role="menuitem"]')];
          targets.forEach(e=>e.classList.add('gpfocus'));
        } else {
          const root = d.createElement('div');
          root.className = 'BasicUIContextMenu';
          d.body.append(root);
          targets = ['', CLASSES.destructive, 'Stop', 'Cancel'].map(extra=>{
            const e = d.createElement('div');
            e.className = [CLASSES.item, CLASSES.focused, 'contextMenuItem', 'gpfocus', extra].join(' ');
            e.textContent = extra || 'Sleep'; root.append(e); return e;
          });
        }
        await new Promise(resolve=>setTimeout(resolve,650));
        return targets.map(e=>({text:e.textContent,background:frame.contentWindow.getComputedStyle(e).backgroundColor,
          foreground:frame.contentWindow.getComputedStyle(e).color,
          children:[...e.children].map(c=>frame.contentWindow.getComputedStyle(c).color)}));
      } finally { frame.remove(); }
    })()'''
    expression = expression.replace('CSS_TEXT', json.dumps(css)).replace('KIND', json.dumps(kind)).replace('CLASSES', json.dumps(classes))
    return asyncio.run(evaluate(expression))


class MenuFocusTests(unittest.TestCase):
    def assert_gold(self, rows):
        self.assertTrue(rows)
        for row in rows:
            with self.subTest(item=row['text']):
                self.assertEqual(row['background'], 'rgb(255, 188, 3)', row)
                self.assertEqual(row['foreground'], 'rgb(26, 93, 108)', row)
                for colour in row['children']:
                    self.assertEqual(colour, 'rgb(26, 93, 108)', row)

    def test_main_menu_focus(self):
        self.assert_gold(colours('main'))

    def test_context_actions_keep_gold_focus(self):
        self.assert_gold(colours('context'))


if __name__ == '__main__':
    unittest.main()
