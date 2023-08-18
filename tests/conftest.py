import pytest
import requests as r

from os import linesep
from datetime import datetime
from Config import Config
from Helpers.requests_helper import TestTimeout
from Utils.RandomData import RandomData

# <editor-fold desc="CI/CD">
"""
Список параметров для CI/CD, которые возможно изменять `на лету` из командной строки запуска тестов
    Пример использования проброса параметров при запуске тестов:
    $ python -m pytest <имя папки с тестами> --<параметр1>=<value1> --<параметр2>=<value2>
"""
PARAMS = (
    'username',
    'password',
)


def pytest_addoption(parser):
    """
    Метод проброса в тестовую сессию pytest параметров из строки команды запуска
    Пример использования:
        $ python -m pytest <имя папки с тестами> --<параметр1>=<value1> --<параметр2>=<value2>
    Help:
        Подсказку по доступным для проброса параметрам можно увидеть после первого запуска тестовой сессии pytest
            - формируется динамически из папки __pycache__
            - в списке доступных опций появится секция [Custom options]
                $ python -m pytest --help
    Зависимости:
        для работы метода необходимо определить:
         - кортеж пробрасываемых констант PARAMS ()
         - в фикстуре config(request) переназначить пробрасываемые параметры в цикле:
           value = request.config.getoption(f'--{param}')

    :param parser: экземпляр служебного класса Parser
    """

    for param in PARAMS:
        prefix = f"если не задан параметр '--{param}', по умолчанию используется из Config файла проекта"
        parser.addoption(f'--{param}', action="store", default=None, help=f'{prefix}')


@pytest.fixture(scope='session')
def config(request) -> Config:
    """
    Фикстура инициализации Config с возможностью пробросить параметры из строки команды запуска pytest

    :param request: служебная фикстура pytest
    :return: экземпляр (Singleton) DotDict словаря с конфигурационными данными
    """

    config = Config()

    for param in PARAMS:
        value = request.config.getoption(f'--{param}')
        if value and param == 'username':
            config.username = value
        elif value and param == 'password':
            config.password = value

    return config


# </editor-fold desc="CI/CD">

@pytest.fixture(scope='session', name='test_data')
def preconditions_teardown(config: Config, faker):
    """
    Фикстура выполняет следующие действия:
    preconditions:
        - Создает тестовые данные/объекты
        - Возвращает текущие тестовые данные/объекты тестовому классу
    teardown:
        - Очищает созданные тестами сущности

    :param config: фикстура инициализации config
    :param faker: фикстура подготовки случайных данных
    :return: параметризированную функцию, которая может быть вызвана непосредственно в теле теста или другой фикстуры
    """

    teardown_params = []
    query_data = {}

    def _preconditions_teardown(pool):

        username = config.username
        password = config.password
        host = config.host
        resource = f'v{host.version}/{host.resource}'
        test_url = f'{host.protocol}://{host.ip}/{resource}' if host.port is None else (
            f'{host.protocol}://{host.ip}:{host.port}/{resource}')
        headers = {'Content-type': 'application/json'}
        query_data['url'] = test_url
        query_data['auth'] = (username, password)
        query_data['headers'] = headers
        query_data['timeout'] = TestTimeout()

        setup_query = query_data.copy()
        setup_query['url'] += 's'

        result = r.get(**setup_query)

        if result.status_code == 200:
            now = datetime.now().strftime("%H:%M:%S")
            print(f"{linesep}{now}: Количество записей в БД: {len(result.json()['result'])}")
            if 490 <= len(result.json()['result']) <= 500:
                setup_query['url'] = setup_query['url'].partition('characters')[0] + 'reset'
                r.post(**setup_query)
        else:
            raise NotImplementedError(
                'Логин неуспешен или URL неверен: проверьте данные в config'
                f'{linesep}ErrorMessage:{linesep}{result.text}'
                f'{linesep}{result.request} {result.status_code} {result.url}'
                f'{linesep}{query_data}'
                f'{linesep}{result.request.headers}'
            )

        test_names = []
        for _ in range(pool):
            test_names.append(faker.fwords(uuid=True))

        teardown_params.append(test_names)

        return {
            "query_data": query_data,
            "test_names": test_names,
        }

    yield _preconditions_teardown

    teardown_params = [_ for __ in teardown_params for _ in __]

    print(f"Список ключей 'name' для созданных тестами временных записей:{linesep}")

    for teardown_param in teardown_params:
        print(f'\t"{teardown_param}"')
        query_data["params"] = f'name={teardown_param}'

        r.delete(**query_data)
        res = r.get(**query_data)

        assert res.status_code == 400
        assert res.json()['error'] == "No such name"


@pytest.fixture(scope='session')
def faker():
    """
    Фикстура инициализации генератора случайных данных

    :return: экземпляр (Singleton) RandomData
    """
    return RandomData()


@pytest.fixture(scope='function')
def overflow_db(test_data, faker):
    """
    Фикстура для проверки переполнения БД:
        - делает количество записей в БД = 500

    :param test_data: базовая фикстура setup/teardown
    :param faker: фикстура подготовки случайных данных
    """

    data = test_data(0)
    query_data_1_character = data['query_data']
    query_data_2_characters = query_data_1_character.copy()
    query_data_2_characters['url'] += 's'

    res = r.get(**query_data_2_characters)

    count = len(res.json()['result'])
    while count < 500:
        query_data_1_character['json'] = {"name": faker.fwords()}
        r.post(**query_data_1_character)
        count += 1


@pytest.fixture(scope="session")
def reset_db(test_data):
    """
    Фикстура подготовки коллекции в БД как условие для идемпотентной проверки тестовых данных:
        - фикстура сбрасывает состояние данных на исходное

    :param test_data: базовая фикстура setup/teardown
    :return: одноименную функцию, которая может быть вызвана непосредственно в теле теста или другой фикстуры
    """

    def _reset_db():
        data = test_data(0)
        reset = data['query_data'].copy()
        reset['url'] = reset['url'].partition('character')[0] + 'reset'
        r.post(**reset)

    return _reset_db
