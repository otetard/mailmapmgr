## -*- coding: utf-8 ; mode: html -*-
<%def name="alias_search_block(type)">
<form method="get" action="/${type}/view/" class="form-search">
  <input type="hidden" value="full" name="mode"/>
  <fieldset class="block_search">
    <legend>Rechercher</legend>
    <div class="alert alert-info">
      <button type="button" class="close" data-dismiss="alert">×</button>
      <strong>Remarque</strong> : la recherche ne fonctionne pas sur les adresse cibles des alias.
    </div>

    <div class="row">
      <div class="col-lg-6">
        <div class="input-group">
            <input type="text" value="${q or ''}" name="q" size="100" class="form-control">
            <div class="input-group-btn">
                <button type="submit" type="button" class="btn">Rechercher</button>
            </div>
            <select name="domain" class="form-control">
	        <option value="">Tous les domaines</option>
	        % for d in domain_list:
	            <option ${'selected="selected' if domain == d else ''} value="${d}">${d}</option>
                % endfor:
            </select>
        </div>
      </div>
    </div>
  </fieldset>
</form>
</%def>
