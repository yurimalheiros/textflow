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
This module implements the trigger of "ctrl+shift+[".
"""

import tf.app

shortcut = "ctrl+shift+{"
sticky = False

class SelectInsideBrackets(object):
    
    def activate(self):
        """
        Trigger activator.
        """
        self.document_manager = tf.app.document_manager
        view = self.document_manager.get_active_view()
        buffer = view.buffer
        open_brackets = {'(' : ')', '[' : ']', '{' : '}'}
        close_brackets = {')' : '(', ']' : '[', '}' : '{'}
        
        insert_mark = buffer.get_insert()
        begin = buffer.get_iter_at_mark(insert_mark)
        end = begin.copy()
        end.backward_char()
        
        left = None
        right = None
        
# minha versão --- início ------------------------------------------------------        
            
        # loop para determinar o início (left)
        cont = 1
        
        while True:
        
            if left == None:
            
                # retrocede no buffer se não for o início do documento 
                if begin.backward_char():
                    
                    # testa o caracter encontrado            
                    begin_char = begin.get_char()
                    
                    if begin_char in close_brackets.keys():
                        # se achou alguém fechando, conta mais um abrindo
                        cont += 1
                        
                    if begin_char in open_brackets.keys():
                        # se achou alguém abrindo, conta menos um
                        # e reseta o valor de "left"
                        cont -= 1
                        left = None
                        
                        # verifica se o contador zerou (match)
                        if cont == 0:
                            # carrega o caracter em "left"
                            left = begin_char

                            # e inicia segundo loop para encontrar o fechamento (right)
                            cont = 1
                            
                            while True:
                            
                                if right == None: 
                                
                                    # avança no buffer se não for o fim do documento
                                    if end.forward_char():
                                        # testa o caracter encontrado
                                        end_char = end.get_char()
                                        
                                        if end_char == left:
                                            # se encontrou alguém abrindo, conta mais um
                                            cont += 1
                                            
                                        if end_char in open_brackets[left]:
                                            # se encontrou alguém fechando, conta menos um
                                            # e reseta valor de "right"
                                            cont -= 1
                                            right = None
                                            
                                            # verifica se contador zerou
                                            if cont == 0:
                                                # carrega caracter em "right"
                                                right = end_char
                                                
                                                # executa a seleção
                                                begin.forward_char()
                                                buffer.select_range(end, begin)
                                                
                                                # e finaliza o segundo loop
                                                break
                                                
                                    else:
                                    
                                        break
                                        # sai da busca do fechamnto pq não 
                                        # encontrou nenhuma correspondência
                            
                            break
                            # termina o loop da busca pela abertura
                            
                else:
                    # sai da busca pq não encontrou nenhum caracter de abertura
                    # SUGESTÃO: deveria dar uma msg no status bar
                    break
        
        return True        
        
# minha versão --- fim ---------------------------------------------------------

    def __search_close_match(self, iterator, char, match):
        iter = iterator.copy()
        cont = 1
        
        while iter.forward_char():
            c = iter.get_char()
            if c == char:
                cont+=1
            elif c == match:
                cont-=1
            
            if cont == 0:
                return iter
        
        return iterator
        
    def __search_open_match(self, iterator, char, match):
        iter = iterator.copy()
        cont = 1
        
        while iter.backward_char():
            c = iter.get_char()
            if c == char:
                cont+=1
            elif c == match:
                cont-=1
            
            if cont == 0:
                return iter
        
        return iterator

