import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ed import *
import subprocess, os
O = sys.argv[1] if len(sys.argv) > 1 else "sortie"; os.makedirs(O, exist_ok=True)
NUM, DATE, T = "008", "NOV. 2026", 7
SLUG = "tranches-impot"
def nb(t): return f'<span style="white-space:nowrap;font:inherit;color:inherit">{t}</span>'
# Espace fine insécable des milliers, élargie : seule, elle disparaît presque en Instrument Serif.
TH = f'<span style="font:inherit;color:inherit;margin-left:.12em">{N}</span>'
def e(n, serif=False):
    # Montant en euros : milliers séparés, euro collé par une espace insécable.
    return nb(n.replace(" ", TH) + f"{S}€")
def p(t): return nb(f"{t}{S}%")
VU = f"consultées le {nb('8 novembre 2026')}"
SP = f"{nb('service-public.gouv.fr')}, fiche F1419 «{S}Quel est le barème de l’impôt sur le revenu{S}?{S}», vérifiée le {nb('15 avril 2026')}"
IMP = f"impots.gouv.fr, «{S}À quoi correspondent le taux moyen et le taux marginal d’imposition affichés sur l’avis d’impôt sur le revenu{S}?{S}»"
LAB = "font:700 22px/1.3 var(--font-texte);letter-spacing:.12em;text-transform:uppercase;color:var(--texte-doux)"

def bareme(rows):
    # Le barème : la tranche à gauche, le taux en serif à droite, filets de journal.
    out = (f'<div style="display:flex;justify-content:space-between;padding:0 0 12px"><span style="{LAB}">Revenu, pour une part</span>'
           f'<span style="{LAB}">Taux</span></div><div style="border-top:2px solid var(--texte)">')
    for k, v in rows:
        out += (f'<div style="display:flex;justify-content:space-between;align-items:baseline;gap:32px;padding:20px 0 16px;border-bottom:1px solid var(--filet)">'
                f'<span style="font:700 36px/1.2 var(--font-texte);font-variant-numeric:tabular-nums">{k}</span>'
                f'<span style="font-family:var(--font-titre);font-size:76px;line-height:.9;color:var(--accent);font-style:italic;white-space:nowrap;padding-right:4px">{v}</span></div>')
    return out + '</div>'

def decoupe(parts, total):
    # 30 000 € coupés en trois morceaux, à l'échelle : la part taxée à 30 % est une fine tranche.
    fonds = ["var(--fond-2)", "var(--sapin)", "var(--lime)"]
    barre = '<div style="display:flex;height:96px;gap:4px">'
    for (m, _t, _i), f in zip(parts, fonds):
        barre += f'<div style="flex:{m} 0 0;background:{f};min-width:10px;box-shadow:inset 0 0 0 2px var(--sapin)"></div>'
    barre += '</div>'
    g = "display:grid;grid-template-columns:1fr 150px 290px;column-gap:24px;align-items:baseline"
    lignes = (f'<div style="{g};padding:30px 0 12px"><span style="{LAB}">Part du revenu</span>'
              f'<span style="{LAB};text-align:right">Taux</span><span style="{LAB};text-align:right">Impôt</span></div>')
    for i, ((m, t, imp), f) in enumerate(zip(parts, fonds)):
        bord = "2px solid var(--texte)" if i == 0 else "1px solid var(--filet)"
        lignes += (f'<div style="{g};border-top:{bord};padding:18px 0 14px">'
                   f'<span style="font:700 34px/1.2 var(--font-texte);display:flex;align-items:center;gap:18px">'
                   f'<i style="display:inline-block;width:28px;height:28px;background:{f};box-shadow:inset 0 0 0 2px var(--sapin);flex:none"></i>{e(f"{m:,}".replace(",", " "))}</span>'
                   f'<span style="font:400 34px/1.2 var(--font-texte);text-align:right">{p(t)}</span>'
                   f'<span style="font-family:var(--font-titre);font-size:58px;line-height:1;text-align:right;white-space:nowrap">{imp}</span></div>')
    lignes += (f'<div style="{g};border-top:2px solid var(--texte);padding:20px 0 0">'
               f'<span style="font:700 34px/1.2 var(--font-texte)">Impôt brut</span><span></span>'
               f'<span style="font-family:var(--font-titre);font-size:64px;line-height:1;text-align:right;white-space:nowrap;color:var(--accent);font-style:italic">{total}</span></div>')
    return barre + lignes

