:: https://stackoverflow.com/questions/62984477/running-python-scripts-in-anaconda-environment-through-windows-cmd
:: call "<condapath>\Scripts\activate.bat" <env_name> & cd "<folder_for_your_py_script>" & python <scriptname.py> [<arguments>]

:: First - script2 - FBprophet + Statsmodels + GluonTS for one year
call "C:\Users\ropai\anaconda3\Scripts\activate.bat" Python3.8_Env-GluonTS_on_1h_simple & cd "C:\Python\Crypto\Script2\Scratch\BTC\1H_Close" & python Script_Report_BTC_1H.py