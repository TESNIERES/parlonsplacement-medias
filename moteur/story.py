# Story 9:16 qui annonce le post du jour.
# Usage : python3 moteur/story.py <page1.png> "<rubrique>" "<titre court, <em> autorisé>" <sortie.png> [papier|sapin]
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ed import *
img, rubrique, titre, out = sys.argv[1:5]
theme = sys.argv[5] if len(sys.argv) > 5 else "papier"
inner = (tete(theme)
         + f'<div class="ed-corps" style="padding-top:56px"><p class="ed-rubrique">{rubrique}</p><div class="ed-g1"></div>'
           f'<h1 class="ed-titre m" style="font-size:88px">{titre}</h1><div class="ed-g2"></div>'
           f'<div class="ed-tirage"><img src="file://{os.path.abspath(img)}"></div>'
           f'<div style="flex:1"></div><p class="ed-renvoi">Le post complet est sur notre profil <i>→</i></p></div>')
html = os.path.abspath(out) + ".html"
open(html, "w").write(doc(page(theme, inner, "story")))
subprocess.run(["python3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "render.py"), html, out, "1080", "1920"], check=True)
os.remove(html)
print("ok", out)
