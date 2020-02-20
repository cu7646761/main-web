After install 1 package -> save name into requirements.txt
=======================================
 > pip freeze > requirements.txt

How to run server
=======================================
1. Access folder that contain run.py file
2. Custom config
    > export APP_SETTINGS=config.DevelopmentConfig
3. Install virtual env
    > virtualenv -p (address python3) venv <br>
     . venv/bin/activate <br>
     pip install -r requirements.txt
4. Start mongo db
5. Run server
    > python flasky.py <br>

How to run tdd test
=======================================
1. Access folder that contain run.py file
2. Run command
    > python manage.py test
    
How to run bdd test
=======================================
1. Access folder that contain run.py file
2. Run command
    > behave features/checkform.feature <br>
     behave features/checkfb.feature <br>
     behave features/checktw.feature

Work with github
=======================================
1. Link docs: https://docs.google.com/document/d/1dyJDHd9g7ZIg4bhdWCf1m3j3L5yI3tpefdt1XyxIaLY/edit
