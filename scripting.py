#!/usr/local/bin/python3
#!/home/ubuntu/homework01-Linux/envs/bin/python3


import pymysql
import os
import subprocess
import sys
import re
import json

#Function check privileges for database
def check_mysql_permissions(mysql_user, mysql_password, mysql_host):
    con = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db='world')
    result_list = []
    try: 
        with con:
            cur = con.cursor()
            cur.execute("SHOW GRANTS FOR 'ubuntu'@'localhost';")

            while True:
                next_row = cur.fetchone()
                if next_row:
                    result_list.append(next_row[0])
                else:
                    break

            has_all_privileges = any("GRANT ALL PRIVILEGES" in row for row in result_list)

            if has_all_privileges:
                print("You have all privileges for the 'world' database.")
            else:
                print("You do not have any privileges for the 'world' database.")
        except Exception as e:
            print("Something gone wrong. Please use README.md to install all needed tools.")
            print(str(e))
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
        status = subprocess.run(["pip", "install", "-r", "requirements.txt"], capture_output=True, text=True)
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
    if sys.version_info.major < 3:
        print(f"Your Python version {sys.version_info.major} does not meet the requirements. Please use README.md to install all needed tools.")
        exit()
    if sys.version_info.minor < 7:
        print(f"Your Python version {sys.version_info.major} + '.' + {sys.version_info.minor} does not meet the requirements. Please use README.md to install all needed tools.")
        exit() 
    if sys.version_info.major == 3 and sys.version_info.minor >= 7:
        version_info = subprocess.run(['python3', '--version'], capture_output=True)
        print(f"{version_info.stdout} already installed and meet the requirements")

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
    
    check_mysql_permissions(mysql_user, mysql_host, mysql_password)
    modify_settings(mysql_user, mysql_password, mysql_host, mysql_port, email_host_user, email_host_password)
    run_server()

if __name__ == "__main__":
    main()
