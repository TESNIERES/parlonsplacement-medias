import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ed import *
import subprocess, os
O = sys.argv[1] if len(sys.argv) > 1 else "sortie"; os.makedirs(O, exist_ok=True)
NUM, DATE, T = "005", "NOV. 2026", 8
SLUG = "taeg-credit-immobilier"
ER = '1<sup class="o">er</sup>'
def nb(t): return f'<span style="white-space:nowrap;font:inherit;color:inherit">{t}</span>'
P = lambda v: f"{v}{S}%"          # pourcentage (espace insécable)
VU = f"consultée le {nb('4 novembre 2026')}"
SP = "service-public.gouv.fr"
F2456 = f"{SP}, fiche «{S}Qu’est-ce que le taux annuel effectif global (TAEG){S}?{S}»"
A17054 = f"{SP}, actualité du {nb('30 septembre 2026')}"
BDF = f"banque-france.fr, «{S}Taux d’usure - 2026-Q4{S}», publié le {nb('28 septembre 2026')}"
LAB = "font:700 22px/1.3 var(--font-texte);letter-spacing:.12em;text-transform:uppercase;color:var(--texte-doux)"

def deux_taux():
    # Deux taux, deux mesures : une grille à filets, comme un tableau de journal.
    out = f'<p style="margin:0 0 18px;{LAB}">Deux taux, deux mesures</p>'
    for nom, txt, acc in (("Taux d’intérêt", "Les intérêts, sans les frais.", False),
                          ("TAEG", "Les intérêts et les frais liés au prêt.", True)):
        col = "color:var(--accent);font-style:italic;" if acc else ""
        out += (f'<div style="display:grid;grid-template-columns:260px 1fr;column-gap:40px;align-items:baseline;'
                f'border-top:{"2px solid var(--texte)" if not acc else "1px solid var(--filet)"};padding:26px 0 22px">'
                f'<span style="font:700 30px/1.2 var(--font-texte)">{nom}</span>'
                f'<span style="font-family:var(--font-titre);font-size:70px;line-height:1;{col}">{txt}</span></div>')
    return out

def sigle(rows):
    # Le sigle décodé, lettre par lettre : grande capitale serif dans la marge, définition à droite.
    out = ""
    for i, (l, mot, defi) in enumerate(rows):
        bord = "2px solid var(--texte)" if i == 0 else "1px solid var(--filet)"
        out += (f'<div style="display:grid;grid-template-columns:120px 1fr;column-gap:32px;align-items:baseline;border-top:{bord};padding:20px 0 16px">'
                f'<span style="font-family:var(--font-titre);font-size:110px;line-height:.85;color:var(--accent)">{l}</span>'
                f'<div><b style="display:block;font:700 34px/1.2 var(--font-texte)">{mot}</b>'
                f'<span style="font:400 30px/1.35 var(--font-texte);color:var(--texte-doux)">{defi}</span></div></div>')
    return out

def postes(titre, items):
    # Une colonne de marge (le statut), une liste à filets (les frais).
    lis = "".join(f'<div style="padding:16px 0 14px;border-top:1px solid var(--filet);font:500 32px/1.3 var(--font-texte)">{t}</div>' for t in items)
    return (f'<div class="ed-marge"><div class="m">{titre}</div>'
            f'<div style="border-top:2px solid var(--texte)">{lis}</div></div>')

def seuils(rows):
    # Les plafonds, un par ligne : catégorie à gauche, taux en serif à droite.
    out = f'<div style="border-top:2px solid var(--texte)">'
    for nom, v, fort in rows:
        st = "color:var(--accent);font-style:italic;" if fort else ""
        out += (f'<div style="display:flex;justify-content:space-between;align-items:baseline;padding:14px 0 10px;border-bottom:1px solid var(--filet)">'
                f'<span style="font:{"700" if fort else "500"} 28px/1.2 var(--font-texte)">{nom}</span>'
                f'<span style="font-family:var(--font-titre);font-size:58px;line-height:1;{st}">{v}</span></div>')
    return out + '</div>'

