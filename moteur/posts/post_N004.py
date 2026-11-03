import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ed import *
import subprocess, os
O = sys.argv[1] if len(sys.argv) > 1 else "sortie"; os.makedirs(O, exist_ok=True)
NUM, DATE, T = "004", "NOV. 2026", 8
SLUG = "inflation-1000-euros"
def nb(t): return f'<span style="white-space:nowrap;font:inherit;color:inherit">{t}</span>'
# Espace fine insécable des milliers, élargie : seule, elle disparaît presque en Instrument Serif.
TH = f'<span style="font:inherit;color:inherit;margin-left:.12em">{N}</span>'
E = lambda v: f"{v}{S}€"          # montant en euros (espace insécable)
P = lambda v: f"{v}{S}%"          # pourcentage (espace insécable)
MILLE = E(f"1{TH}000")
VU = f"consulté le {nb('3 novembre 2026')}"
IR = f"Insee, Informations rapides n°{S}8 du {nb('15 janvier 2026')}"
SRC_IPC = f"Source{S}: {IR}, indice des prix à la consommation, moyennes annuelles, base 100 en 2015, {VU}."
LAB = "font:700 22px/1.3 var(--font-texte);letter-spacing:.12em;text-transform:uppercase;color:var(--texte-doux)"

def panier():
    # Le même panier, deux années : une grille à filets, comme un tableau de journal.
    out = f'<p style="margin:0 0 18px;{LAB}">Pour acheter le même panier moyen</p>'
    for an, val, acc in (("2015", MILLE, False), ("2025", E(f"1{TH}209,50"), True)):
        col = "color:var(--accent);font-style:italic;" if acc else ""
        out += (f'<div style="display:grid;grid-template-columns:170px 1fr;column-gap:40px;align-items:baseline;'
                f'border-top:{"2px solid var(--texte)" if an == "2015" else "1px solid var(--filet)"};padding:22px 0 18px">'
                f'<span style="font:700 30px/1 var(--font-texte)">{an}</span>'
                f'<span style="font-family:var(--font-titre);font-size:150px;line-height:.9;{col}">{val}</span></div>')
    return out

def postes(rows, vmax):
    # Barres horizontales maison : angles droits, sans dégradé, valeur au bout de la barre.
    out = f'<p style="margin:0 0 20px;{LAB}">Hausse des prix de 2015 à 2025</p><div style="display:flex;flex-direction:column;gap:12px">'
    for nom, v, txt, fort in rows:
        w = v / vmax * 100
        fond = "var(--sapin)" if not fort else "var(--texte)"
        out += (f'<div style="display:grid;grid-template-columns:330px 1fr;column-gap:24px;align-items:center;'
                f'{"border-top:1px solid var(--filet);border-bottom:1px solid var(--filet);padding:10px 0;" if fort else ""}">'
                f'<span style="font:{"700" if fort else "600"} 28px/1.15 var(--font-texte)">{nom}</span>'
                f'<div style="display:flex;align-items:center;gap:18px;height:64px">'
                f'<div style="width:{w * 0.78:.1f}%;height:100%;background:{fond}"></div>'
                f'<span style="font:600 32px/1 var(--font-texte);font-variant-numeric:tabular-nums;white-space:nowrap">{txt}</span></div></div>')
    return out + '</div>'

def annees(rows):
    # Les quatre dernières années, en colonnes séparées par des filets.
    cells = ""
    for i, (an, val) in enumerate(rows):
        bord = "border-left:1px solid var(--filet);padding-left:26px;" if i else ""
        cells += (f'<div style="{bord}"><div style="{LAB}">{an}</div>'
                  f'<div style="font-family:var(--font-titre);font-size:68px;line-height:1;margin-top:10px">{val}</div></div>')
    return f'<div style="display:grid;grid-template-columns:repeat(4,1fr);column-gap:26px;border-top:2px solid var(--texte);padding-top:20px">{cells}</div>'

