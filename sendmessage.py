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


from datoveschranky import sendmessage


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
    
    # load attachements
    attchs = []
    for a in options.attachements:
        attchs.append(sendmessage.load_attachement(a))

    try:
        reply = sendmessage.send(recpt_box_id, options.uname,
                                 options.pwd, subj, attchs)
        print reply.status
        print "Message ID is:", reply.data
    except Exception, e:
        print str(e)
