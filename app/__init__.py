from flask import Flask, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from celery import Celery
from config import Config
from flask_wtf.csrf import CSRFProtect
import click
from flask.cli import with_appcontext
import logging
import os


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)
csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate = Migrate(app, db)
    celery.conf.update(app.config)

    from app.utils.json_encoder import CustomJSONEncoder

    app.json_provider_class = CustomJSONEncoder

    from app.views import auth, projects, tools, workflows, main, settings

    app.register_blueprint(auth.bp)
    app.register_blueprint(projects.bp)
    app.register_blueprint(tools.bp)
    app.register_blueprint(workflows.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(settings.bp)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.errors import register_error_handlers

    register_error_handlers(app)

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return render_template('401.html'), 401

    @app.context_processor
    def override_url_for():
        return dict(url_for=versioned_url_for)

    def versioned_url_for(endpoint, **values):
        if endpoint == "static":
            filename = values.get("filename", None)
            if filename:
                file_path = os.path.join(app.root_path, endpoint, filename)
                values["v"] = int(os.stat(file_path).st_mtime)
        return url_for(endpoint, **values)

    with app.app_context():
        # Initialize or upgrade the database
        from flask_migrate import upgrade as db_upgrade

        try:
            db_upgrade()
        except:
            from flask_migrate import init as db_init, migrate as db_migrate

            db_init()
            db_migrate()
            db_upgrade()

        # Create admin user if not exists
        from app.models import User

        admin = User.query.filter_by(username="admin").first()
        if not admin:
            admin = User(username="admin", email="admin@example.com", role="admin")
            admin.password = "admin"  # Change this in production
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully.")

        print("Database initialized and up to date.")

    app.cli.add_command(init_db_command)

    return app


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()


def init_db():
    try:
        db.create_all()
        from app.models import User

        admin = User.query.filter_by(username="admin").first()
        if not admin:
            admin = User(username="admin", email="admin@example.com", role="admin")
            admin.password = "admin"  # You should change this in production
            db.session.add(admin)
            db.session.commit()
        click.echo("Database initialized successfully.")
    except Exception as e:
        click.echo(f"Error initializing database: {str(e)}")
        logging.error(f"Database initialization error: {str(e)}")
