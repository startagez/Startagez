from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

    db.init_app(app)
    login_manager.init_app(app)

    from auth import auth_bp
    from stories import stories_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(stories_bp)

    @app.route("/")
    def index():
        from models import Story
        stories = Story.query.all()
        return render_template("index.html", stories=stories)

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
