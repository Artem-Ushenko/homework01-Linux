#!/usr/bin/python3

import os
import subprocess
import sys

def install_environment():
    try:
        subprocess.run(['pip', 'install', '--upgrade', 'setuptools'])
        subprocess.run(['pip', 'install', 'lxml']) 
        subprocess.run(['sudo', 'pip', 'install', 'virtualenv'])
        subprocess.run(["mkdir", "envs"])
        subprocess.run(['virtualenv', './envs/'])
        subprocess.run(["source", "envs/bin/activate"], shell=True)
        git_path = "https://github.com/Manisha-Bayya/simple-django-project.git"
        subprocess.run(['git', 'clone', git_path])
        os.chdir('simple-django-project')
        venv_path = "../envs/bin/"
        subprocess.run([venv_path + "pip", "install", "-r", "requirements.txt"])
        print("Virtual environment installed successfully.")
    except Exception as e:
        print("Something gone wrong.")
        print(str(e))

def install_python():
    try:
        if sys.version_info.minor < 7:
            subprocess.run(['mkdir', 'temp'])
            subprocess.run(['cd', 'temp'])
            subprocess.run(['wget', 'https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz'])
            subprocess.run(['tar', '-xvf', 'Python-3.7.2.tgz'])
            subprocess.run(['cd', 'Python-3.7.2.tgz'])
            subprocess.run(['./configure'])
            subprocess.run(['make'])
            subprocess.run(['sudo', 'make', 'install']) 
        else:
            subprocess.run(['sudo', 'apt', 'update'])
            subprocess.run(['sudo', 'apt', 'install', 'python3'])
            print("Python 3 was installed successfully.")
    except Exception as e:
        print(f"Python 3 install failed...")
        print(str(e))
   
def install_pip():
    try:
        subprocess.run(['sudo', 'apt', 'update'])
        subprocess.run(['sudo', 'apt', 'install', 'python3-pip'])
        print("Pip was installed successfully.")
    except Exception as e:
        print(f"Pip install failed...")
        print(str(e))

def install_mysql():
    try:
        subprocess.run(['sudo', 'apt', 'update'])
        subprocess.run(['sudo', 'apt', 'install', 'mysql-server'])
        version_info = subprocess.run(['mysql', '--version'], capture_output=True, text=True)
        print(f"{version_info.stdout[:17]} was installed successfully.")
    except Exception as e:
        print(f"Mysql 8 install failed.")
        print(str(e))

def check_requirements():
    #check Python version 
    if sys.version_info.major < 3:
        print(f"Your Python version {sys.version_info.major} does not meet the requirements.\nPython 3 will be installed now : ")
        install_python()
    if sys.version_info.minor < 7:
        print(f"Your Python version {sys.version_info.major} + '.' + {sys.version_info.minor} does not meet the requirements.\nPython 3 will be installed now : ")
        install_python()
    if sys.version_info.minor >= 7:
        version_info = subprocess.run(['python3', '--version'], capture_output=True)
        print(f"{version_info.stdout} already installed and meet the requirements")

    #check PIP install
    try:
        version_info = subprocess.run(["pip", "--version"])
        print("Pip is already installed on your system.")
    except:
        print("Pip was not found on your system. It will be install now: ")
        install_pip()

    #check MySql version
    version_info = subprocess.run(['mysql', '--version'], capture_output=True, text=True)
    if 'mysql  Ver 8' in version_info.stdout:
        print(f"{version_info.stdout[:17]} already installed." )

check_requirements()
install_environment()
