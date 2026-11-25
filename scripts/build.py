#!/usr/bin/env python3
"""Generate all six Ayu Custom Zed themes (Dark, Mirage, Light — borderless & bordered).

Usage: python3 scripts/build.py

Faithful to ayu-theme/vscode-ayu with:
  - Both borderless (transparent dividers, seamless surfaces) and bordered variants
  - Gently toned text/syntax contrast (no harsh glare)
  - Harmonized Ayu git status colors + 65%-blended gutter bars + inline word-diff highlights
  - Pure white (#ffffff) cursor on dark themes (#1a1d24 on light themes)
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "themes"
SCHEMA = "https://zed.dev/schema/themes/v0.2.0.json"
AUTHOR = "Dallas Gere"
TRANSPARENT = "#00000000"
GIT_DIM = 0.65


def blend(fg, alpha, bg):
    """Straight sRGB mix: alpha of fg over bg."""
    a = [int(fg[i : i + 2], 16) for i in (1, 3, 5)]
    b = [int(bg[i : i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x * alpha + y * (1 - alpha)):02x}" for x, y in zip(a, b))


def tok(color, style="normal", weight=400):
    return {"color": color, "font_style": style, "font_weight": weight}


FAMILIES = {
    "dark": {
        "label": "Ayu Dark",
        "appearance": "dark",
        "cursor": "#ffffff",
        "unbordered": {
            "editor": "#0d1017",
            "shell": "#0d1017",
            "elevated": "#141821",
            "tab_active": "#141821",
            "line": "#161a24",
            "hover": "#181d28",
            "selected": "#1f2634",
            "selection": "#223552",
            "border": TRANSPARENT,
            "border_variant": TRANSPARENT,
        },
        "bordered": {
            "editor": "#10141c",
            "shell": "#0d1017",
            "elevated": "#161b26",
            "tab_active": "#10141c",
            "line": "#181d28",
            "hover": "#181d28",
            "selected": "#202838",
            "selection": "#243957",
            "border": "#1e2430",
            "border_variant": "#171c26",
        },
        "guides": {
            "wrap": "#171c26",
            "wrap_active": "#242c3b",
            "invisible": "#2b3342",
            "indent": "#161b26",
            "indent_active": "#273042",
            "scroll": "#5a667338",
            "scroll_hover": "#5a66735c",
            "scroll_active": "#5a667380",
            "minimap": "#5a667330",
            "minimap_hover": "#5a667350",
            "minimap_active": "#5a667375",
            "doc_read": "#59c2ff1c",
            "doc_write": "#59c2ff2e",
            "doc_bracket": "#e6b45024",
            "search": "#e6b4502b",
            "search_active": "#e6b45055",
        },
        "palette": {
            "fg": "#bebcb7",
            "ui_text": "#b5b3ae",
            "ui_muted": "#6e7887",
            "ui_disabled": "#47505e",
            "line_number": "#434c5a",
            "punct": "#898886",
            "comment": "#5f6b78",
            "accent": "#e6b450",
            "orange": "#ff8f40",
            "gold": "#ffb454",
            "green": "#aad94c",
            "sky": "#59c2ff",
            "cyan": "#39bae6",
            "coral": "#f07178",
            "lavender": "#d2a6ff",
            "peach": "#f29668",
            "mint": "#95e6cb",
            "red": "#d95757",
        },
        "git": {
            "added": "#70bf56",
            "modified": "#e6b450",
            "deleted": "#f06b73",
            "conflict": "#f2883d",
            "ignored": "#5f6b78",
            "gutter_added": "#70bf56",
            "gutter_modified": "#73b8ff",
            "gutter_deleted": "#f26d78",
        },
        "ansi": {
            "black": "#161a24", "bright_black": "#5f6b78",
            "red": "#f06b73", "bright_red": "#f5878e",
            "green": "#70bf56", "bright_green": "#9ec949",
            "yellow": "#e6b450", "bright_yellow": "#f0a94c",
            "blue": "#56b6ee", "bright_blue": "#73b8ff",
            "magenta": "#c79df0", "bright_magenta": "#d8b4ff",
            "cyan": "#85d4ba", "bright_cyan": "#95e6cb",
            "white": "#bebcb7", "bright_white": "#e6e3da",
        },
    },
    "mirage": {
        "label": "Ayu Mirage",
        "appearance": "dark",
        "cursor": "#ffffff",
        "unbordered": {
            "editor": "#1f2430",
            "shell": "#1f2430",
            "elevated": "#282e3b",
            "tab_active": "#282e3b",
            "line": "#252b39",
            "hover": "#272d3b",
            "selected": "#2f3747",
            "selection": "#2c4666",
            "border": TRANSPARENT,
            "border_variant": TRANSPARENT,
        },
        "bordered": {
            "editor": "#242936",
            "shell": "#1f2430",
            "elevated": "#2b3140",
            "tab_active": "#242936",
            "line": "#2a303f",
            "hover": "#272d3b",
            "selected": "#30384a",
            "selection": "#2f4a6b",
            "border": "#32394a",
            "border_variant": "#292f3e",
        },
        "guides": {
            "wrap": "#293040",
            "wrap_active": "#384154",
            "invisible": "#3c4559",
            "indent": "#293040",
            "indent_active": "#3b4459",
            "scroll": "#6e7c8f38",
            "scroll_hover": "#6e7c8f5c",
            "scroll_active": "#6e7c8f80",
            "minimap": "#6e7c8f30",
            "minimap_hover": "#6e7c8f50",
            "minimap_active": "#6e7c8f75",
            "doc_read": "#73d0ff1c",
            "doc_write": "#73d0ff2e",
            "doc_bracket": "#ffcc6624",
            "search": "#ffcc662b",
            "search_active": "#ffcc6655",
        },
        "palette": {
            "fg": "#c4c2bd",
            "ui_text": "#bab8b4",
            "ui_muted": "#7b8799",
            "ui_disabled": "#535d6e",
            "line_number": "#525c6d",
            "punct": "#929496",
            "comment": "#6e7c8f",
            "accent": "#ffcc66",
            "orange": "#ffa659",
            "gold": "#ffcd66",
            "green": "#d5ff80",
            "sky": "#73d0ff",
            "cyan": "#5ccfe6",
            "coral": "#f28779",
            "lavender": "#dfbfff",
            "peach": "#f29e74",
            "mint": "#95e6cb",
            "red": "#ff6666",
        },
        "git": {
            "added": "#87d96c",
            "modified": "#ebc05e",
            "deleted": "#f27983",
            "conflict": "#f09c54",
            "ignored": "#6e7c8f",
            "gutter_added": "#87d96c",
            "gutter_modified": "#80bfff",
            "gutter_deleted": "#f27983",
        },
        "ansi": {
            "black": "#1a1f29", "bright_black": "#6e7c8f",
            "red": "#f27983", "bright_red": "#f7949c",
            "green": "#87d96c", "bright_green": "#bdd96e",
            "yellow": "#ebc05e", "bright_yellow": "#ffd173",
            "blue": "#68bfe8", "bright_blue": "#80bfff",
            "magenta": "#cfb2eb", "bright_magenta": "#dfbfff",
            "cyan": "#85d1b8", "bright_cyan": "#95e6cb",
            "white": "#c4c2bd", "bright_white": "#e8e6e1",
        },
    },
    "light": {
        "label": "Ayu Light",
        "appearance": "light",
        "cursor": "#1a1d24",
        "unbordered": {
            "editor": "#f8f9fa",
            "shell": "#f8f9fa",
            "elevated": "#ffffff",
            "tab_active": "#ffffff",
            "line": "#eef1f5",
            "hover": "#edf0f4",
            "selected": "#e3e8ef",
            "selection": "#d2e3f8",
            "border": TRANSPARENT,
            "border_variant": TRANSPARENT,
        },
        "bordered": {
            "editor": "#fcfcfc",
            "shell": "#f3f5f7",
            "elevated": "#ffffff",
            "tab_active": "#fcfcfc",
            "line": "#f1f4f7",
            "hover": "#eaedf1",
            "selected": "#e1e6ed",
            "selection": "#d2e3f8",
            "border": "#dfe3e8",
            "border_variant": "#e8ecef",
        },
        "guides": {
            "wrap": "#e8ecef",
            "wrap_active": "#d4dae2",
            "invisible": "#cdd4dc",
            "indent": "#e8ecef",
            "indent_active": "#cfd6df",
            "scroll": "#6b7d8f28",
            "scroll_hover": "#6b7d8f44",
            "scroll_active": "#6b7d8f66",
            "minimap": "#6b7d8f22",
            "minimap_hover": "#6b7d8f3c",
            "minimap_active": "#6b7d8f5c",
            "doc_read": "#22a4e61c",
            "doc_write": "#22a4e630",
            "doc_bracket": "#f2971824",
            "search": "#f2971828",
            "search_active": "#f297184d",
        },
        "palette": {
            "fg": "#535a62",           # #020a12a3 over #f8f9fa, crisp and comfortable
            "ui_text": "#4c535b",
            "ui_muted": "#7d8690",
            "ui_disabled": "#adb4bc",
            "line_number": "#a6adb5",
            "punct": "#828991",
            "comment": "#959ca4",
            "accent": "#f29718",
            "orange": "#fa8532",
            "gold": "#eba400",
            "green": "#86b300",
            "sky": "#22a4e6",
            "cyan": "#55b4d4",
            "coral": "#f07171",
            "lavender": "#a37acc",
            "peach": "#ed9366",
            "mint": "#4cbf99",
            "red": "#e65050",
        },
        "git": {
            "added": "#58a634",
            "modified": "#c98900",
            "deleted": "#dc5868",
            "conflict": "#e37220",
            "ignored": "#959ca4",
            "gutter_added": "#6cbf43",
            "gutter_modified": "#478acc",
            "gutter_deleted": "#ed6475",
        },
        "ansi": {
            "black": "#4c535b", "bright_black": "#828991",
            "red": "#d94545", "bright_red": "#ed6475",
            "green": "#58a634", "bright_green": "#6d9400",
            "yellow": "#c98900", "bright_yellow": "#e88b12",
            "blue": "#1b8fcb", "bright_blue": "#478acc",
            "magenta": "#8a62b3", "bright_magenta": "#a37acc",
            "cyan": "#2f9e7b", "bright_cyan": "#3596b5",
            "white": "#e8ecef", "bright_white": "#f8f9fa",
        },
    },
}


def build_syntax(p, git):
    groups = [
        (tok(p["comment"], "italic", 400), ("comment", "comment.doc")),
        (tok(p["comment"], "normal", 400), ("hint", "predictive")),
        (tok(p["orange"]), (
            "keyword", "keyword.conditional", "keyword.control", "keyword.coroutine",
            "keyword.directive", "keyword.exception", "keyword.export", "keyword.function",
            "keyword.import", "keyword.modifier", "keyword.repeat", "keyword.return",
            "keyword.storage", "keyword.type", "preproc",
        )),
        (tok(p["peach"]), ("keyword.operator", "operator")),
        (tok(p["gold"]), (
            "function", "function.call", "function.definition", "function.method",
            "function.method.call", "attribute", "selector", "selector.pseudo",
        )),
        (tok(p["coral"]), (
            "function.builtin", "function.special",
        )),
        (tok(p["green"]), (
            "string", "string.doc", "string.special", "string.special.symbol",
            "text.literal", "link_text", "title",
        )),
        (tok(p["mint"]), ("string.regex", "string.escape")),
        (tok(p["sky"]), (
            "type", "type.interface", "type.parameter", "constructor", "namespace", "enum",
            "variable.member", "property", "property.json_key",
        )),
        (tok(p["cyan"]), (
            "type.builtin", "variable.special", "tag", "tag.doctype", "link_uri",
        )),
        (tok(p["lavender"]), (
            "number", "boolean", "constant", "constant.builtin", "variant", "variable.parameter",
        )),
        (tok(p["punct"]), (
            "punctuation", "punctuation.bracket", "punctuation.delimiter",
            "punctuation.list_marker", "punctuation.markup", "punctuation.special",
        )),
        (tok(p["fg"]), (
            "variable", "label", "embedded", "primary", "emphasis", "emphasis.strong",
        )),
        (tok(git["added"]), ("diff.plus",)),
        (tok(git["deleted"]), ("diff.minus",)),
    ]
    syntax = {}
    for entry, keys in groups:
        for key in keys:
            syntax[key] = dict(entry)
    return dict(sorted(syntax.items()))


def build_style(family, bordered):
    bg = family["bordered" if bordered else "unbordered"]
    g = family["guides"]
    p = family["palette"]
    git = family["git"]
    ansi = family["ansi"]

    g_add = blend(git["gutter_added"], GIT_DIM, bg["editor"])
    g_mod = blend(git["gutter_modified"], GIT_DIM, bg["editor"])
    g_del = blend(git["gutter_deleted"], GIT_DIM, bg["editor"])
    g_con = blend(git["conflict"], GIT_DIM, bg["editor"])

    return {
        "background.appearance": "opaque",
        "background": bg["shell"],
        "border": bg["border"],
        "border.variant": bg["border_variant"],
        "border.focused": p["accent"],
        "border.selected": p["accent"],
        "border.transparent": TRANSPARENT,
        "border.disabled": bg["border"],
        "elevated_surface.background": bg["elevated"],
        "surface.background": bg["shell"],
        "element.background": bg["elevated"],
        "element.hover": bg["hover"],
        "element.active": bg["selected"],
        "element.selected": bg["selected"],
        "element.disabled": bg["elevated"],
        "drop_target.background": p["accent"] + "2b",
        "ghost_element.background": TRANSPARENT,
        "ghost_element.hover": bg["hover"],
        "ghost_element.active": bg["selected"],
        "ghost_element.selected": bg["selected"],
        "ghost_element.disabled": TRANSPARENT,
        "text": p["ui_text"],
        "text.muted": p["ui_muted"],
        "text.placeholder": p["ui_muted"],
        "text.disabled": p["ui_disabled"],
        "text.accent": p["accent"],
        "icon": p["ui_text"],
        "icon.muted": p["ui_muted"],
        "icon.disabled": p["ui_disabled"],
        "icon.placeholder": p["ui_muted"],
        "icon.accent": p["accent"],
        "status_bar.background": bg["shell"],
        "title_bar.background": bg["shell"],
        "title_bar.inactive_background": bg["shell"],
        "toolbar.background": bg["editor"],
        "tab_bar.background": bg["shell"],
        "tab.inactive_background": bg["shell"],
        "tab.active_background": bg["tab_active"],
        "search.match_background": g["search"],
        "search.active_match_background": g["search_active"],
        "panel.background": bg["shell"],
        "panel.focused_border": p["accent"] if bordered else TRANSPARENT,
        "panel.indent_guide": g["indent"],
        "panel.indent_guide_active": g["indent_active"],
        "panel.indent_guide_hover": g["indent_active"],
        "pane.focused_border": TRANSPARENT,
        "pane_group.border": bg["border"],
        "scrollbar.thumb.background": g["scroll"],
        "scrollbar.thumb.hover_background": g["scroll_hover"],
        "scrollbar.thumb.active_background": g["scroll_active"],
        "scrollbar.thumb.border": TRANSPARENT,
        "scrollbar.track.background": TRANSPARENT,
        "scrollbar.track.border": TRANSPARENT,
        "minimap.thumb.background": g["minimap"],
        "minimap.thumb.hover_background": g["minimap_hover"],
        "minimap.thumb.active_background": g["minimap_active"],
        "minimap.thumb.border": TRANSPARENT,
        "editor.foreground": p["fg"],
        "editor.background": bg["editor"],
        "editor.gutter.background": bg["editor"],
        "editor.subheader.background": bg["elevated"],
        "editor.active_line.background": bg["line"],
        "editor.highlighted_line.background": bg["line"],
        "editor.line_number": p["line_number"],
        "editor.active_line_number": p["fg"],
        "editor.hover_line_number": p["fg"],
        "editor.invisible": g["invisible"],
        "editor.wrap_guide": g["wrap"],
        "editor.active_wrap_guide": g["wrap_active"],
        "editor.indent_guide": g["indent"],
        "editor.indent_guide_active": g["indent_active"],
        "editor.document_highlight.read_background": g["doc_read"],
        "editor.document_highlight.write_background": g["doc_write"],
        "editor.document_highlight.bracket_background": g["doc_bracket"],
        "link_text.hover": p["sky"],
        "terminal.background": bg["editor"],
        "terminal.foreground": p["fg"],
        "terminal.ansi.background": bg["editor"],
        "terminal.bright_foreground": ansi["bright_white"] if family["appearance"] == "dark" else "#2a2f36",
        "terminal.dim_foreground": p["ui_muted"],
        **{f"terminal.ansi.{k}": v for k, v in ansi.items()},
        **{
            f"{name}{suffix}": c + (a or "")
            for name, c in {
                "error": p["red"],
                "warning": p["accent"],
                "info": p["sky"],
                "hint": p["ui_muted"],
                "success": git["added"],
                "created": git["added"],
                "modified": git["modified"],
                "deleted": git["deleted"],
                "renamed": git["added"],
                "conflict": git["conflict"],
                "ignored": git["ignored"],
                "hidden": p["ui_disabled"],
                "unreachable": p["ui_muted"],
                "predictive": p["comment"],
            }.items()
            for suffix, a in (("", None), (".background", "1f"), (".border", "66"))
        },
        "hint.background": bg["elevated"],
        "version_control.added": g_add,
        "version_control.modified": g_mod,
        "version_control.deleted": g_del,
        "version_control.renamed": g_mod,
        "version_control.conflict": g_con,
        "version_control.ignored": git["ignored"],
        "version_control.word_added": g_add + "47",
        "version_control.word_deleted": g_del + "47",
        "players": [
            {"cursor": family["cursor"], "background": p["accent"], "selection": bg["selection"]},
            {"cursor": p["sky"], "background": p["sky"], "selection": p["sky"] + "3d"},
            {"cursor": p["green"], "background": p["green"], "selection": p["green"] + "3d"},
            {"cursor": p["lavender"], "background": p["lavender"], "selection": p["lavender"] + "3d"},
            {"cursor": p["coral"], "background": p["coral"], "selection": p["coral"] + "3d"},
        ],
        "accents": [p["accent"], p["sky"], p["green"], p["lavender"], p["coral"], p["mint"]],
        "syntax": build_syntax(p, git),
    }


def main():
    OUT.mkdir(exist_ok=True)
    themes = []
    for key in ("dark", "mirage", "light"):
        fam = FAMILIES[key]
        for bordered in (False, True):
            name = f"{fam['label']} Bordered Custom" if bordered else f"{fam['label']} Custom"
            themes.append({
                "name": name,
                "appearance": fam["appearance"],
                "style": build_style(fam, bordered),
            })

    family = {
        "$schema": SCHEMA,
        "name": "Ayu Custom",
        "author": AUTHOR,
        "themes": themes,
    }
    target = OUT / "ayu.json"
    target.write_text(json.dumps(family, indent=2, ensure_ascii=False) + "\n")
    for t in themes:
        print(f"themes/ayu.json: {t['name']} ({t['appearance']})")


if __name__ == "__main__":
    main()
