# -*- coding: utf-8 -*-
import cherrypy

__all__ = ['MailmapTool']

class MailmapTool(cherrypy.Tool):
    def __init__(self):
        cherrypy.Tool.__init__(self, 'on_start_resource',
                               self.bind_session,
                               priority=20)
 
    def _setup(self):
        cherrypy.Tool._setup(self)
        cherrypy.request.hooks.attach('on_end_resource',
                                      self.commit_transaction,
                                      priority=80)
 
    def bind_session(self):
        mailmap = cherrypy.engine.publish('mailmap-session').pop()
        cherrypy.request.mailmap = mailmap
 
    def commit_transaction(self):
        if not hasattr(cherrypy.request, 'mailmap'):
            return

        cherrypy.request.mailmap = None
        cherrypy.engine.publish('mailmap-commit')
