## -*- coding: utf-8 ; mode: html -*-

<%inherit file="../base.mako"/>

<%block name="title">Changement de mot de passe</%block>

<form class="form-horizontal" action="/user/password" method="post">
  ${parent.csrf_token()}

  % if token:
  <input type="hidden" name="token" id="token" value="${token}"/>
  % endif

  <div class="control-group">
    <label class="control-label" for="username">Identifiant</label>
    <div class="controls">
      <span class="uneditable-input" />${user.username}</span>
    </div>
  </div>

  <div class="control-group">
    <label class="control-label" for="current_password">Mot de passe actuel</label>
    <div class="controls">
      <input type="password" name="current_password" id="current_password" placeholder="Mot de passe actuel">
    </div>
  </div>

  <div class="control-group">
    <label class="control-label" for="password">Nouveau mot de passe</label>
    <div class="controls">
      <input type="password" name="password" id="password" placeholder="Mot de passe">
    </div>
  </div>

  <div class="control-group">
    <label class="control-label" for="password2">Nouveau mot de passe (répétez)</label>
    <div class="controls">
      <input type="password" name="password2" id="password2" placeholder="Mot de passe">
    </div>
  </div>

  <div class="control-group">
    <div class="controls">
      <button type="submit" class="btn btn-primary">Modifier le mot de passe</button>
    </div>
  </div>
</form>
