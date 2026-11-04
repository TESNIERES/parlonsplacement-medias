# Reel 9:16 (MP4) tiré d'un carrousel déjà produit : une couverture, chaque page du carrousel, une page de fin.
# Usage : python3 moteur/reel.py <dossier publications/NXXX-slug> "<rubrique>" "<titre court, <em> autorisé>" [secondes par page]
# Sorties dans le dossier : reel.mp4 (H.264 + piste audio muette, 30 i/s, faststart) et reel-couverture.jpg.
import sys, os, glob, subprocess, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ed import *
from PIL import Image

dossier, rubrique, titre = sys.argv[1:4]
par_page = float(sys.argv[4]) if len(sys.argv) > 4 else 3.2
dossier = os.path.abspath(dossier)
pages = sorted(p for p in glob.glob(os.path.join(dossier, "*-0[0-9].jpg")) + glob.glob(os.path.join(dossier, "*-1[0-9].jpg"))
               if not os.path.basename(p).startswith(("story", "reel")))
if not pages:
    sys.exit("aucune page de carrousel trouvée dans " + dossier)
W, H, PAPIER = 1080, 1920, (0xF4, 0xEF, 0xE4)
RENDU = os.path.join(os.path.dirname(os.path.abspath(__file__)), "render.py")
tmp = tempfile.mkdtemp(prefix="reel-")

def rendre(inner, sortie):
    html = os.path.join(tmp, os.path.basename(sortie) + ".html")
    open(html, "w").write(doc(page("papier", inner, "story")))
    subprocess.run(["python3", RENDU, html, sortie, str(W), str(H)], check=True)

# 1. Couverture : la promesse en grand, la une du carrousel en dessous (droite, sans rotation).
rendre(tete("papier")
       + f'<div class="ed-corps" style="padding-top:40px"><p class="ed-rubrique">{rubrique}</p><div class="ed-g1"></div>'
         f'<h1 class="ed-titre m" style="font-size:96px">{titre}</h1><div class="ed-g2"></div>'
         f'<div style="width:720px;box-shadow:0 2px 0 rgba(12,26,20,.08),0 24px 48px rgba(12,26,20,.18)">'
         f'<img src="file://{pages[0]}" style="width:100%;display:block"></div></div>',
       os.path.join(tmp, "00.png"))

# 2. Les pages suivantes du carrousel (la une est déjà sur la couverture), en pleine largeur utile,
#    hors des zones couvertes par l'interface Instagram (haut, bas et colonne de droite).
images = [os.path.join(tmp, "00.png")]
for i, p in enumerate(pages[1:], 1):
    fond = Image.new("RGB", (W, H), PAPIER)
    im = Image.open(p).convert("RGB").resize((960, 1200), Image.LANCZOS)
    fond.paste(im, (60, 250))
    out = os.path.join(tmp, f"{i:02d}.png")
    fond.save(out)
    images.append(out)

# 3. Page de fin : le rendez-vous, sans flèche ni bouton.
rendre(tete("papier")
       + '<div class="ed-corps" style="padding-top:120px"><p class="ed-rubrique">Parlons Placement</p><div class="ed-g1"></div>'
         '<h1 class="ed-titre m" style="font-size:112px">Une fiche <em>sourcée</em> par jour.</h1><div class="ed-g2"></div>'
         '<p class="ed-renvoi" style="font-size:40px">Suis @parlonsplacement</p><div style="flex:1"></div>'
         '<p style="font:500 26px/1.4 var(--font-texte);color:var(--texte-doux)">Contenu pédagogique. Ne constitue pas un conseil '
         'en investissement personnalisé.</p></div>',
       os.path.join(tmp, f"{len(images):02d}.png"))
images.append(os.path.join(tmp, f"{len(images):02d}.png"))

# 4. Montage : glissement vers la gauche comme un carrousel, 30 images par seconde, piste audio muette pour la compatibilité.
durees = [3.4] + [par_page] * (len(pages) - 1) + [2.6]
fondu = 0.35
cmd = ["ffmpeg", "-y", "-loglevel", "error"]
for img, d in zip(images, durees):
    cmd += ["-loop", "1", "-t", f"{d + fondu:.2f}", "-framerate", "30", "-i", img]
cmd += ["-f", "lavfi", "-t", f"{sum(durees) + fondu:.2f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000"]
# Chaque plan dure d + fondu ; le fondu k commence à la somme des durées des plans précédents.
filtres, prec, t = [], "[0:v]", 0.0
for k in range(1, len(images)):
    t += durees[k - 1]
    filtres.append(f"{prec}[{k}:v]xfade=transition=slideleft:duration={fondu}:offset={t:.2f}[v{k}]")
    prec = f"[v{k}]"
filtres.append(f"{prec}format=yuv420p[vout]")
mp4 = os.path.join(dossier, "reel.mp4")
cmd += ["-filter_complex", ";".join(filtres), "-map", "[vout]", "-map", f"{len(images)}:a",
        "-c:v", "libx264", "-profile:v", "high", "-preset", "medium", "-crf", "20", "-r", "30", "-g", "60",
        "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", mp4]
subprocess.run(cmd, check=True)
Image.open(os.path.join(tmp, "00.png")).convert("RGB").save(os.path.join(dossier, "reel-couverture.jpg"), quality=92, subsampling=0)
print("ok", mp4, f"{sum(durees):.1f} s", len(images), "plans")
