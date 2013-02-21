# -*- coding: utf-8 -*-

import cherrypy
from cherrypy.process import wspbus, plugins
from lib.mailmap import Mailmap

import os

class MailmapEnginePlugin(plugins.Monitor):
    def __init__(self, bus):
        self.mailmap_engine = None
        self.mailmap_file = cherrypy.config.get("mailmap.file")
        self.mailmap_backupdir = cherrypy.config.get("mailmap.backupdir")
        self.mailmap_last_updated = None
        plugins.Monitor.__init__(self, bus, self.run, 1, name="_Mailmap_Engine")

    def start(self):
        if self.thread is None:
            self.mailmap_last_updated = None

        self.bus.log('Starting up Mailmap access')
        self.mailmap_engine = Mailmap(self.mailmap_file, backupdir=self.mailmap_backupdir)
        self.bus.subscribe("mailmap-session", self.mailmap_session)
        self.bus.subscribe("mailmap-commit", self.mailmap_commit)

        plugins.Monitor.start(self)

    def stop(self):
        self.bus.log('Stopping down Mailmap access')
        self.bus.unsubscribe("mailmap-session", self.mailmap_session)
        self.bus.unsubscribe("mailmap-commit", self.mailmap_commit)

        if self.mailmap_engine:
            self.mailmap_engine.sync_to_disk()
            self.mailmap_engine = None

    def mailmap_session(self):
       return self.mailmap_engine

    def mailmap_commit(self):
        if self.mailmap_engine:
            self.bus.log("Writing mailmap file to disk")
            self.mailmap_engine.sync_to_disk()

    def run(self):
        t = os.stat(self.mailmap_file).st_mtime

        if self.mailmap_last_updated is None:
            self.mailmap_last_updated = t
        elif t > self.mailmap_last_updated:
            self.mailmap_last_updated = t
            self.bus.log("Restarting because %s changed." % self.mailmap_file)
            self.thread.cancel()
            self.bus.log("Stopped thread %r." % self.thread.getName())
            self.bus.restart()
            return
