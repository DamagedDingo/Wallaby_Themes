# Wallaby for Steam Deck CSS Loader

A standalone, one-toggle Wallaby colour theme for Gaming Mode / Big Picture.
It uses the teal palette from this repository's KDE Wallaby colour scheme,
adapting Srcery v0.7.0's MIT-licensed Steam UI styling. Srcery does not need
to be installed or enabled. No slider setup or Capy dependencies are needed.

The accent uses gold `#ffbc03`, sampled from the user's Hermes screenshot and
shared with KDE. Teal surfaces, text and semantic status colours are unchanged.

## Apply on this Deck

The theme is installed at `/home/deck/homebrew/themes/Wallaby`.

1. In Gaming Mode, open Decky → CSS Loader and reload themes. If Wallaby does
   not appear, restart Steam / the Deck to refresh the theme list.
2. Turn off **CapyInputs**, **CapyMenu (Context Menus)**,
   **CapyMenu (QAM)**, **CapyMenu (Steam Menu)**, **Colored Toggles**,
   **Customizable Keyboard**, and **Bright Home Background** for the initial
   Wallaby test. Leave Srcery, Catppuccin and Outrun disabled too.
3. Enable **Wallaby**. Its menu, settings, controls, dialog and keyboard
   sections default to on; each can be turned off separately.

Your existing theme settings have not been edited. To go back, disable
Wallaby and re-enable the themes you switched off. CSS Loader profiles can
save both combinations if you want to switch between them later.

Layout and artwork themes can usually stay enabled. Footer Editor,
FooterBlur and Top Bar Transparency may override Wallaby in those areas;
turn them off if you want its solid teal header/footer. If a screen looks
wrong, test with only Wallaby enabled to isolate overlapping CSS.

## Install or update from this repository

Run from this directory:

```sh
./install.sh
```

Or specify a different themes directory as the first argument. The script
backs up any previous Wallaby folder under `homebrew/wallaby-backups` and
preserves its saved `config_USER.json`. It never activates themes or changes
another theme's settings. To install manually, copy the **Wallaby** folder
into `~/homebrew/themes/`, then reload CSS Loader and enable it.

## Colours and coverage

| Role | Colour |
| --- | --- |
| Main background | `#1a5d6c` |
| Panels | `#2a6c7a` |
| Raised surfaces | `#347483` |
| Buttons | `#488693` |
| Main text | `#f2f2f2` |
| Secondary text | `#c6c6c6` |
| Selection / accent | `#ffbc03` |
| Links | `#63d0df` |
| Success | `#92cf9c` |
| Error | `#fda1a0` |

The source palette lives in `Wallaby/shared.css`. Coverage includes home,
library, game details, Steam and Quick Access menus, settings, controller
settings, buttons, toggles, sliders, context menus, dialogs, notifications,
downloads, friends and the default Steam keyboard. Game artwork is retained;
the theme uses Steam's fonts. Select the default Steam keyboard skin for its
keyboard colours. Games themselves and web store pages are not fully themed.

The four configurations edited on 16 September 2026 were CapyInputs and the
three CapyMenu folders (including QAM). They contain saved options, not the
complete theme implementation. Other installed folders are independent
colour, layout, artwork or utility themes; `.profile` folders save groups
of themes and settings.

## Validation and limitations

This is a first local port, not a published or visually certified release.
Validation passed: all 24 CSS files parse, every Wallaby variable resolves,
and the installed CSS Loader parses the manifest and loads all 24 CSS
injections with class translation. Installer backup and settings preservation
were checked in a temporary directory; the live copy matches the repository
and all pre-existing theme configurations remain unchanged.

The CSS selectors are inherited from installed Srcery v0.7.0, with CSS
Loader's class translation mechanism available for Steam UI changes.
A Gaming Mode visual check is still needed: home/library, both side menus,
a game context menu, settings controls, keyboard, and an in-game overlay.
Steam updates or third-party layout themes may require selector adjustments.

