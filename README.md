# it-parostok

не комерційний проект (типу https://www.behance.net/ )
python + fastapi + sqlalchemy + postgresql = BackEnd

18.08.2024 Що реалізовано на сьогодні:
- створена структура проекту
- збереження файлів в папці static/images (після перевірки файлу що це дійсно зображення)
- підтягування важливих credentials з файлу .env (є файл прикладу .env.example)
- додав CORSMiddleware для коректної роботи React frontend-a
- створена БД PostgreSQL поки що з двома таблицями

**Користувач**:
- створена таблиця "users" з полями:
    - id: Mapped[int]
    - email: Mapped[EmailStr]
    - password: Mapped[str]
    - name: Mapped[Optional[str]]
    - surname: Mapped[Optional[str]]
    - who_are_you: Optional[Literal["employee", "employer"]]
    - photo: Mapped[Optional[str]]  # зберігається в БД ім'я файлу
    - created_at: Mapped[date]
    - last_login: Mapped[Optional[datetime]]
    - is_super: Mapped[bool]
    - is_active: Mapped[bool]

Реалізовано:
- реєстрація по email + password (збереження в БД email + хеш пароля)
- логін с перевіркой email + хеш пароля, отримання JWT токену, та збереження його в кукі
- logout 
- читання профіля залогіненого користувача
- редугування профіля залогіненого користувача
- отримання інформації по користувачу по його id (тільки для адміна)
- отримання інформації по всім користувачам  (тільки для адміна)

**Projects**
- створена таблиця "projects" з полями:
    - id: Mapped[int]
    - user_id: Mapped[int] = mapped_column(ForeignKey)
    - title: Mapped[str]
    - text: Mapped[str]
    - photos: Mapped[Optional[List[str]]]  # зберігається в БД список імен файлів
    - created_at: Mapped[datetime]
    - updated_at: Mapped[datetime]
    - is_active: Mapped[bool]

Реалізовано:
- додавання нового проекту
- просмотр проектов залогіненого користувача
- просмотр всіх проектов (тільки для адміна)


Що не доробив (планую на наступний тиждень):

    - збереження файлу зображення користувача
    - редагування Project, додавання списку файлов зображень Project, якщо це потрібно (поки що зберігається один файл)
    - інши типи авторизації
    - адмінка, потрібна?

![Screen.jpg](static%2Fimages%2FScreen.jpg)