call %HOMEPATH%\miniconda3\Scripts\activate.bat
call conda create -y -n mosa -c conda-forge python=3.8 git pip limitedinteraction
call %HOMEPATH%\miniconda3\Scripts\deactivate.bat

call %HOMEPATH%\miniconda3\Scripts\activate.bat mosa
pip install git+https://github.com/felixchenier/mosa
python -c "import mosa; mosa.install()"

python -c "import limitedinteraction as li; li.button_dialog('MOSA has been installed. Launch using mosa.bat', ['Nice'])"
