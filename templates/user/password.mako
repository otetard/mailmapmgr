## -*- coding: utf-8 ; mode: html -*-

<%inherit file="../base.mako"/>

<%block name="title">Changement de mot de passe</%block>

<form action="/user/password" method="post">
    ${parent.csrf_token()}

    % if token:
        <input type="hidden" name="token" id="token" value="${token}"/>
    % endif

    <div class="form-group">
        <label for="username">Identifiant</label>
        <div class="controls">
            <span class="form-control disabled" />${user.username}</span>
        </div>
    </div>

    <div class="form-group">
        <label for="current_password">Mot de passe actuel</label>
        <input class="form-control" type="password" name="current_password" id="current_password" placeholder="Mot de passe actuel">
    </div>

    <div class="form-group">
        <label for="password">Nouveau mot de passe</label>
        <input class="form-control" type="password" name="password" id="password" placeholder="Mot de passe">
    </div>

    <div class="form-group">
        <label for="password2">Nouveau mot de passe (répétez)</label>
        <input class="form-control" type="password" name="password2" id="password2" placeholder="Mot de passe">
    </div>

    <button type="submit" class="btn btn-primary">Modifier le mot de passe</button>
    </div>
</form>
