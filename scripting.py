#!/usr/bin/python3

import os
import subprocess


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
    pass

def install_pip():
    result = subprocess.run(['sudo', 'apt', 'install', 'python-pip'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if result.returncode == 0:
        return (print("The command completed successfully."))
    else:
        return (print(f"The command failed with error code: {result.returncode}"))

def install_mysql():
    try:
        subprocess.run(['wget', 'https://dev.mysql.com/get/mysql-apt-config_0.8.15-1_all.deb'])
        subprocess.run(['sudo', 'dpkg', '-i', 'mysql-apt-config_0.8.15-1_all.deb'])
        subprocess.run(['sudo', 'apt', 'update'])
        subprocess.run(['sudo', 'apt', 'install', 'mysql-server'])
        subprocess.run(['sudo', 'apt', 'install', '-f', 'mysql-client=8.0* mysql-community-server=8.0* mysql-server=8.0*'])
    except Exception as e:
        print("Something gone wrong.")
        print(str(e)) 

def check_requirements():
    #check linux disributor id
    version_info = os.popen('lsb_release -a 2>&1').read()
    if 'Ubuntu' or 'Debian' in version_info:
        #check Python version 
        version_info = os.popen('python3 --version 2>&1').read()
        if 'Python 3.7.2' not in version_info:
            print("Python 3.7.2 will be installed now: ")
            install_python()
        else:
            print("Python 3.7.2 is already installed.")

        #check PIP install
        version_info = subprocess.run(['pip3',  '--version'])
        if version_info != 0:
            print("Pip will be installed now: ")
            install_pip()
        else:
            print("Pip is already installed")

        #check MySql version
        version_info = subprocess.run(['mysql', '--version', '2>&1'], stdout=subprocess.PIPE, text=True)
        if 'Mysql-8.0.15' not in version_info.stdout:
            print("Mysql-8.0.15 will be installed now: ")
            install_mysql()
        else:
            print("Mysql-8.0.15 is already installed.")
    else:
        print("Please install ans use Linux Ubuntu/Debian distribution")

#check_requirements()          
#install_environment()

install_mysql()
