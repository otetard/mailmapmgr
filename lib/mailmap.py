#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import logging
import re
import hashlib
import os
import datetime
from threading import Lock
import time
import subprocess
import shutil

from collections import OrderedDict

debugging = True

def check_email(email):
    """Check if supplied email address is valid"""

    if re.match('^[A-Za-z0-9\-\._\$\+]+@[A-Za-z0-9\-\.]+$', email):
        return True

    return False

class Field_Exception(Exception):
    pass

class Field:
    subtype = None
    value  = None

    MAIL_CATCHALL = 0
    MAIL_NORMAL = 1
    PASSWORD_NOPASSWORD = 2
    PASSWORD_MD5 = 4
    TARGET_LOCAL = 8
    TARGET_PIPE = 16
    TARGET_ALIAS = 32
    TARGET_DOMAIN = 64

    def __str__(self):
        return self.value

    def __init__(self, mailmap, value, subtype=None):
        self.mailmap = mailmap
        self.value = value
        self.subtype = subtype

class Field_Mail(Field):

    @staticmethod
    def parse_field(mailmap, value):
        """Check if supplied field is a valid email field. This field
        might be an email address or a catchall address
        (*@example.org). For this special case, we just replace "*" by
        a "x" to make it valid

        If everything is ok, just create a Field_Mail object.
        """

        if check_email(re.sub('^\*@', "x@", value)) == False:
            raise Field_Exception("Invalid email address: {0}".format(value))

        if re.match('^\*@', value):
            return Field_Mail(mailmap, value, Field.MAIL_CATCHALL)
        else:
            return Field_Mail(mailmap, value, Field.MAIL_NORMAL)

class Field_Password(Field):

    @staticmethod
    def parse_field(mailmap, value):
        if value == "":
            return Field_Password(mailmap, value, Field.PASSWORD_NOPASSWORD)

        if re.match("^[0-9a-f]{32}$", value):
            return Field_Password(mailmap, value, Field.PASSWORD_MD5)

        raise Field_Exception("Invalid password supplied: {0}".format(value))

    def change_password(value):
        if self.value == "":
            raise Field_Exception("As of now, the password field is empty which indicates that the account is not a classic mail account")

        self.value = hashib.md5(value)

class Field_Target(Field):

    def __str__(self):
        if self.subtype == Field.TARGET_ALIAS:
            return ",".join(self.value)
        return self.value

    def add_target(self, alias):
        logging.info("Adding new alias: {0}".format(alias))

        if not check_email(alias):
            raise Field_Exception("Invalid email address suplied: {0}".format(alias))

        self.value.append(alias)

    def remove_target(self, alias):
        logging.info("Removing alias: {0}".format(alias))

        if not self.subtype == Field.TARGET_ALIAS:
            raise Field_Exception("Unable to remove target for non alias entries")

        if len(self.value) == 1:
            raise Field_Exception("Alias must have at least one target")

        self.value.remove(alias)

    def update_target(self, targets):
        logging.info("Updating target of alias: {0}".format(targets))

        if not self.subtype == Field.TARGET_ALIAS:
            raise Field_Exception("Unable to set target for non alias entries")

        if len(targets) < 1:
            raise Field_Exception("Alias must have at least one target")

        self.value = targets
        print(self.value)

    @staticmethod
    def parse_field(mailmap, value):
        if value == "local":
            return Field_Target(mailmap, value, Field.TARGET_LOCAL)

        if value[0] == "|":
            return Field_Target(mailmap, value, Field.TARGET_PIPE)

        (newfield, substn) = re.subn("^\*@", "x@", value)

        if substn == 1:
            if check_email(newfield) == False:
                raise Field_Exception("Invalid domain: {0}".format(value))
            else:
                return Field_Target(mailmap, value, Field_Target.TARGET_DOMAIN)

        targets = []
        for email in value.split(','):
            if not check_email(email):
                raise Field_Exception("Unable to parse email address ({0}) in such entry: {1}".format(email, value))
            targets.append(email)

        return Field_Target(mailmap, targets, Field_Target.TARGET_ALIAS)

