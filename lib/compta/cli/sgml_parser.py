#!/usr/bin/python
# -*- coding: utf8 -*-
""" Module to manage smgl parser """

#import sys
#import re
#import copy
import locale
from datetime import datetime
from sgmllib import SGMLParser

class LinkParser(SGMLParser):
    """Class to import ofx file"""

    def __init__(self):
        """Inheritance of sgmlparser"""
        SGMLParser.__init__(self)
        self.bankacctfrom = False
        self.banktranlist = False
        self.stmttrn = False
        # Banque account
        self.bankid = False
        self.branchid = False
        self.acctid = False
        # Ecriture
        self.dtposted = False
        self.trnamt = False
        self.trntype = False
        self.name = False
        self.memo = False
        self.compte = {}
        self.ecriture = []
        self.ecriture_tmp = None

    def start_bankacctfrom(self, attributes):
        """Begin tag BANKACCTFROM """
        self.bankacctfrom = True

    def end_bankacctfrom(self):
        """End tag BANKACCTFROM """
        self.bankacctfrom = False

    def start_bankid(self, attributes):
        """Begin tag BANKID """
        self.bankid = True

    def start_branchid(self, attributes):
        """Begin tag BRANCHID """
        self.branchid = True

    def start_acctid(self, attributes):
        """Begin tag ACCTID """
        self.acctid = True

    def start_banktranlist(self, attributes):
        """Begin tag BANKTRANLIST """
        self.banktranlist = True

    def end_banktranlist(self):
        """End tag BANKTRANLIST """
        self.banktranlist = False

    def start_stmttrn(self, attributes):
        """Begin tag STMTTRN """
        self.stmttrn = True
        #self.ecriture.append(self.ecriture_tmp)
        self.ecriture_tmp = {}

    def end_stmttrn(self):
        """End tag STMTTRN """
        self.stmttrn = False
        self.ecriture.append(self.ecriture_tmp)

    def start_name(self, attributes):
        """Begin tag NAME -> nom """
        self.name = True

    def start_memo(self, attributes):
        """Begin tag MEMO -> description """
        self.memo = True

    def start_dtposted(self, attributes):
        """Begin tag DTPOSTED -> date """
        self.dtposted = True

    def start_trnamt(self, attributes):
        """Begin tagTRNAMPT -> montant """
        self.trnamt = True

    def start_trntype(self, attributes):
        """Begin tag TRNTYPE -> type """
        self.trntype = True

    def handle_data(self, text):
        """Save test far each tag that we need"""
        if self.bankacctfrom:
            if self.bankid:
                self.compte['banque'] = text.strip()
                self.bankid = False
            if self.branchid:
                self.compte['guichet'] = text.strip()
                self.branchid = False
            if self.acctid:
                self.compte['compte'] = text.strip()
                self.acctid = False
        if self.banktranlist:
            if self.stmttrn:
                if self.dtposted:
                    self.ecriture_tmp['date'] = datetime.strptime(text.strip(), "%Y%m%d")
                    self.dtposted = False
                if self.trnamt:
                    self.ecriture_tmp['montant'] = locale.atof(text.strip())
                    self.trnamt = False
                if self.trntype:
                    self.ecriture_tmp['type'] = text.strip()
                    self.trntype = False
                if self.name:
                    self.ecriture_tmp['name'] = text.strip()
                    self.name = False
                if self.memo:
                    self.ecriture_tmp['memo'] = text.strip()
                    self.memo = False


