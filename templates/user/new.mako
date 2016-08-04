## -*- coding: utf-8 ; mode: html -*-

<%inherit file="../base.mako"/>

<%block name="title">Création de compte</%block>

<form action="/user/new" method="post">
  ${parent.csrf_token()}

  <div class="form-group">
    <label for="username">Identifiant</label>
    <input class="form-control" type="text" name="username" id="username" value="${username or ''}" placeholder="Identifiant"/>
  </div>

  <div class="form-group">
    <label for="username">Nom</label>
    <input class="form-control" type="text" name="name" id="name" value="${name or ''}" placeholder="Nom"/>
  </div>

  <div class="form-group">
    <label for="username">Courriel</label>
    <input class="form-control" type="text" name="email" id="email" value="${email or ''}" placeholder="Courriel"/>
  </div>

  <div class="checkbox">
    <label>
      <input type="checkbox" name="is_admin" id="is_admin"
	     % if is_admin:
	     checked="checked"
	     % endif
	     />
      Super-administrateur
    </label>    
  </div>

  <button type="submit" class="btn btn-primary">Créer le compte</button>
</form>
