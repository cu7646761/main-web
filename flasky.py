from flask_mongo_sessions import MongoDBSessionInterface

from app import create_app, cache, db
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

with app.app_context():
    mongo_sess = db.connection[app.config['MONGODB_DB']]
    app.session_interface = MongoDBSessionInterface(app, mongo_sess, 'sessions')
    # cache.clear()

if __name__ == "__main__":
    app.run(host="localhost", port="5000", debug=True)
