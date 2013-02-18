## -*- coding: utf-8 ; mode: html -*-

<%inherit file="../base.mako"/>

<%block name="title">Création de compte</%block>

<form class="form-horizontal" action="/user/new" method="post">
  ${parent.csrf_token()}

  <div class="control-group">
    <label class="control-label" for="username">Identifiant</label>
    <div class="controls">
      <input type="text" name="username" id="username" value="${username or ''}" placeholder="Identifiant"/>
    </div>
  </div>

  <div class="control-group">
    <label class="control-label" for="username">Nom</label>
    <div class="controls">
      <input type="text" name="name" id="name" value="${name or ''}" placeholder="Nom"/>
    </div>
  </div>

  <div class="control-group">
    <label class="control-label" for="username">Courriel</label>
    <div class="controls">
      <input type="text" name="email" id="email" value="${email or ''}" placeholder="Courriel"/>
    </div>
  </div>

  <div class="control-group">
    <label class="control-label" for="username">Super-administrateur </label>
    <div class="controls">
      <input type="checkbox" name="is_admin" id="is_admin"
	     % if is_admin:
	     checked="checked"
	     % endif
	     />
    </div>
  </div>

  <div class="control-group">
    <div class="controls">
      <button type="submit" class="btn btn-primary">Créer le compte</button>
    </div>
  </div>
</form>
