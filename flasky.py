from app import create_app
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


# with app.app_context():
#     # cache.clear()


if __name__ == "__main__":
    # app.run(debug=True)
    # app.run()
    app.run(host="127.0.0.1", port="5001", debug=True)
