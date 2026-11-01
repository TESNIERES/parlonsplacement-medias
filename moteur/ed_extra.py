from ed import *
def cadre(h, label="Photo réelle", credit="Photo : [Prénom Nom] / Unsplash", src=None):
    inside = f'<img src="{src}">' if src else f'<div class="ed-vide" style="height:100%">{label}</div>'
    return (f'<div class="ed-photo" style="height:{h}px">{inside}</div>'
            f'<p class="ed-legende">{credit}</p>')
def portrait(num, date, folio, total, citation, nom, role, credit, src=None, theme="papier"):
    return page(theme, tete(theme, num, date, True)
      + f'<div class="ed-corps" style="padding-top:36px">{cadre(640, "Photo réelle de l&#39;invité", credit, src)}<div class="ed-g2"></div>'
        f'<p class="ed-inter" style="font-size:64px">« {citation} »</p><div class="ed-g1"></div>'
        f'<p class="ed-rubrique" style="color:var(--texte)">{nom}</p><p class="ed-notes" style="margin-top:8px;font-size:24px">{role}</p></div>'
      + pied("Parlons-en, la série d'entretiens de Parlons Placement.", folio, total))
def reel_une(rubrique, titre, src=None):
    vid = f'<img src="{src}" style="width:100%;height:100%;object-fit:cover">' if src else '<div class="ed-vide" style="height:100%;border:0;color:#A9B8B0">Vidéo de l&#39;invité</div>'
    return (f'<section class="ed-reel" data-theme="papier"><div class="video">{vid}</div>'
            f'<div class="une"><p class="ed-rubrique">{rubrique}</p><div class="ed-g1"></div><h1 class="ed-titre">{titre}</h1></div></section>')
def reel_st(texte, src=None):
    vid = f'<img src="{src}" style="width:100%;height:100%;object-fit:cover">' if src else '<div class="ed-vide" style="height:100%;border:0;color:#A9B8B0">Vidéo de l&#39;invité</div>'
    return f'<section class="ed-reel" data-theme="encre"><div class="video">{vid}</div><div class="ed-st"><p>{texte}</p></div></section>'
def partenariat(num, date, partenaire, titre, chapo, risque, total):
    return page("papier",
      f'<div class="ed-pub"><b>Publicité</b><span>·</span><span>Collaboration commerciale avec {partenaire}</span></div>'
      + tete("papier", num, date, True)
      + f'<div class="ed-corps"><p class="ed-rubrique">Qui gère ton argent{S}?</p><div class="ed-g1"></div>'
        f'<h1 class="ed-titre m">{titre}</h1><div class="ed-g1"></div><p class="ed-chapo ed-doux">{chapo}</p>'
        f'<div style="flex:1"></div><div class="ed-marge"><div class="m">Avec</div><div class="t"><div class="ed-vide" style="height:110px;width:340px">Logo {partenaire}</div></div></div></div>'
      + pied(risque, 1, total))
