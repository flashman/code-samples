#!/usr/bin/env python
'''
@author: homoflashmanicus (Michael Flashman)
@date: March 30, 2014
@about: A simple commandline tool for rendering <*..*> formated html templates.
@requirments: sys, json, arparse, re
@usage:
    money-cash$ python templater.py [-h] template data.json output.html
    positional arguments:
      main
      template    Path to html template file
      json        Path to JSON data used to populate the template.
      saveas      Save processed html file with this name.

    optional arguments:
      -h, --help  show this help message and exit
@details: 
    Template files are assumed to be (reasonably) well formatted with respect to <*...*> expressions. 
    Template consists of:
      Value insertion elements: <* key *>. key of a value in the json data
      Loop construcion elements: <* EACH arrayName itemName *>...<* ENDEACH *>. arrayName is the key to an array in the json data
      All other content is treated as strings
'''

import sys
import json
from argparse import ArgumentParser
import re

DATA = dict()
TOKENIZE = re.compile('<[\s]*(?=[*])|(?<=[*])[\s]*>')

class Tokenizer():
    '''Tokenize a string based by splitting on the givie  regex'''
    def __init__(self,string,regex):
        '''initialize the  tokenizer.  
        String is a string to be tokenize
        Regix is a compliled regular expression used  for splittin the string.
        The tokenizer also serves as a centralized que for subseqient processing (mostly popping) of the tokens
        '''
        self.tokens = regex.split(string)
        self.tokens.reverse()
    
    def pop_token(self):
        if self.tokens:
            return self.tokens.pop()
        else:
            return None

    def __str__(self):
        return str(self.tokens)

class Node():
    '''
    A class for converting a tokenized html template (<*..*> format) into a parse tree
    Render the parse tree as pure html with data injection. Data is stored in a json-like dictionary.
    '''

    def __init__(self,init_content=None):
        '''
        Initialize node.
        Optionally pass in some initial content.
        '''
        self.content = []
        if init_content: self.content.append(init_content)
        self.has_end_token = False
        self.build_recursively = False
        self.end_token = None

    def build(self,tokens):
        '''
        Build node by digesting tokens one by.
        Tokens are converted to subnodes (of an appropriate subclasse) and added to the node's content list.
        Build is called recursively on subnodes when appropriate. 
        '''
        token = tokens.pop_token()
        while token and not self.is_end_token(token):
            node = self.make_new_node(token)
            self.content.append(node)
            if node.build_recursively:
                node.build(tokens)
            token = tokens.pop_token()

        self.check_for_errors(token)

    def is_end_token(self,token):
        '''Check if token ends the current node's scope...This is only relevent for EachNode'''
        return False

    def to_html(self,data=DATA):
        '''Convert Node to html string literal.  Call recursively'''
        return ''.join( [c.to_html(data) for c in self.content if c] )
        
    def check_for_errors(self,token):
        '''Check for parsing issues, such as missing end tokens'''
        if self.has_end_token and not (token and self.is_end_token(token)):
            print 'WARNING: Missing %s.  Template may have been rendered incorrectly.' % self.end_token


    #UPDATE THE FOLLOWING STATIC METHODS WHEN ADDING NEW NODE SUBCLASSES.
    @staticmethod
    def make_new_node(token=None):
        '''Add new node by type'''
        if not token: 
            return Node()
        elif Node.is_string(token):
            return StringNode(token)
        elif Node.is_value(token):
            return ValueNode(token)
        elif Node.is_each(token):
            return EachNode(token)

    @staticmethod
    def is_string(token):
        '''check if token is string type'''
        return (not token.startswith('*')) or (not token.endswith('*'))  
    
    @staticmethod
    def is_value(token):
        ''' check if token is value type'''
        return (token.startswith('*') and token.endswith('*')) and not token.find('EACH')>-1  

    @staticmethod
    def is_each(token):
        '''check if token is each type'''
        return token.startswith('*') and token.endswith('*') and token.find('EACH')>-1  


class StringNode(Node):
    '''Node subclass for storing simple html strings'''

    def to_html(self,data):
        '''Convett Node to html string literal'''
        return ''.join( [str(c) for c in self.content if c] )


class ValueNode(Node):
    '''
    Node subclass for parsing and rendering template elements of the form:  
    <* key *> where key is a json-formated lookup key for the associated data.
    The contents of <*....*> is stored in the first entry of content.
    '''

    def get_value(self,data):
        '''look up value of stored key in data, where data is a dictionary''' 
        key = self.content[0].strip('* ').split('.')
        return lookup_value(key,data) 

    def to_html(self,data):
        '''Convert node to html with data injected'''
        return self.get_value(data)


class EachNode(Node):
    '''
    Node subclass for parsing and rendering template elements of the form:  
       <* EACH arrayName itemName *> ... <* ENDEACH *>
    where arrayName is a json-formaged key for an array in the associated data.
    The contents of <*....*> is stored in the first entry of content.
    '''
    
    def __init__(self,init_content):
        Node.__init__(self,init_content)
        self.has_end_token=True
        self.build_recursively=True
        self.end_token='ENDEACH'

    def is_end_token(self,token):
        '''Check if token ends the each loop.'''
        return Node.is_each(token) and token.find(self.end_token)>-1

    def get_item_array(self,data):
        '''Parse lookup key from content and get data'''
        lookup_key= self.content[0].strip('* ').split(' ')[1].split('.')
        return lookup_value(lookup_key, data)
        
    def get_item_name(self):
        '''Parse item name from content'''
        return self.content[0].strip('* ').split(' ')[2]

    def to_html(self,data):
        '''Convert node to html with data injected'''
        data = self.get_item_array(data)
        item_name = self.get_item_name()
        s=''
        if data and type(data)==list:
            for d in data:
                s += ''.join( [c.to_html({item_name: d}) for c in self.content[1:] if c] )
        return s

def lookup_value(keys,data):
    '''
    Lookup value in a json-like nested dictionary <data>  by a list of keys 
    where each key access a layer in the dictionary
    '''
    def __get_value__(ks,d):
        try:
            if len(ks)>1:
                return __get_value__(ks[1:],d[ks[0]])
            else:
                return d[ks[0]]
        except:
            return None

    return __get_value__(keys,data)

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("main")
    parser.add_argument("template",  help="Path to html template file")
    parser.add_argument("json",  help="Path to JSON data used to populate the template.")
    parser.add_argument("saveas",  help="Save processed html file here.")    
    args = parser.parse_args(sys.argv)
    
    TEMPLATE = open(args.template).read()
    DATA = json.load(open(args.json))
    
    tokens = Tokenizer(TEMPLATE,TOKENIZE)
    templater = Node()
    templater.build(tokens)
    
    f = open(args.saveas,'w')
    f.write( templater.to_html(DATA) )
    f.close()
