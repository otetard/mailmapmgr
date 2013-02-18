## -*- coding: utf-8 ; mode: html -*-
<%inherit file="../base.mako"/>

<%block name="error_block"></%block>

<%block name="title">Créer un nouvel alias</%block>

<script type="text/javascript" lang="JavaScript">
function add_new_input() {
    $("#target").prepend('<p><input type="text" class="span4" value="" placeholder="Adresse de destination" name="targets"/></p>');
}

function remove_line(arg) {
}
</script>

<div class="alert alert-info">
  <button type="button" class="close" data-dismiss="alert">×</button>

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
    <legend>Ajout d'un alias</legend>

    <div class="control-group">
      <label class="control-label">Adresse&nbsp:&nbsp;</label>
      <input type="text" value="${mail or ''}" placeholder="Définition du nouvel alias" name="mail"/>
    </div>

    <div class="control-group">
      <label class="control-label">Domaine&nbsp;:&nbsp;</label>
      <select name="domain">
	<option value="">Sélectionner un domaine</option>
	% for d in domain_list:
	<option value="${d}"
	% if d == domain:
	selected="selected"
	% endif
	>${d}</option>
	% endfor
      </select>
    </div>

    <div class="control-group">
      <label class="control-label">Destinataires&nbsp;:&nbsp;</label>
      <div class="controls">

	% for t in targets:
	<p><input type="text" class="span4" value="${t}" placeholder="Adresse de destination" name="targets"/>
	<i class="icon-minus"></i>&nbsp;<span><a href="javascript:remove_line($(this));">Remove this line</span></p>
	% endfor

	<p><input type="text" class="span4" value="" placeholder="Adresse de destination" name="targets"/></p>

	<p id="target"><a href="javascript:add_new_input()"><i class="icon-plus"></i> Ajouter une autre adresse cible.</a></p>
      </div>
    </div>

    <p>
      <button id="submit" type="submit" class="btn  btn-primary" name="submit">Valider la création de l'alias</button>
    </p>
  </fieldset>
</form>
