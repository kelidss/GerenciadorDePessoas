import os
from dotenv import load_dotenv
from pathlib import Path
from flask import Flask
from flask_cors import CORS

dotenv_path = Path("../.env").absolute()
load_dotenv(dotenv_path=dotenv_path)

from models import db

class Config:
    """Classe de configuração do Flask."""
    
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('DB_CONNECTION')}:5432/{os.getenv('POSTGRES_DB')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    def __str__(self):
        return f"SQLALCHEMY_DATABASE_URI: {self.SQLALCHEMY_DATABASE_URI}"

class CreateApp:
    """Classe responsável por inicializar e configurar o aplicativo Flask."""
    
    def __init__(self):
        """Inicializa a configuração do aplicativo."""
        self.app = Flask(__name__)
        self.app.config.from_object(Config)
        db.init_app(self.app)
        CORS(self.app)

    def _register_routes(self):
        """Registra as rotas do aplicativo."""
        from routes import routes
        routes.Routes(self.app)

    def _create_tables(self):
        """Cria tabelas no banco de dados."""
        with self.app.app_context():
            try:
                from models.person import Person
                from models.child import Child
                db.create_all()
                print("Tabelas criadas com sucesso.")
            except Exception as e:
                print(f"Erro ao criar tabelas: {e}")

    def get_app(self):
        """Configura e retorna o aplicativo Flask."""
        self._create_tables()
        self._register_routes()
        return self.app

class StartApp:
    """Classe responsável por inicializar o aplicativo Flask."""    
    def __init__(self):
        self.app = CreateApp().get_app()

    def run(self):
        self.app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    StartApp().run()
