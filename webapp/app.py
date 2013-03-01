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
import urllib

import smtplib
from email.mime.text import MIMEText

import subprocess

messages = {
    'pre_new': u"La création du compte <mail>{0}</mail> s'est correctement déroulée",
    'pre_update': u"La modification du compte s'est correctement déroulée"
}

SESSION_KEY = "_cp_username"

class UserControllerException(Exception):
    pass


class UserController(object):

    # Crypto inspired by http://codeghar.wordpress.com/2011/09/01/aes-encryption-with-python/

    _block_size = 32
    _interrupt = u'\u0001'
    _pad = u'\u0000'
    _secret_key = cherrypy.config.get("user.key")
    _iv = cherrypy.config.get("user.iv4")

    def _add_padding(self, data):
        new_data = ''.join([data, self._interrupt])
        new_data_len = len(new_data)
        remaining_len = self._block_size - new_data_len
        to_pad_len = remaining_len % self._block_size
        pad_string = self._pad * to_pad_len
        return ''.join([new_data, pad_string])

    def _strip_padding(self, data):
        return data.rstrip(self._pad).rstrip(self._interrupt)

    def _aes_encrypt(self, data):
        try:
            cipher = AES.new(self._secret_key, AES.MODE_CBC, self._iv)
            return b64encode(cipher.encrypt(self._add_padding(data)))
        except Exception, e:
            raise UserControllerException("Erreur cryptographique : {0}".format(e))

    def _aes_decrypt(self, enc_data):
        try:
            cipher = AES.new(self._secret_key, AES.MODE_CBC, self._iv)
            return self._strip_padding(cipher.decrypt(b64decode(enc_data)))
        except Exception, e:
            raise UserControllerException("Erreur cryptographique : {0}".format(e))

    @cherrypy.expose
    @cherrypy.tools.mako(template="user/login.mako")
    @cherrypy.tools.csrf(enable=False)
    def login(self, username=None, password=None, from_page="/", msg=None):
        # FIXME: ne pas autoriser un second login si déjà authentifié

        db = cherrypy.request.db

        if User.get_all(db).count() == 0:
            raise cherrypy.HTTPRedirect("/install")

        if username is None and password is None:
            return {'from_page': from_page,
                    'ok_messages': [msg] if msg is not None else None,
                    }

        if User.authenticate(db, username, password):
            # Authentication successful
            cherrypy.session.regenerate()
            cherrypy.session[SESSION_KEY] = cherrypy.request.login = username
            raise cherrypy.HTTPRedirect(from_page or "/")


        # Authentication failed
        username = cherrypy.session[SESSION_KEY] = cherrypy.request.login = None
        return {'user': username,
                'auth_error': u"L'authentification a échoué (utilisateur ou mot de passe invalide)",
                'from_page': from_page}

    @cherrypy.expose
    def logout(self, from_page="/"):
        username = cherrypy.session.get(SESSION_KEY, None)
        cherrypy.session[SESSION_KEY] = None

        if username:
            cherrypy.request.login = None

        raise cherrypy.HTTPRedirect(from_page or "/")

    @cherrypy.expose
    @cherrypy.tools.mako(template="user/reset.mako")
    def reset(self, username=None):
        db = cherrypy.request.db

        if username:
            user = User.get(db, username)

            # Compte inexistant
            if user:
                email = user.email

                expiration_date = time.mktime((datetime.utcnow() + timedelta(1)).timetuple())
                token = self._aes_encrypt("{0}|{1}".format(username, expiration_date))

                url = "https://mailmapmgr.attac.org/user/validate?token={0}".format(urllib.quote(token))

                msg = MIMEText("""Bonjour\n\nPour changer votre mot de passe, veuillez cliquer sur le lien suivant : {0}""".format(url))

                msg['Subject'] = '[MailmapMgr Attac] Changement de mot de passe'
                msg['From'] = "attac.technique@attac.org"
                msg['To'] = email
                s = smtplib.SMTP('localhost')
                s.sendmail("attac.technique@attac.org", email, msg.as_string())
                s.quit()

                return {
                    'mail_sent': True,
                    'email': email,
                    }

            return {
                'user': cherrypy.request.user,
                'error_messages': [u"Compte inexistant"]
                }

        return {}


    @cherrypy.expose
    @cherrypy.tools.mako(template="user/password.mako")
    @cherrypy.tools.forcepost(params=["current_password", "password", "password2"])
    def password(self, current_password=None, password=None, password2=None):
        db = cherrypy.request.db
        user = cherrypy.request.user

        if current_password is not None or password is not None or password2 is not None:
            try:
                if not User.authenticate(db, user.username, current_password):
                    raise UserControllerException(u"Mot de passe courant incorrect")

                elif password != password2:
                    raise UserControllerException(u"Les deux mot de passe ne concordent pas")

                else:
                    User.set_password(db, user.username, password)
                    msg = u"Le changement de mot de passse a bien été pris en compte"

                    # Utilisateur déjà authentifié
                    return {'ok_messages': [u"Le changement de mot de passe s'est bien déroulé"],
                            'user': user,
                            }

            except UserControllerException, e:
                return {'error_messages': [e],
                        'user': user}

        return {'user': user}


    @cherrypy.expose
    @cherrypy.tools.mako(template="user/validate.mako")
    @cherrypy.tools.forcepost(params=["password", "password2"])
    def validate(self, token, password=None, password2=None):
        try:
            db = cherrypy.request.db

            # L'utilisateur n'est pas authentfié, il utilise son jeton
            dec_token = self._aes_decrypt(token)
            username, expiration_date = dec_token.split("|")

            if datetime.utcfromtimestamp(float(expiration_date)) < datetime.utcnow():
                raise UserControllerException("Le jeton a expiré")

            if User.get(db, username) is None:
                raise UserControllerException("Compte inexistant")

            if password is not None or password2 is not None:
                if password != password2:
                    return {'valid_token': True,
                            'username': username,
                            'token': token,
                            'error_messages': [u"Les deux mot de passe ne concordent pas"]}
                else:
                    User.set_password(db, username, password)
                    msg = u"Le changement de mot de passse a bien été pris en compte"
                    raise cherrypy.HTTPRedirect(u"/user/login?msg={0}".format(msg))

            return {'valid_token': True,
                    'username': username,
                    'token': token}

        except UserControllerException, e:
            return {'error_messages': [e]}

    @cherrypy.expose
    @cherrypy.tools.mako(template="user/info.mako")
    def info(self):
        u = cherrypy.request.user

        if u is None:
            raise cherrypy.HTTPRedirect("/user/login")

        return {'user': cherrypy.request.user,
                'name': u.name,
                'email': u.email}

    @cherrypy.expose
    @cherrypy.tools.mako(template="user/list.mako")
    @cherrypy.tools.auth(require_admin=True)
    def list(self):
        db = cherrypy.request.db
        user_list = User.get_all(db)

        return {
            'user': cherrypy.request.user,
            'user_list': user_list
            }

    @cherrypy.expose
    @cherrypy.tools.mako(template="user/delete.mako")
    @cherrypy.tools.auth(require_admin=True)
    @cherrypy.tools.forcepost(params=["confirm"])
    def delete(self, username, confirm=None):
        db = cherrypy.request.db

        try:
            user_to_delete = User.get(db, username)

            if user_to_delete is None:
                raise UserControllerException(u"Utilisateur inexistant")

            if user_to_delete.is_admin is True and User.get_all_admin(cherrypy.request.db).count() == 1:
                raise UserControllerException(u"Impossible de supprimer le dernier administrateur")

            if confirm is None:
                return {'user': cherrypy.request.user,
                        'user_to_delete': user_to_delete,
                        'confirm': False
                        }

            if confirm == "1":
                try:
                    db.delete(user_to_delete)

                    return {'user': cherrypy.request.user,
                            'ok_messages': [u"L'utilisateur a bien été supprimé"]}

                except Exception, e:
                    return {'user': cherrypy.request.user,
                            'error_messages': [u"Une erreur a été recontrée: {0}".format(e)]}


        except UserControllerException, e:
            return {'user': cherrypy.request.user,
                    'error_messages': [u"Une erreur a été recontrée: {0}".format(e)]}

        return {}

    @cherrypy.expose
    @cherrypy.tools.mako(template="user/new.mako")
    @cherrypy.tools.auth(require_admin=True)
    @cherrypy.tools.forcepost(params=["username", "name", "email", "is_admin"])
    def new(self, username=None, name=None, email=None, is_admin=None):
        if username or name or email:
            db = cherrypy.request.db
            error_messages = []

            if not username:
                error_messages.append(u"Identifiant utilisateur manquant")
            elif User.user_exists(db, username):
                error_messages.append(u"Cet utilisateur existe déjà")

            if not email:
                error_messages.append(u"Adresse électronique manquante")
            elif not check_email(email):
                error_messages.append(u"Adresse électronique invalide")

            if not name:
                error_messages.append(u"Nom de l'utilisateur manquant")


            if len(error_messages) == 0:
                u = User(username = username,
                         email = email,
                         name = name)

                if is_admin == "on":
                    u.is_admin = True

                db.add(u)

                return {
                    'user': cherrypy.request.user,
                    'ok_messages': [u"Le compte <b>{0}</b> a bien été crée".format(username)]
                    }


            return {
                'user': cherrypy.request.user,
                'username': username,
                'name': name,
                'email': email,
                'is_admin': is_admin,
                'error_messages': error_messages
                }

        return {
            'user': cherrypy.request.user,
                }


