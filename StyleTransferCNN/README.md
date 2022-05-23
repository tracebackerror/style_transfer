# styletransfer

_**Before going to start make sure that you have installed python3 on your system. if not, download and install from below link**_
https://www.python.org/downloads/

For First Time Run, Follow Instructions Given Below :-
***Open Command Prompt or Terminal And Type Below Commands Sequencially***

1. Install all dependency which is required for this project
 - pip install -r requirements.txt

2. If you are windows users install VC_redist.x86.exe or VC_redist.x64.exe based on your system requirement

note : you can skip step-3 you have *db.sqlite3* file on this project
3. create migrations and migrate them
 - python manage.py makemigrations
 - python manage.py migrate

4. for run this project, finally type below command in cmd
 - python manage.py runserver

