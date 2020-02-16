from app import create_app, db, cache
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

with app.app_context():
    cache.clear()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="3000", debug=True)