pages = []
# 1 - Une
pages.append(page("papier",
  tete("papier", NUM, DATE)
  + f'<div class="ed-corps"><p class="ed-rubrique">Le chiffre</p><div class="ed-g1"></div>'
    f'<h1 class="ed-titre">Ce que l’inflation a fait à <em>{MILLE} en dix ans.</em></h1><div class="ed-g1"></div>'
    f'<p class="ed-chapo ed-doux">De 2015 à 2025, les prix ont augmenté de près de {P("21")} en France. Un billet de {MILLE}, lui, n’a pas bougé.</p>'
    f'<div style="flex:1"></div>' + panier() + '</div>'
  + pied(f"{SRC_IPC} Calcul Parlons Placement{S}: {MILLE} × 120,95 ÷ 100.", 1, T)))
# 2 - La règle
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">La règle</p><div class="ed-g1"></div>'
    f'<h2 class="ed-titre m">L’inflation, c’est <em>la hausse moyenne des prix.</em></h2><div class="ed-g3"></div>'
    f'<div class="ed-frise grand" style="grid-template-columns:100fr 121fr"><div class="q1"><b>100</b><span>Indice moyen 2015</span></div>'
    f'<div class="q2"><b>120,95</b><span>Indice moyen 2025</span></div></div>'
    f'<div style="flex:1"></div>'
    f'<p class="ed-texte">L’Insee la mesure chaque mois avec l’<b>indice des prix à la consommation</b>, l’IPC. Il suit les prix des biens et des services achetés par les ménages. L’année 2015 sert de repère{S}: elle vaut 100.<span class="ed-sup">1</span></p></div>'
  + pied(f"1. {IR}. Moyennes annuelles, ensemble des ménages, France.", 2, T)))
# 3 - Le chiffre
pages.append(page("sapin",
  tete("sapin", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">Le chiffre</p><div style="flex:1"></div>'
    f'<p class="ed-chiffre" style="color:var(--lime)">827<small>{S}€</small></p><div class="ed-g2"></div>'
    f'<p class="ed-inter">En 2025, {MILLE} gardés dans un tiroir depuis 2015 achètent ce que {E("827")} achetaient en 2015.<span class="ed-sup">2</span></p><div class="ed-g2"></div>'
    f'<p class="ed-texte ed-doux">Le billet n’a pas changé. Ce qu’il permet d’acheter, si{S}: environ {P("17")} de moins.</p></div>'
  + pied(f"2. Calcul Parlons Placement{S}: {MILLE} × 100 ÷ 120,95 = {E('826,79')}, arrondi à {E('827')}. Indice Insee des prix à la consommation, moyennes annuelles, base 100 en 2015.", 3, T)))
# 4 - Si / alors
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">Ce que ça change pour ton épargne</p><div class="ed-g1"></div>'
    f'<h2 class="ed-titre m">Plus d’euros, <em>pas forcément plus d’achats.</em></h2><div class="ed-g2"></div>'
    f'<div class="ed-fleche" style="grid-template-columns:170px 1fr"><div class="quand">Si</div><div class="effet">ton épargne rapporte moins que la hausse des prix,</div>'
    f'<div class="quand">Alors</div><div class="effet">ton solde monte, mais ton pouvoir d’achat baisse.</div></div>'
    f'<div style="flex:1"></div>'
    f'<p class="ed-texte ed-doux">Exemple{S}: {P("1")} d’intérêts, des prix en hausse de {P("2")}. Ce qui reste après l’inflation, c’est le <b>rendement réel</b>{S}: ici, {nb(f"environ −1{S}%")}.</p></div>'
  + pied("Exemple fictif, à but pédagogique. Il ne décrit aucun produit d’épargne.", 4, T)))
# 5 - Dans le détail
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">Dans le détail</p><div class="ed-g1"></div>'
    f'<h2 class="ed-titre m">Tout n’a pas augmenté <em>au même rythme.</em></h2><div class="ed-g3"></div>'
    + postes([("Énergie", 50.29, f"+{P('50')}", False), ("Alimentation", 33.22, f"+{P('33')}", False),
              ("Ensemble", 20.95, f"+{P('21')}", True), ("Services", 18.67, f"+{P('19')}", False),
              ("Produits manufacturés", 4.42, f"+{P('4')}", False)], 50.29)
    + f'<div style="flex:1"></div><p class="ed-texte ed-doux">Ta propre inflation dépend de ce que tu achètes. Selon la place de l’énergie ou des courses dans ton budget, elle peut être plus forte ou plus faible que la moyenne.<span class="ed-sup">3</span></p></div>'
  + pied(f"3. {IR}. Indices moyens 2025, base 100 en 2015{S}: énergie 150,29{N}; alimentation 133,22{N}; ensemble 120,95{N}; services 118,67{N}; produits manufacturés 104,42.", 5, T)))
