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
This module implements a Tree with multiple children.
"""

class Tree(object):
    """
    This class represents a tree with multiple children.
    """
    def __init__(self):
        """
        Constructor.
        """
        self.root = None
    
    #################### Public Methods ####################
    
    def add(self, elem, root=None):
        """
        Add a node in the tree.
        
        @param elem: The node element. 
        @type elem: A object.
        
        @param root: The root of the tree or sub-tree. 
        @type root: A TreeNode.
        
        @return: The node added.
        @rtype: A TreeNode
        """
        
        node = TreeNode(elem)
        if root == None:
            self.root = node
        else: 
            root.children.append(node)
        
        return node
    
    def pre_order(self, func, root=None):
        """
        Pre-order walk.
        
        @param func: A function to use in all nodes.
        @type func: A function.
        
        @param root: The root of the tree or sub-tree. 
        @type root: A TreeNode.
        """
        if root == None:
            root = self.root

        func(root)
        
        if root.children == []:
            return
        
        for i in root.children:
            self.pre_order(func, i)
            
    def search(self, key, root=None):
        """
        Search for a element in the tree.
        
        @param key: Search key. 
        @type key: A object.
        
        @param root: The root of the tree or sub-tree. 
        @type root: A TreeNode.
        
        @return: A node or False if the key doesn't exist in the tree.
        @rtype: A TreeNode or False.
        """
        found = False
        if root == None:
            root = self.root
        
        if root.elem != None and root.elem.num == key:
            return root
        else:
        
            if root.children == []:
                return False
            
            for i in root.children:
                found = self.search(key, i)
                if found:
                    return found
                    
        return found
        
class TreeNode(object):
    """
    This class represents a tree node.
    """
    def __init__(self, elem):
        """
        Constructor.
        """
        self.elem = elem
        self.children = []
        self.active = True
