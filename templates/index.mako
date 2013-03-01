## -*- coding: utf-8 ; mode: html -*-
<%inherit file="base.mako"/>

<%block name="title">Accueil</%block>

<div class="alert alert-warning">
  <button type="button" class="close" data-dismiss="alert">×</button>
  Cet outil est encore en développement et contient certains bugs... Voir la <a href="/about/bugs">liste des bugs connus</a>. Vous pouvez <a href="mailto:olivier.tetard@miskin.fr">contacter Olivier</a> si vous rencontrez des problème !
</div>

<div class="alert alert-warning">
  <button type="button" class="close" data-dismiss="alert">×</button>
  Il faut bien penser à <a href="/postfix">redémarrer Postfix</a> pour appliquer la configuration !
</div>

<p>
  <em>Bienvenue sur l'outil hautement experimental de gestion des
  alias d'Attac.</em>
</p>

<p>
  Faites ici comme chez vous. La version actuelle de l'outil permet de
  gérer principalement les alias (et encore, les modifications
  effectuées ne sont <strong>pas</strong> sauvegardées ni appliquées
  pour le moment).
</p>

<p>Vous pouvez quand même :</p>
  <ul>
    <li><a href="/alias/new">ajouter un nouvel alias</a> ;</li>
    <li><a href="/alias/search">rechercher au sein des alias déjà définis</a> ;</li>
    <li>éditer un alias déjà existant ;</li>
    <li>supprimer un alias.</li>
  </ul>

<p>
  En cas de difficuté à utiliser l'outil, vous pouvez
  contacter <a href="mailto:olivier.tetard@miskin.fr">Olivier</a>.
</p>
