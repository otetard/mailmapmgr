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

<form class="form-signin" action="/user/login" method="post">
    ${parent.csrf_token()}
    <input type="hidden" name="from_page" value="${from_page}" />

    <label for="username" class="sr-only">Identifiant</label>
    <input type="text" class="form-control" name="username" id="username" placeholder="Identifiant" value="${username or ''}" required autofocus>

    <label for="password" class="sr-only">Mot de passe</label>
    <input type="password" class="form-control" name="password" id="password" placeholder="Mot de passe" required>
    <button class="btn btn-lg btn-primary btn-block" type="submit">Authentification</button>

    <p><a href="/user/reset">Première connexion ou mot de passe oublié ?</a></p>
</form>

<style>
.form-signin {
        max-width: 330px;
        padding: 15px;
        margin: 0 auto;
    }
    .form-signin .form-control {
        position: relative;
        height: auto;
        box-sizing: border-box;
        padding: 10px;
        font-size: 16px;
    }
    .form-signin .form-control:focus {
        z-index: 2;
    }
    .form-signin input[name="username"] {
        margin-bottom: -1px;
        border-bottom-right-radius: 0;
        border-bottom-left-radius: 0;
    }
    .form-signin input[name="password"] {
        margin-bottom: 10px;
        border-top-left-radius: 0;
        border-top-right-radius: 0;
    }
</style>
