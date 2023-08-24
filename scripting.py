#!/usr/bin/python3

import os
import subprocess
import sys
import re
import json


def check_mysql_permissions(mysql_user):
    permission_to_mysql = subprocess.run(["mysql", "-u", f"{mysql_user} -p"], capture_output=True, shell=True)
    if permission_to_mysql.stderr == 0:
        print(f"Your user {mysql_user} have access to Mysql.")
    else:
        print(f"Access denied to Mysql for {mysql_user}.")

    pass
def run_server():
    subprocess.run(["python simple-django-project/manage.py makemigrations"], shell=True)
    subprocess.run(["python simple-django-project/manage.py migrate"], shell=True)
    subprocess.run(["python simple-django-project/manage.py rebuild_index"], shell=True)
    subprocess.run(["python simple-django-project/manage.py runserver 0:8001"], shell=True)
    print("Your server is up on port 8001")

#def load_data_mysql():
    #subprocess.run(["sudo", "mysql_secure_installation"])
   
    #subprocess.run(["mysql -u root -p"], shell=True)
    #mysql_user = 'bob'
    #mysql_password = 'P@ssword123'
    #mysql_queries = [
    #        f"CREATE USER '{mysql_user}'@'localhost' IDENTIFIED BY '{mysql_password}';",
    #        f"GRANT ALL PRIVILEGES ON world.* TO '{mysql_user}'@'localhost';",
    #        f"FLUSH PRIVILEGES;"
    #        ]
    
    #for command in mysql_queries:
    #    subprocess.run([f'mysql -u root -p -e {command}'], shell=True) 
    
def modify_settings(mysql_user, mysql_password, mysql_host, mysql_port, email_host_user, email_host_password):

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
    settings.EMAIL_HOST_USER = email_host_user
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
        subprocess.run(["python", "-m", "venv", "new_venv"])
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
        subprocess.run(['sudo', 'apt', 'install', 'python-pip'])
        print("Pip was installed successfully.")
    except Exception as e:
        print(f"Pip install failed...")
        print(str(e))

def install_mysql():
    try:
        subprocess.run(['sudo', 'apt', 'update'])
        subprocess.run(['sudo', 'apt', 'install', 'mysql-server', '-y'])
        mysql_status = subprocess.run(['systemctl', 'is-active', 'mysql'], capture_output=True)
        if mysql_status.stdout != 'active':
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
    check_mysql_permissions(mysql_user)
    #load_data_mysql()
    mysql_password = input("Plese enter password for Mysql DB: ")
    mysql_host = input("Plese enter host for Mysql DB: ")
    mysql_port = input("Plese enter port for Mysql DB: ")
    email_host_user = input("Plese enter email host for Mysql DB: ")
    email_host_password = input("Plese enter email host password for Mysql DB: ")
    modify_settings(mysql_user, mysql_password, mysql_host, mysql_port, email_host_user, email_host_password)
    run_server()

if __name__ == "__main__":
    main()
