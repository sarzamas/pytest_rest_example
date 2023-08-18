import random
import string
from uuid import uuid4

from faker import Faker

from Utils.Singleton import Singleton


class RandomData(metaclass=Singleton):
    """
    Провайдер случайных данных
    """

    def __init__(self):
        self.__faker = Faker('ru_RU')

    def __getattr__(self, item):
        return getattr(self.__faker, item)

    def fwords(self, nb=2, capitalize=True, uuid=False):
        """
        Генератор фраз из случайных слов
        :param nb: число слов
        :param capitalize: признак, устанавливающий CapsLock на каждое слово
        :param uuid:  признак, добавляющий uuid к результату
        :return:
        """
        rand = ' '.join([x.capitalize() if capitalize else x for x in self.__faker.words(nb=nb)])
        rand += f' {str(uuid4())}' if uuid else ''
        return rand

    @staticmethod
    def text(length_word=10, count_words=1):
        result_str = ''
        for i in range(count_words):
            letters = string.ascii_letters
            result_str += ''.join(random.choice(letters) for i in range(length_word))
            if i + 1 < count_words:
                result_str += ' '
        return result_str

    @staticmethod
    def int(length=11):
        return random.randint(10 ** (length - 1), 10 ** length - 1)
