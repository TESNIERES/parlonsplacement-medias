# Parlons Placement - générateur style ÉDITION
import os
ICI = os.path.dirname(os.path.abspath(__file__))
LOGO = {"sapin": open(os.path.join(ICI, "logos/pp-logo-horizontal-transparent-sapin.svg")).read(),
        "papier": open(os.path.join(ICI, "logos/pp-logo-horizontal-transparent-papier.svg")).read()}
N = " "; S = " "
def logo_for(theme): return LOGO["papier"] if theme in ("sapin", "encre") else LOGO["sapin"]

def tete(theme, numero, date, mini=False):
    return (f'<header class="ed-tete{" mini" if mini else ""}"><div class="logo">{logo_for(theme)}</div>'
            f'<div class="num">N°{numero}{S}·{S}{date}</div></header>')

def pied(notes, folio, total, suite=True):
    f = f'{folio}{S}/{S}{total}' + ('<i>→</i>' if suite and folio != total else '')
    return f'<footer class="ed-pied"><p class="ed-notes">{notes}</p><div class="ed-folio">{f}</div></footer>'

def page(theme, inner, extra=""):
    return f'<section class="ed {extra}" data-theme="{theme}">{inner}</section>'

def doc(sections, css_prefix=ICI + "/"):
    return (f'<!doctype html><html lang="fr"><head><meta charset="utf-8">'
            f'<link rel="stylesheet" href="{css_prefix}tokens.css"><link rel="stylesheet" href="{css_prefix}edition.css">'
            f'<style>html,body{{margin:0;background:#888}}body{{display:flex;flex-wrap:wrap;gap:0}}</style></head><body>{sections}</body></html>')

def cal(days=30, start=5, key=(1, 16)):
    # start: 0=lundi ... ; jours 1-15 clair, 16+ sapin
    cells = ["<span class='x'></span>"] * start
    for d in range(1, days + 1):
        cls = "b" if d >= 16 else ""
        if d in key: cls += " k"
        cells.append(f"<span class='{cls.strip()}'>{d}</span>")
    while len(cells) % 7: cells.append("<span class='x'></span>")
    head = "".join(f"<span class='x' style='height:40px;font-size:20px;color:var(--texte-doux)'>{j}</span>" for j in "LMMJVSD")
    return f'<div class="ed-cal">{head}{"".join(cells)}</div>'
