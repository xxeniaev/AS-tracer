# Трассировка автономных систем.
Данное приложение позволяет получить информацию о маршрутизаторах (ip адрес, номер автономной системы), через которые проходит пакет, до указанного узла.

### Описание
* Пользователь вводит доменное имя или IP адрес. 
* Осуществляется трассировка до указанного узла.
* Определяется к какой автономной системе относится каждый из полученных IP адресов  маршрутизаторов. 

### Реализация

* Для поиска ip адресов маршрутизаторов используется утилита "tracert"
* Для получения номера автономных систем используется утилита "whois" с обращением сервису "cymru.com"

### Использование 

`python3 main.py yandex.ru`

`python3 main.py 5.255.255.77`

### Автор 
*Xenia Evdokimova* ([xxeniaev](https://github.com/xxeniaev))
