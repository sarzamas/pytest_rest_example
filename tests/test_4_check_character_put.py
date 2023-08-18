import pytest
import requests as r


@pytest.mark.put
class TestCheckCharacterPut:
    TEARDOWN_NAMES_POOl = 1

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
        current_test_data['payload1'] = {
            "other_aliases": faker.fwords(),
            "universe": faker.fwords(),
            "identity": faker.fwords(nb=5),
            "education": faker.fwords(nb=5),
            "height": faker.int(),
            "weight": faker.int(),
        }
        current_test_data['payload2'] = {
            "other_aliases": faker.fwords(),
            "universe": faker.fwords(),
            "identity": faker.fwords(nb=5),
            "education": faker.fwords(nb=5),
            "height": faker.int(),
            "weight": faker.int(),
        }

        return current_test_data

    def test_put_character_positive(self, data):
        """
        Тест проверки метода:
            PUT /character
            - HTTP 200 - запись изменена (все параметры кроме 'name' изменены)

        :param data: фикстура подготовки тестовых данных для этого класса тестов
        """
        query_data1 = data['query_data'].copy()
        query_data1['params'] = f"name={data['test_names'][0]}"
        query_data1['json'] = {"name": data['test_names'][0]}
        query_data2 = query_data1.copy()
        query_data1['json'] = query_data1['json'] | data['payload1']
        query_data2['json'] = query_data1['json'] | data['payload2']

        r.post(**query_data1)
        res = r.put(**query_data2)

        assert res.status_code == 200
        assert len(res.json()) == 1
        assert 'result' in res.json()
        assert res.json()['result'] == query_data2['json']

        res = r.get(**query_data2)

        assert res.json()['result'] == query_data2['json']

    def test_put_character_negative(self, data, faker):
        """
        Тест проверки метода:
            PUT /character
        - HTTP 400 - невозможно изменить параметр 'name'

        :param data: фикстура подготовки тестовых данных для этого класса тестов
        :param faker: фикстура подготовки случайных данных
        """

        query_data = data['query_data'].copy()
        name = faker.fwords()
        query_data['params'] = f"name={name}"
        query_data['json'] = {"name": name}

        res = r.put(**query_data)

        assert res.status_code == 400
        assert len(res.json()) == 1
        assert 'error' in res.json()
        assert res.json()['error'] == "No such name"

    def test_put_character_negative2(self, data):
        """
        Тест проверки метода:
            PUT /character
            - HTTP 400 - отсутствие в запросе обязательного поля - 'name'

        :param data: фикстура подготовки тестовых данных для этого класса тестов
        """
        query_data = data['query_data'].copy()
        query_data['json'] = data['payload1'].copy()

        res = r.put(**query_data)

        assert res.status_code == 400
        assert len(res.json()) == 1
        assert 'error' in res.json()
        assert res.json()['error'] == "name: ['Missing data for required field.']"

    def test_put_character_negative3(self, data):
        """
        Тест проверки метода:
            PUT /character
            - HTTP 400 - пустой JSON {}

        :param data: фикстура подготовки тестовых данных для этого класса тестов
        """
        query_data = data['query_data'].copy()

        res = r.put(**query_data)

        assert res.status_code == 400
        assert len(res.json()) == 1
        assert 'error' in res.json()
        assert res.json()['error'] == 'Payload must be a valid json'
