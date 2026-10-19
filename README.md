# Wallaby Themes

Ports and adaptations of the Wallaby theme for KDE Plasma and other applications.

The original Wallaby theme and colour palette were created by [Jeremie Tamburini (@jeremie2)](https://github.com/jeremie2/Wallaby) for COSMIC Desktop. The KDE Plasma and application adaptations in this repository were created by Me.

Special thanks to Jeremie for creating the original design that made these adaptations possible. My eyes will be forever grateful.

## Palette conventions

Selection highlights use one gold: **`#ffbc03`** (RGB `255,188,3`).
Steam's hover accent references its main accent variable instead of defining
another shade. KDE's normal and alternate selection backgrounds use that same
gold, with dark teal text. KDE taskbar blending/transparency is preserved.

Teal surface levels are intentional: background `#1a5d6c`, panels `#2a6c7a`,
raised surfaces `#347483`, buttons `#488693`, and button hover `#5f93a0`.
Keep warning orange, error pink and success green distinct from highlights.

Run the cross-theme palette checks with `python3 tests/test_palette.py`.

The Hermes-inspired gold is shared by Steam and KDE, including KDE's colour
scheme, Plasma widget fallback colour and packaged theme. All teal surface
levels, ordinary text and semantic warning/error/success colours are unchanged.
