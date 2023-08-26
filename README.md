## This is a README file for a script that installs and configures a Django project.

### How to use
To use the script, first you need to install the dependencies:

- Python 3.7.2
- Pip
- MySQL 8 (create a user and grant necessary permissions)
- Git
- Pexpect 4.8.0 (module for Python)

### Python 3.7.2

1. Download Python 3.7.2 from the [official source](https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz):
   
   ```sh
   ~ wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz
   ```

2. Extract it:

   ```sh
   ~ tar -xvf Python-3.7.2.tgz
   ```

3. Install it:

   ```sh
   ~ cd Python-3.7.2
   ~ ./configure
   ~ sudo make install
   ~ python3 --version
   ```

### Pip for Python 3.7.2

1. Download `get-pip.py` from the [official source](https://bootstrap.pypa.io/get-pip.py):

   ```sh
   ~ wget https://bootstrap.pypa.io/get-pip.py
   ```

2. Install it:

   ```sh
   ~ python3 get-pip.py
   ~ pip3 --version
   ```
   
### Pexpect 4.8.0

Install Pexpect:
   ```sh
   ~ pip install pexpect
   ~ pip show pexpect 
   ```

### Git

Install Git:

```sh
~ sudo apt install git
~ git --version
```

### MySQL 8.*

1. Install MySQL:

   ```sh
   ~ sudo apt install mysql-server
   ~ sudo mysql_secure_installation
   ```

2. Set root password in MySQL and create a user with database access:

   ```sh
   ~ sudo mysql
   ```
   
   Inside MySQL:
   
   ```sql
   ~ ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password';
   ~ CREATE USER 'user_name'@'localhost' IDENTIFIED BY 'your_password';
   ~ GRANT SELECT, INSERT, UPDATE, DELETE, EXECUTE, USAGE ON world.* TO 'user_name'@'localhost';
   ~ FLUSH PRIVILEGES;
   ~ EXIT;
   ```

3. After cloning the [repository](https://github.com/Manisha-Bayya/simple-django-project.git), download `world.sql` to MySQL:

   ```sh
   ~ git clone https://github.com/Manisha-Bayya/simple-django-project.git
   ~ mysql -u ubuntu -p -v < simple-django-project/world.sql
   ~ mysql -u ubuntu -p
   ```

   Inside MySQL:
   
   ```sql
   ~ USE world;
   ~ EXIT;
   ```
   
## Run script

Once the dependencies are installed, you can run the script by running the following command:

```sh
~ python3 scripting.py
or
~ ./scripting.py
```

The script will then install the Django project and configure it with the given settings.

## Settings

The script takes the following settings as input:

* `mysql_user`: The username for the MySQL database.
* `mysql_password`: The password for the MySQL database.
* `mysql_host`: The hostname of the MySQL database.
* `mysql_port`: The port of the MySQL database.
* `email_host_user`: The username for the email server.
* `email_host_password`: The password for the email server.

This will install the Django project and configure it with the given settings.

## Troubleshooting

### Error when installing mysqlclient==1.4.2.post1

```sh
~ sudo apt install libmysqlclient-dev
```

### Could not build wheels for et-xmlfile, mysqlclient, openpyxl, pycparser

```sh
~ pip install --upgrade setuptools wheel
```

### Downloading databses to mysql

```sh
~ mysql -u <mysql-user> -p -v < simple-django-project/world.sql
```

### Error with a mix of tabs and spaces

1. Edit the file `simple-django-project/world/models.py` using your preferred text editor.

2. Go to line 63 and check the indentation. You may find a mix of tabs and spaces.

3. Convert all tabs to spaces.

## License

The script is licensed under the MIT License.

## Author

The script was written by [Artem Ushenko] for DevOps01 courses.
