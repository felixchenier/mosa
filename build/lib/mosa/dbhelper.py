#!/usr/local/bin/python3
import tkinter as tk
import sys
import platform
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path
import subprocess # Pour faire des appels systèmes (shell)
import os


CONST_VERSION = 1.4

# Historique
# 1.4 Correction d'un bogue dans find_files sur Windows : il manquant le n après le dbfixXXX.

#----------------------
# Wrappers vers tkinter
#----------------------

def uigetfilename():
	root = tk.Tk()
	root.iconify()
	# Make it almost invisible - no decorations, 0 size, top left corner.
	root.overrideredirect(True)
	root.geometry('0x0+0+0')
	# Show window again and lift it to top so it can get focus,
	# otherwise dialogs will end up behind the terminal.
	root.deiconify()
	root.lift()
	root.call('wm', 'attributes', '.', '-topmost', '1')
	root.focus_force()
	file_path = filedialog.askopenfilename(parent=root)
	root.destroy()
	return(file_path)

def uimessagebox(message):
	root = tk.Tk()
	root.withdraw()	
	# Make it almost invisible - no decorations, 0 size, top left corner.
	root.overrideredirect(True)
	root.geometry('0x0+0+0')	
	# Show window again and lift it to top so it can get focus,
	# otherwise dialogs will end up behind the terminal.
	root.deiconify()
	root.lift()
	root.call('wm', 'attributes', '.', '-topmost', '1')
	root.focus_force()
	messagebox.showinfo('dbhelper', message, parent=root)
	root.destroy()

#----------------------
# Commands (chaque commande retourne 0 si elle s'est bien déroulée, 1 sinon.
#----------------------

#----------------------
# require_version
#		Utilisé pour s'assurer que dbhelper est au moins la version demandée.
#		Retourne 0 si c'est le cas, 1 sinon.
def require_version(version):
	if (version > CONST_VERSION):
		uimessagebox("Votre version de dbhelper n'est pas à jour.")
		return 1
	return 0

#----------------------
# rename_file
#		Lance une boîte de dialogue pour choisir le fichier à renommer, puis renomme le
#		fichier pour y inclure le dbfidXXXXn.
def rename_file(id):
	filename = uigetfilename()
	print(filename)
	if len(filename) == 0:
		uimessagebox("Action annulée.")
		return 1

	# Vérifier si ce fichier contient déjà la chaîne dbfid
	if ('dbfid' in filename):
		uimessagebox("Ce fichier contient déjà la chaîne de caractères 'dbfid'. N'est-il pas déjà ajouté à la banque de données ?\n\nAction annulée.")
		return 1
	
	base, ext = os.path.splitext(filename)
	# Ajouter la chaîne de caractères
	newname = base + '_dbfid' + str(id) + 'n' + ext
	print(newname)
	os.rename(filename, newname)
	uimessagebox("Le fichier:\n" + filename + "\na été renommé:\n" + newname + "\n\nNe pas oublier de déposer ce fichier sur un serveur de données ou sur Dropbox, si ce n'est pas déjà fait.")
	return 0

#----------------------
# message
#		Écrit un message dans une boîte de dialogue.
def message(value):
	uimessagebox(value)
	return 0

#----------------------
# find_file
#		Affiche une fenêtre Explorer ou Finder avec le(s) fichier(s) trouvé(s) pour un ID
#		spécifié.
def find_file(value):
	# S'assurer que la valeur est un nombre (sécurité pour les subprocess.call)
	try:
		float(value)
	except ValueError:
		return 1

	if platform.system() == "Darwin":
		searchString = "mdfind -name dbfid" + value + "n | grep -v /Library/ -m 1"
		try:
			firstOccurence = subprocess.check_output(searchString, shell=True)
			firstOccurence = firstOccurence.decode() # Convertir vers un string
			firstOccurence = firstOccurence.rstrip() # Enlever le \n
			appleScript = 'tell application "Finder" to reveal the POSIX file "' + firstOccurence + '"'
			appleScript = appleScript.rstrip() #Retirer le \n
			subprocess.call(["osascript", '-e tell application "Finder" to activate'])
			subprocess.call(["osascript", "-e " + appleScript])
			return 0
		except:
			uimessagebox("Ce fichier n'a pas été trouvé sur votre ordinateur.")
			return 1

	elif platform.system() == "Windows":
		searchString = 'search-ms:query="*dbfid' + value + 'n*"'
		subprocess.call("start " + searchString, shell=True)
		return 0
	
	else:
		uimessagebox("Seuls Windows et Mac supportent cette fonction.")
		return 1
	


def parsecommand(command, value):
	if (command == 'require_version'):
		return(require_version(float(value)))
	elif (command == 'rename_file'):
		return(rename_file(value))
	elif (command == 'message'):
		return(message(value))
	elif (command == 'find_file'):
		return(find_file(value))	
	else:
		uimessagebox("Commande inconnue: " + command)
		return 1

#----------------------
# Main
#----------------------

#uimessagebox(str(sys.argv))

# Vérifier s'il y a un argument, sinon montrer la boîte d'information
if (len(sys.argv) <= 1):
	uimessagebox("dbhelper v" + str(CONST_VERSION) + "\n\n(C) Félix Chénier, 2016-2017\n\nCette application est conçue pour gérer les fichiers de la base de données biomec.uqam.ca")
	sys.exit()

# Open and parse command file
# Each command in the file must be in the form "command value"
# No blank line, no extra space.
fileName = str(sys.argv[1])
print(fileName)
f = open(fileName, 'r')
for line in f:
	splittedLine = line.split('=')
	command = splittedLine[0]
	value = splittedLine[1]
	value = value.rstrip()
	print(command)
	print(value)
	if parsecommand(command, value):
                break
	
f.close()
os.remove(fileName);
print('dbhelper end')
