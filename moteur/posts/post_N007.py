import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ed import *
import subprocess, os
O = sys.argv[1] if len(sys.argv) > 1 else "sortie"; os.makedirs(O, exist_ok=True)
NUM, DATE, T = "007", "NOV. 2026", 8
SLUG = "pea-5-points"
def nb(t): return f'<span style="white-space:nowrap;font:inherit;color:inherit">{t}</span>'
# Espace fine insécable des milliers, élargie : seule, elle disparaît presque en Instrument Serif.
TH = f'<span style="font:inherit;color:inherit;margin-left:.12em">{N}</span>'
ER = '<sup class="o">er</sup>'
VU = f"consultée le {nb('6 novembre 2026')}"
SP = f"{nb('service-public.gouv.fr')}, fiche F2385 «{S}Plan d’épargne en actions (PEA){S}», vérifiée le {nb('22 mai 2026')}"
SP_PS = f"{nb('service-public.gouv.fr')}, fiche F2329 «{S}Prélèvements sociaux sur les revenus du patrimoine et de placements{S}», vérifiée le {nb('30 juin 2026')}"
IMP = f"impots.gouv.fr, «{S}L’assurance-vie et le PEA{S}», modifiée le {nb('8 avril 2026')}"
CMF = f"legifrance.gouv.fr, code monétaire et financier, art.{S}L221-30 et L221-31, version en vigueur"
RISQUE = "Investir en actions comporte un risque de perte en capital."
LAB = "font:700 22px/1.3 var(--font-texte);letter-spacing:.12em;text-transform:uppercase;color:var(--texte-doux)"

def sommaire(rows):
    # Les cinq points, numérotés dans la marge : un sommaire de journal.
    out = f'<p style="margin:0 0 14px;{LAB}">Au sommaire</p><div style="border-top:2px solid var(--texte)">'
    for n, t in rows:
        out += (f'<div style="display:grid;grid-template-columns:80px 1fr;column-gap:24px;align-items:baseline;padding:14px 0 10px;border-bottom:1px solid var(--filet)">'
                f'<span style="font-family:var(--font-titre);font-size:60px;line-height:.9;color:var(--accent)">{n}</span>'
                f'<span style="font-family:var(--font-titre);font-size:52px;line-height:1.02">{t}</span></div>')
    return out + '</div>'

def fiche(rows):
    # Critère à gauche, réponse en serif à droite.
    out = '<div style="border-top:2px solid var(--texte)">'
    for k, v in rows:
        out += (f'<div style="display:flex;justify-content:space-between;align-items:baseline;gap:32px;padding:20px 0 16px;border-bottom:1px solid var(--filet)">'
                f'<span style="{LAB};color:var(--texte)">{k}</span>'
                f'<span style="font-family:var(--font-titre);font-size:62px;line-height:1;color:var(--accent);font-style:italic;white-space:nowrap;padding-right:4px">{v}</span></div>')
    return out + '</div>'

def tableau(rows):
    # Trois colonnes à filets : la situation, l'impôt sur le revenu, les prélèvements sociaux.
    g = "display:grid;grid-template-columns:1fr 210px 210px;column-gap:24px;align-items:baseline"
    out = (f'<div style="{g};padding:0 0 12px"><span style="{LAB}">Ton cas</span>'
           f'<span style="{LAB};text-align:right">Impôt sur le revenu</span><span style="{LAB};text-align:right">Prélèvements sociaux</span></div>')
    for i, (cas, ir, ps) in enumerate(rows):
        bord = "2px solid var(--texte)" if i == 0 else "1px solid var(--filet)"
        out += (f'<div style="{g};border-top:{bord};padding:26px 0 22px">'
                f'<span style="font:700 32px/1.25 var(--font-texte)">{cas}</span>'
                f'<span style="font-family:var(--font-titre);font-size:68px;line-height:1;text-align:right;white-space:nowrap">{ir}</span>'
                f'<span style="font-family:var(--font-titre);font-size:68px;line-height:1;text-align:right;white-space:nowrap;color:var(--accent);font-style:italic">{ps}</span></div>')
    return out + '<div style="border-top:1px solid var(--filet)"></div>'

