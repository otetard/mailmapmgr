## -*- coding: utf-8 ; mode: html -*-

<%inherit file="../base.mako"/>

<%block name="title">Suppression d'un utilisateur</%block>

% if user_to_delete:

<form class="form-horizontal" action="/user/delete" method="post">
  ${parent.csrf_token()}
  <input type="hidden" name="username" id="username" value="${user_to_delete.username}"/>
  <input type="hidden" name="confirm" id="confirm" value="1"/>

  <p>Voulez-vous supprimer le compte ${user_to_delete.username} ?</p>

  <div class="control-group">
    <div class="controls">
      <button type="submit" class="btn btn-primary">Supprimer le compte</button>
    </div>
  </div>
</form>

% endif
