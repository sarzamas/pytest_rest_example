import pytest
import requests as r


@pytest.mark.characters
@pytest.mark.reset
class TestCheckCharactersReset:
    TEARDOWN_NAMES_POOl = 0

    @pytest.fixture(scope='class', name='data')
    def current_test_data(self, test_data):
        """
        Фикстура подготовки общих данных для выполнения этого класса тестов
        TEARDOWN_NAMES_POOl: количество используемых этим классом тестов слотов для параметра 'test_names'
        Все тестовые сущности созданные в тестах как POST с именами {'name': ...} взятыми из слотов 'test_names'
        будут автоматически очищены из базы при teardown

        :param test_data: базовая фикстура подготовки данных для выполнения всех тестов класса
        """

        current_test_data = test_data(self.TEARDOWN_NAMES_POOl)
        current_test_data['query_data']['url'] += 's'

        return current_test_data

    @pytest.mark.characters
    def test_characters_positive(self, data):
        """
        Тест проверки выдачи списка всех записей из БД:
            GET /characters
            - количество записей в БД <= 500
            - параметры ответа (HTTP 200, JSON)

        :param data: фикстура подготовки тестовых данных для этого класса тестов
        """

        query_data = data['query_data']

        res = r.get(**query_data)

        assert res.status_code == 200
        assert len(res.json()) == 1
        assert 'error' not in res.json()
        assert 0 <= len(res.json()['result']) <= 500

    @pytest.mark.reset
    def test_reset_positive(self, data, faker):
        """
        Тест проверки reset БД:
            POST /reset
            - HTTP 200
            - количество записей в БД = 302 (reset default)

        :param data: фикстура подготовки тестовых данных для этого класса тестов
        :param faker: фикстура подготовки случайных данных
        """

        query_data_1_characters = data['query_data']
        query_data_2_character = query_data_1_characters.copy()
        query_data_2_character['url'] = query_data_2_character['url'][:-1]
        query_data_3_reset = query_data_1_characters.copy()
        query_data_3_reset['url'] = query_data_3_reset['url'].partition('character')[0] + 'reset'

        res = r.get(**query_data_1_characters)

        count = len(res.json()['result'])
        if count == 302:
            query_data_2_character['json'] = {"name": faker.fwords()}
            r.post(**query_data_2_character)
            count += 1

        res = r.post(**query_data_3_reset)

        assert res.status_code == 200
        assert len(res.text) == 0

        res = r.get(**query_data_1_characters)

        assert count != len(res.json()['result'])