class Field_Comment(Field):

    @staticmethod
    def parse_field(mailmap, value):
        return Field_Comment(mailmap, value)

    def __str__(self):
        return self.value


class Mailmap_Exception(Exception):
    pass


class Mailmap:
    """
    @TODO: ajouter les fonctions de recherches
    @TODO: permettre l'éciture du fichier en sortie
    @TODO: gérer les commentaires
    @TODO: recherche
    @TODO: permettre de réordonner le fichier, dans la mesure où
    l'ordre peut avoir du sens (par exemple les alias définis avant
    les catchall)
    """

    content = OrderedDict()
    filename = None

    def __init__(self, filename, backupdir=None):
        self.lock = Lock()
        self.filename = filename
        self.parse_file()
        self.updated = False
        self.backupdir = backupdir

    def __str__(self):
        x = []
        for (k, v) in list(self.content.items()):
            x.append(str(v))

        return "\n".join(x)

    def get_domain_list(self):
        domains = set()
        for (k, v) in self.content.items():
            try:
                domains.add(k.split("@")[1])
            except Exception as e:
                pass

        return domains

    def get_aliases(self):
        return dict((k, v) for k, v in self.content.items() if isinstance(v, Mail_Alias))

    def add_new_entry(self, entry):
        self.updated = True

        logging.info("Adding new entry {0}: {1}".format(hash(entry), entry))
        if entry in self.content:
            raise Mailmap_Exception("Mail entry must be unique, tried to add multiple times this mail: {0}".format(entry.mail_entry))

        self.content.update({ entry.get_as_key(): entry})

    def get_entry(self, key):
        try:
            return self.content[key]
        except KeyError as e:
            raise Mailmap_Exception("Entrée introuvable")

    def remove_entry(self, key):
        try:
            entry = self.content.pop(key)
            self.updated = True
            return entry
        except KeyError as e:
            raise Mailmap_Exception("Entrée introuvable")

    def sync_to_disk(self):
        if self.updated:
            with self.lock:

                if self.backupdir is not None:
                    # Archive old mailmap
                    archive = "{0}-{1}".format(os.path.basename(self.filename),
                                               datetime.datetime.now().strftime("%s.%f"))
                    shutil.copy(self.filename, os.path.join(self.backupdir, archive))

                    with open(self.filename, 'w') as mailmap_f:
                        mailmap_f.write(str(self))
                        mailmap_f.write("\n")

            self.updated = False

    def parse_file(self):
        with self.lock:

            filename = self.filename

            valid_formats = {Field.MAIL_NORMAL | Field.PASSWORD_MD5 | Field.TARGET_LOCAL: Mail_Account,
                             Field.MAIL_NORMAL | Field.PASSWORD_NOPASSWORD | Field.TARGET_ALIAS: Mail_Alias,
                             Field.MAIL_NORMAL | Field.PASSWORD_NOPASSWORD | Field.TARGET_PIPE: Mail_Pipe,
                             Field.MAIL_CATCHALL | Field.PASSWORD_NOPASSWORD | Field.TARGET_ALIAS: Mail_Catchall,
                             Field.MAIL_CATCHALL | Field.PASSWORD_NOPASSWORD | Field.TARGET_DOMAIN: Mail_Domain_Redirect}

            with open(filename, 'r') as mailmap_f:
                for line in mailmap_f.readlines():
                    line = line.strip()

                    if re.match("^($|#)", line):
                        new_entry = Mail_Comment(self, Field_Comment.parse_field(self, line))
                    else:
                        unparsed_fields = line.split(":")

                        if not len(unparsed_fields) == 3:
                            raise Mailmap_Exception("Invalid mailmap entry, 3 arguments needed instead of {0}.".format(len(unparsed_fields)))

                        mail = Field_Mail.parse_field(self, unparsed_fields[0])
                        password = Field_Password.parse_field(self, unparsed_fields[1])
                        target = Field_Target.parse_field(self, unparsed_fields[2])

                        format = mail.subtype | password.subtype | target.subtype

                        if not format in valid_formats:
                            raise Mailmap_Exception("Invalid format for mailmap entry: {0}".format(line))

                        new_entry = valid_formats[format](self, mail, password, target)

                    self.add_new_entry(new_entry)


