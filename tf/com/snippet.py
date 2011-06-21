# -*- coding: utf-8 -*-

#######################################################################
# Copyright © 2007-2009 Yuri Malheiros.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# the Free Software Foundation; version 2 only.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#######################################################################

"""
This module implements a class that represents a snippet.
"""

import re

class Snippet(object):
    """
    This class represents a snippet.
    """
    def __init__(self, document, fields, mirrors, stop, bounds):
        """
        Constructor.
        
        @param fields: The fields of snippet.
        @type field: A tuple of SnippetFields.
        
        @param bounds: A mark at start of snippet and other at the end.
        @type bounds: A tuple of two marks.
        """
        self.document = document
        self.view = document.view
        self.buffer = self.view.buffer
        self.fields = fields
        self.mirrors = mirrors
        self.stop = stop
        self.current_field = 0
        self.bounds = bounds
        
        self.__start_fields()
        self.__start_mirrors()
    
    #################### Public Methods ####################
    
    def next(self):
        """
        Select the next field
        """
        self.current_field += 1
        
        node = self.fields.search(self.current_field)
        
        if node == False:
            raise KeyError
        
        while node.active == False:
            self.current_field += 1
            node = self.fields.search(self.current_field)
            
            if node == False:
                raise KeyError
            
        ins, bound = node.elem.marks
        ins_iter = self.buffer.get_iter_at_mark(ins)
        bound_iter = self.buffer.get_iter_at_mark(bound)
        self.buffer.select_range(ins_iter, bound_iter)
    
    def previous(self):
        """
        Select the previous field
        """
        self.current_field -= 1

        node = self.fields.search(self.current_field)
        
        if node == False:
            raise KeyError
        else:
            ins, bound = node.elem.marks
            ins_iter = self.buffer.get_iter_at_mark(ins)
            bound_iter = self.buffer.get_iter_at_mark(bound)
            self.buffer.select_range(ins_iter, bound_iter)
    
    def remove_marks(self):
        """
        Remove all marks used in this snippet
        """
        # Disconnect mirrors
        self.fields.pre_order(self.__disconnect_signals)
        
        # Remove stop mark
        if self.stop != None:
            self.buffer.delete_mark(self.stop)
            
        # Remove mirrors marks
        for i in self.mirrors:
            self.buffer.delete_mark(i.marks[0])
            self.buffer.delete_mark(i.marks[1])
        
        # Remove fields marks
        self.fields.pre_order(self.__remove_node_marks)
        
        # Delete bounds marks
        self.buffer.delete_mark(self.bounds[0])
        self.buffer.delete_mark(self.bounds[1])
            
    def field_change(self, field, text, mirror):
        """
        Mirror the text of a field.
        
        @param field: A snippet field.
        @type field: A SnippetField object.
        
        @param text: The text of snippet field.
        @type text: A string.
        
        @param mirror: A snippet mirror.
        @type mirror: A SnippetMirror object.
        """
        
        start = self.buffer.get_iter_at_mark(mirror.marks[0])
        end = self.buffer.get_iter_at_mark(mirror.marks[1])
        indent_iter = start.copy()
        indent = self.document.get_indentation(indent_iter)
        
        field_start_mark = field.marks[0]
        field_end_mark = field.marks[1]
        
        field_start_iter = self.buffer.get_iter_at_mark(field_start_mark)
        field_end_iter = self.buffer.get_iter_at_mark(field_end_mark)
        
        if (start.compare(field_start_iter) >= 0 and start.compare(field_end_iter) <= 0) \
        or (end.compare(field_start_iter) >= 0 and end.compare(field_end_iter) <= 0):
            return
             
        
        if mirror.regexp != None:
            find = re.compile(mirror.regexp[0])
            rep = mirror.regexp[1]

            matches = re.findall(find, text)
            
            self.buffer.delete(start, end)
            for i in matches:
                text = rep.replace("\\n", "\n" + indent)
                text = text.replace("$%", i)
                
                #print text
                #
                ##TODO: pergar o token ${%1} e tratá-lo
                #    
                #begin_curly = 0
                #end_curly = 0
                #j = 0
                #
                #while True:
                #    if text[j] == '$':
                #        begin_curly = j+1
                #
                #        while True:
                #            if text[begin_curly] == '{':
                #            
                #                end_curly = begin_curly+1
                #                while True:
                #                    if text[end_curly] == '}':
                #                        break
                #                    else:
                #                        end_curly += 1
                #                
                #                break
                #                
                #            else:
                #                begin_curly += 1
                #        
                #        break
                #            
                #    else:
                #        j += 1
                #
                #
                #mirror_num = text[begin_curly+2:end_curly]
                #mirror_num.replace(" ", "")
                #mirror_num = int(mirror_num)
                #
                #print "mirror num: " + str(mirror_num)
                #
                #node = self.fields.search(mirror_num)
                #field = node.elem
                #start_iter = self.buffer.get_iter_at_mark(field.marks[0])
                #end_iter = self.buffer.get_iter_at_mark(field.marks[1])
                #text_mirror = self.buffer.get_text(start_iter, end_iter)
                #
                #print "text mirror: " + text_mirror
                #print "text replaced: " + text[:begin_curly-1] + text_mirror + text[end_curly:]
                #print text
                #
                ##TODO: substituir o campo no texto
                
                self.buffer.insert(end, text)
        else:
            self.buffer.delete(start, end)
            self.buffer.insert(end, text)
    
    def __start_mirrors(self):
        """
        Connect the function field_change to all mirrors.
        """
        for i in self.mirrors:
            mirror_num = i.num
            node = self.fields.search(mirror_num)
            field = node.elem
            field.connect("changed", self.field_change, i)
            
            start_iter = self.buffer.get_iter_at_mark(field.marks[0])
            end_iter = self.buffer.get_iter_at_mark(field.marks[1])
            
            text = self.buffer.get_text(start_iter, end_iter)
            
            self.field_change(field, text, i)

    #################### Private Methods ####################

    def __start_fields(self):
        """
        Connect the function __field_changed to all fields.
        """
        self.fields.pre_order(self.__connect_fields)
        
    def __connect_fields(self, node):
        """
        Connect "changed" signal to all snippet fields.
        """
        
        field = node.elem
        if field != None:
            field.connect("changed", self.__field_changed, node)
        
    def __field_changed(self, field, text, node):
        """
        When a field is changed all the children of field is deleted.
        """
        for i in node.children:
            i.active = False

    def __remove_node_marks(self, node):
        field = node.elem
        
        if field != None:
            self.buffer.delete_mark(field.marks[0])
            self.buffer.delete_mark(field.marks[1])
            
    def __disconnect_signals(self, node):
        field = node.elem
        
        if field != None:
            if field.id != None:
                field.view.disconnect(field.id)    
