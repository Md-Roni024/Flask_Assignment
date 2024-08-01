from flask import Flask, redirect, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# Define the Swagger UI configuration
SWAGGER_URL = '/swagger'
API_URL = '/static/openapi.yaml'  # URL for the Swagger file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "User Management API"}
)

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/')
def home():
    return redirect(SWAGGER_URL)  # Redirect to /swagger directly

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)
