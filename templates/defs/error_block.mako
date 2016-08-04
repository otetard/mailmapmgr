## -*- coding: utf-8 ; mode: html -*-
<%def name="error_block()">

% if error_messages:
% for msg in error_messages:
<div class="alert alert-danger">
  <button type="button" class="close" data-dismiss="alert">×</button>
  ${msg | escape_mail}
</div>
% endfor
% elif ok_messages:
% for msg in ok_messages:
<div class="alert alert-success">
  <button type="button" class="close" data-dismiss="alert">×</button>
  ${msg | escape_mail}
</ul>
</div>
% endfor
% endif
</%def>
