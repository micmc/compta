#!/usr/bin/python
# -*- coding: utf8 -*-
""" Module to manage banque """

#from simplejson.scanner import JSONDecodeError

from compta.cli.argparser import ParseArgs
from compta.cli.http_server import RequestServer
from compta.cli.server import Server

class Banque(Server):
    """ List compte account """

    def __init__(self, parser=None):
        """ Init class to manage parse argument """

        Server.__init__(self, parser)
        self.rest_method = "banque"

    def list(self):
        """ Redefine list to print """
        Server.list(self)
        try:
            for banque in self.rqst:
                print "%s, %s %s %s - %s %s" % (banque["nom"],
                                                banque["adresse"],
                                                banque["cp"],
                                                banque["ville"],
                                                banque["code_banque"],
                                                banque["code_guichet"]
                                               )
        except Exception as ex:
            print ex

def main():
    """ Main function """
    parse_args = ParseArgs.get_method("banque")
    banque = Banque(parse_args)
    banque.launch_cmd()

if __name__ == '__main__':
    main()