class PostfixController():

    @cherrypy.expose
    @cherrypy.tools.mako(template="postfix/index.mako")
    def index(self):
        return {
            'user': cherrypy.request.user,
            }

    @cherrypy.expose
    @cherrypy.tools.mako(template="postfix/diff.mako")
    @cherrypy.tools.auth(require_admin=True)
    def diff(self):
        return {
            'user': cherrypy.request.user,
            }

    @cherrypy.expose
    @cherrypy.tools.mako(template="postfix/restart.mako")
    @cherrypy.tools.forcepost(params=["confirm"])
    def restart(self, confirm=False):
        ok_messages = None
        error_messages = None

        if confirm == "1":
            confirm = True

            # Restart Postfix
            process = subprocess.Popen(["/usr/bin/sudo", "/root/attac-mail/bearmail/bearmail-update"],
                                       stderr=subprocess.PIPE)
            err = process.communicate()[1]
            if err != '':
                error_messages = [u"Unable to restart Postfix: (<tt>{0}</tt>)".format(err)]
            else:
                ok_messages = [u"La configuration a bien été appliquée"]

        return {
            'error_messages': error_messages,
            'ok_messages': ok_messages,
            'user': cherrypy.request.user,
            'confirm': confirm,
            }

class SearchManager():

    @cherrypy.expose
    @cherrypy.tools.mako(template="search/index.mako")
    def index(self, q = None):
        results = []
        error_messages = None

        mgr = cherrypy.engine.publish('mailmap-session').pop()

        try:
            r = mgr.get_entry(q)
            results.append(r)
            results.append(r.alias_entry)
        except Exception, e:
            error_messages = e

        return {'q': q,
                'results': results,
                'error_messages': error_messages,
                'domain_list': mgr.get_domain_list(),
                'user': cherrypy.request.user,
                }

