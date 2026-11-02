import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ed import *
import subprocess, os
O = sys.argv[1] if len(sys.argv) > 1 else "sortie"; os.makedirs(O, exist_ok=True)
NUM, DATE, T = "003", "NOV. 2026", 8
SLUG = "livret-a-ldds-lep"
ER = '1<sup class="o">er</sup>'
def nb(t): return f'<span style="white-space:nowrap">{t}</span>'
D_AOUT, D_JANV, D_31DEC = nb(f"{ER} août 2026"), nb("31 janvier 2027"), nb("31 décembre")
D_15JUIL, D_31JUIL = nb("15 juillet 2026"), nb("31 juillet 2026")
VU = f"consultée le {nb('2 novembre 2026')}"
SP = "service-public.gouv.fr"
SRC_TOUS = f"Source{S}: {SP}, fiches «{S}{nb("Livret A")}{S}», «{S}LDDS{S}» et «{S}LEP{S}», {VU}."

def barres(rows, vmax):
    # Graphique maison : barres horizontales, angles droits, sans dégradé.
    out = ('<p style="margin:0 0 18px;font:700 22px/1.3 var(--font-texte);letter-spacing:.12em;'
           'text-transform:uppercase;color:var(--texte-doux)">Plafond des versements</p>'
           '<div style="display:flex;flex-direction:column;gap:14px">')
    for nom, v, txt in rows:
        w = v / vmax * 100
        out += (f'<div style="display:grid;grid-template-columns:150px 1fr;column-gap:24px;align-items:center">'
                f'<span style="font:700 28px/1 var(--font-texte)">{nom}</span>'
                f'<div style="height:76px;background:var(--fond-2)"><div style="width:{w:.1f}%;height:100%;background:var(--sapin);'
                f'display:flex;align-items:center;justify-content:flex-end;padding-right:22px;color:var(--papier);'
                f'font:600 30px/1 var(--font-texte);font-variant-numeric:tabular-nums">{txt}</div></div></div>')
    return out + '</div>'

def duo(items):
    # Deux chiffres côte à côte, séparés par un filet.
    cells = ""
    for i, (lab, val) in enumerate(items):
        bord = "border-left:1px solid var(--filet);padding-left:40px;" if i else ""
        cells += (f'<div style="{bord}"><div style="font:700 22px/1.3 var(--font-texte);letter-spacing:.12em;text-transform:uppercase;'
                  f'color:var(--texte-doux)">{lab}</div><div style="font-family:var(--font-titre);font-size:120px;line-height:1;margin-top:10px">{val}</div></div>')
    return f'<div style="display:grid;grid-template-columns:1fr 1fr;column-gap:40px;border-top:2px solid var(--texte);padding-top:22px">{cells}</div>'

def tableau(entete, lignes):
    # Le face-à-face : une grille à filets, comme un tableau de journal.
    g = 'display:grid;grid-template-columns:190px 1fr 1fr 1fr;column-gap:20px;'
    h = f'<div style="{g}padding-bottom:16px;border-bottom:2px solid var(--texte)"><span></span>'
    h += "".join(f'<span style="font:700 30px/1.1 var(--font-texte)">{e}</span>' for e in entete) + '</div>'
    for lab, vals, serif in lignes:
        st = ("font-family:var(--font-titre);font-size:58px;line-height:1" if serif
              else "font:500 28px/1.3 var(--font-texte)")
        h += (f'<div style="{g}padding:24px 0;border-bottom:1px solid var(--filet);align-items:baseline">'
              f'<span style="font:700 22px/1.3 var(--font-texte);letter-spacing:.12em;text-transform:uppercase;color:var(--texte-doux)">{lab}</span>'
              + "".join(f'<span style="{st}">{v}</span>' for v in vals) + '</div>')
    return h

