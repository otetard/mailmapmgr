## -*- coding: utf-8 ; mode: html -*-

<%inherit file="../base.mako"/>

<%block name="title">Liste des utilisateurs</%block>

<table class="mailmap_list table table-hover">
  <thead>
    <tr>
      <th>Identifiant</th>
      <th>Nom</th>
      <th>Courriel</th>
      <th>Admin</th>
      <th>Action</th>
    </tr>
  </thead>

  <tbody>
  % for u in user_list:
  <tr>
    <td>${u.username}</td>
    <td>${u.name}</td>
    <td>${u.email}</td>
    <td>${u.is_admin}</td>
    <td><a class="delete" title="Supprimer" href="/user/delete/${u.username}"><img alt="Supprimer" src="/static/img/icon_delete.gif"></a></td>
  </tr>
  % endfor
  </tbody>
</table>
