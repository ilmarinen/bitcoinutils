# bitcoinutils

1. `FLASK_APP=tracker.py flask db upgrade`
2. `FLASK_APP=tracker.py flask generate-fixtures`
3. `FLASK_APP=tracker.py flask run -h 0.0.0.0 -p 5000`

If you need to make a migration do:

1. `FLASK_APP=tracker.py flask db migrate -m "Description ..."`
2. `FLASK_APP=tracker.py flask db upgrade`
