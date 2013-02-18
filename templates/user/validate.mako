## -*- coding: utf-8 ; mode: html -*-

<%inherit file="../base.mako"/>

<%block name="title">Changement de mot de passe</%block>

% if valid_token:

<form class="form-horizontal" action="/user/validate" method="post">
  ${parent.csrf_token()}

  % if token:
  <input type="hidden" name="token" id="token" value="${token}"/>
  % endif

  <div class="control-group">
    <label class="control-label" for="username">Identifiant</label>
    <div class="controls">
      <span class="uneditable-input" />${username}</span>
    </div>
  </div>


  <div class="control-group">
    <label class="control-label" for="password">Nouveau mot de passe</label>
    <div class="controls">
      <input type="password" name="password" id="password" placeholder="Mot de passe">
    </div>
  </div>

  <div class="control-group">
    <label class="control-label" for="password">Nouveau mot de passe (répétez)</label>
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

% endif
