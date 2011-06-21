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
This module implements a class responsible for files manipulation.
"""

import os
import gnomevfs
import shutil

class FileList(object):
    """
    This class manipulate a list of files for a directory.
    """
    def __init__(self, current_dir=os.getenv("HOME")):
        """
        Constructor.
        
        @param current_dir: a directory path.
        @type current_dir: a string.
        """
        if current_dir == "":
            self.current_dir = os.getenv("HOME")
        else:
            self.current_dir = current_dir
            try:
                gnomevfs.open_directory(self.current_dir)
            except gnomevfs.NotFoundError:
                self.current_dir = os.getenv("HOME")
            except gnomevfs.IOError:
                self.current_dir = os.getenv("HOME")
            except gnomevfs.AccessDeniedError:
                self.current_dir = os.getenv("HOME")
    
    #################### Public Methods ####################

    def get_current_dir(self):
        """
        Return the current directory.
        
        @return: The current directory.
        @rtype: A string.
        """
        return self.current_dir
    
    def set_current_dir(self, new_dir):
        """
        Set the current directory.
        
        @param current_dir: a directory path.
        @type current_dir: a string.
        """
        self.current_dir = new_dir
        
    def get_files(self, show_hidden = False):
        """
        Get a list of files of the current directory.
        
        @param show_hidden: True if the returned list will
        have hidden files too.
        @type show_hidden: a boolean.
        
        @return: The file list.
        @rtype: A list.
        """
        # Get directory files
        try:
            directory = gnomevfs.DirectoryHandle(self.current_dir)
        except gnomevfs.NotFoundError:
            self.current_dir = os.getenv("HOME")
            directory = gnomevfs.DirectoryHandle(self.current_dir)
        except gnomevfs.InvalidURIError:
            self.current_dir = os.getenv("HOME")
            directory = gnomevfs.DirectoryHandle(self.current_dir)
        except gnomevfs.DirectoryHandle:
            return []
            
        files = []
        
        # Sort the list
        for f_item in sorted(directory, cmp=self.__compare_files):
            #Is this the best way to skip hidden files?
            if (f_item.name.startswith('.') or f_item.name.endswith('~')) \
            and not show_hidden:
                continue
            files.append(f_item)
        
        return files
    
    #################### Private Methods ####################
    
    def __compare_files(self, file_one, file_two):
        """
        Compares two files and determines the first.
        
        @param file_one: the first file to compare.
        @type file_one: a gnomevfs.FileInfo.
        
        @param file_two: the second file to compare.
        @type file_two: a gnomevfs.FileInfo.
        
        @return: -1, 0, or 1.
        @rtype: an integer.
        """
        
        # Put folders at top of the list
        try:
            type_one = file_one.type
        except ValueError:
            type_one = 1
        else:
            if type_one == gnomevfs.FILE_TYPE_DIRECTORY:
                type_one = 0
            else:
                type_one = 1
            
        try:
            type_two = file_two.type
        except ValueError:
            type_two = 1
        else:
            if type_two == gnomevfs.FILE_TYPE_DIRECTORY:
                type_two = 0
            else:
                type_two = 1
        
        
        comp = cmp(type_one, type_two)
        
        # If the files are the same type then compare names
        if comp == 0:
            return cmp(file_one.name.lower(), file_two.name.lower())
            
        return comp

########## Misc Functions ##########

def get_language_from_mime(mime):
    """
    This function returns a language id according a mime type.
    
    @param mime: a mime type.
    @type mime: a String.
    
    @return: a language id.
    @rtype: a String.
    """
    
    dic = {'text/javascript': 'js', 'application/x-m4': 'm4',
           'image/x-xpixmap': 'c', 'text/x-ocl': 'ocl', 'text/x-sh': 'sh',
           'text/x-yacc': 'yacc', 'text/x-gtkrc': 'gtkrc',
           'application/x-shellscript': 'sh', 'text/x-ocaml': 'objective-caml',
           'application/x-awk': 'awk', 'text/x-changelog': 'changelog',
           'text/x-python': 'python', 'text/x-tex': 'latex', 'text/html': 'html',
           'application/x-tcl': 'tcl', 'application/x-gnome-app-info': 'desktop',
           'text/xml': 'xml', 'text/x-msil': 'msil', 'application/x-perl': 'perl',
           'text/x-ini-file': 'ini', 'text/x-php-source': 'php',
           'text/x-gettext-translation': 'gettext-translation',
           'application/docbook+xml': 'docbook', 'text/x-pkg-config': 'pkgconfig',
           'text/x-erlang': 'erlang', 'text/x-fortran': 'fortran',
           'application/xml': 'xml', 'text/x-php': 'php', 'text/x-boo': 'boo',
           'text/x-c++': 'cpp', 'application/x-ruby': 'ruby', 'text/x-dtd': 'dtd',
           'text/x-js': 'js', 'text/x-matlab': 'octave', 'text/x-bison': 'yacc',
           'text/x-csharpsrc': 'c-sharp', 'text/x-vbnet': 'vbnet',
           'text/x-pascal': 'pascal', 'text/x-dpatch': 'dpatch',
           'text/x-sql': 'sql', 'text/x-octave': 'octave',
           'text/x-csharp': 'c-sharp', 'text/x-po': 'gettext-translation',
           'text/x-vala': 'vala', 'text/x-patch': 'diff',
           'application/x-python': 'python', 'application/x-php': 'php',
           'text/x-javascript': 'js', 'text/x-objcsrc': 'objc',
           'text/x-texinfo': 'texinfo', 'text/x-makefile': 'makefile',
           'text/x-c++src': 'cpp', 'application/x-php-source': 'php',
           'text/x-ruby': 'ruby', 'text/x-idl': 'idl',
           'application/x-javascript': 'js', 'text/x-chdr': 'chdr',
           'text/x-shellscript': 'sh', 'text/x-verilog-src': 'verilog',
           'text/x-diff': 'diff', 'text/css': 'css',
           'text/x-pot': 'gettext-translation', 'text/x-csrc': 'c',
           'text/x-java': 'java', 'text/x-pox': 'gettext-translation',
           'text/x-rpm-spec': 'rpmspec', 'text/x-lua': 'lua',
           'text/x-literate-haskell': 'haskell-literate',
           'text/x-scheme': 'scheme', 'text/x-libtool': 'libtool',
           'application/x-desktop': 'desktop', 'text/x-vhdl': 'vhdl',
           'text/x-adasrc': 'ada', 'application/x-ini-file': 'ini',
           'text/x-dsrc': 'd', 'text/x-haskell': 'haskell', 'text/x-ada': 'ada',
           'text/x-c': 'c', 'text/x-cpp': 'cpp', 'text/x-perl': 'perl',
           'text/x-vb': 'vbnet', 'text/x-gap': 'gap',
           'text/x-nemerle': 'nemerle', 'text/x-tcl': 'tcl',
           'text/x-c++hdr': 'chdr', 'text/x-R': 'r', 'application/javascript': 'js'}
    try:
        lang_id = dic[mime]
    except KeyError:
        return None
    else:
        return lang_id

def mkdir(path, remove = False):
    """ 
    Create a full path, directory by directory
    if removeExisting is set it will remove main folder and contents before creation.
    """
    #remove directiory if already exists
    if remove:
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=False)
 	
    if not os.path.exists(path):
        os.makedirs(path)
 	
    return path

def guess_encoding(text, default):
    """
    Tries to guess the encoding of the specified string. The result is a tuple
    of 3 values. the first one is the encoded string. the second one is the
    encoding of the returned result. the third value is a number which indicates
    the quality of the encoding. if the string could be encoded successfully,
    the value is -1. If none of the encodings could encode the string correctly
    this value is the length of the encoded string. the comparison of the encoded
    and the unencoded string can give some indication of the quality of the 
    encoding. However this is not an absolute measure, because the length of
    the string can vary due to the encoding.
    """
    
    encodings = [default, "utf-8", "ascii", 
    "utf-7",  "utf-8-sig", "iso8859-2", "iso8859-3", "iso8859-4", "iso8859-5",
    "iso8859-6", "iso8859-7", "iso8859-8", "iso8859-9", "iso8859-10", "iso8859-13",
    "iso8859-14", "iso8859-15", "iso2022-jp", "iso2022-jp-1", "iso2022-jp-2",
    "iso2022-jp-2004", "iso2022-jp-3", "iso2022-jp-ext", "iso2022-kr", "latin-1",
    "big5", "big5hkscs", "cp037", "cp424", "cp437", "cp500", "cp737", "cp775",
    "cp850", "cp852", "cp855", "cp856", "cp857", "cp860", "cp861", "cp862", "cp863",
    "cp864", "cp865", "cp866", "cp869", "cp874", "cp875", "cp932", "cp949", "cp950",
    "cp1006", "cp1026", "cp1140", "cp1250", "cp1251", "cp1252", "cp1253", "cp1254",
    "cp1255", "cp1256", "cp1257", "cp1258", "euc-jp", "euc-jis-2004", "euc-jisx0213",
    "euc-kr", "gb2312", "gbk", "gb18030", "hz",  "johab", "koi8-r", "koi8-u",
    "mac-cyrillic", "mac-greek", "mac-iceland", "mac-latin2", "mac-roman",
    "mac-turkish", "ptcp154", "shift-jis", "shift-jis-2004", "shift-jisx0213"]

    #first we try to encode the string with each of the encodings and strict
    #encoding policy
    for encoding in encodings:
        try:
            temp = unicode(text, encoding)
            return temp, encoding
        except UnicodeDecodeError:
            continue
    
    raise UnicodeDecodeError
