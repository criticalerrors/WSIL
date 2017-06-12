# WSIL
***Index:***
 - [Requirements](#requirements)
 - [Setup WSIL](#installation)
 - [Usage](#usage)

## Requirements
WSIL is developed using [Python 3.6.1](http://www.python.it/).


## Installation
For running WSIL correctly, you have to install **Python 3.6.1** (or high).
For installing correctly all the requirements you have to install **pip 9.0.1** (or high).

### Setting the environment

Create, in the main project's directory, the python environment by running the following:

    $ virtualenv venv

Remember to set the python interpreter in your virtual envirorment `venv` as the project interpreter used by your IDE.

For more information about the package virtualenv, go [here](https://virtualenv.pypa.io/en/stable/). 

After this, you need to set the SECRET_VARIABLE environment variable in your OS.
### Install dependencies
Activate your virtual environment, then run the following command:
    
    $ pip install -r requirements.txt
or
    
    $ pip3 install -r requirements.txt
if you are on Linux.
### Deployment to Heroku
Connect your local version of the repository to heroku

    $ heroku git:remote -a wsilang

Then push your version

    $ git push heroku master

## Usage
### Running in local
In order to run the server, run in the main project's directory the following:

    $ python manage.py runserver <port>

or

    $ python3 manage.py runserver <port>

if you are on Linux.

If you don't specify the port, Django will use the default port 8000.