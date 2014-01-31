#!/usr/bin/env python
# encoding: utf-8
'''

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
import json
import codecs

    
def reply2json(reply):
    rv = []
    for r in reply:
        o = {}
        for attr in r.KNOWN_ATTRS:
            val = getattr(r, attr) 
            if not val:
                continue
            o[attr] = val
        rv.append(o)
    print json.dumps(rv, indent=2, ensure_ascii=False)


def create_message(client, query):    
    envelope = models.dbOwnerInfo()
    envelope.dbType = 'OVM'
    envelope.firmName = query

    reply = ds_client.FindDataBox(envelope)
    reply2json(reply.data)


if __name__ == "__main__":
    import logging
    from optparse import OptionParser

    parser = OptionParser(usage='''python %prog [options] [searched]''')

    parser.add_option('-u', '--username', action='store', dest='uname',
                      help='uzivatelske jmeno k tvoji DS',)
    parser.add_option('-p', '--pwd', action='store', dest='pwd',
                      help='heslo k tvoji DS',)

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error('wrong number of arguments')

    logging.basicConfig(level=logging.INFO)
    logging.getLogger('suds').setLevel(logging.ERROR)

    query = args[0].decode('utf-8')
    
    logging.info("searching for %s ..." % query) 

    try:
        # create the client
        ds_client = Client(login_method='username',
                           login=options.uname,
                           password=options.pwd,
                           test_environment=False)

        create_message(ds_client, query)
    except Exception, e:
        logging.error(str(e))
    finally:
        ds_client.logout_from_server()
