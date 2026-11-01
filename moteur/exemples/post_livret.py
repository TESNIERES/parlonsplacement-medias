import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ed import *
import subprocess, os
O = sys.argv[1] if len(sys.argv) > 1 else "sortie"; os.makedirs(O, exist_ok=True)
NUM, DATE, T = "002", "NOV. 2026", 8
SRC1 = f"Source{S}: service-public.gouv.fr, fiche « Livret A », vérifiée le 1er août 2026."
pages = []
# 1 - Une
pages.append(page("papier",
  tete("papier", NUM, DATE)
  + f'<div class="ed-corps"><p class="ed-rubrique">Épargne · Mode d\'emploi</p><div class="ed-g1"></div>'
    f'<h1 class="ed-titre">Livret A{S}: le jour où tu verses <em>compte</em>.</h1><div class="ed-g1"></div>'
    f'<p class="ed-chapo ed-doux">Les intérêts ne se calculent pas au jour près, mais par quinzaine. Une règle que peu de gens connaissent.</p>'
    f'<div style="flex:1"></div>{cal(30, 6)}<div class="ed-g1"></div>'
    f'<div class="ed-cal-l"><span><i style="background:var(--fond-2)"></i>1re quinzaine</span><span><i style="background:var(--sapin)"></i>2e quinzaine</span>'
    f'<span><i style="box-shadow:inset 0 0 0 4px var(--lime)"></i>les deux dates qui comptent</span></div></div>'
  + pied(SRC1, 1, T)))
# 2 - La règle
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">La règle</p><div class="ed-g1"></div>'
    f'<h2 class="ed-titre m">Deux dates par mois{S}: <em>le 1<sup class="o">er</sup> et le 16.</em></h2><div class="ed-g3"></div>'
    f'<div class="ed-frise grand"><div class="q1"><b>1 → 15</b><span>1re quinzaine</span></div><div class="q2"><b>16 → 30</b><span>2e quinzaine (jusqu\'au 31 selon le mois)</span></div></div>'
    f'<div style="flex:1"></div>'
    f'<p class="ed-texte">Ta banque calcule les intérêts du Livret A sur ces périodes de 15 jours, les <b>quinzaines</b>. Une somme ne rapporte que si elle reste sur le livret une quinzaine entière.<span class="ed-sup">1</span></p></div>'
  + pied("1. service-public.gouv.fr, fiche « Livret A ».", 2, T)))
# 3 - Versements
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">Quand tu verses</p><div class="ed-g1"></div>'
    f'<h2 class="ed-titre m">Ton argent attend la <em>quinzaine suivante.</em></h2><div class="ed-g3"></div>'
    f'<div class="ed-fleche"><div class="quand">Versé entre le 1er et le 15</div><div class="effet">rapporte à partir du 16.</div>'
    f'<div class="quand">Versé à partir du 16</div><div class="effet">rapporte à partir du 1<sup class="o">er</sup> du mois suivant.</div></div>'
    f'<div style="flex:1"></div><p class="ed-texte ed-doux">Exemple{S}: versés le 15 novembre, tes euros rapportent dès le 16. Versés le 16, ils attendent le 1er décembre.</p></div>'
  + pied(SRC1, 3, T)))
# 4 - Retraits
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">Quand tu retires</p><div class="ed-g1"></div>'
    f'<h2 class="ed-titre m">Pour un retrait, <em>c\'est l\'inverse.</em></h2><div class="ed-g3"></div>'
    f'<div class="ed-fleche"><div class="quand">Retiré entre le 1er et le 15</div><div class="effet">ne rapporte plus rien depuis le 1<sup class="o">er</sup>.</div>'
    f'<div class="quand">Retiré à partir du 16</div><div class="effet">ne rapporte plus rien depuis le 16.</div></div>'
    f'<div style="flex:1"></div><p class="ed-texte ed-doux">Autrement dit, une somme retirée le 14 ne touche aucun intérêt pour la quinzaine en cours.</p></div>'
  + pied(SRC1, 4, T)))
