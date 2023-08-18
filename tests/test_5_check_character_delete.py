import pytest
import requests as r


@pytest.mark.delete
class TestCheckCharacterDelete:
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

        return current_test_data

    def test_delete_character_positive(self, data):
        """
        Тест проверки метода:
            DELETE /character
            - HTTP 200 - с верными данными

        :param data: фикстура подготовки тестовых данных для этого класса тестов
        """
        query_data = data['query_data'].copy()
        query_data['params'] = f"name={data['test_names'][0]}"
        query_data['json'] = {"name": data['test_names'][0]}

        r.post(**query_data)
        res = r.delete(**query_data)

        assert res.status_code == 200
        assert len(res.json()) == 1
        assert 'result' in res.json()
        assert res.json()['result'] == f"Hero {query_data['json']['name']} is deleted"

        res = r.get(**query_data)
        assert res.status_code == 400

    def test_delete_character_negative(self, data, faker):
        """
        Тест проверки метода:
            DELETE /character
            - HTTP 400 - с неверными данными

        :param data: фикстура подготовки тестовых данных для этого класса тестов
        :param faker: фикстура подготовки случайных данных
        """

        query_data = data['query_data'].copy()
        query_data['params'] = f"name={faker.fwords()}"

        res = r.delete(**query_data)

        assert res.status_code == 400
        assert len(res.json()) == 1
        assert 'error' in res.json()
        assert res.json()['error'] == "No such name"

    def test_delete_character_negative2(self, data):
        """
        Тест проверки метода:
            DELETE /character
            - HTTP 400 - в запросе отсутствует параметр 'name'

        :param data: фикстура подготовки тестовых данных для этого класса тестов
        """
        query_data = data['query_data'].copy()

        res = r.delete(**query_data)

        assert res.status_code == 400
        assert len(res.json()) == 1
        assert 'error' in res.json()
        assert res.json()['error'] == "name parameter is required"
