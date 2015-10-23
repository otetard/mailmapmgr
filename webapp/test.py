# -*- coding: utf-8 -*-

import cherrypy

from lib.mailmap import Mailmap, Mailmap_Exception, Mail_Alias
from lib.mailmap import check_email
from lib.tool.user import User

from Crypto.Cipher import AES
from Crypto import Random
from base64 import b64encode, b64decode
import hashlib

import time
from datetime import datetime, timedelta
import urllib.request, urllib.parse, urllib.error

import smtplib
from email.mime.text import MIMEText

messages = {
    'pre_new': "La création du compte <mail>{0}</mail> s'est correctement déroulée",
    'pre_update': "La modification du compte s'est correctement déroulée"
}

SESSION_KEY = "_cp_username"


class AboutManager():

    @cherrypy.expose
    def index(self):

        return """bla bla bla"""


        # user = cherrypy.request.user

        # return [user]

        # return {'user': cherrypy.request.user,
        #         'toto': 'tutu'}


class MailmapManager():

    about = AboutManager()
