from flask import Flask, request, jsonify
from flask_limiter import Limiter
import jwt
import datetime

from logger import setup_logger
from models import User
from database import db
from api import api
from flask import render_template

# Настройка логгера
logger = setup_logger()

app = Flask(__name__)

# Импорт конфигураций
app.config.from_object('config')

# Инициализация экземпляра db
db.init_app(app)

# Инициализация Flask-Limiter
limiter = Limiter(
    app,
    default_limits=["200 per day", "50 per hour"]  # Ограничения по умолчанию
)

# Регистрация Blueprint
app.register_blueprint(api, url_prefix='/api')


@app.route('/ui', methods=['GET'])
def ui():
    return render_template('index.html')


# Функция для создания токена
def create_token(username):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    payload = {"username": username, "exp": expiration_time}
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256").decode("utf-8")


# Функция для декодирования токена
def decode_token(token):
    try:
        return jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])["username"]
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


@limiter.limit("5 per minute")  # Ограничение для этого конкретного маршрута
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    logger.info(f"Login attempt: {username}")

    # Здесь должна быть проверка username и password, но для примера пропустим
    if username == "admin" and password == "password":
        token = create_token(username)
        return jsonify({"token": token}), 200
    else:
        return "Unauthorized", 401


@limiter.limit("5 per minute")
@app.route('/', methods=['GET'])
def home():
    token = request.headers.get("Authorization")
    username = decode_token(token)

    if username:
        name = request.args.get('name', 'World')
        message = request.args.get('message', 'No message')

        user = User.query.filter_by(username=name).first()
        if not user:
            user = User(username=name, message=message)
            db.session.add(user)
        else:
            user.message = message

        db.session.commit()

        return f'Hello {name}!\n{message}!', 200
    else:
        return "Unauthorized", 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
