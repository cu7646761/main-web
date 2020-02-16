from mongoengine import disconnect
from selenium import webdriver
from flasky import app
from app import db, create_app
import threading
from wsgiref import simple_server
from wsgiref.simple_server import WSGIRequestHandler


def before_all(context):
    print("Executing before all")
    disconnect(alias='default')
    context.app = create_app('testing')
    context.app_context = context.app.app_context()
    context.app_context.push()
    # db.drop_all()
    # db.create_all()
    context.server = simple_server.WSGIServer(("", 8000), WSGIRequestHandler)
    context.server.set_app(context.app)
    context.pa_app = threading.Thread(target=context.server.serve_forever)
    context.pa_app.start()
    context.url = "http://localhost:8000"
    context.client = context.app.test_client(use_cookies=True)
    context.browser = webdriver.Chrome('dependencies/chromedriver')
    context.browser.maximize_window()
    context.browser.implicitly_wait(20)


def before_feature(context, feature):
    print("Before feature\n")


# Scenario level objects are popped off context when scenario exits
def before_scenario(context, scenario):
    print("Before scenario\n")


def after_scenario(context, scenario):
    print("After scenario\n")


def after_feature(context, feature):
    print("\nAfter feature")


def after_all(context):
    print("Executing after all")
    context.browser.quit()
    context.server.shutdown()
    context.pa_app.join()
    




