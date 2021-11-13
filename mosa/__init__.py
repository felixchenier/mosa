#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Félix Chénier

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Laboratoire de recherche en mobilité et sport adapté
====================================================

This module provides functions and classes for the Mobility and Adaptive
Sports Research Lab in Montreal. While this code is open and is free to be
shared, it is developed for our own private use.

If you are looking for other code by our lab, you may be happy with these
public packages:

- Kinetics Toolkit (https://github.com/felixchenier/kineticstoolkit)

- Limited Interaction (https://github.com/felixchenier/limitedinteraction)

"""

__author__ = "Félix Chénier"
__copyright__ = "Copyright (C) 2021 Félix Chénier"
__email__ = "chenier.felix@uqam.ca"
__license__ = "Apache 2.0"


import os
import subprocess
import platform
import shutil
import webbrowser
import sys
import limitedinteraction as li


try:
    from mosa.dbinterface import DBInterface
    from mosa import dev
except ModuleNotFoundError:
    pass


# Packages with a specific version number
specific_versions = [
    'python=3.8',
    'tk=8.6.10',  # 8.6.11 has a title bar bug on macOS
]

# Packages to install and keep updated
packages = [
    'spyder',
    'ezc3d',
    'kineticstoolkit',
    'sphinx_rtd_theme',
    'seaborn',
    'statsmodels',
    'git',
    'pytest',
    'mypy',
    'coverage',
    'jupyterlab',
    'sphinx',
    'sphinx-material',
    'recommonmark',
    'sphinx-autodoc-typehints',
    'autodocsumm',
    'nbsphinx',
    'twine',
    'inflection',
    'ffmpeg',
    'openpyxl',  # Read Excel files with pandas
]


# Operating system
_is_pc = True if platform.system() == 'Windows' else False
_is_mac = True if platform.system() == 'Darwin' else False
_is_linux = True if platform.system() == 'Linux' else False

# Current folder
_root_folder = os.path.dirname(os.path.dirname(__file__))


def start_menu() -> None:
    """Run the start menu."""

    print(
        "---------------------------------------------------------\n"
        "Ne fermez cette fenêtre que lorsque vous aurez terminé de\n"
        "travailler avec les outils du laboratoire.\n"
        "---------------------------------------------------------"
    )

    choices = [
        ['Spyder', ['spyder']],
        ['Banque de données', [sys.executable,
                               _root_folder + '/mosa/browser.py']],
        ['Mise à jour des outils du laboratoire', [sys.executable,
                         '-c',
                         'import mosa; mosa.update()']],
        ['Quitter', 'quit']
    ]

    choice = li.button_dialog(
        'Laboratoire de recherche en mobilité et sport adapté',
        [choices[_][0] for _ in range(0, len(choices))],
    )
    if choice == -1 or choices[choice][1] == 'quit':
        pass
    else:
        subprocess.call(choices[choice][1])

    print("--- Vous pouvez maintenant fermer cette fenêtre ---")


def explore(folder_name: str = '') -> None:
    """
    Open an Explorer window (on Windows) or a Finder window (on macOS).

    Parameters
    ----------
    folder_name
        Optional. The name of the folder to open the window in. Default is the
        current folder.

    """
    if not folder_name:
        folder_name = os.getcwd()

    if _is_pc is True:
        os.system(f'start explorer {folder_name}')

    elif _is_mac is True:
        subprocess.call(['open', folder_name])

    else:
        raise NotImplementedError('This function is only implemented on'
                                  'Windows and macOS.')


def terminal(folder_name: str = '') -> None:
    """
    Open a terminal window.

    Parameters
    ----------
    folder_name
        The name of the folder to open the terminal window in. Default is the
        current folder.

    Returns
    -------
    None.
    """
    if not folder_name:
        folder_name = os.getcwd()

    if _is_pc is True:
        os.system(f'cmd /c start /D {folder_name} cmd')

    elif _is_mac is True:
        subprocess.call([
            'osascript',
            '-e',
            """tell application "Terminal" to do script "cd '""" +
            str(folder_name) + """'" """])
        subprocess.call([
            'osascript',
            '-e',
            'tell application "Terminal" to activate'])
    else:
        raise NotImplementedError('This function is only implemented on'
                                  'Windows and macOS.')


def _update_mosa() -> None:
    """Update mosa from github using pip."""
    subprocess.call(
        'pip install --upgrade git+https://github.com/felixchenier/mosa',
        shell=True
    )


def install() -> None:
    """Install lab's packages."""
    li.message("Installation du package mosa...\n")
    _update_mosa()

    li.message(
        "Téléchargement et installation des \n"
        "autres packages du laboratoire..."
    )
    s = 'conda install -y -c conda-forge '
    for _ in specific_versions:
        s += _
        s += ' '
    for _ in packages:
        s += _
        s += ' '
    subprocess.call(s, shell=True)
    li.message("")


def update() -> None:
    """Update lab's packages."""
    li.message("Mise à jour du package mosa...\n")
    _update_mosa()

    li.message(
        "Téléchargement et installation des \n"
        "nouveaux packages du laboratoire..."
    )
    s = 'conda install -y -c conda-forge '
    for _ in specific_versions:
        s += _
        s += ' '
    for _ in packages:
        s += _
        s += ' '
    subprocess.call(s, shell=True)

    li.message(
        "Téléchargement et mise à jour des \n"
        "autres packages du laboratoire..."
    )
    s = 'conda upgrade --all -y -c conda-forge '
    for _ in specific_versions:
        s += _
        s += ' '
    subprocess.call(s, shell=True)

    li.message("")
