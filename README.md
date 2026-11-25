# Ayu Custom Theme

All six **Ayu** variants for [Zed](https://zed.dev) (borderless and bordered), faithful to [ayu-theme/vscode-ayu](https://github.com/ayu-theme/vscode-ayu) with toned-down contrast, harmonized Ayu git colors + 65%-blended gutter bars, and a crisp white (`#ffffff`) cursor on dark themes (`#1a1d24` on light).

## Variants

- **Ayu Dark Custom** — Borderless (`#0d1017` seamless)
- **Ayu Dark Bordered Custom** — Bordered (`#0d1017` shell → `#10141c` editor)
- **Ayu Mirage Custom** — Borderless (`#1f2430` seamless)
- **Ayu Mirage Bordered Custom** — Bordered (`#1f2430` shell → `#242936` editor)
- **Ayu Light Custom** — Borderless (`#f8f9fa` seamless)
- **Ayu Light Bordered Custom** — Bordered (`#f3f5f7` shell → `#fcfcfc` editor)

## Install locally

1. In Zed, open the command palette and run `zed: install dev extension`.
2. Select this folder.
3. Run `theme selector: toggle` and pick any `Ayu … Custom` variant.

Or copy `themes/ayu.json` into `~/.config/zed/themes/`.

## Regenerating

```bash
python3 scripts/build.py
```
