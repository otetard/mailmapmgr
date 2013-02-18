## -*- coding: utf-8 ; mode: html -*-
<%inherit file="../base.mako"/>

<%block name="title">Administration de Postfix</%block>

% if not confirm is True:

<h2>Redémarrer Postfix</h2>

<form class="form-horizontal" action="/postfix/restart" method="post">
  ${parent.csrf_token()}
  <input type="hidden" name="confirm" id="confirm" value="1"/>

  <p>Voulez-vous vraiment appliquer la configuration courante ?</p>

  <div class="control-group">
    <div class="controls">
      <button type="submit" class="btn btn-primary">Appliquer la configuration</button>
    </div>
  </div>
</form>

% endif

