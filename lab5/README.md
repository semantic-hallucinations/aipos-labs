Аппаратное и программное обеспечение сетей и защита информации  
**Общие требования к выполнению:**

* Можно выполнять в парах, но вклад каждого будет оцениваться индивидуально;  
* За каждую лабораторную будет ставиться оценка \[0, 10\];  
* Создать в парах публичный гит-репозиторий, заливать лабораторные по мере прогресса (развитие должно прослеживаться по истории коммитов). Следовать примерно следующей структуре:  
  my-cool-repo/  
          awesome-lab-1/  
          awesome-lab-2/


**⭐** \- Необязательное к выполнению задание.

# Лабораторная работа 5

**Общие требования:**

* Любой язык программирования;  
* Допускается использование разумного количества сторонних библиотек;  
* Обработка и создание HTTP пакетов без использование сторонних библиотек;  
* Консольное приложение (если другое не указано в задании);  
* Конфигурация всех параметров (в разумных пределах) с помощью command line аргументов (Используйте стороннюю библиотеку для парсинга). Поддержка коротких и длинных вариантов (-a, \--argument), help по всем доступным аргументам.

**Требования к серверу:**

* Запись подробного лога с деталями работы протокола в log файл;  
* Вывод краткой, понятной человеку информации в консоль.

**Требования к клиенту:**

* Конфигурация запросов с помощью command line аргументов;  
* Поддержка выполнения запросов по шаблону из файла;  
* Обработка и вывод сообщений об ошибках согласно работе/статусам ответа протокола.

## **HTTP 1.1 Сервер**

* Программа должна “раздавать” файлы из указанной директории  
* Конфигурация заголовков по умолчанию, которые будут отправляться с каждым запросом. Например:  
  Access-Control-Allow-Origin: https://my-cool-site.com  
  Access-Control-Allow-Methods: GET, POST, OPTIONS  
* Поддерживаемые виды запросов: GET, POST, OPTIONS;  
* Поддерживать необходимое для работы количество статусов ответов [HTTP response status codes \- HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status).

[RFC 2616 \- Hypertext Transfer Protocol \-- HTTP/1.1](https://tools.ietf.org/html/rfc2616). Тестируйте с помощью браузера (Должен работать с html, css, js, svg, png)  или любых других http клиентов (postman, insomnia).

## **HTTP 1.1 Клиент**

* Поддержка любого метода запроса;  
* Конфигурация произвольных заголовков запроса;  
* Возможность отправки тела запроса из файла или command line аргумента.

[RFC 2616 \- Hypertext Transfer Protocol \-- HTTP/1.1](https://tools.ietf.org/html/rfc2616). Можно вдохновляться [curl](https://curl.haxx.se/).