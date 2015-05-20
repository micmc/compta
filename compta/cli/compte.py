#!/usr/bin/python
# -*- coding: utf8 -*-

from argparser import ParseArgs
from http_server import RequestServer

class Compte(object):
    """ Default class to manage compte """

    def __init__(self):
        """ Init class to manage parse argument """

        self.options = ParseArgs.get_method("compte")

    def list_compte(self):
        """ List compte account """
        if self.options.id:
            pass
        #rqst = RequestServer('localhost', '8080')
        #print rqst.get('compte')
        rqst = RequestServer.get_method("compte")
        for compte in rqst.json():
            print "%s / %s, %s -  %s" % (compte["nom"],
                                            compte["type"],
                                            compte["numero"],
                                            compte["cle"]
                                           )

def main():
    compte = Compte()
    if compte.options.cmd == 'list':
        compte.list_compte()

if __name__ == '__main__':
    main()



