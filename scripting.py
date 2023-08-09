#!/usr/local/bin/python3

import os
import subprocess
import sys


def install_environment():
    try:
        subprocess.run(['sudo', 'pip', 'install', 'virtualenv'])
        os.mkdir('envs')
        subprocess.run(['virtualenv', './envs/'])
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
    if sys.version_info.major < 3:
        subprocess.run(['wget', 'https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz'])
        subprocess.run(['tar', '-xvf', 'Python-3.7.2.tgz'])
        os.chdir('Python-3.7.2')
        subprocess.run(['./configure'])
        subprocess.run(['make'])
        subprocess.run(['sudo', 'make', 'install'])
        version_info = subprocess.run(['python3','--version'], stdout=subprocess.PIPE, universal_newlines=True)
        print(version_info.stdout + 'was installed successfully')
    elif sys.version_info.minor < 7:
        subprocess.run(['sudo', 'apt', 'remove', 'python3'])
        subprocess.run(['sudo', 'apt', 'autoremove'])
        subprocess.run(['sudo', 'apt', 'autoclean'])
        subprocess.run(['wget', 'https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz'])
        subprocess.run(['tar', '-xvf', 'Python-3.7.2.tgz'])
        os.chdir('Python-3.7.2')
        subprocess.run(['./configure'])
        subprocess.run(['make'])
        subprocess.run(['sudo', 'make', 'install'])
        version_info = subprocess.run(['python3','--version'], stdout=subprocess.PIPE, universal_newlines=True)
        print(version_info.stdout + 'was installed successfully')

def install_pip():
    result = subprocess.run(['sudo', 'apt', 'install', 'python-pip'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if result.returncode == 0:
        return (print("The command completed successfully."))
    else:
        return (print(f"The command failed with error code: {result.returncode}"))

def install_mysql():
    subprocess.run(['wget', 'https://dev.mysql.com/get/mysql-apt-config_0.8.15-1_all.deb'])
    subprocess.run(['sudo', 'dpkg', '-i', 'mysql-apt-config_0.8.15-1_all.deb'])
    subprocess.run(['sudo', 'apt', 'update'])
    subprocess.run(['sudo', 'apt', 'install', 'mysql-server'])
    return 'OK'

def check_requirements():
   #check Python version 
    version_info = os.popen('python3.7 --version 2>&1').read()
    if 'Python 3.7.2' not in version_info:
        print("Python 3.7.2 will be installed now: ")
        install_python()
    else:
        print("Python 3.7.2 is already installed.")

    #check PIP install
    version_info = os.system('pip --version')
    if version_info != 0:
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
install_environment()
