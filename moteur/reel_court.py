# Reel court 9:16 (8 à 11 s) pensé pour les personnes qui ne nous suivent pas : l'accroche est lisible dès la première image,
# une idée par plan, des coupes franches toutes les 2 secondes environ, un léger zoom pour le mouvement.
# Pourquoi : du 1er au 7 novembre 2026, les Reels diaporamas de 28 s étaient vus 0,6 à 2,9 s en moyenne (Metricool IGRE24).
#
# Usage : python3 moteur/reel_court.py <dossier publications/NXXX-slug> "<accroche>" "<plan 2>" "<plan 3>" ["<plan 4>"] --source "<source courte>"
#   - accroche : 8 mots au plus, le chiffre ou la question, un passage en <em> autorisé ;
#   - plans 2 à 4 : une phrase de 10 mots au plus chacun, un chiffre par plan ;
#   - --source : par exemple "service-public.gouv.fr, novembre 2026" (affichée en bas de chaque plan).
# Dans les textes, espaces insécables avant : ? ! et milliers en 150&#8239;000 ; jamais de tiret cadratin.
# Sorties dans le dossier : reel.mp4 (H.264 + piste audio muette, 30 i/s, faststart) et reel-couverture.jpg (= premier plan).
import sys, os, subprocess, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ed import *
from PIL import Image

args = sys.argv[1:]
source = ""
if "--source" in args:
    k = args.index("--source"); source = args[k + 1]; del args[k:k + 2]
if len(args) < 3:
    sys.exit("usage : reel_court.py <dossier> <accroche> <plan 2> [plan 3] [plan 4] --source <source>")
dossier, accroche, plans = os.path.abspath(args[0]), args[1], args[2:5]
W, H, FPS = 1080, 1920, 30
RENDU = os.path.join(os.path.dirname(os.path.abspath(__file__)), "render.py")
tmp = tempfile.mkdtemp(prefix="reelc-")

# Zone sûre : Instagram couvre environ 250 px en haut, 420 px en bas et 160 px à droite.
CADRE = "position:absolute;left:80px;right:170px;top:250px;bottom:430px;display:flex;flex-direction:column"
SRC = (f'<p style="margin:0;font:600 26px/1.3 var(--font-texte);letter-spacing:.06em;color:var(--texte-doux)">'
       f'Source{S}: {source}</p>') if source else ""

def rendre(theme, inner, nom):
    html = os.path.join(tmp, nom + ".html"); png = os.path.join(tmp, nom + ".png")
    open(html, "w").write(doc(page(theme, f'<div style="{CADRE}">{inner}</div>', "story")))
    subprocess.run(["python3", RENDU, html, png, str(W), str(H)], check=True)
    return png

images, durees = [], []
# 1. L'accroche, sur fond sapin : contraste maximal dès la première image, aucun fondu d'entrée.
images.append(rendre("sapin",
    f'<div style="height:40px">{logo_for("sapin").replace("<svg", "<svg style=height:40px;width:auto")}</div>'
    f'<div style="flex:1;display:flex;align-items:center"><h1 class="ed-titre" style="font-size:150px;line-height:.95">{accroche}</h1></div>'
    f'<p class="ed-renvoi" style="color:var(--texte-doux)">La réponse en 10 secondes.</p>', "p1"))
durees.append(2.4)
# 2. Une idée par plan, sur papier, numérotée comme une note.
for i, t in enumerate(plans, 2):
    images.append(rendre("papier",
        f'<p class="ed-rubrique">{i - 1}{S}/{S}{len(plans)}</p>'
        f'<div style="flex:1;display:flex;align-items:center"><p class="ed-inter" style="font-size:112px;line-height:1.02">{t}</p></div>{SRC}',
        f"p{i}"))
    durees.append(2.1)
# 3. La fin : le rendez-vous et la mention pédagogique.
images.append(rendre("sapin",
    '<div style="flex:1;display:flex;flex-direction:column;justify-content:center">'
    '<h1 class="ed-titre" style="font-size:118px">La fiche complète <em>est sur le profil.</em></h1><div class="ed-g2"></div>'
    '<p class="ed-renvoi" style="font-size:44px">Suis @parlonsplacement<i> · </i>une fiche sourcée par jour</p></div>'
    '<p style="margin:0;font:500 26px/1.4 var(--font-texte);color:var(--texte-doux)">Contenu pédagogique. '
    'Ne constitue pas un conseil en investissement personnalisé.</p>', "fin"))
durees.append(2.2)

# Montage : chaque plan zoome lentement de 1,00 à 1,035 (rendu en 2x pour éviter les saccades), coupes franches.
cmd = ["ffmpeg", "-y", "-loglevel", "error"]
for img in images:
    cmd += ["-i", img]
cmd += ["-f", "lavfi", "-t", f"{sum(durees):.2f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000"]
filtres = []
for k, d in enumerate(durees):
    n = round(d * FPS)
    filtres.append(f"[{k}:v]scale={W*2}:{H*2},zoompan=z='1+0.035*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                   f":d={n}:s={W}x{H}:fps={FPS},setsar=1[c{k}]")
filtres.append("".join(f"[c{k}]" for k in range(len(durees))) + f"concat=n={len(durees)}:v=1:a=0,format=yuv420p[vout]")
mp4 = os.path.join(dossier, "reel.mp4")
cmd += ["-filter_complex", ";".join(filtres), "-map", "[vout]", "-map", f"{len(images)}:a",
        "-c:v", "libx264", "-profile:v", "high", "-preset", "medium", "-crf", "19", "-r", str(FPS), "-g", str(FPS),
        "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", mp4]
subprocess.run(cmd, check=True)
Image.open(images[0]).convert("RGB").save(os.path.join(dossier, "reel-couverture.jpg"), quality=92, subsampling=0)
print("ok", mp4, f"{sum(durees):.1f} s", len(images), "plans")