pages = []
# 1 - Une
pages.append(page("papier",
  tete("papier", NUM, DATE)
  + f'<div class="ed-corps"><p class="ed-rubrique">Les bases</p><div class="ed-g1"></div>'
    f'<h1 class="ed-titre" style="font-size:104px">Le PEA en 5 points, <em>du premier versement au retrait.</em></h1><div class="ed-g1"></div>'
    f'<p class="ed-chapo ed-doux">Le plan d’épargne en actions (PEA) sert à détenir des actions avec moins d’impôt, à condition d’attendre. Voici ses règles.</p>'
    f'<div style="flex:1"></div>'
    + sommaire([("1", "Qui peut l’ouvrir"), ("2", "Combien verser"), ("3", "Ce qu’on y met"),
                ("4", "Quand retirer"), ("5", "Quel impôt")]) + '</div>'
  + pied(f"Sources{S}: service-public.gouv.fr, impots.gouv.fr, legifrance.gouv.fr, {VU}. {RISQUE}", 1, T)))
# 2 - Point 1 : qui peut l'ouvrir
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">1. Qui peut l’ouvrir</p><div class="ed-g1"></div>'
    f'<h2 class="ed-titre m">Un PEA par personne, <em>pas un de plus.</em><span class="ed-sup">1</span></h2><div class="ed-g2"></div>'
    + fiche([("Âge", "majeur"), ("Domicile fiscal", "en France"), ("Nombre", "un seul PEA"), ("En couple", "chacun le sien")])
    + f'<div style="flex:1"></div>'
    f'<p class="ed-texte ed-doux">Pas de compte joint. Un majeur rattaché au foyer fiscal de ses parents peut ouvrir un PEA plafonné à <b>{nb(f"20{TH}000{S}€")}</b>.</p></div>'
  + pied(f"1. {SP}{N}; {CMF}. Aucune condition de nationalité. Le plafond de {nb(f'20{N}000{S}€')} vaut tant que dure le rattachement.", 2, T)))
# 3 - Point 2 : le plafond (le chiffre)
pages.append(page("sapin",
  tete("sapin", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">2. Combien verser</p><div style="flex:1"></div>'
    f'<p class="ed-chiffre" style="color:var(--lime);font-size:250px">150{TH}000<small>{S}€</small></p><div class="ed-g2"></div>'
    f'<p class="ed-inter" style="font-size:56px">C’est le maximum que tu peux verser sur un PEA classique, en cumulé depuis l’ouverture.<span class="ed-sup">2</span></p><div class="ed-g2"></div>'
    f'<p class="ed-texte ed-doux">Le PEA-PME-ETI, tourné vers les petites et moyennes entreprises et les entreprises de taille intermédiaire, monte à <b>{nb(f"225{TH}000{S}€")}</b>. Les deux réunis{S}: {nb(f"225{TH}000{S}€")} au plus.</p></div>'
  + pied(f"2. {CMF}{N}; {SP}. Le plafond porte sur les versements, en argent uniquement, pas sur la valeur du plan.", 3, T)))
# 4 - Point 3 : ce qu'on y met
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">3. Ce qu’on y met</p><div class="ed-g1"></div>'
    f'<h2 class="ed-titre m">Des actions européennes, <em>pas n’importe lesquelles.</em><span class="ed-sup">3</span></h2><div class="ed-g2"></div>'
    f'<ol class="ed-liste">'
    f'<li><div><b>Des actions de sociétés</b><span>Siège dans l’Union européenne ou l’Espace économique européen, soumises à l’impôt sur les sociétés.</span></div></li>'
    f'<li><div><b>Des parts de fonds</b><span>Investis à plus de 75{S}% dans ces actions.</span></div></li>'
    f'<li><div><b>De l’argent, pas des titres</b><span>Tu verses en euros, puis tu achètes dans le plan.</span></div></li></ol>'
    f'<div style="flex:1"></div><p class="ed-texte ed-doux">La valeur d’un PEA monte et baisse avec celle des actions qu’il contient.</p></div>'
  + pied(f"3. {CMF}{N}; {SP}. Espace économique européen{S}: l’Union européenne plus l’Islande, le Liechtenstein et la Norvège. {RISQUE}", 4, T)))
# 5 - Point 4 : quand retirer (si / alors)
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">4. Quand retirer</p><div class="ed-g1"></div>'
    f'<h2 class="ed-titre m">Le compteur démarre <em>au premier versement.</em><span class="ed-sup">4</span></h2><div class="ed-g2"></div>'
    f'<div class="ed-fleche" style="grid-template-columns:250px 1fr"><div class="quand">Retrait avant 5{N}ans</div><div class="effet">le plan est en principe clôturé.</div>'
    f'<div class="quand">Retrait après 5{N}ans</div><div class="effet">le plan reste ouvert, et tu peux encore verser.</div></div>'
    f'<div style="flex:1"></div>'
    f'<p class="ed-texte ed-doux">Avant 5{N}ans, le plan n’est pas clôturé en cas de licenciement, d’invalidité ou de mise à la retraite anticipée.</p></div>'
  + pied(f"4. {SP}. La date d’ouverture du plan est celle du 1{ER} versement. Après 5{N}ans, un retrait total clôture le plan. Autre exception{S}: une somme affectée sous 3{N}mois à la création ou à la reprise d’une entreprise.", 5, T)))
