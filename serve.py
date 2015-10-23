#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cherrypy
import os, os.path

#import lib.tool.mako_tool

SESSION_KEY = "_cp_username"

def check_auth(*args, **kwargs):
    """A tool that looks in config for 'auth.require'. If found and it
    is not None, a login is required and the entry is evaluated as a
    list of conditions that the user must fulfill"""

    require_auth = cherrypy.request.config.get('tools.auth.require_auth', None)
    if require_auth is True:
        username = cherrypy.session.get(SESSION_KEY)
        if username:
            cherrypy.request.login = username
        else:
            raise cherrypy.HTTPRedirect("/user/login")

def on_error_403(status, message, traceback, version):
    return """Permission denied! {0}""".format(message)

if __name__ == '__main__':
    base_dir = os.path.abspath(os.getcwd())
    conf_path = os.path.join(base_dir, "conf")


    log_dir = os.path.join(base_dir, "logs")
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    cherrypy.config.update(os.path.join(conf_path, "server.conf"))
    cherrypy.config.update({'error_page.403': on_error_403})

    from lib.plugin.mailmapplugin import MailmapEnginePlugin
    MailmapEnginePlugin(cherrypy.engine).subscribe()

    # # Template engine plugin
    from lib.plugin.makoplugin import MakoTemplatePlugin
    MakoTemplatePlugin(cherrypy.engine, os.path.join(base_dir, 'templates'), base_cache_dir=os.path.join(base_dir, 'cache')).subscribe()

    # Database access tool
    from lib.tool.db import SATool
    cherrypy.tools.db = SATool()

    from lib.tool.csrf import CsrfTool
    cherrypy.tools.csrf = CsrfTool()

    from lib.tool.forcepostmethod import ForcePostMethodTool
    cherrypy.tools.forcepost = ForcePostMethodTool()

    # Mailmap access tool
    from lib.tool.mailmap import MailmapTool
    cherrypy.tools.mailmap = MailmapTool()

    # Template engine tool
    from lib.tool.makotool import MakoTool
    cherrypy.tools.mako = MakoTool()

    # Tool to load the logged in user or redirect
    # the client to the login page
    from lib.tool.user import UserAuthTool
    cherrypy.tools.auth = UserAuthTool()

    from webapp.app import MailmapManager
    webapp = MailmapManager()
    # Let's mount the application so that CherryPy can serve it
    app = cherrypy.tree.mount(webapp, '/', os.path.join(conf_path, "app.conf"))

    # Database connection management plugin
    from lib.plugin.db import SAEnginePlugin
    cherrypy.engine.db = SAEnginePlugin(cherrypy.engine)
    cherrypy.engine.db.subscribe()

    if hasattr(cherrypy.engine, "signal_handler"):
        cherrypy.engine.signal_handler.subscribe()
            
    if hasattr(cherrypy.engine, "console_control_handler"):
        cherrypy.engine.console_control_handler.subscribe()

    # Let's start the CherryPy engine so that everything works
    cherrypy.engine.start()

    # Run the engine main loop
    cherrypy.engine.block()
