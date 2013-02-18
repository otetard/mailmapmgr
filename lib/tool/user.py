# -*- coding: utf-8 -*-

import cherrypy

from lib.model.user import User

__all__ = ['UserAuthTool']


class UserAuthTool(cherrypy.Tool):
    def __init__(self):
        """
        The user tool takes care of fetching the current logged in
        user to then associating it with the request.
        """
        cherrypy.Tool.__init__(self, 'before_handler',
                               self._fetch,
                               priority=20)

    def _setup(self):
        cherrypy.Tool._setup(self)
        cherrypy.request.hooks.attach('on_end_resource',
                                      self._cleanup,
                                      priority=80)

    def _fetch(self, require_auth, require_admin=False):
        user = None
        username = cherrypy.session.get("_cp_username", None)

        if username:
            user = User.get(cherrypy.request.db, username)

        if require_auth and user is None and require_admin is not None:
            raise cherrypy.HTTPRedirect("/user/login")           

        cherrypy.request.user = user

        if require_admin and user.is_admin is False:
            raise cherrypy.HTTPError("403 Forbidden", "You are not allowed to access this resource.")

    def _cleanup(self):
        cherrypy.request.user = None
