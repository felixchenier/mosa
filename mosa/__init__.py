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

try:
    from mosa.dbinterface import DBInterface
    from mosa import dev
except ModuleNotFoundError:
    pass


# Package list to install and keep to date from conda-forge
install_packages = [
    'python=3.8',
    'spyder=4',
]

packages = [
    'kineticstoolkit',
    'seaborn',
    'statsmodels',
    'ezc3d',
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
]


# Operating system
_is_pc = True if platform.system() == 'Windows' else False
_is_mac = True if platform.system() == 'Darwin' else False
_is_linux = True if platform.system() == 'Linux' else False

# Current folder
_root_folder = os.path.dirname(os.path.dirname(__file__))


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
    subprocess.call(['pip',
                     'install',
                     '--upgrade',
                     'git+https://github.com/felixchenier/mosa'])


def install() -> None:
    """Install lab's packages."""
    print("*******************************")
    print("UPDATING MOSA...")
    _update_mosa()
    print("*******************************")
    print("INSTALLING PACKAGES...")
    subprocess.call(['conda',
                     'install',
                     '-c',
                     'conda-forge',
                     *install_packages, *packages])


def update() -> None:
    """Update lab's packages."""
    print("*******************************")
    print("UPDATING MOSA...")
    _update_mosa()
    print("*******************************")
    print("INSTALLING NEW PACKAGES...")
    subprocess.call(['conda',
                     'install',
                     '-c',
                     'conda-forge',
                     *install_packages, *packages])
    print("*******************************")
    print("UPDATING PACKAGES...")
    subprocess.call(['conda',
                     'upgrade',
                     '-c',
                     'conda-forge',
                     *packages])

