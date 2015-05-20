#!/usr/bin/python
# -*- coding: utf8 -*-
""" Module to manage compte """

from compta.cli.argparser import ParseArgs
from compta.cli.http_server import RequestServer

class Compte(object):
    """ Default class to manage compte """

    def __init__(self):
        """ Init class to manage parse argument """

        self.options = ParseArgs.get_method("compte")

    def list_compte(self):
        """ List compte account """

        id = None
        filter = {}
        if self.options.id:
            id = self.options.id
        if self.options.type:
            filter["filter"] = self.options.type
        if self.options.sort:
            filter["sort"] = self.options.sort
        if not self.options.all:
            if self.options.archive:
                filter["archive"] = "yes"
            else:
                filter["archive"] = "no"
        #rqst = RequestServer('localhost', '8080')
        #print rqst.get('compte')
        rqst = RequestServer.get_method("compte",
                                        compte=id,
                                        filter=filter
                                       )
        for compte in rqst.json():
            print "%s / %s, %s -  %s" % (compte["nom"],
                                         compte["type"],
                                         compte["numero"],
                                         compte["cle"]
                                        )

def main():
    """ Main function """
    compte = Compte()
    if compte.options.cmd == 'list':
        compte.list_compte()

if __name__ == '__main__':
    main()



