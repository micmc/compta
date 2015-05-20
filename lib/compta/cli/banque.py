#!/usr/bin/python
# -*- coding: utf8 -*-
""" module to manage banque """

from compta.cli.argparser import ParseArgs
from compta.cli.http_server import RequestServer

class Banque(object):
    """ Default class to manage banque """

    def __init__(self):
        """ Init class to manage parse argument """

        self.options = ParseArgs.get_method("banque")

    def list_banque(self):
        """ List banque account """
        if self.options.id:
            pass
        #rqst = RequestServer('localhost', '8080')
        #print rqst.get('banque')
        rqst = RequestServer.get_method("banque")
        for banque in rqst.json():
            print "%s, %s %s %s - %s %s" % (banque["nom"],
                                            banque["adresse"],
                                            banque["cp"],
                                            banque["ville"],
                                            banque["code_banque"],
                                            banque["code_guichet"]
                                           )

def main():
    """ Main function """
    banque = Banque()
    if banque.options.cmd == 'list':
        banque.list_banque()

if __name__ == '__main__':
    main()


