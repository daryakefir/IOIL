!!!!!!!Для успешной работы убедитесь, что на вашем компьюетере установлены docker и docker compose!!!!!!!!!!!!!!

Скачайте проект себе на компьютер.

Через командную строку перейдите в директорию приложения irkutskoiltest

Поочередно выполните следующие команды:

docker compose up -d --build

docker compose exec web python manage.py migrate --noinput

docker compose exec db psql -U user -d test -f /docker-entrypoint-initdb.d/init

Перейдите на страницу http://127.0.0.1:8000 и приступайте к работе!
