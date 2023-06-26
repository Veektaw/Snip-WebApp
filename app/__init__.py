from .snipe import create_app
from flask import session
from datetime import timedelta



app = create_app()

@app.before_request
def refresh_session():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=7)

if __name__ == "__main__":
    app.run(debug=True)