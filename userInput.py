#!/usr/local/bin/python
#
#  u s e r I n p u t . p y
#
#  Copyright 2001 by Chris Meyers. 
#
#  General class to input string. Support of indirect files and ability to
#  comment input. 
#
import sys, string

class InputString :
    # class variable. used by all instances. Currently open @files
    fd = 0

    def __init__ (self, Echo=0) :
        # if true echo prompts and inputs from @files to screen
        self.echo = Echo
        return

    def get (self) :
        if self.fd == 0 :
            self.fd = open('test.lsp','r')
            line = self.fd.readline()
            if line == '':
                self.fd.close()
                self.fd = 0
        else:
            line = self.fd.readline()
            if line == '':
                self.fd.close()
                self.fd = 0
        return line
