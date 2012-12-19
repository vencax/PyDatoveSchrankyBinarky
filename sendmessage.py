#!/usr/bin/env python
# encoding: utf-8
'''
Created on Dec 3, 2012

@author: vencax

#install:
#--------
sudo pip install git+git://github.com/vencax/dslib.git
sudo pip install git+git://git.nic.cz/sudsds/

usage:
python sendmessage.py --username fjdsakj --pwd dsfafafdasdf \
-a /home/vencax/tosend.txt -a /home/vencax/another.pdf \
DSadresaUradu "oznameni uradu"
'''

import os
import base64
import subprocess
from dslib.client import Client
from dslib import models


def create_attachemet(att_file):
    dmfile = models.dmFile()
    try:
        mime = subprocess.Popen('/usr/bin/file -i %s' % att_file, shell=True,
                                stdout=subprocess.PIPE).communicate()[0]
        dmfile._dmMimeType = mime.split(' ')[1].rstrip(';')
    except Exception:
        dmfile._dmMimeType = 'text/plain'
    dmfile._dmFileMetaType = "main"
    dmfile._dmFileDescr = os.path.basename(att_file)
    with open(att_file, 'r') as f:
        dmfile.dmEncodedContent = base64.standard_b64encode(f.read())
    return dmfile


def create_message(client, recipient, subject, attachmentfiles):
    if not isinstance(attachmentfiles, list):
        attachmentfiles = [attachmentfiles]
    envelope = models.dmEnvelope()
    envelope.dbIDRecipient = recipient
    envelope.dmAnnotation = subject
    dmfiles = []
    for a in attachmentfiles:
        dmfiles.append(create_attachemet(a))
    reply = ds_client.CreateMessage(envelope, dmfiles)
    print reply.status
    print "Message ID is:", reply.data


if __name__ == "__main__":
    import logging
    from optparse import OptionParser

    parser = OptionParser(usage='''\
python %prog [options] [recipient] [subject]

recipient - adresa DS prijemce
subject - predmet DS''')

    parser.add_option('-u', '--username', action='store', dest='uname',
                      help='uzivatelske jmeno k tvoji DS',)
    parser.add_option('-p', '--pwd', action='store', dest='pwd',
                      help='heslo k tvoji DS',)
    parser.add_option('-a', '--attachement', action='append',
                      dest='attachements',
                      help='create a XHTML template instead of HTML')

    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error('wrong number of arguments')

    logging.basicConfig(level=logging.INFO)
    logging.getLogger('suds').setLevel(logging.ERROR)

    recpt_box_id, subj = args

    try:
        # create the client
        ds_client = Client(login_method='username',
                           login=options.uname,
                           password=options.pwd,
                           test_environment=False)

        create_message(ds_client, recpt_box_id, subj, options.attachements)
    except Exception, e:
        logging.error(str(e))
    finally:
        ds_client.logout_from_server()
