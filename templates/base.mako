## -*- coding: utf-8 ; mode: html -*-

<%def name="csrf_token()">
% if csrftoken:
<input type="hidden" value="${csrftoken}" name="csrftoken"/>
% endif
</%def>

<%!
def escape_mail(text):
   return text.replace("<mail>", '<span class="label">').replace("</mail>", "</span>")
%>

<!DOCTYPE html>
<html lang="fr" dir="ltr">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Attac - Une autre gestion des alias est possible !</title>
    <link rel="stylesheet" href="/static/css/bootstrap.min.css"/>
    <link rel="stylesheet" href="/static/css/main.css" type="text/css" media="all" />
    <script type="text/javascript" src="/static/js/jquery.js"></script>
    <script type="text/javascript" src="/static/js/attac.js"></script>
    <script type="text/javascript" src="/static/js/bootstrap.min.js"></script>
  </head>

  <body class="sommaire">
    <div id="container">
      <div id="entete">
        <%block name="header">
          <h1><%block name="title"/></h1>
        </%block>

        <div id="userinfo">
	  <div class="btn-group">
	    % if user:
	    <a class="btn dropdown-toggle" data-toggle="dropdown" href="#">
	      Compte utilisateur
	      <span class="caret"></span>
	    </a>
	    <ul class="dropdown-menu">
	      <li><a href="/user/info">Connecté en tant que « ${user.username} »</a></li>
	      <li><a href="/user/password">Changer de mot de passe</a></li>
	      <li><a href="/user/logout">Se déconnecter</a></li>
	    </ul>
	    % else:
	    <a class="btn btn-primary" href="/user/login">S'authentifier</a></li>
            % endif
	  </div>
	</div>
      </div>
      <div id="nav">
	<div class="menu-conteneur">
	  <ul class="menu-liste menu-items">
	    <li class="menu-entree item">
	      <a href="/">Accueil</a>
	    </li>
	    <li class="menu-entree item">
	      <a href="/alias/search">Alias</a>
	      <ul class="menu-liste menu-items">
		<li class="menu-entree item"><a href="/alias/search">Rechercher un alias</a></li>
		<li class="menu-entree item"><a href="/alias/new">Ajouter un alias</a></li>
		<li class="menu-entree item"><a href="/alias/view">Tous les alias</a></li>
	      </ul>
	    </li>

	    % if user and user.is_admin == True:
	    <li class="menu-entree item">
	      <a href="/user/list">Utilisateurs</a>
	      <ul class="menu-liste menu-items">
		<li class="menu-entree item"><a href="/user/list">Liste des utilisateurs</a></li>
		<li class="menu-entree item"><a href="/user/new">Ajouter un utilisateur</a></li>
	      </ul>
	    </li>
	    % endif

	    <li class="menu-entree item">
	      <a href="/postfix/">Postfix</a>
	      <ul class="menu-liste menu-items">
		<li class="menu-entree item"><a href="/postfix/restart">Redémarrer Postfix</a></li>
		<li class="menu-entree item"><a href="/postfix/diff">Voir les modifications</a></li>
	      </ul>
	    </li>

	    <li class="menu-entree item">
	      <a href="/about/">À propos</a>
	    </li>
	  </ul>	  
	</div>
      </div>

      <div id="content">
	% if error_messages:

	% for msg in error_messages:
	<div class="alert alert-error">
	  <button type="button" class="close" data-dismiss="alert">×</button>
	  ${msg | escape_mail}
	</div>
	% endfor
	% elif ok_messages:
	% for msg in ok_messages:
	<div class="alert alert-success">
	  <button type="button" class="close" data-dismiss="alert">×</button>
	  ${msg | escape_mail}
	  </ul>
	</div>
        % endfor
	% endif

        ${self.body()}
      </div>

      <div id="pied">
        <%block name="pied">
	Réalisé par Olivier Tétard, pour Attac France.
      </%block>
    </div>
  </div>
</body>
</html>
