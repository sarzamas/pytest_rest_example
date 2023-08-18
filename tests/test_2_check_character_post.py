import pytest
import requests as r


@pytest.mark.post
class TestCheckCharacterPost:
    TEARDOWN_NAMES_POOl = 3

    @pytest.fixture(scope='class', name='data')
    def current_test_data(self, test_data, faker):
        """
        Фикстура подготовки общих данных для выполнения этого класса тестов
        TEARDOWN_NAMES_POOl: количество используемых этим классом тестов слотов для параметра 'test_names'
        Все тестовые сущности созданные в тестах как POST с именами {'name': ...} взятыми из слотов 'test_names'
        будут автоматически очищены из базы при teardown

        :param test_data: базовая фикстура подготовки данных для выполнения всех тестов класса
        :param faker: фикстура подготовки случайных данных
        """

        current_test_data = test_data(self.TEARDOWN_NAMES_POOl)
        current_test_data['payload'] = {
            "other_aliases": faker.fwords(),
            "universe": faker.fwords(),
            "identity": faker.fwords(nb=5),
            "education": faker.fwords(nb=5),
            "height": faker.int(),
            "weight": faker.int(),
        }

        return current_test_data

    def test_post_character_positive(self, data):
        """
        Тест проверки метода:
            POST /character
            - HTTP 200 - запрос с валидными данными в JSON (все параметры)

        :param data: фикстура подготовки тестовых данных для этого класса тестов
        """

        query_data = data['query_data'].copy()
        query_data['params'] = f"name={data['test_names'][0]}"
        query_data['json'] = data['payload'].copy()
        query_data['json']['name'] = data['test_names'][0]

        res = r.post(**query_data)

        assert res.status_code == 200
        assert len(res.json()) == 1
        assert 'result' in res.json()
        assert res.json()['result'] == query_data['json']

        res = r.get(**query_data)

        assert res.json()['result'] == query_data['json']

    def test_post_character_positive2(self, data):
        """
        Тест проверки метода:
            POST /character
            - HTTP 200 - запрос с валидными данными в JSON (min число параметров - 'name')

        :param data: фикстура подготовки тестовых данных для этого класса тестов
        """

        query_data = data['query_data'].copy()
        query_data['params'] = f"name={data['test_names'][1]}"
        query_data['json'] = {"name": data['test_names'][1]}

        res = r.post(**query_data)

        assert res.status_code == 200
        assert len(res.json()) == 1
        assert 'result' in res.json()
        assert res.json()['result'] == query_data['json']

        res = r.get(**query_data)

        assert res.json()['result'] == query_data['json']

    def test_post_character_negative(self, data):
        """
        Тест проверки метода:
            POST /character
            - HTTP 400 - проверка идемпотентности (запрет дублирования записи с пересечением по 'name')

        :param data: фикстура подготовки тестовых данных для этого класса тестов
        """
        query_data = data['query_data'].copy()
        query_data['params'] = f"name={data['test_names'][2]}"
        query_data['json'] = {"name": data['test_names'][2]}

        r.post(**query_data)
        res = r.post(**query_data)

        assert res.status_code == 400
        assert len(res.json()) == 1
        assert 'error' in res.json()
        assert res.json()['error'] == f"{query_data['json']['name']} is already exists"

    def test_post_character_negative2(self, data, faker):
        """
        Тест проверки метода:
            POST /character
            - HTTP 400 - запрос с валидными JSON но с отсутствием -H 'Content-type: application/json'

        :param data: фикстура подготовки тестовых данных для этого класса тестов
        :param faker: фикстура подготовки случайных данных
        """

        query_data = data['query_data'].copy()
        query_data['headers']['Content-type'] = 'text/html; charset=UTF-8'
        query_data['json'] = {"name": faker.fwords()}

        res = r.post(**query_data)

        assert res.status_code == 400
        assert len(res.json()) == 1
        assert 'error' in res.json()
        assert res.json()['error'] == "_schema: ['Invalid input type.']"

        query_data['headers']['Content-type'] = 'application/json'

    def test_post_character_negative3(self, data, faker):
        """
        Тест проверки метода:
            POST /character
            - HTTP 400 - запрос с невалидными JSON в блоке данных

        :param data: фикстура подготовки тестовых данных для этого класса тестов
        :param faker: фикстура подготовки случайных данных
        """

        query_data = data['query_data'].copy()
        query_data['json'] = faker.fwords(nb=1000)

        res = r.post(**query_data)

        assert res.status_code == 400
        assert len(res.json()) == 1
        assert 'error' in res.json()
        assert res.json()['error'] == "_schema: ['Invalid input type.']"

    def test_post_character_negative4(self, data):
        """
        Тест проверки метода:
            POST /character
            - HTTP 400 - отсутствие в запросе обязательного поля - 'name'

        :param data: фикстура подготовки тестовых данных для этого класса тестов
        """

        query_data = data['query_data'].copy()
        query_data['json'] = data['payload'].copy()

        res = r.post(**query_data)

        assert res.status_code == 400
        assert len(res.json()) == 1
        assert 'error' in res.json()
        assert res.json()['error'] == "name: ['Missing data for required field.']"

    def test_post_character_negative5(self, data):
        """
        Тест проверки метода:
            POST /character
            - HTTP 400 - пустой JSON {}

        :param data: фикстура подготовки тестовых данных для этого класса тестов
        """
        query_data = data['query_data'].copy()

        res = r.post(**query_data)

        assert res.status_code == 400
        assert len(res.json()) == 1
        assert 'error' in res.json()
        assert res.json()['error'] == 'Payload must be a valid json'

    def test_post_character_negative6(self, data, faker):
        """
        Тест проверки метода:
            POST /character
            - HTTP 400 - неверный тип данных - int <-> str

        :param data: фикстура подготовки тестовых данных для этого класса тестов
        :param faker: фикстура подготовки случайных данных
        """

        query_data = data['query_data'].copy()
        query_data['json'] = {
            "name": faker.int(),
            "other_aliases": faker.int(),
            "universe": faker.int(),
            "identity": faker.int(),
            "education": faker.int(),
            "height": faker.fwords(),
            "weight": faker.fwords(),
        }

        res = r.post(**query_data)

        assert res.status_code == 400
        assert len(res.json()) == 1
        assert 'error' in res.json()

        sample_to_compare = {
            "name: ['Not a valid string.']",
            "other_aliases: ['Not a valid string.']",
            "universe: ['Not a valid string.']",
            "identity: ['Not a valid string.']",
            "education: ['Not a valid string.']",
            "height: ['Not a valid number.']",
            "weight: ['Not a valid number.']",
        }

        sample_from_json = set([item.lstrip(' ') for item in res.json()['error'].split(',')])

        assert sample_to_compare == sample_from_json

    @pytest.mark.skip
    @pytest.mark.reset
    def test_post_character_negative7(self, data, faker, overflow_db, reset_db):
        """
        Тест проверки метода:
            POST /character
        Проверка переполнения БД:
            - количество записей в БД = 500
            - HTTP 400 - при следующем запросе POST /character

        :param data: фикстура подготовки тестовых данных для этого класса тестов
        :param overflow_db: фикстура создания количества записей в БД = 500
        :param reset_db: фикстура сброса базы в исходное состояние
        :param faker: фикстура подготовки случайных данных
        """

        query_data = data['query_data'].copy()
        query_data['json'] = {"name": faker.fwords()}

        res = r.post(**query_data)

        assert res.status_code == 400
        assert len(res.json()) == 1
        assert 'error' in res.json()
        assert res.json()['error'] == "Collection can't contain more than 500 items"

        reset_db()
