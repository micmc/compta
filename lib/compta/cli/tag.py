#!/usr/bin/python
# -*- coding: utf8 -*-
""" Module to manage banque """

from compta.db.ecriture import Tag as DBTag

from compta.cli.argparser import ParseArgs
from compta.cli.http_server import RequestServer
from compta.cli.server import Server

class Tag(Server):
    """ List compte account """

    def __init__(self, parser=None):
        """ Init class to manage parse argument """

        Server.__init__(self, parser)
        self.rest_method = "tag"
        self.database = (DBTag,)

    def list(self):
        """ Redefine list to print """
        Server.list(self)
        try:
            for tag in self.rqst:
                print "%s, %s, %s" % (tag["id"],
                                      tag["nom"],
                                      tag["valeur"]
                                     )
        except Exception as ex:
            print ex

def main():
    """ Main function """
    parse_args = ParseArgs.get_method("tag")
    tag = Tag(parse_args)
    tag.launch_cmd()

if __name__ == '__main__':
    main()
