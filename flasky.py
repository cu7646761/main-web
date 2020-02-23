from app import create_app
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# with app.app_context():
#     # cache.clear()

if __name__ == "__main__":
    app.run(host="localhost", port="5000", debug=True)