def siAlors(rows):
    # Une ligne = un filet sur toute la largeur : la situation à gauche, l'effet en serif à droite.
    out = ''
    for i, (q, eff) in enumerate(rows):
        bord = "2px solid var(--texte)" if i == 0 else "1px solid var(--filet)"
        out += (f'<div style="display:grid;grid-template-columns:330px 1fr;column-gap:32px;align-items:baseline;border-top:{bord};padding:30px 0 26px">'
                f'<div style="font:700 32px/1.25 var(--font-texte)">{q}</div>'
                f'<div style="font-family:var(--font-titre);font-size:66px;line-height:1.02">{eff}</div></div>')
    return out + '<div style="border-top:1px solid var(--filet)"></div>'

pages = []
# 1 - Une : l'idée reçue, barrée
pages.append(page("papier",
  tete("papier", NUM, DATE)
  + f'<div class="ed-corps"><p class="ed-rubrique">Le chiffre</p><div class="ed-g1"></div>'
    f'<h1 class="ed-titre" style="font-size:108px">Passer à {p("30")}, <em>ce n’est pas payer {p("30")} sur tout.</em></h1><div class="ed-g1"></div>'
    f'<p class="ed-chapo ed-doux">L’impôt sur le revenu se calcule par tranches. Chaque taux ne touche que la part de ton revenu qui tombe dans sa tranche.</p>'
    f'<div style="flex:1"></div><p style="margin:0 0 22px;{LAB}">L’idée reçue</p>'
    f'<div class="ed-barres"><p class="ed-barre">«{S}Je change de tranche,</p><p class="ed-barre">donc je gagne moins.{S}»</p></div></div>'
  + pied(f"Sources{S}: service-public.gouv.fr, impots.gouv.fr, {VU}. Barème de l’impôt sur le revenu appliqué aux revenus de 2025.", 1, T)))
# 2 - Le barème
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">Le barème 2026</p><div class="ed-g1"></div>'
    f'<h2 class="ed-titre m">Cinq tranches, <em>cinq taux.</em><span class="ed-sup">1</span></h2><div class="ed-g2"></div>'
    + bareme([(f"Jusqu’à {e('11 600')}", p("0")),
              (f"De {e('11 601')} à {e('29 579')}", p("11")),
              (f"De {e('29 580')} à {e('84 577')}", p("30")),
              (f"De {e('84 578')} à {e('181 917')}", p("41")),
              (f"Plus de {e('181 917')}", p("45"))])
    + f'<div style="flex:1"></div>'
    f'<p class="ed-texte ed-doux">Une part, c’est une personne seule sans enfant. Un couple marié ou pacsé a deux parts{S}: le barème s’applique à la moitié de son revenu, puis l’impôt est doublé.</p></div>'
  + pied(f"1. {SP}. Barème fixé par la loi de finances pour 2026, appliqué aux revenus de 2025. Le nombre de parts, c’est le quotient familial.", 2, T)))
# 3 - La règle, sur l'exemple officiel
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">La règle</p><div class="ed-g1"></div>'
    f'<h2 class="ed-titre m">Chaque taux ne touche <em>que sa tranche.</em><span class="ed-sup">2</span></h2><div class="ed-g1"></div>'
    f'<p class="ed-texte ed-doux">L’exemple officiel{S}: une personne seule, {e("30 000")} de revenu net imposable.</p><div class="ed-g2"></div>'
    + decoupe([(11600, "0", f"0{S}€"), (17979, "11", f"1{TH}977,69{S}€"), (421, "30", f"126,30{S}€")], f"2{TH}103,99{S}€")
    + '</div>'
  + pied(f"2. {SP}, exemple d’une personne seule (une part). Impôt brut{S}: le résultat du barème, qui «{S}n’est qu’un élément du calcul de l’impôt sur le revenu{S}».", 3, T)))
