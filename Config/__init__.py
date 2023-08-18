import json
import os

from Utils.Singleton import Singleton
from Utils.DotDict import DotDict


class Config(DotDict, metaclass=Singleton):
    """
    Класс экземпляра конфигурации (Singleton)
    """

    def __init__(self):
        config_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(config_dir, 'config.json')
        local_config_path = os.path.join(config_dir, 'config.local.json')
        self.config_path = local_config_path if os.path.exists(local_config_path) else config_path
        config_data = self.read_config(self.config_path)
        super().__init__(DotDict(config_data))

        self._host = self.rest_config.host
        self._username = self.rest_config.user.username
        self._password = self.rest_config.user.password

    @staticmethod
    def read_config(config_path: str) -> dict:
        """
        Метод чтения файла конфигурации
        :param config_path: - путь до файла конфигурации
        :return: - json
        """
        with open(config_path) as file:
            config_data = json.load(file)
        return config_data

    def rewrite_config(self):
        """
        Перезаписывает содержимое текущего экземпляра Config в json файл, определяющий Config
        """
        with open(self.config_path, 'w') as file:
            file.write(json.dumps(self))

    @property
    def host(self) -> DotDict:
        """
        Свойство возвращает элемент словаря с данными удаленного хоста
        :return: DotDict
        """
        return self._host

    @property
    def username(self) -> DotDict:
        """
        Свойство возвращает элемент словаря с именем учетной записи пользователя на удаленном хосте
        :return: DotDict
        """
        return self._username

    @username.setter
    def username(self, value: str):
        self._username = value

    @property
    def password(self) -> DotDict:
        """
        Свойство возвращает элемент словаря с паролем к имени учетной записи пользователя на удаленном хосте
        :return: DotDict
        """
        return self._password

    @password.setter
    def password(self, value: str):
        self._password = value