pages = []
# 1 - Une
pages.append(page("papier",
  tete("papier", NUM, DATE)
  + f'<div class="ed-corps"><p class="ed-rubrique">Face à face</p><div class="ed-g1"></div>'
    f'<h1 class="ed-titre">Livret A, LDDS, LEP{S}: <em>qui peut ouvrir quoi{S}?</em></h1><div class="ed-g1"></div>'
    f'<p class="ed-chapo ed-doux">Trois livrets d’épargne réglementée, trois règles d’accès. Conditions, plafonds, taux{S}: on pose tout côte à côte.</p>'
    f'<div style="flex:1"></div>'
    + barres([("Livret A", 22950, f"22{N}950{S}€"), ("LDDS", 12000, f"12{N}000{S}€"), ("LEP", 10000, f"10{N}000{S}€")], 22950)
    + '</div>'
  + pied(SRC_TOUS, 1, T)))
# 2 - Le Livret A
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">Le Livret A</p><div class="ed-g1"></div>'
    f'<h2 class="ed-titre">Ouvert à <em>tout le monde.</em></h2><div class="ed-g2"></div>'
    f'<p class="ed-chapo">Toute personne peut en ouvrir un, même un mineur. Aucune condition de revenus.</p>'
    f'<div style="flex:1"></div>'
    + duo([("Plafond", f"22{N}950{S}€"), ("Taux", f"1,7{S}%")])
    + f'<div class="ed-g2"></div><p class="ed-texte ed-doux">Un seul Livret A par personne.<span class="ed-sup">1</span></p></div>'
  + pied(f"1. {SP}, fiche «{S}Livret A{S}», {VU}. Taux en vigueur du {D_AOUT} au {D_JANV}.", 2, T)))
# 3 - Le LDDS
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">Le LDDS</p><div class="ed-g1"></div>'
    f'<h2 class="ed-titre m">Il faut <em>ton propre foyer fiscal.</em></h2><div class="ed-g1"></div>'
    f'<p class="ed-texte ed-doux">Livret de développement durable et solidaire.</p>'
    f'<div style="flex:1"></div>'
    f'<div class="ed-marge"><div class="m">Qui</div><div class="t"><p class="ed-texte">Toute personne domiciliée fiscalement en France. Aucune condition de revenus.</p></div></div><div class="ed-g1"></div>'
    f'<div class="ed-marge"><div class="m">Sauf</div><div class="t"><p class="ed-texte">Si tu es rattaché au foyer fiscal de tes parents, c’est-à-dire inscrit sur leur déclaration.</p></div></div><div class="ed-g2"></div>'
    + f'<div class="ed-marge"><div class="m">Plafond</div><div class="t"><p class="ed-inter" style="font-size:96px">12{N}000{S}€</p></div></div><div class="ed-g1"></div>'
    + f'<div class="ed-marge"><div class="m">Taux</div><div class="t"><p class="ed-inter" style="font-size:96px">1,7{S}% <em style="font-size:56px">comme le Livret A</em></p></div></div>'
    + '</div>'
  + pied(f"Source{S}: {SP}, fiche «{S}Livret de développement durable et solidaire (LDDS){S}», {VU}.", 3, T)))
# 4 - Le LEP (si / alors)
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">Le LEP · Livret d’épargne populaire</p><div class="ed-g1"></div>'
    f'<h2 class="ed-titre m">Une question <em>de revenus.</em></h2><div class="ed-g2"></div>'
    f'<div class="ed-fleche" style="grid-template-columns:170px 1fr"><div class="quand">Si</div><div class="effet">ton revenu fiscal de référence ne dépasse pas un plafond,</div>'
    f'<div class="quand">Alors</div><div class="effet">tu peux ouvrir un LEP{S}: jusqu’à 10{N}000{S}€, à 2,5{S}%.</div></div>'
    f'<div style="flex:1"></div>'
    f'<p class="ed-texte ed-doux">Comme pour le LDDS{S}: domicile fiscal en France, sans être rattaché à tes parents. Preuve demandée{S}: ton avis d’impôt.</p></div>'
  + pied(f"Source{S}: {SP}, fiche «{S}Livret d’épargne populaire (LEP){S}», {VU}.", 4, T)))
