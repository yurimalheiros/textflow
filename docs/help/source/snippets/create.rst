Creating Snippets
====================================

XML File Structure
------------------------------------

Each snippet are defined in a XML file called snippet.xml. This file must be in the directory of its language, for example, a file snippet.xml in the languages/python/ has the definitions of python snippets.
 
In the end of this page you find the name of all supported languages.

The XML file structure is simple, see the following example:
::

   <snippets>
     <snippet>
       <key>snippet keyword</key>
       <body>snippet text</body>
       <name>snippet name</name>
     </snippet>
     <snippet>
       <key>snippet keyword</key>
       <body>snippet text</body>
       <name>snippet name</name>
     </snippet>
   </snippets>


The content of the tag key is the word that must be before the cursor when **Tab** key is pressed for activate the snippet. The text between body tag is the text inserted in the activation of a snippet. As writed before, the snippets are more than simple text addition, in the next sections we will learn how to define the different snippet components. Finally the text between the name tag is the snippet name, for example, **New function** or **Insert tag <div>**.


Fields
------------------------------------

What are they?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Fields are snippet components that can be accessed using **Tab** and/or **Shift+Tab** where any text could be typed. For understand it easily, we could think on they as form fields. To be more useful each field is stored in a variable and this variable can be used in other parts of the snippet definition.

Each field has a number and an optional initial value, the number one field is accessed in the begining, then, by pressing **Tab**, the field number two is accessed and so on. When the **Tab** key is pressed on the last field or the **Shift+Tab** combination in the first field, TextFlow leaves the Snippet mode and these keys get their normal behavior again.

Syntax
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

  ${field number:default value} 

field number: any integer greater than 0.
default value: field initial text. This value is optional.

Example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

  ${2:my text} 

The field 2 has "my text" as initial value. 
::

  ${1:}
   
The field 1 doesn't have inital value.

Nested Fields
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The fields can be set nested, in other words, one inside the other. When a field that includes other fields is changed, all fields inside it are destroyed and can no longer be accessed.
::

  ${1:value="${2:}"}

Stops
------------------------------------

What are they?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A stop is a special field that has the number zero and has no default value. This field indicates where the cursor will be after pressing **Tab** in the last snippet field.

Syntax
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

  ${0}

Example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

  if (${1:}) {
    ${0}
  }

When **Tab** is pressed after the last field, the field 1 in this example, the snippet finalize and the cursor will be in the ${0} place.
 
Mirrors
------------------------------------

What are they?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 
The mirrors are special structures of snippets that copy the value of a field to the place where the mirror is defined. We can think in the mirror as access to a variable that stores the contents of a field. 

Syntax
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

  ${%field number}

Example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

  <${1:tag}>${0}</${%1}>

The text typed in the field 1 will be copied into the mirror 1. You can use more than one mirror for the same field.

.. note::

  Remember that the characters '< 'and'> 'can not be used in a XML text file, in their place you must use &lt; and &gt; respectively.
 
Mirrors as default values
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An interesting feature of mirrors is that they can be used inside a text of a field, this feature can be useful to user replace, if necessary, the text mirrored.
::

  <a href="${1:http://${2:}}">${3:${%1}}</a>${0}
  
The text typed in the field 1 will be mirrored between the tags and <a> </a>, but if the user wants to replace text it can be done normally.
 
Mirror with transformation
------------------------------------

What are they?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
There are cases that we don't want just a simple copy of a field, sometimes we need only the first word or just a certain pattern to be copied. This is possible using mirrors with transformation.

A pattern is defined by a regular expression and each substring found in the field can be mirrored using **$%**, or other text can be placed.

Syntax
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:: 

  ${%field number/regex/new text}

Example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:: 

  def __init__(self, ${1:params}):
      ${%1/\w+/self.$% = $%\n}${0}

If you are entered in field 1 "name, age" the mirrored text will be:
::

  self.name = name
  self.idade = idade

Conditionals
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An interesting trick that can be done using mirrors with transformation is the creation of a conditional mirror, in other words, some text will appear only if a pattern occurs, if not, the mirror does not display anything.
::

  ${%1/int|float|char|double/return}

Only when the field 1 has the values int or float or char or double the mirror will display return. 
