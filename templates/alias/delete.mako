## -*- coding: utf-8 ; mode: html -*-
<%inherit file="../base.mako"/>

<%block name="title">Supprimer un alias</%block>

<%namespace name="defs" file="../defs/alias_search_block.mako"/>

% if mail is not None:
<form method="POST" action="">
  ${parent.csrf_token()}
  <fieldset class="rm_alias">
    <legend>Supprimer un alias</legend>

    <div class="alert alert-error">
      <p><strong>Voulez-vous vraiment supprimer l'alias <span class="label label-important">${mail}</span> ?</strong></p>
      
      % if len(targets) == 1:
      <p>Cette alias redirige les courriels vers l'adresse suivante&nbsp;:</p>
      % else:
      <p>Cette alias redirige les courriels vers les adresses suivantes&nbsp;:</p>
      % endif
      
      <ul>
	% for t in targets:
	<li>${t}</li>
	% endfor
      </ul>
    </div>

    <p>
      <button class="btn" id="cancel" type="button" name="cancel">Annuler</button>
      <button class="btn btn-primary" id="submit" type="submit" name="submit">Confirmer la suppression de l'alias</button>
    </p>
  </fieldset>
</form>

% else:

${defs.alias_search_block(type = 'alias')}

% endif