# 6 - Point 5 : quel impôt
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">5. Quel impôt</p><div class="ed-g1"></div>'
    f'<h2 class="ed-titre m">Ce que tu paies <em>dépend de la date.</em><span class="ed-sup">5</span></h2><div class="ed-g2"></div>'
    + tableau([("Tant que tu ne retires rien", "0", "0"),
               (f"Retrait avant 5{N}ans", f"12,8{S}%", f"18,6{S}%"),
               (f"Retrait après 5{N}ans", "0", f"18,6{S}%")])
    + f'<div style="flex:1"></div><p class="ed-texte ed-doux">Ces taux portent sur le gain, pas sur toute la somme retirée.</p></div>'
  + pied(f"5. {IMP}{N}; {SP_PS}. Prélèvements sociaux au taux en vigueur à la date du retrait{S}: 18,6{S}% en 2026 (CSG 10,6{S}%, CRDS 0,5{S}%, prélèvement de solidarité 7,5{S}%).", 6, T)))
# 7 - Le document + à retenir
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">Le document</p><div class="ed-g1"></div>'
    f'<div class="ed-coupure"><div class="src">impots.gouv.fr · Particulier</div><div class="date">Modifié le {nb("8 avril 2026")}</div>'
    f'<p class="titre" style="font-size:76px">«{S}L’assurance-vie et le PEA{S}»</p>'
    f'<div class="url" style="word-break:normal">impots.gouv.fr/particulier/lassurance-vie-et-le-pea-0</div></div>'
    f'<div style="flex:1"></div><p style="margin:0 0 6px;{LAB}">À retenir</p>'
    f'<ol class="ed-liste"><li><div><b>Un seul PEA par personne majeure</b></div></li>'
    f'<li><div><b>{nb(f"150{N}000{S}€")} de versements au plus</b><span>Sur un PEA classique.</span></div></li>'
    f'<li><div><b>Après 5{N}ans, pas d’impôt sur le revenu</b><span>Les prélèvements sociaux restent dus.</span></div></li></ol></div>'
  + pied(f"Titre cité tel que publié sur impots.gouv.fr. Lien complet en légende. {RISQUE}", 7, T)))
# 8 - Parlons-en + colophon
pages.append(page("sapin",
  tete("sapin", NUM, DATE, True)
  + f'<div class="ed-corps"><h2 class="ed-titre">Une question{S}? <em>Parlons-en.</em></h2><div class="ed-g1"></div>'
    f'<p class="ed-chapo ed-doux">Envoie ce post à un proche qui se demande comment marche un PEA.</p><div style="flex:1"></div>'
    f'<div class="ed-colo"><div><h4>Sources</h4>'
    f'<p><b>service-public.gouv.fr</b>, fiche F2385 «{S}Plan d’épargne en actions (PEA){S}», vérifiée le {nb("22 mai 2026")}.</p>'
    f'<p><b>service-public.gouv.fr</b>, fiche F2329 «{S}Prélèvements sociaux{S}», vérifiée le {nb("30 juin 2026")}.</p>'
    f'<p><b>impots.gouv.fr</b>, «{S}L’assurance-vie et le PEA{S}», modifiée le {nb("8 avril 2026")}.</p>'
    f'<p><b>legifrance.gouv.fr</b>, code monétaire et financier, art.{S}L221-30 et L221-31.</p></div>'
    f'<div><h4>Ce post</h4><p>Rédaction{S}: Parlons Placement, novembre 2026. Sources {nb("consultées le 6 novembre 2026")}.</p>'
    f'<p>{RISQUE}</p>'
    f'<p>Contenu pédagogique. Ne constitue pas un conseil en investissement personnalisé.</p></div></div></div>'
  + pied("@parlonsplacement", 8, T, suite=False)))
if __name__ == '__main__':
  for i, p in enumerate(pages, 1):
    h = os.path.abspath(f"{O}/page_{i}.html"); open(h, "w").write(doc(p))
    subprocess.run(["python3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "render.py"), h, f"{O}/{SLUG}-{i:02d}.png", "1080", "1350"], check=True)
print("ok")
