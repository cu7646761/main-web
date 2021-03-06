After install 1 package -> save name into requirements.txt
=======================================
 > pip freeze > requirements.txt

Upgrade all packages in project
=======================================
 > pip install -r requirements.txt --upgrade

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
5. Config .env file, run command in terminal project directory
    > cp .env.example .env <br>
    Then change the value of API_KEY
6. Create Index, go to mongo command
    > db.store.createIndex({ classification: 1 })
7. Run server
    > python flasky.py <br>

How to run tdd test
=======================================
1. Convert to testing config
    > export FLASK_CONFIG='testing'
2. Run command
    > python manage.py test
                  
How to run generate_data
=======================================
1. Access folder that contain gen.py file
2. Run command
    > python gen.py <br>

3. (Development) To generate fake classification, Run command
    > python gen_classify.py <br>

Work with github
=======================================
1. Link docs: https://docs.google.com/document/d/1dyJDHd9g7ZIg4bhdWCf1m3j3L5yI3tpefdt1XyxIaLY/edit

How to config mail with sendgrid email
=======================================
1. Steps <br>
1.1. echo "export SENDGRID_API_KEY='this is private'" > sendgrid.env <br>
1.2. echo "sendgrid.env" >> .gitignore <br>
1.3. source ./sendgrid.env <br>
