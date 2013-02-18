# -*- coding: utf-8 -*-

import cherrypy

__all__ = ['ForcePostMethodTool']


class ForcePostMethodTool(cherrypy.Tool):
    def __init__(self):
        """
        The user tool takes care of fetching the current logged in
        user to then associating it with the request.
        """
        cherrypy.Tool.__init__(self, 'before_handler',
                               self._filter_method,
                               priority=20)

    def _filter_method(self, params=[]):
        req_method = cherrypy.request.method.upper()
        req_params = cherrypy.request.params

        if req_method == "POST":
            return True
        else:
            for param in req_params:
                if param in params:
                    cherrypy.response.headers['Allow'] = "POST"
                    raise cherrypy.HTTPError(405)
