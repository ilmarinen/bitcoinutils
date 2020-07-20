# bitcoinutils

## Installation

1. `python3 -m venv venv`
2. `pip install -r requirements.txt`
3. With venv activated `python setup.py develop`
4. `npm install`
5. `npx webpack`


## Database Setup and Migrations

1. `FLASK_APP=tracker.py flask db upgrade`
2. `FLASK_APP=tracker.py flask generate-fixtures`

## Start the Server

1. `FLASK_APP=tracker.py flask run -h 0.0.0.0 -p 5000`


## Development

If you need to make a migration do:

1. `FLASK_APP=tracker.py flask db migrate -m "Description ..."`
2. `FLASK_APP=tracker.py flask db upgrade`

To have Webpack run and watch for changes do:

1. `npx webpack --watch`


## Deployment

The following command will generate the config files needed to set this up on a server.

1. `FLASK_APP=tracker.py flask generate-deployment-configs --host tracker.zay.io --application-root /var/www/tracker/code/bitcoinutils`
2. Follow the printed out instructions
