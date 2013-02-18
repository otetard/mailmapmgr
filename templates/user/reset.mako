## -*- coding: utf-8 ; mode: html -*-

<%inherit file="../base.mako"/>

<%block name="title">Changement de mot de passe</%block>

% if mail_sent:

<div class="alert alert-success">
  Un courriel vient d'être envoyé à l'adresse <span class="label">${email}</span> permettant de valider le changement de mot de passe.
</div>

% else:

<div class="alert alert-info">
  <button type="button" class="close" data-dismiss="alert">×</button>
  Pour obtenir un compte, veuillez contacter <a href="mailto:olivier.tetard@miskin.fr">Olivier Tétard</a>
</div>

<form class="form-horizontal" action="/user/reset" method="post">
  ${parent.csrf_token()}

  <div class="control-group">
    <label class="control-label" for="username">Identifiant</label>
    <div class="controls">
      <input type="text" name="username" id="username" placeholder="Identifiant" value="${username or ''}">
    </div>
  </div>

  <div class="control-group">
    <div class="controls">
      <button type="submit" class="btn btn-primary">Modifier le mot de passe</button>
    </div>
  </div>
</form>

% endif
