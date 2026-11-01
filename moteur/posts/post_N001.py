import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ed import *
import subprocess, os
O = sys.argv[1] if len(sys.argv) > 1 else "sortie"; os.makedirs(O, exist_ok=True)
NUM, DATE, T = "001", "NOV. 2026", 3
pages = []
pages.append(page("sapin",
  tete("sapin", NUM, DATE)
  + f'<div class="ed-corps bas"><p class="ed-rubrique" style="color:var(--lime)">Le manifeste</p><div class="ed-g1"></div>'
    f'<h1 class="ed-titre" style="font-size:138px">On va parler d\'argent. <em>Simplement.</em></h1><div class="ed-g2"></div>'
    f'<p class="ed-chapo ed-doux">L\'épargne, le logement, la bourse, la retraite. Ce que ça change pour toi, expliqué clairement, chiffres et sources à l\'appui.</p></div>'
  + pied("Parlons Placement, le média qui parle d'argent comme on en parle entre amis.", 1, T)))
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">Ce que tu trouveras ici</p><div class="ed-g1"></div>'
    f'<h2 class="ed-titre m">Du concret, <em>sourcé.</em></h2><div class="ed-g2"></div>'
    f'<ol class="ed-liste"><li><div><b>Ce que ça change pour toi</b><span>Ton livret, ton loyer, ton crédit, ta retraite, tes impôts.</span></div></li>'
    f'<li><div><b>Chaque chiffre a sa source</b><span>Datée, citée en bas de page. Tu peux tout vérifier.</span></div></li>'
    f'<li><div><b>Des histoires vraies</b><span>Des gens qui racontent leur argent, leurs choix et leurs erreurs.</span></div></li></ol>'
    f'<div style="flex:1"></div><div class="ed-marge"><div class="m">Au sommaire</div><div class="t"><p class="ed-texte">Les bases · Le chiffre · La source · Face à face · Côté CGP · et <b>Parlons-en</b>, nos conversations avec celles et ceux qui vivent l\'argent au quotidien.</p></div></div></div>'
  + pied("Sources citées dans chaque publication, liens en légende.", 2, T)))
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">Ce que tu ne liras jamais ici</p><div class="ed-g3"></div>'
    f'<div class="ed-barres"><span class="ed-barre">« Achète maintenant »</span><span class="ed-barre">« Rendement garanti »</span>'
    f'<span class="ed-barre">« Sans aucun risque »</span><span class="ed-barre">« Devenir riche en 6 mois »</span></div>'
    f'<div style="flex:1"></div><p class="ed-chapo"><b>On explique, tu décides.</b> Aucun contenu Parlons Placement n\'est un conseil en investissement personnalisé.</p>'
    f'<div class="ed-g1"></div><p class="ed-inter">Abonne-toi. <em>Parlons-en.</em></p></div>'
  + pied("@parlonsplacement", 3, T, suite=False)))
if __name__ == '__main__':
  for i, p in enumerate(pages, 1):
    h = os.path.abspath(f"{O}/page_{i}.html"); open(h, "w").write(doc(p))
    subprocess.run(["python3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "render.py"), h, f"{O}/manifeste-{i:02d}.png", "1080", "1350"], check=True)
print("ok")
