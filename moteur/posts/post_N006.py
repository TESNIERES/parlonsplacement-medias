import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ed import *
import subprocess, os
O = sys.argv[1] if len(sys.argv) > 1 else "sortie"; os.makedirs(O, exist_ok=True)
NUM, DATE, T = "006", "NOV. 2026", 8
SLUG = "arnaques-signaux-alerte"
def nb(t): return f'<span style="white-space:nowrap;font:inherit;color:inherit">{t}</span>'
# Espace fine insécable des milliers, élargie : seule, elle disparaît presque en Instrument Serif.
TH = f'<span style="font:inherit;color:inherit;margin-left:.12em">{N}</span>'
VU = f"consultée le {nb('5 novembre 2026')}"
AMF_C = f"amf-france.org, «{S}Quelles sont les arnaques les plus courantes{S}?{S}», {nb('21 février 2025')}"
AMF_E = f"amf-france.org, «{S}Éviter les arnaques{S}», {nb('12 février 2026')}"
AMF_V = f"amf-france.org, «{S}Vérifier une autorisation{S}», {nb('27 juillet 2026')}"
RA = f"Pôle commun ACPR-AMF, «{S}Rapport d’activité 2025{S}», juin 2026, p.{S}9"
TEL = nb(f"01{S}53{S}45{S}62{S}00")
LAB = "font:700 22px/1.3 var(--font-texte);letter-spacing:.12em;text-transform:uppercase;color:var(--texte-doux)"

def dit_amf(rows):
    # Ce qu'on te dit, ce qu'en dit l'AMF : une grille à filets, comme un tableau de journal.
    out = f'<p style="margin:0 0 18px;{LAB}">Ce qu’on te dit, ce qu’en dit l’AMF</p>'
    for i, (dit, amf) in enumerate(rows):
        bord = "2px solid var(--texte)" if i == 0 else "1px solid var(--filet)"
        out += (f'<div style="display:grid;grid-template-columns:300px 1fr;column-gap:40px;align-items:baseline;'
                f'border-top:{bord};padding:26px 0 22px">'
                f'<span style="font:700 30px/1.25 var(--font-texte)">{dit}</span>'
                f'<span style="font-family:var(--font-titre);font-size:56px;line-height:1.02;color:var(--accent);font-style:italic">{amf}</span></div>')
    return out

def scenarios(rows):
    # Le scénario dans la marge, sa mécanique à droite : une liste à filets.
    out = ""
    for i, (m, t) in enumerate(rows):
        bord = "2px solid var(--texte)" if i == 0 else "1px solid var(--filet)"
        out += (f'<div style="display:grid;grid-template-columns:250px 1fr;column-gap:32px;align-items:baseline;border-top:{bord};padding:22px 0 18px">'
                f'<span style="{LAB};color:var(--texte)">{m}</span>'
                f'<span style="font-family:var(--font-titre);font-size:50px;line-height:1.04">{t}</span></div>')
    return out

def registres(rows):
    # Qui vérifier, où : catégorie à gauche, registre en serif à droite.
    out = f'<div style="border-top:2px solid var(--texte)">'
    for nom, ou in rows:
        out += (f'<div style="display:flex;justify-content:space-between;align-items:baseline;gap:32px;padding:18px 0 14px;border-bottom:1px solid var(--filet)">'
                f'<span style="font:500 30px/1.25 var(--font-texte)">{nom}</span>'
                f'<span style="font-family:var(--font-titre);font-size:56px;line-height:1;color:var(--accent);font-style:italic;white-space:nowrap;padding-right:4px">{ou}</span></div>')
    return out + '</div>'

pages = []
# 1 - Une
pages.append(page("papier",
  tete("papier", NUM, DATE)
  + f'<div class="ed-corps"><p class="ed-rubrique">La source</p><div class="ed-g1"></div>'
    f'<h1 class="ed-titre" style="font-size:100px">Arnaque au placement{S}: cinq signaux qui doivent <em>te faire raccrocher.</em></h1><div class="ed-g1"></div>'
    f'<p class="ed-chapo ed-doux">Le gendarme de la Bourse, l’Autorité des marchés financiers (AMF), décrit les pièges les plus courants. Les voici.</p>'
    f'<div style="flex:1"></div>'
    + dit_amf([(f"«{S}C’est sans risque.{S}»", "Pas de rendement élevé sans risque élevé."),
               (f"«{S}Décide vite.{S}»", "Prends le temps de la réflexion.")]) + '</div>'
  + pied(f"Source{S}: {AMF_C}, {VU}.", 1, T)))
