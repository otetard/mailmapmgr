## -*- coding: utf-8 ; mode: html -*-
<%inherit file="../base.mako"/>

<%block name="title">Ajouter un alias</%block>

<%block name="error_block"></%block>

<% if mail is None: return  %>

<script type="text/javascript" lang="JavaScript">
 function add_new_input() {
     $("#target").prepend('<div class="input-group"><span class="input-group-addon">@</span><input class="form-control" type="text" value="" placeholder="Adresse de destination" name="targets"/><span class="input-group-addon"><a href="javascript:remove_line($(this));"><i class="glyphicon glyphicon-minus"></i></a></span></div>');
 }

 function remove_line(arg) {

 }
</script>

<div class="alert alert-info">
    <p>
        Ce formulaire permet de créer de nouveaux alias. Veuillez saisir le nom de la nouvelle adresse, lui associer un domaine, puis saisir les adresses vers lesquelles les courriels doivent être redirigés. <strong>Les adresses de destination doivent être saisies sur des lignes séparées</strong>.
    </p>
    <p>
        <em>Remarque : il n'est pas encore possible d'ajouter un nouveau domaine par ce formulaire. Il n'est pas non plus possible d'ajouter des redirection de domaines par ce formulaire</em>
    </p>
</div>


<form method="POST" action="">
    ${parent.csrf_token()}
    <fieldset class="add_new_alias">
        <legend>Modification d'un alias</legend>

        <div class="form-group">
            <label>Adresse</label>
            <span class="form-control disabled" />${mail}</span>
        </div>

        <div class="form-group">
            <label>Destinataires</label>

            % for t in targets:
	        <div class="input-group">
                    <span class="input-group-addon">@</span>
                    <input class="form-control" type="text" value="${t}" placeholder="Adresse de destination" name="targets"/>
                    <span class="input-group-addon"><a href="javascript:remove_line($(this));"><i class="glyphicon glyphicon-minus"></i></a></span>
                </div>
	    % endfor
            <p id="target"><a href="javascript:add_new_input()"><i class="glyphicon glyphicon-plus"></i> Ajouter une autre adresse cible.</a></p>
        </div>

        <div class="form-group">
            <button id="submit" type="submit" class="btn  btn-primary" name="submit">Valider la modification de l'alias</button>
            <button class="btn" id="cancel" type="button" name="cancel">Annuler</button>
        </div>
    </fieldset>
</form>