class AliasManager():

    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect("/alias/search")

    @cherrypy.expose
    @cherrypy.tools.mako(template="alias/view.mako")
    def view(self, q="", domain="", force=False, mode="end", pre=None):
        mgr = cherrypy.engine.publish('mailmap-session').pop()
        mailmap_list = mgr.get_aliases()
        error_messages = None
        search_str = q
        ok_messages = None

        if domain != "":
            search_str = "{0}@{1}".format(q, domain)

        if search_str and mode == "end":
            mailmap_list = dict((key, value) for key, value in mailmap_list.iteritems() if key.endswith(search_str))
        elif search_str and mode == "full":
            mailmap_list = dict((key, value) for key, value in mailmap_list.iteritems() if search_str in key)

        if pre is not None:
            ok_messages = [messages["pre_{0}".format(pre)].format(q)]

        return {'mailmap_list': mailmap_list,
                'q': q,
                'domain': domain,
                'domain_list': mgr.get_domain_list(),
                'error_messages': error_messages,
                'ok_messages': ok_messages,
                'user': cherrypy.request.user,
                }

    @cherrypy.expose
    @cherrypy.tools.mako(template="alias/search.mako")
    def search(self, q=None):
        mgr = cherrypy.engine.publish('mailmap-session').pop()

        return {'domain_list': mgr.get_domain_list(),
                'q': "",
                'user': cherrypy.request.user}

    @cherrypy.expose
    @cherrypy.tools.mako(template="alias/new.mako")
    @cherrypy.tools.forcepost(params=["mail", "domain", "submit"])
    def new(self, mail=None, domain=None, submit=None, **args):
        mgr = cherrypy.engine.publish('mailmap-session').pop()

        domain_list = mgr.get_domain_list()
        error_messages = []
        targets = []

        if submit is not None:
            mail_full = "{0}@{1}".format(mail, domain)

            # Vérification du domaine soumis pour l'adresse principale
            if len(domain) == 0:
                error_messages.append("Le nom de domaine soumis est vide.")
            elif not domain in domain_list:
                error_messages.append("<mail>{0}</mail> n'est pas un domaine reconnu".format(domain))
            elif not check_email(mail_full):
                error_messages.append("<mail>{0}</mail> n'est pas une adresse valide".format(mail_full))

            try:
                if isinstance(args['targets'], basestring):
                    targets = [args["targets"]]
                else:
                    targets = args['targets']
            except KeyError:
                pass

            # Mail verification
            targets = filter(None, targets) # Suppression des entrées vides

            if len(targets) == 0:
                error_messages.append("Aucune adresse cible n'est définie")
            for t in targets:
                if not check_email(t):
                    error_messages.append("L'adresse cible <mail>{0}</mail> n'est pas une adresse valide".format(t))

            try:
                if mgr.get_entry(mail_full) is not None:
                    error_messages.append(u"<mail>{0}</mail> est une adresse déjà définie".format(mail_full))
            except Mailmap_Exception, e:
                pass

            if len(error_messages) == 0:
                try:
                    mgr.add_new_entry(Mail_Alias.create(mgr, mail_full, targets))
                    raise cherrypy.HTTPRedirect("/alias/view/?q={0}&pre=new".format(mail_full), 302)
                except Mailmap_Exception, e:
                    error_messages.append(u"Une erreur est apparue lors de la création de l'alias : <mail>{0}</mail>".format(e))

        return {'domain_list': domain_list,
                'domain': domain,
                'mail': mail,
                'targets': targets,
                'error_messages': error_messages,
                'user': cherrypy.request.user
                }

    @cherrypy.expose
    @cherrypy.tools.mako(template="alias/delete.mako")
    @cherrypy.tools.forcepost(params=["submit"])
    def delete(self, mail, submit = None):
        mgr = cherrypy.engine.publish('mailmap-session').pop()

        error_messages = []
        ok_messages = []
        targets  = []

        # Vérification du format de l'adresse soumise en entrée
        if not check_email(mail):
            error_messages.append("<mail>{0}</mail> n'est pas une adresse valide".format(mail))

        try:
            # Récupération de l'entrée passée en paramètre et
            # récupération des alias correspondants
            #
            # @TODO: vérifier qu'il s'agit bien d'une entrée de
            # type alias !

            entry = mgr.get_entry(mail)
            targets = entry.target_entry.value

            if submit is not None:
                mgr.remove_entry(mail)
                ok_messages = [u"L'alias <mail>{0}</mail> a bien été supprimé !".format(mail)]
                targets = []
                mail = None

        except Mailmap_Exception, e:
            error_messages.append(u"Une erreur est apparue lors de la suppression de l'alias <mail>{0}</mail> : {1}".format(mail, e))
            targets = []
            mail = None


        return {'mail': mail,
                'targets': targets,
                'ok_messages': ok_messages,
                'error_messages': error_messages,
                'domain_list': mgr.get_domain_list(),
                'user': cherrypy.request.user
                }


    @cherrypy.expose
    @cherrypy.tools.mako(template="alias/edit.mako")
    @cherrypy.tools.forcepost(params=["submit"])
    def edit(self, mail, submit=None, **args):
        mgr = cherrypy.engine.publish('mailmap-session').pop()

        targets = []
        error_messages = []
        new_targets = []

        domain_list = mgr.get_domain_list()

        # Vérification du format de l'adresse soumise en entrée
        if not check_email(mail):
            error_messages.append("<mail>{0}</mail> n'est pas une adresse valide".format(mail))

        try:
            # Récupération de l'entrée passée en paramètre et
            # récupération des alias correspondants
            #
            # @TODO: vérifier qu'il s'agit bien d'une entrée de
            # type alias !

            entry = mgr.get_entry(mail)
            targets = entry.target_entry.value
            new_targets = targets

            # UPDATE DATA
            if submit is not None:

                if isinstance(args['targets'], basestring):
                    new_targets = [args["targets"]]
                else:
                    new_targets = args['targets']

                new_targets = filter(None, new_targets) # Suppression des entrées vides

                if len(new_targets) == 0:
                    error_messages.append(u"Il est nécessaire de fournir au moins une adresse de destination.")

                for t in new_targets:
                    if not check_email(t):
                        error_messages.append("<mail>{0}</mail> n'est pas une adresse valide".format(t))

                if len(error_messages) == 0:
                    entry.update_target(new_targets)
                    raise cherrypy.HTTPRedirect("/alias/view/{0}?pre=update".format(mail), 302)

            return {'mail': mail,
                    'targets': new_targets,
                    'error_messages': error_messages,
                    'domain_list': mgr.get_domain_list(),
                    'user': cherrypy.request.user
                    }

        except Mailmap_Exception, e:
            error_messages.append(u"<mail>{0}</mail> n'est pas une adresse connue".format(mail))
            return {'mail': None,
                    'targets': None,
                    'error_messages': error_messages,
                    'domain_list': mgr.get_domain_list(),
                    'user': cherrypy.request.user
                    }

