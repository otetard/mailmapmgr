## -*- coding: utf-8 ; mode: html -*-

<%inherit file="../base.mako"/>

<%block name="title">Authentification</%block>

<div class="alert alert-info">
  <button type="button" class="close" data-dismiss="alert">×</button>
  Pour obtenir un compte, veuillez contacter <a href="mailto:olivier.tetard@miskin.fr">Olivier Tétard</a>
</div>

% if auth_error:
<div class="alert alert-error">
  <button type="button" class="close" data-dismiss="alert">×</button>
  ${auth_error}
</div>
% endif

<form class="form-horizontal" action="/user/login" method="post">
  ${parent.csrf_token()}
  <input type="hidden" name="from_page" value="${from_page}" />

  <div class="control-group">
    <label class="control-label" for="username">Identifiant</label>
    <div class="controls">
      <input type="text" name="username" id="username" placeholder="Identifiant" value="${username or ''}">
    </div>
  </div>

  <div class="control-group">
    <label class="control-label" for="password">Mot de passe</label>
    <div class="controls">
      <input type="password" name="password" id="password" placeholder="Mot de passe">
    </div>
  </div>

  <div class="control-group">
    <div class="controls">
      <p>
	<a href="/user/reset">Première connexion ou mot de passe oublié ?</a>
      </p>
    </div>
  </div>

  <div class="control-group">
    <div class="controls">
      <button type="submit" class="btn btn-primary">Authentification</button>
    </div>
  </div>
</form>
