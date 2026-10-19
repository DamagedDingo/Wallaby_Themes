"""Exercise Play -> Controller -> Settings focus colours in Steam CEF.

Uses actual Steam sp.css and CSS Loader translations in a disposable iframe.
Run with Steam open: python3 tests/test_play_button_focus.py
"""
import asyncio
import json
import unittest

from test_menu_focus import THEME, evaluate, mappings, translated


def focus_states():
    css = '\n'.join(translated((THEME / name).read_text()) for name in (
        'shared.css', 'Custom.css', 'readability.css'))
    table = mappings()
    classes = {key: table.get(value, value) for key, value in {
        'container': 'appactionbutton_PlayButtonContainer_1FnJ6',
        'green': 'appactionbutton_Green_3cI5T',
        'child': 'appactionbutton_ButtonChild_2AzIX',
        'text': 'appactionbutton_ButtonText_33cnX',
        'menu': 'appdetailsplaysection_MenuButton_3qDWQ',
    }.items()}
    expression = '''(async () => {
      const response = await fetch('https://steamloopback.host/css/sp.css');
      if (!response.ok) throw Error('Steam stylesheet unavailable: '+response.status);
      const baseCSS = await response.text();
      const f = document.createElement('iframe');
      f.style.cssText = 'position:fixed;left:-10000px;top:0;width:1280px;height:800px;pointer-events:none';
      document.body.append(f);
      try {
        const d=f.contentDocument;
        const s=d.createElement('style');s.textContent=baseCSS+'\\n'+CSS_TEXT;d.head.append(s);
        const root=d.createElement('div');root.className='BasicUI';d.body.append(root);
        const wrapper=d.createElement('div');wrapper.className=CLASSES.container+' '+CLASSES.green;root.append(wrapper);
        const play=d.createElement('div');play.className=CLASSES.child+' Focusable';wrapper.append(play);
        const text=d.createElement('span');text.className=CLASSES.text;text.textContent='Play';play.append(text);
        const icon=d.createElementNS('http://www.w3.org/2000/svg','svg');play.append(icon);
        const buttons=[play];
        for (const label of ['Controller','Settings']) {
          const e=d.createElement('div');e.className=CLASSES.menu+' Focusable';
          e.textContent=label;root.append(e);buttons.push(e);
        }
        const results=[];
        for (const focused of buttons) {
          buttons.forEach(e=>e.classList.toggle('gpfocus',e===focused));
          await new Promise(resolve=>setTimeout(resolve,650));
          const style=f.contentWindow.getComputedStyle(play);
          results.push({focus:focused===play?'Play':focused.textContent,
            background:style.backgroundColor,text:f.contentWindow.getComputedStyle(text).color,
            icon:f.contentWindow.getComputedStyle(icon).color});
        }
        return results;
      } finally { f.remove(); }
    })()'''.replace('CSS_TEXT', json.dumps(css)).replace('CLASSES', json.dumps(classes))
    return asyncio.run(evaluate(expression, title='SharedJSContext'))


class PlayButtonFocusTests(unittest.TestCase):
    def test_play_returns_to_teal_after_focus_moves(self):
        states = focus_states()
        self.assertEqual([s['focus'] for s in states], ['Play', 'Controller', 'Settings'])
        for state in states:
            with self.subTest(focus=state['focus']):
                focused = state['focus'] == 'Play'
                self.assertEqual(state['background'], 'rgb(255, 188, 3)' if focused else 'rgb(52, 116, 131)')
                self.assertEqual(state['text'], 'rgb(26, 93, 108)' if focused else 'rgb(242, 242, 242)')
                self.assertEqual(state['icon'], state['text'])


if __name__ == '__main__':
    unittest.main()