# 6 - La source
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">La source</p><div class="ed-g2"></div>'
    f'<div class="ed-coupure"><div class="src">insee.fr · Informations rapides n°{S}8</div><div class="date">Publié le {nb("15 janvier 2026")}</div>'
    f'<p class="titre" style="font-size:66px">«{S}En 2025, nouveau ralentissement des prix à la consommation en moyenne annuelle{S}»</p>'
    f'<div class="url">insee.fr/fr/statistiques/8726461</div></div>'
    f'<div style="flex:1"></div><p style="margin:0 0 18px;{LAB}">Hausse des prix, en moyenne annuelle</p>'
    + annees([("2022", f"+5,2{S}%"), ("2023", f"+4,9{S}%"), ("2024", f"+2,0{S}%"), ("2025", f"+0,9{S}%")])
    + f'<div class="ed-g1"></div><p class="ed-texte" style="font-size:32px">Ralentir ne veut pas dire baisser{S}: en moyenne, les prix montent encore, mais moins vite.</p></div>'
  + pied(f"Titre cité tel que publié sur insee.fr. Chiffres{S}: même publication, ensemble des ménages, France. Lien complet en légende.", 6, T)))
# 7 - À retenir
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">À retenir</p><div class="ed-g1"></div>'
    f'<h2 class="ed-titre">Ce qu’il faut <em>garder en tête.</em></h2><div class="ed-g3"></div>'
    f'<ol class="ed-liste"><li><div><b>L’inflation est une moyenne</b><span>Celle de l’Insee porte sur l’ensemble des ménages. La tienne dépend de ton panier.</span></div></li>'
    f'<li><div><b>En dix ans, près de {P("21")} de hausse</b><span>{MILLE} de 2015 équivalent à {E(f"1{TH}209,50")} de 2025.</span></div></li>'
    f'<li><div><b>Tu peux refaire le calcul</b><span>Le convertisseur franc-euro de l’Insee couvre les années 1901 à 2025.</span></div></li></ol></div>'
  + pied(f"Sources{S}: {IR} et {nb('convertisseur franc-euro')} de l’Insee, {nb('consultés le 3 novembre 2026')}.", 7, T)))
# 8 - Parlons-en + colophon
pages.append(page("sapin",
  tete("sapin", NUM, DATE, True)
  + f'<div class="ed-corps"><h2 class="ed-titre">Une question{S}? <em>Parlons-en.</em></h2><div class="ed-g1"></div>'
    f'<p class="ed-chapo ed-doux">Pose-la en commentaire. Les plus fréquentes deviennent un prochain post.</p><div style="flex:1"></div>'
    f'<div class="ed-colo"><div><h4>Sources</h4>'
    f'<p><b>insee.fr</b>, «{S}En 2025, nouveau ralentissement des prix à la consommation en moyenne annuelle{S}», Informations rapides n°{S}8, {nb("15 janvier 2026")}, {VU}.</p>'
    f'<p><b>insee.fr</b>, «{S}Convertisseur franc-euro{S}: pouvoir d’achat de l’euro et du franc{S}», {VU}.</p></div>'
    f'<div><h4>Ce post</h4><p>Rédaction{S}: Parlons Placement, novembre 2026. Calculs Parlons Placement d’après les indices Insee.</p>'
    f'<p>Contenu pédagogique. Ne constitue pas un conseil en investissement personnalisé.</p></div></div></div>'
  + pied("@parlonsplacement", 8, T, suite=False)))
if __name__ == '__main__':
  for i, p in enumerate(pages, 1):
    h = os.path.abspath(f"{O}/page_{i}.html"); open(h, "w").write(doc(p))
    subprocess.run(["python3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "render.py"), h, f"{O}/{SLUG}-{i:02d}.png", "1080", "1350"], check=True)
print("ok")