# 2 - Les signaux : la liste
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">Les signaux</p><div class="ed-g1"></div>'
    f'<h2 class="ed-titre m">Cinq signaux <em>à ne pas ignorer.</em><span class="ed-sup">1</span></h2><div class="ed-g2"></div>'
    f'<ol class="ed-liste">'
    f'<li><div><b>Un contact que tu n’as pas demandé</b><span>Appel, message, réseau social.</span></div></li>'
    f'<li><div><b>Un gros rendement «{S}sans risque{S}»</b></div></li>'
    f'<li><div><b>On te presse d’investir tout de suite</b></div></li>'
    f'<li><div><b>On te demande de garder le secret</b></div></li>'
    f'<li><div><b>Rien par écrit</b><span>Tout passe par messagerie privée.</span></div></li></ol></div>'
  + pied(f"1. {AMF_C}, {VU}. L’AMF conseille d’exiger une documentation écrite, sur papier ou par e-mail.", 2, T)))
# 3 - Dans le détail : les scénarios
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">Dans le détail</p><div class="ed-g1"></div>'
    f'<h2 class="ed-titre m">Les scénarios <em>les plus courants.</em><span class="ed-sup">2</span></h2><div class="ed-g2"></div>'
    + scenarios([("Crypto, Forex", "Des gains rapides, ou une formation express au trading."),
                 ("Atypiques", f"Parkings, vins, diamants, faux placements «{S}verts{S}»."),
                 ("Célébrités", "Faux articles, fausses vidéos créées par intelligence artificielle."),
                 ("Recouvrement", f"Des frais pour «{S}récupérer{S}» l’argent déjà perdu."),
                 ("Usurpation", "Le nom et le logo d’une société autorisée, copiés.")])
    + '</div>'
  + pied(f"2. {AMF_C}, {VU}. Forex{S}: le marché des devises. Investir comporte un risque de perte en capital, même auprès d’un acteur autorisé.", 3, T)))
# 4 - Le chiffre
pages.append(page("sapin",
  tete("sapin", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">Le chiffre</p><div style="flex:1"></div>'
    f'<p class="ed-chiffre" style="color:var(--lime)">1{TH}351</p><div class="ed-g2"></div>'
    f'<p class="ed-inter" style="font-size:54px">noms de sites ou d’acteurs non autorisés ajoutés en 2025 aux listes noires de l’AMF et de l’ACPR.<span class="ed-sup">3</span></p><div class="ed-g2"></div>'
    f'<p class="ed-texte ed-doux">Fin 2025, ces six listes comptaient <b>{nb(f"9{TH}269")} noms</b>{S}: surtout de faux livrets, de faux crédits et de faux placements.</p></div>'
  + pied(f"3. {RA}, {VU}. ACPR{S}: Autorité de contrôle prudentiel et de résolution, qui contrôle banques et assurances. En 2024{S}: {nb(f'1{TH}459')} noms ajoutés.", 4, T)))
# 5 - Si / alors : ton réflexe
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">Ton réflexe</p><div class="ed-g1"></div>'
    f'<h2 class="ed-titre m">L’AMF ne t’appellera <em>pas pour ça.</em></h2><div class="ed-g2"></div>'
    f'<div class="ed-fleche" style="grid-template-columns:170px 1fr"><div class="quand">Si</div><div class="effet">quelqu’un se dit de l’AMF et te réclame une taxe ou des frais,</div>'
    f'<div class="quand">Alors</div><div class="effet">ce n’est pas l’AMF. C’est une arnaque.</div></div>'
    f'<div style="flex:1"></div>'
    f'<p class="ed-texte ed-doux">L’AMF ne contacte pas les épargnants de sa propre initiative par téléphone ou messagerie privée. Elle ne perçoit pas de taxe auprès des particuliers.<span class="ed-sup">4</span></p></div>'
  + pied(f"4. {AMF_E}, {VU}. Elle ne bloque pas de comptes et ne propose pas de service de recouvrement de fonds ({AMF_C}).", 5, T)))