class Mailmap_Entry_Exception(Exception):
    pass


class Mailmap_Entry():

    def __init__(self, mailmap, mail_entry, password_entry, target_entry):
        self.mailmap = mailmap
        self.mail_entry = mail_entry
        self.password_entry = password_entry
        self.target_entry = target_entry

    def __str__(self):
        return "{0}:{1}:{2}".format(self.mail_entry, self.password_entry, self.target_entry)

    def get_as_key(self):
        return self.mail_entry.value

    def remove_target(self, alias):
        raise Mailmap_Entry_Exception("Unavailable fonction for mail alias")

    def add_target(self, alias):
        raise Mailmap_Entry_Exception("Unavailable fonction for mail alias")

    def change_password(self, password):
        raise Mailmap_Entry_Exception("Unavailable fonction for mail alias")


# TODO
class Mail_Comment():
    def __init__(self, mailmap, comment):
        self.mailmap = mailmap
        self.comment = comment

    def get_as_key(self):
        return self.comment

    def __str__(self):
        return "{0}".format(self.comment)


class Mail_Account(Mailmap_Entry):

    def change_password(self, password):
        self.mailmap.updated = True
        self.password_entry.change_password(password)

    @staticmethod
    def create(mailmap, mail, password):
        return Mail_Account(Field_Mail(mailmap, mail, Field.MAIL_NORMAL),
                            Field_Password(mailmap, password, Field.PASSWORD_MD5),
                            Field_Target(mailmap, "local", Field.TARGET_LOCAL))


class Mail_Alias(Mailmap_Entry):
    def remove_target(self, alias):
        self.mailmap.updated = True
        self.target_entry.remove_target(alias)

    def update_target(self, targets):
        self.mailmap.updated = True
        self.target_entry.update_target(targets)

    def add_target(self, alias):
        self.mailmap.updated = True
        self.target_entry.add_target(alias)

    @staticmethod
    def create(mailmap, mail, targets):
        return Mail_Alias(mailmap,
                          Field_Mail(mailmap, mail, Field.MAIL_NORMAL),
                          Field_Password(mailmap, "", Field.PASSWORD_NOPASSWORD),
                          Field_Target(mailmap, targets, Field.TARGET_ALIAS))


class Mail_Pipe(Mailmap_Entry):
    pass


class Mail_Catchall(Mailmap_Entry):
    pass


class Mail_Domain_Redirect(Mailmap_Entry):
    pass



















if __name__ == '__main__':
    import sys

    mmap = Mailmap('../data/mailmap')
    mmap.parse_file()

    print(mmap.get_domain_list())

    print(mmap.get_aliases())
    sys.exit(42)

    #print mmap

    #print "--------------------------------------------------"

    e = mmap.get_entry("cac03moulins@audit-citoyen.org")
    e.add_target("toto@miskin.fr")
    # print e


    mmap.add_new_entry(Mail_Account.create("cac05moulins@audit-citoyen.org", "toto"))
    mmap.add_new_entry(Mail_Alias.create("cac04moulins@audit-citoyen.org", ["anfragen@attac-bern.ch", "info@attac-bern.ch"]))

    # print "--------------------------------------------------"

    e = mmap.get_entry("cac03moulins@audit-citoyen.org")
    #print e
    # e.remove_target("gerard.hatab@wanadoo.fr")
    # e.remove_target("toto@miskin.fr")
    #print e

    #print "--------------------------------------------------"

    print(mmap)

    #print "--------------------------------------------------"


    # # try:
    #     mmap = Mailmap.parse_file('mailmap')
    #     print mmap
    # except Exception as e:
    #     logging.fatal("Fatal exception: {0}".format(e))
