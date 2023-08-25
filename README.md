## Project Setup Guide

Before using the script, you'll need to install the required dependencies:

- Python 3.7.2
- Pip
- MySQL 8 (create a user and grant necessary permissions)
- Git

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

Run scripting.py:

```sh
~ python3 scripting.py
or
~ ./scripting.py
```

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
```
