"""Development functions for mosa module."""

import subprocess
import mosa
import os
import shutil


def build() -> None:
    """Build the mosa module in a pip-accessible format."""
    # Bump version number
    with open(mosa._root_folder + '/mosa/VERSION', 'r') as fh:
        version = fh.read()
    with open(mosa._root_folder + '/mosa/VERSION', 'w') as fh:
        fh.write(f'{float(version) + 0.1:.2}')

    os.chdir(mosa._root_folder)

    subprocess.call(['python',
                     'setup.py',
                     'sdist',
                     'bdist_wheel'])


def run_unit_tests() -> None:  # pragma: no cover
    """Run all unit tests."""
    # Run pytest in another process to ensure that the workspace is and stays
    # clean, and all Matplotlib windows are closed correctly after the tests.
    print('Running unit tests...')

    cwd = os.getcwd()
    os.chdir(mosa._root_folder + '/tests')
    subprocess.call(['coverage', 'run',
                     '--source', '../mosa',
                     '-m', 'pytest', '--ignore=interactive'])
    subprocess.call(['coverage', 'html'])
    mosa.webbrowser.open_new_tab(
        'file://'
        + mosa._root_folder
        + '/tests/htmlcov/index.html')
    os.chdir(cwd)