# 5 - Le chiffre
pages.append(page("sapin",
  tete("sapin", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">Le chiffre</p><div style="flex:1"></div>'
    f'<p class="ed-chiffre" style="color:var(--lime);font-size:300px">23{N}028<small>{S}€</small></p><div class="ed-g2"></div>'
    f'<p class="ed-inter">Le revenu fiscal de référence maximal pour ouvrir un LEP en 2026, avec une part, en métropole.<span class="ed-sup">2</span></p><div class="ed-g2"></div>'
    f'<p class="ed-texte ed-doux">Une part, c’est par exemple une personne seule sans enfant. Chaque demi-part en plus ajoute 6{N}149{S}€.</p></div>'
  + pied(f"2. {SP}, fiches «{S}LEP{S}» et «{S}Quotient familial d’une personne seule{S}», {VU}. Revenu de l’année N-2 ou N-1 selon la date de la demande. Plafonds plus élevés en outre-mer.", 5, T)))
# 6 - Le face-à-face
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">Le face-à-face</p><div class="ed-g1"></div>'
    f'<h2 class="ed-titre m">Les trois, <em>côte à côte.</em></h2><div class="ed-g3"></div>'
    + tableau(["Livret A", "LDDS", "LEP"], [
        ("Pour qui", ["Tout le monde, même mineur", "Domicile fiscal en France", "Revenus sous un plafond"], False),
        ("Plafond", [f"22{N}950{S}€", f"12{N}000{S}€", f"10{N}000{S}€"], True),
        ("Taux", [f"1,7{S}%", f"1,7{S}%", f"2,5{S}%"], True),
        ("Impôts", ["Exonéré", "Exonéré", "Exonéré"], False)])
    + f'<div style="flex:1"></div><p class="ed-texte ed-doux" style="font-size:30px">Exonéré{S}: ni impôt sur le revenu, ni prélèvements sociaux sur les intérêts.</p></div>'
  + pied(f"{SRC_TOUS} Taux en vigueur du {D_AOUT} au {D_JANV}.", 6, T)))
# 7 - À retenir
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">À retenir</p><div class="ed-g1"></div>'
    f'<h2 class="ed-titre">Ce qui vaut <em>pour les trois.</em></h2><div class="ed-g3"></div>'
    f'<ol class="ed-liste"><li><div><b>Un seul de chaque par personne</b><span>LDDS et LEP{S}: deux au plus par couple marié ou pacsé.</span></div></li>'
    f'<li><div><b>Des intérêts sans impôt</b><span>Ajoutés au livret chaque {D_31DEC}.</span></div></li>'
    f'<li><div><b>Des taux fixés pour six mois</b><span>Du {D_AOUT} au {D_JANV}.</span></div></li></ol></div>'
  + pied(f"{SRC_TOUS} Actualité {SP} du {D_15JUIL} sur les taux au {D_AOUT}.", 7, T)))
# 8 - Parlons-en + colophon
pages.append(page("sapin",
  tete("sapin", NUM, DATE, True)
  + f'<div class="ed-corps"><h2 class="ed-titre">Une question{S}? <em>Parlons-en.</em></h2><div class="ed-g1"></div>'
    f'<p class="ed-chapo ed-doux">Pose-la en commentaire. Les plus fréquentes deviennent un prochain post.</p><div style="flex:1"></div>'
    f'<div class="ed-colo"><div><h4>Sources</h4>'
    f'<p><b>{SP}</b>, fiches «{S}{nb("Livret A")}{S}», «{S}Livret de développement durable et solidaire (LDDS){S}», «{S}Livret d’épargne populaire (LEP){S}» et «{S}Quotient familial d’une personne seule{S}», {VU}.</p>'
    f'<p><b>{SP}</b>, actualité du {D_15JUIL}, mise à jour le {D_31JUIL}, sur les taux au {D_AOUT}.</p></div>'
    f'<div><h4>Ce post</h4><p>Rédaction{S}: Parlons Placement, novembre 2026.</p><p>Contenu pédagogique. Ne constitue pas un conseil en investissement personnalisé.</p></div></div></div>'
  + pied("@parlonsplacement", 8, T, suite=False)))
if __name__ == '__main__':
  for i, p in enumerate(pages, 1):
    h = os.path.abspath(f"{O}/page_{i}.html"); open(h, "w").write(doc(p))
    subprocess.run(["python3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "render.py"), h, f"{O}/{SLUG}-{i:02d}.png", "1080", "1350"], check=True)
print("ok")
