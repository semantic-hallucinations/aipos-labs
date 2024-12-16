Аппаратное и программное обеспечение сетей и защита информации  
**Общие требования к выполнению:**

* Можно выполнять в парах, но вклад каждого будет оцениваться индивидуально;  
* За каждую лабораторную будет ставиться оценка \[0, 10\];  
* Создать в парах публичный гит-репозиторий, заливать лабораторные по мере прогресса (развитие должно прослеживаться по истории коммитов). Следовать примерно следующей структуре:  
  my-cool-repo/  
          awesome-lab-1/  
          awesome-lab-2/


**⭐** \- Необязательное к выполнению задание.

# Лабораторная работа 7

За основу берем 6 лабораторную работу. В результате лабораторной должен получиться REST api сервер, который отвечает за работу с базой данных, а также html сервер, который принимает запрос на страницу, делает запрос на REST сервер и генерирует html. Тестируем в браузере.  
**Условие:**

* Тема для приложения из лабораторной работы 6;  
* Реализовать REST сервер, позволяющий делать CRUD операции над каждой сущностью (backend). Хороший пример REST api \- [SWAPI \- The Star Wars API](https://swapi.co/);  
* Переделать реализованный в лабораторной работе 2 html сервер, только уже в качестве клиента к REST сервису (frontend).

**Общие требования:**

* Любой язык программирования;  
* Допускается использование разумного количества сторонних библиотек;  
* ⭐ Запускать все компоненты приложения в docker через docker-compose.

**Требования к базе данных:**

* SQL / NoSQL

**Требования к серверу:**

* Конфигурация через ENV переменные;  
* Запись access log в файл;  
* Вывод краткой, понятной человеку информации в консоль.
```
lab7
├─ .gitignore
├─ Dockerfile
├─ README.md
├─ api
│  ├─ Dockerfile
│  ├─ config.py
│  ├─ crud.py
│  ├─ database.py
│  ├─ main.py
│  └─ requirements.txt
├─ docker-compose.yml
├─ init.sql
├─ main.py
├─ requirements.txt
└─ web
   ├─ Dockerfile
   ├─ main.py
   ├─ requirements.txt
   └─ templates
      ├─ but_curr_date_object.html
      ├─ but_curr_object.html
      ├─ but_curr_type_object.html
      ├─ edit_date.html
      ├─ edit_event.html
      ├─ edit_object.html
      ├─ edit_owner.html
      ├─ edit_popularity.html
      ├─ menu.html
      ├─ select_object_date.html
      ├─ select_object_type.html
      ├─ upcoming_events.html
      ├─ view_dates.html
      ├─ view_events.html
      ├─ view_objects.html
      ├─ view_owners.html
      └─ view_popularities.html

```