The packaging follows the [official CSS Loader theme format](https://docs.deckthemes.com/CSSLoader/Features/).
See [CSS Loader profiles](https://docs.deckthemes.com/CSSLoader/Profiles/)
for saving combinations, and [credits](Wallaby/ATTRIBUTION.md) for provenance.
The upstream MIT license is preserved in `Wallaby/LICENSE`.

## v0.2.0 — screenshot readability pass

- Ordinary copy, dates, playtime, game names and descriptions default to white.
- Section headings and selected states retain yellow accents.
- Play actions, selected friends pills and keyboard toggle backgrounds use yellow.
- Header, tab strip, search field and library sort/date labels have opaque teal
  backgrounds. Search text is white; selected cover outlines are yellow.
- Green remains for semantic statuses such as verified compatibility, battery,
  online/in-game status and storage categories.

Validated CSS syntax, selector syntax, all palette references and installed
CSS Loader parsing/class translation. These are static checks; verify the
four reported screens in Gaming Mode after reloading CSS Loader.
Disable overlapping colour themes, particularly Top Bar Transparency,
Colored Toggles, the Capy themes and Bright Home Background, when testing.

## v0.3.0 — settings and toggle states

Settings cards use raised teal and retain yellow focus. The selected Quick
Access tab rests on teal when focus moves to the right pane, with its dark
Steam animation disabled. Menu separators use teal. Off toggles use dark teal
rails and white knobs; on toggles use yellow rails and dark teal knobs,
including when the surrounding row is focused. Slider styling is unchanged.

## v0.3.1 — focused slider contrast

Slider fills, knobs, icons and labels turn dark teal inside yellow focused
rows; empty tracks and inactive ticks use lighter teal. Unfocused sliders
retain yellow fills and knobs. Both direct slider focus and containing-field
focus are covered, including settings and Quick Access controls.

The same contrast audit corrected controller-configuration actions, in-game
guide buttons, focused storage drive pills, game action icons, input
placeholders and keyboard function/extended keys. Ordinary comment panels
use teal instead of yellow. Existing menu and sidebar focus colours remain.

## v0.3.2 — consistent library selection

Game covers and collection focus rings use a steady yellow outline. Removed
the old grey cover-outline override and its fade/blink keyframes; disabled
outline animation on focused covers and library focus rings.

## v0.3.3 — default keyboard

Fixed Steam's more-specific default skin overriding keyboard variables.
Keyboard backing is dark teal, normal keys are secondary teal, function keys
are lighter teal, and selected/pressed keys are yellow with dark teal text.
Added shift-label and emoji colours, and removed the default white touch flash.
Keep Steam's keyboard skin set to Default and Wallaby's Keyboard option on.

## v0.3.4 — Steam and power menu focus

The Steam menu uses semantic menu-item selectors instead of stale translated
item/icon/label classes. Selected entries have a steady yellow background and
dark teal text/icons. Context-menu focus stays yellow for destructive, Stop
and Cancel entries too, including the power menu; error/status colours elsewhere
are unchanged. This does not change physical power-button handling.

Computed-colour regression tests use the running Steam renderer and its real
stylesheets, with a cloned main menu and context-action fixtures in a disposable
off-screen iframe. They do not activate Steam actions or restart Steam.
With Steam CEF debugging available on localhost:8080 and CSS Loader installed:

```sh
python3 -m pip install websockets
python3 tests/test_menu_focus.py
```

Both tests were observed failing before the corresponding fixes, then passing.
An on-device controller-navigation check is still recommended after reloading
CSS Loader, especially when other menu themes are enabled.

## v0.3.7 — Play button follows focus

The primary Play button returns to a teal background with white text and icon
when focus moves to Controller or Settings. It uses gold with dark teal text
only while focused. The former readability override incorrectly applied the
accent to Steam's Green action variant unconditionally.

`python3 tests/test_play_button_focus.py` exercises Play → Controller → Settings
using Steam's actual stylesheet and translated theme selectors in an isolated
iframe. The test failed on both off-Play states before the fix and passes after it.
