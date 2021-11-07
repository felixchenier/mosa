from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
import sys
import limitedinteraction as li
import urllib.parse as parse
import subprocess
import mosa
import os
import threading


biomec_url = 'https://felixchenier.uqam.ca/biomec/interface'
window_title = "Laboratoire de recherche en mobilité et sport adapté - Banque de données"


# creating main window class
class MainWindow(QMainWindow):

    # constructor
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # creating a QWebEngineView
        self.browser = QWebEngineView()

        # Set window title
        title = self.browser.page().title()
        self.setWindowTitle(window_title)

        # setting default browser url as google
        self.browser.setUrl(QUrl(biomec_url))

        # adding action when url get changed
        self.browser.urlChanged.connect(self.scan_new_url)

        # # adding action when loading is finished
        # self.browser.loadFinished.connect(self.update_title)

        # set this browser as central widget or main window
        self.setCentralWidget(self.browser)

        # creating a status bar object
        self.status = QStatusBar()

        # adding status bar to the main window
        self.setStatusBar(self.status)

        # creating QToolBar for navigation
        navtb = QToolBar("Navigation")

        # adding this tool bar tot he main window
        self.addToolBar(navtb)

        # adding actions to the tool bar
        # creating a action for back
        back_btn = QAction("Back", self)

        # setting status tip
        back_btn.setStatusTip("Back to previous page")

        # adding action to the back button
        # making browser go back
        back_btn.triggered.connect(self.browser.back)

        # adding this action to tool bar
        navtb.addAction(back_btn)

        # similarly for forward action
        next_btn = QAction("Forward", self)
        next_btn.setStatusTip("Forward to next page")

        # adding action to the next button
        # making browser go forward
        next_btn.triggered.connect(self.browser.forward)
        navtb.addAction(next_btn)

        # similarly for reload action
        reload_btn = QAction("Refresh", self)
        reload_btn.setStatusTip("Refresh page")

        # adding action to the reload button
        # making browser to reload
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        # showing all the components
        self.showMaximized()
        self.show()

    # method called by the home action
    def navigate_home(self):
        # open the google
        self.browser.setUrl(QUrl("http://www.google.com"))

    # method for scanning the url for tasks
    def scan_new_url(self, q):
        q = q.toString()
        query = parse.parse_qs(parse.urlsplit(q).query)

        if 'command' in query:

            if query['command'][0] == 'find_file':
                thread = threading.Thread(
                    target=find_file,
                    args=(query['value'][0], )
                )
                thread.start()
                self.browser.back()

            elif query['command'][0] == 'rename_file':
                thread = threading.Thread(
                    target=rename_file,
                    args=(query['value'][0], )
                )
                thread.start()
                self.browser.back()


#-------------------------
# BIOMEC related functions
#-------------------------

def find_file(value: str) -> bool:
    """
    Find a file in the system explorer.

    value: str corresponding to the dbfid (just the int part).
    returns True if the file was found, and False otherwise.
    """

    # Ensure that the id is a number.
    try:
        float(value)
    except ValueError:
        return False

    if mosa._is_mac:
        searchString = "mdfind -name dbfid" + value + "n | grep -v /Library/ -m 1"
        try:
            firstOccurence = subprocess.check_output(searchString, shell=True)
            firstOccurence = firstOccurence.decode() # Convertir vers un string
            firstOccurence = firstOccurence.rstrip() # Enlever le \n
            appleScript = (
                'tell application "Finder" to reveal the POSIX file "'
                + firstOccurence
                + '"')
            appleScript = appleScript.rstrip() #Retirer le \n
            subprocess.call([
                "osascript",
                '-e tell application "Finder" to activate'
            ])
            subprocess.call(["osascript", "-e " + appleScript])
            return True
        except:
            li.button_dialog(
                "This file was not found on your computer.",
                ['OK'],
            )
            return False

    elif mosa._is_pc:
        searchString = 'search-ms:query="*dbfid' + value + 'n*"'
        subprocess.call("start " + searchString, shell=True)
        return True

    else:
        li.button_dialog(
            "Only Windows and macOS are supported at the moment.",
            ['OK']
        )
        return 1


def rename_file(file_id: str) -> bool:
    """
    Rename file to include dbfid in file name.

    file_id: file id as a string that contains only a number.
    returns True if the file was renamed, False otherwise.
    """
    filename = li.get_filename()
    if len(filename) == 0:
        return False

    if ('dbfid' in filename):
        li.button_dialog(
            ("This file already contains a `dbfid` part.\n"
             "I won't rename this file.\n"
             "If you are sure that the file must be renamed,\n"
             "please first remove its `dbfid` part manually."),
            ['Cancel']
        )
        return False

    base, ext = os.path.splitext(filename)
    newname = base + '_dbfid' + str(file_id) + 'n' + ext

    os.rename(filename, newname)

    li.button_dialog(
        f"File\n{filename}\nwas renamed to\n{newname}",
        ['OK']
    )
    return True


# creating a pyQt5 application
app = QApplication(sys.argv)

# setting name to the application
app.setApplicationName(window_title)

# creating a main window object
window = MainWindow()

# loop
app.exec_()