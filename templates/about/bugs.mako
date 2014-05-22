## -*- coding: utf-8 ; mode: html -*-

<%inherit file="../base.mako"/>

<%block name="title">À propos</%block>

<h2>Bugs et problèmes connus</h2>

<ul>
  <li>Lors de la création ou de la modification d'une adresse, Mailmapmgr identifie que le fichier mailmap a changé (normal, c'est lui qui vient de le modifier) et du coup, entraine l'utilisateur vers une erreur 503. Il ne doit pas être nécessaire de redémarrer Mailmapmgr dans tous les cas.</li>
  <li>Le fichier mailmap est parfois écrit sur disque sans raison (sur la page /user/login/ par exemple</li>
  <li>Il faudrait supprimer les espaces autour des adresses lorsqu'elle sont soumises dans les formulaires (trim).</li>
  <li><s>Le fichier mailmap n'est pas écrit sur le disque en cas de modification d'un alias.</s></li>
</ul>

<h2>Choses à faire</h2>

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
