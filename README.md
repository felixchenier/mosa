![logo](../logo/logo_standard_light_small.png)

Laboratoire de recherche en mobilité et sport adapté
====================================================

This module and resources are dedicated for the Mobility and Adaptive
Sports Research Lab in Montreal. While this code is open and is free to be
shared, it is developed for our own private use.

If you are looking for other code by our lab, you may be happy with these
public packages:

- [Kinetics Toolkit](https://github.com/felixchenier/kineticstoolkit)
- [Limited Interaction](https://github.com/felixchenier/limitedinteraction)


Installation de Python et des packages utilisés par le laboratoire
------------------------------------------------------------------

1. Installer [miniconda](https://docs.conda.io/en/latest/miniconda.html)

2. Dans un terminal (Terminal sur macOS, Anaconda shell (bash) sur Windows):

    - conda create -n mosa python=3.8
    - conda activate mosa
    - pip install git+https://github.com/felixchenier/mosa
    - python -c "import mosa; mosa.install()"

3. Sur Windows, on peut alors démarrer Spyder à partir de son icône. Sur macOS, dans un terminal:

    - conda activate mosa
    - spyder

4. Pour faire les mises à jour, à partir d'un terminal (e.g., console Spyder):

    - import mosa
    - mosa.update()
    - Il peut être nécessaire de redémarrer Spyder après une mise à jour.


Procédures de laboratoire
----------------------------------------

- [Coding Style](procedures/coding_style.md)
- [Communication et suivi de tâches avec Trello](procedures/trello.md)

