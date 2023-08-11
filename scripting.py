#!/usr/bin/python3

import os
import subprocess
import sys

def install_environment():
    try:
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
    pass
   
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
        version_info = subprocess.run(['mysql', '--version'], capture_output=True)
        print(f"{version_info.stdout[:17]} was installed successfully.")
    except Exception as e:
        print(f"Pip install failed.")
        print(str(e))

def check_requirements():
    #check Python version 
    if sys.version_info.major < 3:
        print(f"Your Python version {sys.version_info.major} does not meet the requirements. Please install Python 3.7.2 or higher")
    if sys.version_info.minor < 7:
        print(f"Your Python version {sys.version_info.major} + '.' + {sys.version_info.minor} does not meet the requirements. Please install Python 3.7.2 or higher")
    if sys.version_info.minor >= 7:
        version_info = subprocess.run(['python3', '--version'], capture_output=True)
        print(str(version_info.stdout) + 'already installed and meet the requirements')

    #check PIP install
    try:
        version_info = subprocess.run(["pip", "--version"])
        print("Pip is already installed on your system.")
    except:
        print("Pip was not found on your system. It will be install now: ")
        install_pip()

    #check MySql version
    try:
        version_info = subprocess.run(['mysql', '--version'], capture_output=True)
        if 'mysql  Ver 8' not in version_info.stdout:
            print("Mysql 8 will be installed now: ")
            install_mysql()
    except:
        print("Mysql was not found on your system. It will be installed now")
        install_mysql()

check_requirements()
install_environment()
