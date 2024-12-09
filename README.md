# backend
The backend side of HospiCare

## Idiots(me included xD)' guide
For fedora users install these:
```sh
sudo dnf install mysql mysql-devel python3-devel pkgconf
```


To setup virtuel environment:
- on linux
	```bash
	python3 -m venv .venv
	source .venv/bin/activate # for bash
    source .venv/bin/activate.fish # for fish users :)
	pip install -r requirements.txt
	```
- on windows (come on use linux!)
	```sh
	python -m venv .venv
	Set-ExecutionPolicy RemoteSigned # run on Powershell as administrator in case of activate fail 
	.\.venv\Scripts\activate # for Cmd
	.\.venv\Scripts\Activate # for Powershell
	pip install -r requirements.txt
	```

To create the database and get the user and port values
```sql
mysql> CREATE DATABASE DATABASE_NAME;
mysql> select user();
mysql> show variables;
```

> Make sure to copy `sample.env` into `.env` and to give each field its value

To get the static files
```sh
python3 manage.py collectstatic --noinput
```

To create admin
```sh
python manage.py createsuperuser
```

Cool commands to not forget about
```sh
python manage.py makemigrations
python manage.py migrate
```

To build docs:
```sh
cd docs/
sphinx-apidoc -o . ..
make html
```

To run tests:
```sh
pytest
```

To run the dev server:
```sh
python3 -m uvicorn app.asgi:application --reload
```

> if something does't work debug it!
