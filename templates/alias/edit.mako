## -*- coding: utf-8 ; mode: html -*-
<%inherit file="../base.mako"/>

<%block name="title">Ajouter un alias</%block>

<%block name="error_block"></%block>

<% if mail is None: return  %>

<script type="text/javascript" lang="JavaScript">
function add_new_input() {
    $("#target").prepend('<p><input type="text" class="span4" value="" placeholder="Adresse de destination" name="targets"/></p>');
}

function remove_line(arg) {
}
</script>

<div class="alert alert-info">
  <p>
    Ce formulaire permet de créer de nouveaux alias. Veuillez saisir
    le nom de la nouvelle adresse, lui associer un domaine, puis
    saisir les adresses vers lesquelles les courriels doivent être
    redirigés. <strong>Les adresses de destination doivent être
    saisies sur des lignes séparées</strong>.
  </p>
  <p>
    <em>Remarque : il n'est pas encore possible d'ajouter un nouveau
      domaine par ce formulaire. Il n'est pas non plus possible
      d'ajouter des redirection de domaines par ce formulaire</em>
  </p>
</div>


<form method="POST" action="" class="form-horizontal">
  ${parent.csrf_token()}
  <fieldset class="add_new_alias">
    <legend>Modification d'un alias</legend>

    <div class="control-group">
      <label class="control-label">Adresse&nbsp:&nbsp;</label>
      <span class="uneditable-input" />${mail}</span>
    </div>

    <div class="control-group">
      <label class="control-label">Destinataires&nbsp;:&nbsp;</label>
      <div class="controls">

	% for t in targets:
	<p><input type="text" class="span4" value="${t}" placeholder="Adresse de destination" name="targets"/>
	<i class="icon-minus"></i>&nbsp;<span><a href="javascript:remove_line($(this));">Remove this line</a></span></p>
	% endfor

	<p id="target"><a href="javascript:add_new_input()"><i class="icon-plus"></i> Ajouter une autre adresse cible.</a></p>
      </div>
    </div>

    <p>
      <button id="submit" type="submit" class="btn  btn-primary" name="submit">Valider la modification de l'alias</button>
      <button class="btn" id="cancel" type="button" name="cancel">Annuler</button>
    </p>
  </fieldset>
</form>