# 6 - Les vérifications
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">Avant de verser</p><div class="ed-g1"></div>'
    f'<h2 class="ed-titre m">On te sollicite{S}? <em>Vérifie le nom.</em><span class="ed-sup">5</span></h2><div class="ed-g2"></div>'
    f'<p style="margin:0 0 14px;{LAB}">Qui vérifier, et où</p>'
    + registres([("Banque, entreprise d’investissement", "Regafi"),
                 ("Conseiller en investissements financiers", "Orias"),
                 ("Fonds, Sicav", "Geco"),
                 ("Plateforme de crypto-actifs", "Liste blanche AMF")])
    + f'<div style="flex:1"></div><p class="ed-texte ed-doux">Absent d’une liste noire ne veut pas dire autorisé. Et un nom peut être copié{S}: vérifie l’adresse du site.</p></div>'
  + pied(f"5. {AMF_V} et {AMF_C}, {VU}. Regafi, Orias{S}: registres officiels{N}; Geco{S}: base de l’AMF. Une offre de placement atypique doit aussi figurer sur la liste blanche de l’AMF.", 6, T)))
# 7 - Le document + à retenir
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">Le document</p><div class="ed-g1"></div>'
    f'<div class="ed-coupure"><div class="src">amf-france.org · Espace épargnants</div><div class="date">Publié le {nb("21 février 2025")}</div>'
    f'<p class="titre" style="font-size:72px">«{S}Quelles sont les arnaques les plus courantes{S}?{S}»</p>'
    f'<div class="url" style="word-break:normal">amf-france.org/fr/espace-epargnants/proteger-son-epargne/eviter-les-arnaques/<br>quelles-sont-les-arnaques-les-plus-courantes</div></div>'
    f'<div style="flex:1"></div><p style="margin:0 0 6px;{LAB}">À retenir</p>'
    f'<ol class="ed-liste"><li><div><b>Pas de rendement élevé sans risque élevé</b></div></li>'
    f'<li><div><b>Ne verse rien, ne signe rien avant d’être sûr</b></div></li>'
    f'<li><div><b>Un doute{S}? AMF Épargne Info Service</b><span>{TEL}</span></div></li></ol></div>'
  + pied(f"Titre cité tel que publié sur amf-france.org. Numéro{S}: {AMF_V}. Lien complet en légende.", 7, T)))
# 8 - Parlons-en + colophon
pages.append(page("sapin",
  tete("sapin", NUM, DATE, True)
  + f'<div class="ed-corps"><h2 class="ed-titre">Une question{S}? <em>Parlons-en.</em></h2><div class="ed-g1"></div>'
    f'<p class="ed-chapo ed-doux">Tu as déjà reçu une offre de placement que tu n’avais pas demandée{S}? Réponds oui ou non en commentaire.</p><div style="flex:1"></div>'
    f'<div class="ed-colo"><div><h4>Sources</h4>'
    f'<p><b>amf-france.org</b>, «{S}Quelles sont les arnaques les plus courantes{S}?{S}», {nb("21 février 2025")}.</p>'
    f'<p><b>amf-france.org</b>, «{S}Éviter les arnaques{S}», {nb("12 février 2026")}.</p>'
    f'<p><b>amf-france.org</b>, «{S}Vérifier une autorisation{S}», {nb("27 juillet 2026")}.</p>'
    f'<p><b>Pôle commun ACPR-AMF</b>, «{S}Rapport d’activité 2025{S}», juin 2026, p.{S}9.</p></div>'
    f'<div><h4>Ce post</h4><p>Rédaction{S}: Parlons Placement, novembre 2026. Sources {nb("consultées le 5 novembre 2026")}.</p>'
    f'<p>Contenu pédagogique. Ne constitue pas un conseil en investissement personnalisé.</p></div></div></div>'
  + pied("@parlonsplacement", 8, T, suite=False)))
if __name__ == '__main__':
  for i, p in enumerate(pages, 1):
    h = os.path.abspath(f"{O}/page_{i}.html"); open(h, "w").write(doc(p))
    subprocess.run(["python3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "render.py"), h, f"{O}/{SLUG}-{i:02d}.png", "1080", "1350"], check=True)
print("ok")