class AboutManager():

    @cherrypy.expose
    @cherrypy.tools.mako(template="about/index.mako")
    def index(self):
        mgr = cherrypy.engine.publish('mailmap-session').pop()

        return {'user': cherrypy.request.user,
                }

    @cherrypy.expose
    @cherrypy.tools.mako(template="about/bugs.mako")
    def bugs(self):
        mgr = cherrypy.engine.publish('mailmap-session').pop()

        return {'user': cherrypy.request.user,
                }


class MailmapManager():

    #search = SearchManager()
    about = AboutManager()
    alias = AliasManager()
    user = UserController()
    postfix = PostfixController()

    @cherrypy.expose
    @cherrypy.tools.mako(template="index.mako")
    @cherrypy.tools.csrf()
    def index(self):
        return {'user': cherrypy.request.user,
                }

    @cherrypy.expose
    @cherrypy.tools.mako(template="install.mako")
    def install(self):
        if User.get_all(cherrypy.request.db).count() == 0:
            u = User(username="admin", is_admin=True)
            cherrypy.request.db.add(u)
            User.set_password(cherrypy.request.db, "admin", "admin")

            cherrypy.session.delete()

            return {'ok_messages': [u"Le compte administrateur par défaut a été crée. Attention à bien changer le mot de passe !"]
                    }

        raise cherrypy.HTTPError("403 Forbidden", "You are not allowed to access this resource.")
