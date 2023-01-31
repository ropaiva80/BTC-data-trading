:: https://stackoverflow.com/questions/62984477/running-python-scripts-in-anaconda-environment-through-windows-cmd
:: call "<condapath>\Scripts\activate.bat" <env_name> & cd "<folder_for_your_py_script>" & python <scriptname.py> [<arguments>]

:: First - script2 - FBprophet (predict) for one year
call "C:\Users\ropai\anaconda3\Scripts\activate.bat" Python3.7_Env-GluonTS_off_1h_simple & cd "C:\Python\Crypto\Script2\Scratch\BTC\1H_Close" & python Script2_BTC_COINBASE_HOURLY-Autots_GluonTS-1H_OFF_Simple-30D.py