pages = []
# 1 - Une
pages.append(page("papier",
  tete("papier", NUM, DATE)
  + f'<div class="ed-corps"><p class="ed-rubrique">Les bases</p><div class="ed-g1"></div>'
    f'<h1 class="ed-titre">Crédit immobilier{S}: le{S}TAEG dit <em>ce que ton prêt coûte vraiment.</em></h1><div class="ed-g1"></div>'
    f'<p class="ed-chapo ed-doux">Le taux d’intérêt n’est qu’une partie de la facture. Le TAEG y ajoute les frais liés au crédit.</p>'
    f'<div style="flex:1"></div>' + deux_taux() + '</div>'
  + pied(f"Source{S}: {F2456}, {VU}.", 1, T)))
# 2 - La règle : le sigle décodé
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">La règle</p><div class="ed-g1"></div>'
    f'<h2 class="ed-titre m">Quatre lettres, <em>un coût total.</em></h2><div class="ed-g2"></div>'
    + sigle([("T", "Taux", "Un pourcentage du montant emprunté."),
             ("A", "Annuel", "Exprimé pour une année."),
             ("E", "Effectif", "Il tient compte des frais que tu paies."),
             ("G", "Global", "Intérêts et frais liés au crédit, ensemble.")])
    + f'<div style="flex:1"></div><p class="ed-texte" style="font-size:32px">Le TAEG représente le coût total d’un crédit{S}: il prend en compte l’ensemble des frais liés au crédit.<span class="ed-sup">1</span></p></div>'
  + pied(f"1. {F2456}, {VU}.", 2, T)))
# 3 - Dans le détail : ce qu'il additionne
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">Dans le détail</p><div class="ed-g1"></div>'
    f'<h2 class="ed-titre m">Ce que le TAEG <em>additionne.</em><span class="ed-sup">2</span></h2><div class="ed-g2"></div>'
    + postes("Pris en compte", ["Les intérêts", "Les frais de dossier payés à la banque", "La rémunération d’un intermédiaire, un courtier par exemple"])
    + '<div class="ed-g1"></div>'
    + postes("Souvent en plus", ["L’assurance emprunteur", "La garantie{S}: hypothèque ou cautionnement".format(S=S), "L’évaluation du bien", "Tous les autres frais imposés pour obtenir le prêt"])
    + f'<div style="flex:1"></div><p class="ed-texte ed-doux" style="font-size:32px">Une exception{S}: pour un achat sur plan (VEFA), les intérêts payés pendant la construction ne sont pas comptés.</p></div>'
  + pied(f"2. {F2456}, rubrique «{S}Crédit immobilier{S}», {VU}. Exemple de frais imposé{S}: la tenue d’un compte qu’il faut ouvrir chez le prêteur.", 3, T)))
# 4 - Le chiffre
pages.append(page("sapin",
  tete("sapin", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">Le chiffre</p><div style="flex:1"></div>'
    f'<p class="ed-chiffre" style="color:var(--lime)">5,40<small>{S}%</small></p><div class="ed-g2"></div>'
    f'<p class="ed-inter" style="font-size:54px">Le TAEG maximal d’un prêt immobilier à taux fixe de 20{S}ans et plus, depuis le {nb(ER + " octobre 2026")}.<span class="ed-sup">3</span></p><div class="ed-g2"></div>'
    f'<p class="ed-texte ed-doux">Ce plafond s’appelle le <b>taux d’usure</b>. Il est égal au taux moyen de ces prêts au trimestre précédent, {P("4,05")}, augmenté d’un tiers.</p></div>'
  + pied(f"3. {BDF}{S}: taux effectif moyen au 3<sup class=\"o\">e</sup> trimestre 2026, {P('4,05')}{N}; taux d’usure, {P('5,40')}. Règle de l’article L314-6 du code de la consommation.", 4, T)))
# 5 - La source
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">La source</p><div class="ed-g1"></div>'
    f'<div class="ed-coupure"><div class="src">service-public.gouv.fr · Actualité</div><div class="date">Publié le {nb("30 septembre 2026")}</div>'
    f'<p class="titre" style="font-size:60px">«{S}Crédit immobilier{S}: quels sont les plafonds du taux d’usure à compter du {ER} octobre{S}?{S}»</p>'
    f'<div class="url">service-public.gouv.fr/particuliers/actualites/A17054</div></div>'
    f'<div style="flex:1"></div><p style="margin:0 0 14px;{LAB}">Taux d’usure au 1<sup class="o" style="text-transform:none">er</sup> octobre 2026</p>'
    + seuils([(f"Taux fixe, moins de 10{S}ans", P("4,09"), False),
              (f"Taux fixe, 10 à moins de 20{S}ans", P("4,68"), False),
              (f"Taux fixe, 20{S}ans et plus", P("5,40"), True),
              ("Taux variable", P("5,52"), False),
              ("Prêt relais", P("6,49"), False)])
    + f'</div>'
  + pied(f"Titre cité tel que publié sur {SP}. Chiffres{S}: même publication et {BDF}. Revus chaque trimestre. Lien complet en légende.", 5, T)))