# 5 - Le chiffre
pages.append(page("sapin",
  tete("sapin", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">Le chiffre</p><div style="flex:1"></div>'
    f'<p class="ed-chiffre" style="color:var(--lime)">7,08<small>{S}€</small></p><div class="ed-g2"></div>'
    f'<p class="ed-inter">C\'est ce que rapporte une quinzaine sur 10{N}000{S}€ placés à 1,7{S}%.<span class="ed-sup">2</span></p><div class="ed-g2"></div>'
    f'<p class="ed-texte ed-doux">Pas de quoi changer de vie. Mais c\'est ton argent{S}: autant connaître la règle.</p></div>'
  + pied(f"2. Calcul Parlons Placement{S}: 10{N}000{S}€ × 1,7{S}% ÷ 24 quinzaines. Taux en vigueur du 1er août 2026 au 31 janvier 2027 (service-public.gouv.fr).", 5, T)))
# 6 - La source
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">La source</p><div class="ed-g3"></div><div class="ed-g2"></div>'
    f'<div class="ed-coupure"><div class="src">info.gouv.fr · Gouvernement</div><div class="date">Publié le 31 juillet 2026</div>'
    f'<p class="titre">« Le taux du livret A augmente à compter du 1<sup class="o">er</sup> août 2026 »</p>'
    f'<div class="url">info.gouv.fr/actualite/augmentation-du-taux-du-livret-a-a-compter-du-1er-aout-2026</div></div>'
    f'<div style="flex:1"></div><div class="ed-marge"><div class="m">En clair</div><div class="t"><p class="ed-texte">Le taux est passé de <b>1,5{S}% à 1,7{S}%</b> au 1er août 2026. Il est revu deux fois par an{S}: prochaine révision le <b>1er février 2027</b>.</p></div></div></div>'
  + pied(f"Titre cité tel que publié sur info.gouv.fr. Lien complet en légende.", 6, T)))
# 7 - À retenir
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">À retenir</p><div class="ed-g1"></div>'
    f'<h2 class="ed-titre m">Trois choses <em>à savoir.</em></h2><div class="ed-g2"></div>'
    f'<ol class="ed-liste"><li><div><b>Les intérêts comptent par quinzaine</b><span>À partir du 1er ou du 16 de chaque mois.</span></div></li>'
    f'<li><div><b>Ils sont versés une fois par an</b><span>Le 31 décembre, sans impôt ni prélèvements sociaux.</span></div></li>'
    f'<li><div><b>Le plafond est de 22{N}950{S}€</b><span>Au-delà, plus de versement possible, mais les intérêts continuent de s\'ajouter.</span></div></li></ol></div>'
  + pied(SRC1, 7, T)))
# 8 - Parlons-en + colophon
pages.append(page("sapin",
  tete("sapin", NUM, DATE, True)
  + f'<div class="ed-corps"><h2 class="ed-titre">Une question{S}? <em>Parlons-en.</em></h2><div class="ed-g1"></div>'
    f'<p class="ed-chapo ed-doux">Pose-la en commentaire. Les plus fréquentes deviennent un prochain post.</p><div style="flex:1"></div>'
    f'<div class="ed-colo"><div><h4>Sources</h4><p><b>service-public.gouv.fr</b>, fiche « Livret A », vérifiée le 1er août 2026.</p>'
    f'<p><b>info.gouv.fr</b>, « Le taux du livret A augmente à compter du 1er août 2026 », 31 juillet 2026.</p></div>'
    f'<div><h4>Ce post</h4><p>Rédaction{S}: Parlons Placement, novembre 2026.</p><p>Contenu pédagogique. Ne constitue pas un conseil en investissement personnalisé.</p></div></div></div>'
  + pied("@parlonsplacement", 8, T, suite=False)))
if __name__ == '__main__':
  for i, p in enumerate(pages, 1):
    h = os.path.abspath(f"{O}/page_{i}.html"); open(h, "w").write(doc(p))
    subprocess.run(["python3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "render.py"), h, f"{O}/livret-a-quinzaines-{i:02d}.png", "1080", "1350"], check=True)
print("ok")
