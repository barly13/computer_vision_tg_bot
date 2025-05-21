from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


class SessionController:
    def __init__(self):
        self.session = None
        self.engine = None

    def set_session(self, path):
        try:
            self.engine = create_engine(f'sqlite:///{path}')
            self.session = sessionmaker(bind=self.engine)()
            return self.session

        except Exception as exp:
            raise Exception(f'Не удалось изменить сессию. Укажите правильный путь до файла: {exp}')

    def get_session(self) -> Session:
        return self.session


session_controller = SessionController()