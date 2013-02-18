## -*- coding: utf-8 ; mode: html -*- 
<%inherit file="../base.mako"/>

<%block name="title">Toutes les entrées</%block>

<%namespace name="defs" file="../defs/alias_search_block.mako"/>
${defs.alias_search_block(type = 'alias')}

% if len(mailmap_list) > 0:
<table class="mailmap_list table table-hover">
  <thead>
    <tr>
      <th>Adresse</th>
      <th>Redirection vers</th>
      <th>Action</th>
    </tr>
  </thead>

  <tbody>
  % for key in mailmap_list:
  <tr>
    <td><a href="/alias/edit/${key}">${key}</a></td>
    <td>
      <ul>
	% for alias in mailmap_list[key].target_entry.value:
	<li>${alias}</li>
	% endfor
      </ul>
    </td>

    <td>
      <ul class="actions">
	<li><a title="Modifier" href="/alias/edit/${key}"><img alt="Modifier" src="/static/img/icon_edit.gif"></a></li>
	<li><a class="delete_fwd" title="Supprimer" href="/alias/delete/${key}"><img alt="Supprimer" src="/static/img/icon_delete.gif"></a></li>
      </ul>
    </td>
  </tr>
  % endfor
  </tbody>
</table>

%else:

<div class="alert">
  Aucun résultat n'a été trouvé.
</div>

%endif
