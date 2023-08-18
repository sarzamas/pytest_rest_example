import pytest
import requests as r


@pytest.mark.patch
class TestCheckCharacterPatch:
    TEARDOWN_NAMES_POOl = 0

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

    def test_put_character_negative(self, data, faker):
        """
        Тест проверки метода:
            PATCH /character
        - HTTP 405 - метод не реализован

        :param data: фикстура подготовки тестовых данных для этого класса тестов
        :param faker: фикстура подготовки случайных данных
        """

        query_data = data['query_data'].copy()

        res = r.patch(**query_data)

        assert res.status_code == 405
        assert "405 Method Not Allowed" in res.text
