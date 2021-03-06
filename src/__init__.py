# -*- coding: utf-8 -*-
# Version: 0.2.1
# See github page to report issues or to contribute:
# https://github.com/c-okelly/org_to_anki

# Anki Imports => with try catch for testing
try:
    # import the main window object (mw) from aqt
    from aqt import mw
    # import the "show info" tool from utils.py
    from aqt.utils import showInfo
    # import all of the Qt GUI library
    from aqt.qt import *
    from aqt.importing import ImportDialog
    from .org_to_anki.main import parseAndUploadOrgFile
except:
    QAction = None
    mw = None
    pass

import traceback
import logging

errorTemplate = """
Hey there! It seems an error has occurred while running the importer.

The error was {}.

If you would like me to fix it please report it here: https://github.com/c-okelly/org_to_anki/issues

Please be sure to provide as much information as possible. Specifically the file the caused the error.
"""
def importNewFile():

    d = QFileDialog(mw)
    filePath = d.getOpenFileName()[0]
    if len(filePath) == 0:
        showInfo("No file selected")
        return
        
    ## Do real main
    try:
        parseAndUploadOrgFile(filePath, embedded=True)
    
    except TypeError as e:
        error = "The file that was selected for upload is not either an org, txt, html or htm file. Path was {}"
        showInfo(error.format(filePath))
    
    except FileNotFoundError as e:
        error = "The file {} as not found. Please double check the path is correct."
        showInfo(error.format(filePath))

    # General exception
    except Exception as e:
        errorMessage = str(e)
        trace = traceback.format_exc()
        showInfo(errorTemplate.format(errorMessage))



if (QAction != None and mw != None):
    # create a new menu item, "test"
    action = QAction("Import list into Anki cards", mw)
    # set it to call testFunction when it's clicked
    action.triggered.connect(importNewFile)
    # and add it to the tools menu
    mw.form.menuTools.addAction(action)