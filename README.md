# CMX Battleship

## CMX Members
- William Morris [morriswa] morris.william@ku.edu
- Kevin Rivers
- Timothy Holmes [TimoHolmes] t338h273@home.ku.edu
- Makenna Loewenherz
- Rahul Bhattachan

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
- Setup PIP with morriswa-central repository (assumes AWS CLI is already configured with morriswa-developer credentials)

      aws codeartifact login --tool pip --domain morriswa-org --repository morriswa-central
- Install project dependencies with PIP

      pip install .
- Create local app environment file 'secrets.properties' in project root directory
- Include values in secrets.properties

      DB_HOST=host_here
      DB_NAME=database_name_here
      DB_USER=database_username_here
      DB_PASSWORD=database_password_here

- Setup development database

      ./src/manage.py migrate
- Run on local machine http://localhost:8000
      
      ./src/manage.py runserver
