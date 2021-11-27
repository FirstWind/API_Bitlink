# Проверка ссылки на битлинк

Программа использует сервис bitly для обрезки длинных ссылок.  
Необходимо зарегестироваться на [bitly.com](bitly.com) и получить Token для работы скрипта с сервисом.  
Далее создать файл `.env` в корне проекта и туда занести полученный Ваш Token в виде:
```dotenv
TOKEN_BITLY=здесь ваш токен без ковычек
```
Запуск программы производится в терминале.  
Ссылка передается в качестве параметра командой: 
```shell
python main.py url
```

### Как установить

Python3 должен быть уже установлен.
Для установки используйте pip (или pip3, есть конфликт с Python2) зависимостей.  
Введите команду:
```
pip install -r requirements.txt
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).