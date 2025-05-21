import logging
import os

from .session_controller import session_controller
from .models import Base


class DBManager:
    root_dir = 'database'

    @staticmethod
    def __default_db_name() -> str:
        return 'database.db'

    def start_app(self) -> bool:
        try:
            db_file_name = self.__default_db_name()

            db_path = os.path.abspath(os.path.join(self.root_dir, db_file_name))

            if os.path.isfile(db_path):
                session_controller.set_session(db_path)

            else:
                engine = session_controller.set_session(db_path)
                Base.metadata.create_all(bind=engine)

            return True

        except Exception as exp:
            logging.error(f'Не удалось запустить БД-менеджер: {exp}')
            return False
    

