#!/usr/bin/python3

import os
import subprocess


def install_python():
    pass

def install_pip():
    pass

def install_mysql():
    pass

def check_rquirements():
   #check Python version 
    version_info = os.popen('python3 --version 2>&1').read()
    if 'Python 3.7.2' not in version_info:
        print("Python 3.7.2 will be installed now: ")
        install_python()
    else:
        print("Python 3.7.2 is already installed.")

    #check PIP install
    version_info = os.system('pip --version')
    if version_info not 0:
        print("Pip will be installed now: ")
        install_pip()
    else:
        print("Pip is already installed")

    #check MySql version
    version_info = os.popen('mysql --version 2>&1').read()
    if 'Mysql-8.0.15' not in version_info:
        print("Mysql-8.0.15 will be installed now: ")
        install_mysql()
    else:
        print("Mysql-8.0.15 is already installed.")
            
                                                               

check_requirements()                                             
