from distutils.core import setup
import glob
import os

# I18N
I18NFILES = []
LANGUAGE_PACKAGES = []
PACKAGE_FILES = {}

for filepath in glob.glob("po/mo/*/LC_MESSAGES/*.mo"):
    lang = filepath[len("po/mo/"):]
    targetpath = os.path.dirname(os.path.join("share/locale",lang))
    I18NFILES.append((targetpath, [filepath]))
    
for root, dirs, files in os.walk('tf/languages'):
    package = root.replace(os.path.sep, ".")
    LANGUAGE_PACKAGES.append(package)
    PACKAGE_FILES[package] = ["snippets.xml"]

setup(name='textflow',
      version='0.2.9',
      packages=['tf', 'tf.com', 'tf.core',
                'tf.ui', 'tf.widgets', "tf.languages"] + LANGUAGE_PACKAGES,
      package_data = PACKAGE_FILES,
      scripts=['textflow'],
      data_files=[("/usr/share/textflow/icons/256x256/apps", glob.glob("icons/256x256/apps/*.png")),
                  ("/usr/share/textflow/icons/192x192/apps", glob.glob("icons/192x192/apps/*.png")),
                  ("/usr/share/textflow/icons/128x128/apps", glob.glob("icons/128x128/apps/*.png")),
                  ("/usr/share/textflow/icons/64x64/apps", glob.glob("icons/64x64/apps/*.png")),
                  ("/usr/share/textflow/icons/48x48/apps", glob.glob("icons/48x48/apps/*.png")),
                  ("/usr/share/textflow/icons/32x32/apps", glob.glob("icons/32x32/apps/*.png")),
                  ("/usr/share/textflow/icons/16x16/apps", glob.glob("icons/32x32/apps/*.png")),
                  ("/usr/share/textflow/icons/scalable/apps", glob.glob("icons/scalable/apps/*.svg")),
                  ("/usr/share/pixmaps", glob.glob("icons/192x192/apps/*.png")),
                  ("/usr/share/applications", ["textflow.desktop"]),
                  ("/usr/share/textflow/triggers", glob.glob("tf/triggers/*.py")),
                  ("/usr/share/textflow/sidepanels", glob.glob("tf/sidepanels/*.py")),
                  ('/usr/share/textflow/glade/', glob.glob('tf/glade/*.glade'))]
                   + I18NFILES
      )
