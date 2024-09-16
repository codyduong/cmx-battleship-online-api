# CMX Battleship

## Project Setup Guide
- Install python 3.12 https://www.python.org/downloads/
- Open project root directory in terminal
- Install project environment

      python3.12 -m venv .
      source bin/activate
    - NOTE: to deactivate project environment

          deactivate
    - NOTE: to reset project environment (macos, linux, powershell?)

          rm -rf bin include lib pyvenv.cfg
- Install project in development mode and dependencies with PIP 

      pip install -e .
- Create local app environment file 'secrets.properties' in project root directory
- Include values in secrets.properties

      DB_HOST=host_here
      DB_NAME=database_name_here
      DB_USER=database_username_here
      DB_PASSWORD=database_password_here
      SECRET_KEY=a_bunch_of_nonsense
- Setup development database

      ./src/manage.py migrate
- Run on local machine http://localhost:8000
      
      ./src/manage.py runserver

## Django Migrate Guide
please note all database scripts are located in src/core/migrations 
and all sql commands are stored in src/*/daos.py 

- Reset app database

      ./src/manage.py migrate core zero
- Migrate app database to specific version 
  (replace xxxx with migration code eg 0001, 0002, etc) 

      ./src/manage.py migrate core xxxx

- Migrate app database to latest version

      ./src/manage.py migrate 
