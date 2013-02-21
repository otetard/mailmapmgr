## -*- coding: utf-8 ; mode: html -*-

<%inherit file="../base.mako"/>

<%block name="title">À propos</%block>

<h2>À propos de cette application</h2>

<p>
  Réalisé par <a href="mailto:olivier.tetard@amossys.fr">Olivier
  Tétard</a>, pour Attac France. Le code source de cette application
  est disponible sur demande, pour l'instant. Il est diffusé sous les
  termes de la
  licence <a href="http://www.gnu.org/licenses/gpl.html">GNU
  GPLv3</a>.
</p>

<blockquote>
  <p>Copyright (C) 2012 Olivier Tétard &lt;<a href="mailto:olivier.tetard@miskin.fr">olivier.tetard@miskin.fr</a>&gt;</p>
  <p>This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.</p>
  <p>This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.</p>
  <p>You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.</p>
</blockquote>

<h2>Liste des choses à faire...</h2>

<ul>
  <li>Afficher un bandeau d'« alerte » lorsque la configuration a été modifiée mais qu'elle n'a pas encore été appliquée</li>
  <li>Avant de valider une modification d'un alias, s'assurer qu'il s'agit bien du fichier pour lequel la modification a été demandée (vérifier si il n'y a pas de conflit de modification)</li>
  <li>Permettre une recherche sur les adresse cibles aussi</li>
  <li>Permettre la gestion des droits d'accès (<s>super-administrateurs</s>, autorisations par domaines, etc.)</li>
  <li>Permettre la gestion des comptes classiques :</li>
    <ul>
      <li>Ajout, suppression, modification des comptes</li>
      <li>Permettre aux utilisateurs de changer leur mot de passe eux même</li>
    </ul>
  <li><s>Mettre des <em>token</em> pour protéger contre les attaques CSRF</s>
    <ul>
      <li>Améliorer l'obligation d'envoyer les données en POST</li>
      <li><s>Permettre la désactivation ponctuelle de la protection CSRF pour certaines pages</s></li>
      <li><s>Corriger la durée de validité du token côté client</s></li>
      <li><s>Ne générer un nouveau token que si cela est utile (c'est-à-dire, si il y a des formulaires)</s></li>
    </ul>
  </li>
  <li><s>Utiliser une vraie bibliothèque pour gérer les formulaires (type Formish)</s>. Finalement, non.</li>
  <li><s>Permettre la gestion des comptes utilisateurs</s></li>
  <li><s>Permettre de déployer un nouveau fichier <tt>mailmap</tt> (via <tt>bearmail-update</tt>)</s></li>
  <li><s>Permettre de relire le fichier <tt>mailmap</tt> en cas de modification</s></li>
</ul>

<h2>Bugs connus</h2>

<ul>
  <li>Le fichier mailmap n'est pas écrit sur le disque en cas de modification d'un alias.</li>
</ul>
