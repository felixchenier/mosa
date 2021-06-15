Laboratoire de recherche en mobilité et sport adapté
====================================================

This module provides functions and classes for the Mobility and Adaptive
Sports Research Lab in Montreal. While this code is open and is free to be
shared, it is developed for our own private use.

If you are looking for other code by our lab, you may be happy with these
public packages:

- [Kinetics Toolkit](https://github.com/felixchenier/kineticstoolkit)
- [Limited Interaction](https://github.com/felixchenier/limitedinteraction)

----------------------------------------

Installing MOSA to configure lab's and students' computers:

1. Install [miniconda](https://docs.conda.io/en/latest/miniconda.html)
2. In a terminal - Terminal on macOS, Anaconda shell (bash) on Windows:
    - conda create -n mosa python=3.8
    - conda activate mosa
    - pip install git+https://github.com/felixchenier/mosa
    - python -c "import mosa; mosa.install()"
3. Spyder can then be started using its icon on Windows, or on macOS:
    - conda activate mosa
    - spyder

To keep the lab's packages up to date, from a python interpreter:
    - import mosa
    - mosa.update()

----------------------------------------

Reference to the lab's [coding style](coding_style/coding_style.md)