# 6 - Si / alors : le droit méconnu
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">Ton droit</p><div class="ed-g1"></div>'
    f'<h2 class="ed-titre m">Un TAEG absent ou faux <em>n’est pas sans effet.</em></h2><div class="ed-g2"></div>'
    f'<div class="ed-fleche" style="grid-template-columns:170px 1fr"><div class="quand">Si</div><div class="effet">ton contrat de prêt n’indique pas le TAEG, ou le donne avec une erreur,</div>'
    f'<div class="quand">Alors</div><div class="effet">tu peux demander au juge de supprimer tout ou partie des intérêts.</div></div>'
    f'<div style="flex:1"></div>'
    f'<p class="ed-texte ed-doux">Le juge tient compte notamment du préjudice subi. Le capital, lui, reste à rembourser.<span class="ed-sup">4</span></p></div>'
  + pied(f"4. {F2456}, {VU}. Les intérêts déjà payés sont alors restitués ou déduits du capital restant dû.", 6, T)))
# 7 - À retenir
pages.append(page("papier",
  tete("papier", NUM, DATE, True)
  + f'<div class="ed-corps"><p class="ed-rubrique">À retenir</p><div class="ed-g1"></div>'
    f'<h2 class="ed-titre m">L’essentiel <em>en trois lignes.</em></h2><div class="ed-g3"></div>'
    f'<ol class="ed-liste"><li><div><b>Le TAEG, c’est le coût total</b><span>Intérêts et frais liés au crédit, en pourcentage par an.</span></div></li>'
    f'<li><div><b>Il doit être affiché</b><span>Publicités, offres préalables et contrats de prêt.</span></div></li>'
    f'<li><div><b>Tu peux l’estimer</b><span>Le site {SP} renvoie vers le simulateur de l’Anil, l’agence nationale pour l’information sur le logement, pour les prêts à taux fixe. Résultat indicatif.</span></div></li></ol></div>'
  + pied(f"Sources{S}: {F2456} et simulateur R2924, {nb('consultés le 4 novembre 2026')}.", 7, T)))
# 8 - Parlons-en + colophon
pages.append(page("sapin",
  tete("sapin", NUM, DATE, True)
  + f'<div class="ed-corps"><h2 class="ed-titre">Une question{S}? <em>Parlons-en.</em></h2><div class="ed-g1"></div>'
    f'<p class="ed-chapo ed-doux">Un mot de ton offre de prêt te bloque{S}? Écris-le en commentaire. Les plus fréquents deviennent un prochain post.</p><div style="flex:1"></div>'
    f'<div class="ed-colo"><div><h4>Sources</h4>'
    f'<p><b>service-public.gouv.fr</b>, «{S}Qu’est-ce que le taux annuel effectif global (TAEG){S}?{S}», fiche vérifiée le {nb("16 avril 2025")}, {VU}.</p>'
    f'<p><b>service-public.gouv.fr</b>, «{S}Crédit immobilier{S}: quels sont les plafonds du taux d’usure à compter du {nb(ER + " octobre")}{S}?{S}», {nb("30 septembre 2026")}.</p>'
    f'<p><b>banque-france.fr</b>, {nb(f"«{S}Taux d’usure - 2026-Q4{S}»")}, {nb("28 septembre 2026")}.</p></div>'
    f'<div><h4>Ce post</h4><p>Rédaction{S}: Parlons Placement, novembre 2026. Sources {nb("consultées le 4 novembre 2026")}.</p>'
    f'<p>Contenu pédagogique. Ne constitue pas un conseil en investissement personnalisé.</p></div></div></div>'
  + pied("@parlonsplacement", 8, T, suite=False)))
if __name__ == '__main__':
  for i, p in enumerate(pages, 1):
    h = os.path.abspath(f"{O}/page_{i}.html"); open(h, "w").write(doc(p))
    subprocess.run(["python3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "render.py"), h, f"{O}/{SLUG}-{i:02d}.png", "1080", "1350"], check=True)
print("ok")
