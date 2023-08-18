#!/usr/bin/python3

import os
import subprocess
import sys
import re
import json



def load_data_mysql(mysql_user):
    subprocess.run(["sudo", "mysql", "-u", mysql_user, "-p", "<", "simple-django-project/world.sql"], shell=True)

def modify_settings(mysql_user, mysql_password, mysql_host, mysql_port, email_host, email_host_password):

    # Temporarily add the directory containing settings.py to sys.path
    sys.path.append('simple-django-project/panorbit/')

    import settings

    # Remove the temporarily added path from sys.path
    sys.path.remove('simple-django-project/panorbit/')

    # Modify the DATABASES dictionary
    settings.DATABASES['default']['USER'] = mysql_user
    settings.DATABASES['default']['PASSWORD'] = mysql_password
    settings.DATABASES['default']['HOST'] = mysql_host
    settings.DATABASES['default']['PORT'] = mysql_port
    settings.EMAIL_HOST = email_host
    settings.EMAIL_HOST_PASSWORD = email_host_password

    def replace_database_config(file_path, db_data, email_host, email_host_password):

        with open(file_path, 'r') as file:
            content = file.read()
        # Use regex to match and replace the 'DATABASES' section
        content = re.sub(r'DATABASES\s*=\s*{(?:[^{}]*{[^{}]*}[^{}]*)*}', db_data, content, flags=re.DOTALL)

        # Use regex to match and replace 'EMAIL_HOST'
        content = re.sub(r'EMAIL_HOST\s*=\s*\'[^\']+\'', f'EMAIL_HOST = \'{email_host}\'', content)

        # Use regex to match and replace 'EMAIL_HOST_PASSWORD'
        content = re.sub(r'EMAIL_HOST_PASSWORD\s*=\s*\'[^\']+\'', f'EMAIL_HOST_PASSWORD = \'{email_host_password}\'', content)


        with open(file_path, 'w') as file:
            file.write(content)

    # Usage
    file_path = 'simple-django-project/panorbit/settings.py'
    data_bases_settings = str(json.dumps(settings.DATABASES, indent = 4))

    db_data = 'DATABASES = ' + data_bases_settings  # Replace with the desired content
    email_host = str(settings.EMAIL_HOST)
    email_host_password = str(settings.EMAIL_HOST_PASSWORD)

    replace_database_config(file_path, db_data, email_host, email_host_password)

def install_environment():
    try:
        subprocess.run(["python3", "-m", "venv", "myvenv"])
        git_path = "https://github.com/Manisha-Bayya/simple-django-project.git"
        subprocess.run(["git", "clone", git_path])
        status = subprocess.run(["pip", "install", "-r", "requirements.txt"], capture_output=True, text=True)
        if status.returncode == 0:
            print("Virtual environment installed successfully.")
        else:
            print(f"Virtual environment not installed. Error {status.stderr}")
    except Exception as e:
        print("Something gone wrong.")
        print(str(e))

def install_python():
    try:
        subprocess.run(['mkdir', 'temp'])
        subprocess.run(['cd', 'temp'])
        subprocess.run(['wget', 'https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz'])
        subprocess.run(['tar', '-xvf', 'Python-3.7.2.tgz'])
        subprocess.run(['rm', '-rf', 'Python-3.7.2.tgz'])
        subprocess.run(['cd', 'Python-3.7.2'])
        subprocess.run(['./configure'])
        subprocess.run(['make'])
        subprocess.run(['sudo', 'make', 'install']) 
        print("Python 3.7.2 was installed successfully.")
    except Exception as e:
        print(f"Python 3.7.2 install failed...")
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
        subprocess.run(['sudo', 'apt', 'install', 'mysql-server', 'mysql-client', '-y'])
        mysql_status = subprocess.run(['systemctl', 'is-active', 'mysql'], capture_output=True)
        if 'active' not in mysql_status.stdout:
            subprocess.run(['sudo', 'systemctl', 'start', 'mysql'])
        else:
            version_info = subprocess.run(['mysql', '--version'], capture_output=True, text=True)
            print(f"{version_info.stdout[:17]} was installed successfully.")
    except Exception as e:
        print(f"Mysql 8 install failed.")
        print(str(e))

def check_requirements():
    #check Python version 
    if sys.version_info.major < 3:
        print(f"Your Python version {sys.version_info.major} does not meet the requirements.\nPython 3.7.2 will be installed now : ")
        install_python()
    if sys.version_info.minor < 7:
        print(f"Your Python version {sys.version_info.major} + '.' + {sys.version_info.minor} does not meet the requirements.\nPython 3.7.2 will be installed now : ")
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
    try:
        version_info = subprocess.run(['mysql', '--version'], capture_output=True, text=True)
        if 'mysql  Ver 8' in version_info.stdout:
            print(f"{version_info.stdout[:17]} already installed." )
        else:
            print("Mysql 8 will be install now: ")
            install_mysql()
    except:
        print("Mysql was not found on your system. It will be install now: ")
        install_mysql()

def main():
    check_requirements()
    install_environment()
    mysql_user = input("Plese enter your user name for Mysql DB: ")
    load_data_mysql(mysql_user)
    mysql_password = input("Plese enter password for Mysql DB: ")
    mysql_host = input("Plese enter host for Mysql DB: ")
    mysql_port = input("Plese enter port for Mysql DB: ")
    email_host = input("Plese enter email host for Mysql DB: ")
    email_host_password = input("Plese enter email host password for Mysql DB: ")
    modify_settings(mysql_user, mysql_password, mysql_host, mysql_port, email_host, email_host_password)

if __name__ == "__main__":
    main()
