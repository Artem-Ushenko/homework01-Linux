#!/usr/local/bin/python3

import os
import subprocess
import sys
import re
import json
import pexpect

#Function check privileges for database
def check_mysql_permissions(mysql_password, mysql_user):
    try:
        #Load db world.sql to Mysql
        mysql_queries = pexpect.spawn(f"mysql -u {mysql_user} -p -v < simple-django-project/world.sql")
        mysql_queries.expect('Enter password:')
        mysql_queries.sendline(f'{mysql_password}')
        mysql_queries = pexpect.spawn(f"mysql -u {mysql_user} -p")
        mysql_queries.expect('[>#]')
        check_err.sendline('USE world;')
        mysql_queries.expect('[>#]')
        mysql_queries.sendline('EXIT')
        
        #Check access to db world.sql
        check_err = pexpect.spawn("mysql world -p")
        check_err.expect('Enter password:')
        check_err.sendline(f'{mysql_password}')
        check_err.expect('[>#]')
        check_err.sendline('EXIT')
    except Exception as e:
        raise Exception("Something has gone wrong. Please use README.md to install all needed tools.") from e
        exit()

#Function is run a server
def run_server():
    try:
        subprocess.run(["python3 simple-django-project/manage.py makemigrations"], shell=True)
        subprocess.run(["python3 simple-django-project/manage.py migrate"], shell=True)
        subprocess.run(["python3 simple-django-project/manage.py rebuild_index"], shell=True)
        subprocess.run(["python3 simple-django-project/manage.py runserver 0:8001"], shell=True)
        print("Your server is up on port 8001")
    except Exception as e:
        print("Something gone wrong. Please use README.md to install all needed tools.")
        print(str(e))
        exit()
   
#Function add information about user to simple-django-project/panorbit/settings.py
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

#Function is create a virtual environment
def install_environment():
    try:
        subprocess.run(["pip", "install", "virtualenv"])
        subprocess.run(["python3", "-m", "virtualenv", "envs"])
        git_path = "https://github.com/Manisha-Bayya/simple-django-project.git"
        subprocess.run(["git", "clone", git_path])
        status = subprocess.run(["pip", "install", "-r", "simple-django-project/requirements.txt"], capture_output=True, text=True)
        if status.returncode == 0:
            print("Virtual environment installed successfully.")
        else:
            print(f"Virtual environment not installed. Error {status.stderr}. Please use README.md to install all needed tools.")
            exit()
    except Exception as e:
        print("Something gone wrong. Please use README.md to install all needed tools.")
        print(str(e))
        exit()

#Function is check all needed tools for use
def check_requirements():
    
    #check Python version 
    try: 
        if sys.version_info.major < 3:
            print(f"Your Python version {sys.version_info.major} does not meet the requirements. Please use README.md to install all needed tools.")
            exit()
        if sys.version_info.minor < 7:
            print(f"Your Python version {sys.version_info.major} + '.' + {sys.version_info.minor} does not meet the requirements. Please use README.md to install all needed tools.")
            exit() 
        if sys.version_info.major == 3 and sys.version_info.minor == 7:
            version_info = subprocess.run(['python3', '--version'], capture_output=True)
            print(f"{version_info.stdout} already installed and meet the requirements")
    except Exception as e:
        print("Something gone wrong. Please use README.md to install all needed tools.")
        print(str(e))  
        exit()

    #check PIP install
    try:
        version_info = subprocess.run(["pip", "--version"])
        print("Pip is already installed on your system.")
    except:
        print("Pip was not found on your system. Please use README.md to install all needed tools.")
        exit()
    #check MySql version
    try:
        version_info = subprocess.run(['mysql', '--version'], capture_output=True, text=True)
        if 'mysql  Ver 8' in version_info.stdout:
            print(f"{version_info.stdout[:17]} already installed." )
        else:
            print(f"Your {version_info.stdout[:17]} does not meet the requirements. Please use README.md to install all needed tools.")
            exit() 
    except:
        print("Mysql was not found on your system. Please use README.md to install all needed tools.")
        exit()

def main():
    check_requirements()
    install_environment()
    
    mysql_user = input("Plese enter your user name for Mysql DB: ")
    mysql_password = input("Plese enter password for Mysql DB: ")
    mysql_host = input("Plese enter host for Mysql DB: ")
    mysql_port = input("Plese enter port for Mysql DB: ")
    
    email_host_user = input("Plese enter email host for Mysql DB: ")
    email_host_password = input("Plese enter email host password for Mysql DB: ")
    
    check_mysql_permissions(mysql_password, mysql_user)
    modify_settings(mysql_user, mysql_password, mysql_host, mysql_port, email_host_user, email_host_password)
    run_server()

if __name__ == "__main__":
    main()
