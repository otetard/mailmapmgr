## -*- coding: utf-8 ; mode: html -*-
<%inherit file="../base.mako"/>

<%block name="title">Administration de Postfix</%block>

<p>
  Cette page permet d'administrer le serveur de messagerie à
  proprement parler (voir les changements a appliquer et redémarrer le
  serveur).
</p>

<p>Actions possibles :</p>
<ul>
  <li><a href="/postfix/restart">redémarrer Postfix</a> ;</li>
  <li><a href="/postfix/diff">voir les modifications qui vont être appliquées</li>
</ul>
