## -*- coding: utf-8 ; mode: html -*-

<%inherit file="../base.mako"/>

<%block name="title">Informations utilisateur</%block>

<ul>
  <li>Identifiant : ${user.username}</li>
  <li>Nom : ${user.name or ''}</li>
  <li>Adresse électronique : ${user.email or ''}</li>
</ul>
