@echo off

cd /d C:\Users\Adarsh Priyadarshi\Techies

call venv\Scripts\activate

start http://127.0.0.1:8000

python manage.py runserver

pause