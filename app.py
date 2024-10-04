# app.py
from flask import Flask, jsonify, request, render_template
from config import Config
from models import db, bcrypt, User
from routes.auth import auth_bp
from routes.protected import protected_bp
from routes.user_profile import user_profile_bp
from routes.email_verification import email_verification_bp
from routes.password_reset import password_reset_bp
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

mail = Mail(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(protected_bp, url_prefix='/protected')
app.register_blueprint(user_profile_bp, url_prefix='/user_profile')
app.register_blueprint(email_verification_bp, url_prefix='/email_verification')
app.register_blueprint(password_reset_bp, url_prefix='/password_reset')

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == "__main__":
    app.run(debug=True)
