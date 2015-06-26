#!/usr/bin/python
# -*- coding: utf8 -*-
""" Module to manage compte """

from simplejson.scanner import JSONDecodeError

from compta.cli.argparser import ParseArgs
from compta.cli.http_server import RequestServer
from compta.cli.server import Server

class Compte(Server):
    """ List compte account """

    def __init__(self, parser=None):
        """ Init class to manage parse argument """

        Server.__init__(self, parser)
        self.rest_method = "compte"

    def list(self):
        """ Redefine list to print """
        Server.list(self)
        try:
            for compte in self.rqst.json():
                print "(%2d) - %s / %s, %s -  %s" % (compte["id"],
                                                     compte["nom"],
                                                     compte["type"],
                                                     compte["numero"],
                                                     compte["cle"]
                                                    )
        except JSONDecodeError as ex:
            print ex

def main():
    """ Main function """
    parse_args = ParseArgs.get_method("compte")
    compte = Compte(parse_args)
    compte.launch_cmd()

if __name__ == '__main__':
    main()