# 4 - Le chiffre
pages.append(page("sapin",
  tete("sapin", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">Le chiffre</p><div style="flex:1"></div>'
    f'<p class="ed-chiffre" style="color:var(--lime);font-size:280px">7,01<small>{S}%</small></p><div class="ed-g2"></div>'
    f'<p class="ed-inter" style="font-size:58px">C’est le taux moyen de cette personne{S}: {e("2 103,99", True)} d’impôt brut pour {e("30 000", True)} de revenu.<span class="ed-sup">3</span></p><div class="ed-g2"></div>'
    f'<p class="ed-texte ed-doux">Son taux marginal, celui de sa tranche la plus haute, est de <b>{p("30")}</b>. Il ne s’applique qu’à <b>{e("421")}</b>.</p></div>'
  + pied(f"3. {SP}{N}; {IMP}. Taux moyen{S}: l’impôt rapporté au revenu. Taux marginal{S}: le taux de la tranche la plus élevée de tes revenus.", 4, T)))
# 5 - Si tu es augmenté (si / alors)
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">Si tu es augmenté</p><div class="ed-g1"></div>'
    f'<h2 class="ed-titre m">{e("1 000", True)} de plus, <em>{e("300", True)} d’impôt en plus.</em><span class="ed-sup">4</span></h2><div class="ed-g2"></div>'
    + siAlors([(f'Les {nb(f"30{TH}000")} premiers euros', f'taxés comme avant{S}: {e("2 103,99", True)}'),
               (f'Les {e("1 000")} en plus', f'taxés à {p("30")}{S}: {e("300", True)}'),
               ('Ce qu’il te reste', f'<em style="color:var(--accent)">{e("700", True)} de plus</em>')])
    + f'<div style="flex:1"></div>'
    f'<p class="ed-texte ed-doux">Dans le barème, chaque euro en plus est taxé au taux de sa tranche, {p("45")} au plus. Une augmentation laisse donc toujours plus qu’avant.</p></div>'
  + pied(f"4. Calcul Parlons Placement avec le barème de la fiche F1419, pour une part{S}: ({e("31 000")} − {e("29 579")}) × {p("30")} + {e("1 977,69")} = {e("2 403,99")} d’impôt brut, soit {e("300")} de plus qu’à {e("30 000")}. Ce post ne traite que du barème de l’impôt sur le revenu.", 5, T)))
# 6 - Le document + à retenir
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">Le document</p><div class="ed-g1"></div>'
    f'<div class="ed-coupure"><div class="src">service-public.gouv.fr · Particuliers</div><div class="date">Vérifié le {nb("15 avril 2026")}</div>'
    f'<p class="titre" style="font-size:72px">«{S}Quel est le barème de l’impôt sur le revenu{S}?{S}»</p>'
    f'<div class="url" style="word-break:normal">service-public.gouv.fr/particuliers/vosdroits/F1419</div></div>'
    f'<div style="flex:1"></div><p style="margin:0 0 6px;{LAB}">À retenir</p>'
    f'<ol class="ed-liste"><li><div><b>Cinq tranches, de {p("0")} à {p("45")}</b></div></li>'
    f'<li><div><b>Chaque taux ne touche que sa tranche</b><span>Le taux marginal ne vise pas tout le revenu.</span></div></li>'
    f'<li><div><b>Changer de tranche ne fait rien perdre</b><span>Seuls les euros en plus sont taxés plus.</span></div></li></ol></div>'
  + pied("Titre cité tel que publié sur service-public.gouv.fr. Lien complet en légende.", 6, T)))
# 7 - Parlons-en + colophon
pages.append(page("sapin",
  tete("sapin", NUM, DATE, True)
  + f'<div class="ed-corps"><h2 class="ed-titre">Une question{S}? <em>Parlons-en.</em></h2><div class="ed-g1"></div>'
    f'<p class="ed-chapo ed-doux">Envoie ce post à quelqu’un qui a peur de changer de tranche.</p><div style="flex:1"></div>'
    f'<div class="ed-colo"><div><h4>Sources</h4>'
    f'<p><b>service-public.gouv.fr</b>, fiche F1419 «{S}Quel est le barème de l’impôt sur le revenu{S}?{S}», vérifiée le {nb("15 avril 2026")}.</p>'
    f'<p><b>impots.gouv.fr</b>, «{S}À quoi correspondent le taux moyen et le taux marginal d’imposition affichés sur l’avis d’impôt sur le revenu{S}?{S}».</p></div>'
    f'<div><h4>Ce post</h4><p>Rédaction{S}: Parlons Placement, novembre 2026. Sources {nb("consultées le 8 novembre 2026")}.</p>'
    f'<p>Calculs pour une part, sur l’impôt brut, avec le barème appliqué aux revenus de 2025.</p>'
    f'<p>Contenu pédagogique. Ne constitue pas un conseil en investissement personnalisé.</p></div></div></div>'
  + pied("@parlonsplacement", 7, T, suite=False)))
if __name__ == '__main__':
  for i, pg in enumerate(pages, 1):
    h = os.path.abspath(f"{O}/page_{i}.html"); open(h, "w").write(doc(pg))
    subprocess.run(["python3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "render.py"), h, f"{O}/{SLUG}-{i:02d}.png", "1080", "1350"], check=True)
print("ok")
