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

Utilisation du package MOSA pour configurer un ordinateur du laboratoire :

1. Installer [miniconda](https://docs.conda.io/en/latest/miniconda.html)
2. Dans un terminal (Terminal sur macOS, Anaconda bash sur Windows) :
    - conda create -n mosa python=3.8
    - conda activate mosa
    - pip install git+https://github.com/felixchenier/mosa
    - python -c "import mosa; mosa.install()"
