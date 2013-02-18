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
    <div class="input-append">
      <input type="text" value="${q or ''}" name="q" size="100"  class="span4 search-query">
      <button type="submit" type="button" class="btn">Rechercher</button>
    </div>

    <select name="domain">
	<option value="">Tous les domaines</option>
	% for d in domain_list:
	<option 
	   % if domain == d:
	   selected="selected"
	 % endif
	 value="${d}">${d}</option>
      % endfor:
    </select>
  </fieldset>
</form>
</%def>
