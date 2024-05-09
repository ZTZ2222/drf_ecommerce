# Проект E-Commerce на Django

Это простой проект электронной коммерции, построенный с использованием Django, Django Rest Framework (DRF), Celery и PostgreSQL.

## Функции

- Авторизация по логину/паролю
- Возможность создавать товар, в котором хранятся следующие данные:
  - название
  - обычная цена
  - скидочная цена
  - товарный остаток
  - характеристики товара
  - категория
- К категории можно добавлять подкатегории
- Добавление товара в корзину
- Оформление корзины в заказ
  - отправка запроса в платежную систему для получения ссылки на оплату
  - при оформлении заказа отправляется письмо на почту с номером заказа и платежной ссылкой
- Наличие документации Swagger
