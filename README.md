Проверка REST на базе Pytest
============================

Table of Contents
-----------------
* [Запуск автотестов](#запуск-автотестов)
  * [1. Зависимости проекта](#1-зависимости-проекта)
  * [2. Варианты конфигурации](#2-варианты-конфигурации)
  * [3. Запуск скрипта автотестов](#3-запуск-скрипта-автотестов)
  * [4. Отчеты](#4-отчеты)
* [Документация](#Документация)
  * [Описание тестового покрытия](#описание-тестового-покрытия)

Запуск автотестов
============================
#### 1. Зависимости проекта
- Предполагается что уже установлена версия Python >=3.9
- Выполнить для установки зависимых пакетов:
```
$ cd <директория проекта>
$ pip install -r requirements.txt
```
#### 2. Варианты конфигурации
Конфигурация запуска реализована по приоритетам:
- Приоритет №1: параметризация из командной строки (для CI/CD pipeline)
 * * список параметров для модерации из командной строки:
 * * `username`  <-- имя пользователя для авторизации на ресурсе
 * * `password`  <-- пароль
- Приоритет №2: параметризация из локального файла `config.local.json` (не коммитится в GitLab)
- Приоритет №3: параметризация из общего файла `config.json` (коммитится в GitLab)
#### 3. Запуск скрипта автотестов
Пример использования проброса параметров конфигурации при запуске тестов:
```
 $ python -m pytest <путь к папке tests> --username=<value> --<password>=<valuе>
```
Пример запуска тестов с фильтром по маркерам, установленным в файле `pytest.ini`:
```
 $ python -m pytest <marker1> ... <markerN>
```
- Для просмотра всех маркеров: ```$ pytest --markers```
- Для просмотра всех доступных fixtures: ```$ pytest --fixtures```
> shown according to specified file_or_dir or current dir if not specified;
> fixtures with leading '_' are only shown with the '-v' option)

#### 4. Отчеты
- на данном этапе реализации предусмотрен отчет в stdout

Документация
============================
#### Описание тестового покрытия
- Ссылка на требования: http://rest.test.ivi.ru/v2
- Тестовые сценарии находятся в папке проекта  ```\DOC``` в виде ```html``` документов:
 * * [test_1_check_characters_reset](https://github.com/sarzamas/pytest_rest_example/blob/master/DOC/test_1_check_characters_reset.html)
 * * [test_2_check_character_post](https://github.com/sarzamas/pytest_rest_example/blob/master/DOC/test_2_check_character_post.html)
 * * [test_3_check_character_get](https://github.com/sarzamas/pytest_rest_example/blob/master/DOC/test_3_check_character_get.html)
 * * [test_4_check_character_put](https://github.com/sarzamas/pytest_rest_example/blob/master/DOC/test_4_check_character_put.html)
 * * [test_5_check_character_patch](https://github.com/sarzamas/pytest_rest_example/blob/master/DOC/test_5_check_character_patch.html)
 * * [test_6_check_character_delete](https://github.com/sarzamas/pytest_rest_example/blob/master/DOC/test_6_check_character_delete.html)
