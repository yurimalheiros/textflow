Example
====================================
Snippets for Python:
::

  <snippets>
    <snippet>
      <key>for</key>
      <body>for ${1:variable} in ${2:list}:
      ${0}</body>
      <name>Loop: for</name>
    </snippet>
    
    <snippet>
      <key>init</key>
      <body>def __init__(self, ${1:params}):
      ${%1/\w+/self.$% = $%\n}${0}</body>
      <name>Constructor</name>
    </snippet>
    
    <snippet>
      <key>.</key>
      <body>self.</body>
      <name>self</name>
    </snippet>

    <snippet>
      <key>def</key>
      <body>def ${1:method}(${2:self${3:}}):
      ${0}</body>
      <name>Function Definition</name>
    </snippet>

    <snippet>
      <key>imp</key>
      <body>import ${1:module}</body>
      <name>import</name>
    </snippet>

    <snippet>
      <key>imp</key>
      <body>from ${1:module} import ${2:class}</body>
      <name>from/import</name>
    </snippet>

    <snippet>
      <key>main</key>
      <body>if __name__ == "__main__":
      ${0}</body>
      <name>Main</name>
    </snippet>
    <snippet>
      <key>class</key>
      <body>class ${1:ClassName}(${2:object}):
      def __init__(self, ${3:params}):
          ${%3/\w+/self.$% = $%\n}${0}</body>
      <name>New Class</name>
    </snippet>

    <snippet>
      <key>cod</key>
      <body># -*- coding: utf-8 -*-</body>
      <name>utf-8</name>
    </snippet>

    <snippet>
      <key>cod</key>
      <body># -*- coding: iso-8859-1 -*-</body>
      <name>iso-8859-1</name>
    </snippet>
  </snippets>
