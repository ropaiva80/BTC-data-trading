:: https://stackoverflow.com/questions/62984477/running-python-scripts-in-anaconda-environment-through-windows-cmd
:: call "<condapath>\Scripts\activate.bat" <env_name> & cd "<folder_for_your_py_script>" & python <scriptname.py> [<arguments>]

:: First - script1 - FBprophet (predict) for one year
call "C:\Users\ropai\anaconda3\Scripts\activate.bat" Python3.8_Env-GluonTS_on_1h_simple & cd "C:\Python\Crypto\Script1\Scratch" & python Script1_LPT-v2_fbphrophet-1Y.py