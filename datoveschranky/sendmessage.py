# encoding: utf-8
'''
Created on Dec 3, 2012

@author: vencax
'''

import base64
import os
import subprocess

from dslib import models
from dslib.client import Client
from sudsds.sax.text import Text


def send(recpt_box_id, uname, pwd, subj, attachements):
    """
    attachements: list of tuples of (mime, description, content)
    """
    ds_client = None
    try:
        # create the client
        ds_client = Client(login_method='username',
                           login=uname,
                           password=pwd,
                           test_environment=False)

        return _create_message(ds_client, recpt_box_id, subj, attachements)
    finally:
        if ds_client:
            ds_client.logout_from_server()


def load_attachement(att_file):
    try:
        mime = subprocess.Popen('/usr/bin/file -i %s' % att_file, shell=True,
                                stdout=subprocess.PIPE).communicate()[0]
        mime = mime.split(' ')[1].rstrip(';')
    except Exception:
        mime = 'text/plain'

    desc = os.path.basename(att_file)
    with open(att_file, 'r') as f:
        content = base64.standard_b64encode(f.read())
    return (mime, desc, content)


def _create_attachemet(mime, desc, content):
    dmfile = models.dmFile()
    dmfile._dmMimeType = mime
    dmfile._dmFileMetaType = "main"
    dmfile._dmFileDescr = desc
    dmfile.dmEncodedContent = content
    return dmfile


def _create_message(ds_client, recipient, subject, attachmentfiles):
    if not isinstance(attachmentfiles, list):
        attachmentfiles = [attachmentfiles]
    envelope = models.dmEnvelope()
    envelope.dbIDRecipient = recipient
    envelope.dmAnnotation = Text(subject, escaped=True)
    dmfiles = []
    for a in attachmentfiles:
        dmfiles.append(_create_attachemet(*a))
    return ds_client.CreateMessage(envelope, dmfiles)
