# main.py
from flask import Flask, render_template, redirect, url_for
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.file_routes import file_bp
from routes.user_routes import user_bp
from routes.test_routes import test_bp
from config import db
from flask import send_from_directory
from config import Config

app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")
app.secret_key = 'salt'
app.config.from_object(Config)

# Registrar blueprints de autenticación y API del dashboard
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(dashboard_bp, url_prefix="/api") 
app.register_blueprint(file_bp, url_prefix="/api/files")
app.register_blueprint(user_bp, url_prefix="/api")
app.register_blueprint(test_bp, url_prefix='/api/test')

# Ruta para mostrar el formulario de inicio de sesión
@app.route('/login', methods=['GET'])
def login_page():
    if db.users.count_documents({}) == 0:
        return redirect(url_for('register_page'))
    return render_template('login.html')

# Ruta para el formulario de registro inicial
@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

# Ruta para el dashboard
@app.route('/dashboard', methods=['GET'])
def dashboard_page():
    return render_template('dashboard.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9000)