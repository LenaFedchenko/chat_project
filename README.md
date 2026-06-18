# Chat Project


Chat Project is a web application for real-time group communication. It is built with Flask, stores data in SQLite, and uses Flask-SocketIO for live message delivery and online user status updates.

<details>
<summary>Українською</summary>

Chat Project - це вебзастосунок для спілкування в групових чатах у реальному часі. Проєкт написаний на Flask, зберігає дані в SQLite і використовує Flask-SocketIO для миттєвої доставки повідомлень та оновлення статусу користувачів.

</details>

## Features

- user registration and login;
- email verification through a confirmation message;
- personal chat creation;
- chat search;
- joining and leaving chats;
- real-time message sending and loading;
- chat member list with online/offline status;
- profile editing;
- account and created chat deletion.

<details>
<summary>Українською</summary>

- реєстрація та вхід користувачів;
- підтвердження email через лист;
- створення власного чату;
- пошук доступних чатів;
- приєднання до чатів і вихід із них;
- надсилання та завантаження повідомлень у реальному часі;
- список учасників чату з online/offline статусом;
- редагування профілю;
- видалення акаунта та створеного чату.

</details>

## Tech Stack

- Python;
- Flask;
- Flask-SQLAlchemy;
- Flask-Migrate;
- Flask-Login;
- Flask-SocketIO;
- SQLite;
- HTML, CSS, JavaScript.

<details>
<summary>Українською</summary>

- Python;
- Flask;
- Flask-SQLAlchemy;
- Flask-Migrate;
- Flask-Login;
- Flask-SocketIO;
- SQLite;
- HTML, CSS, JavaScript.

</details>

## Project Structure

```text
chat-project/
├── manage.py                  # application entry point
├── requirements.txt           # project dependencies
├── project/                   # Flask settings, database, routes
├── user/                      # registration, login, email verification, profile
├── chat/                      # chat pages and chat logic
└── message/                   # Socket.IO events and message handling
```

<details>
<summary>Українською</summary>

```text
chat-project/
├── manage.py                  # точка входу застосунку
├── requirements.txt           # залежності проєкту
├── project/                   # налаштування Flask, база даних, маршрути
├── user/                      # реєстрація, вхід, підтвердження email, профіль
├── chat/                      # сторінки та логіка чатів
└── message/                   # Socket.IO події та робота з повідомленнями
```

</details>

## Installation

1. Clone the repository and open the project folder:

```bash
git clone <repository-url>
cd chat-project
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

For Windows:

```bash
venv\Scripts\activate
```

3. Install dependencies:

```bash
python -m pip install -r requirements.txt
python -m pip install Flask-Login Flask-SocketIO python-dotenv
```

<details>
<summary>Українською</summary>

1. Клонуйте репозиторій і перейдіть у папку проєкту:

```bash
git clone <repository-url>
cd chat-project
```

2. Створіть і активуйте віртуальне оточення:

```bash
python -m venv venv
source venv/bin/activate
```

Для Windows:

```bash
venv\Scripts\activate
```

3. Встановіть залежності:

```bash
python -m pip install -r requirements.txt
python -m pip install Flask-Login Flask-SocketIO python-dotenv
```

</details>

## Environment Variables

Create a `.env` file in the project root:

```env
SECRET_TOKEN=your-secret-token
EMAIL_SENDER=your-email@gmail.com
PASSWORD_KEY=your-google-app-password
DB_INIT=flask --app manage.py db init
DB_MIGRATE=flask --app manage.py db migrate
DB_UPGRADE=flask --app manage.py db upgrade
```

`EMAIL_SENDER` and `PASSWORD_KEY` are required for sending verification emails. For Gmail, use an app password instead of the regular account password.

<details>
<summary>Українською</summary>

У корені проєкту створіть файл `.env`:

```env
SECRET_TOKEN=your-secret-token
EMAIL_SENDER=your-email@gmail.com
PASSWORD_KEY=your-google-app-password
DB_INIT=flask --app manage.py db init
DB_MIGRATE=flask --app manage.py db migrate
DB_UPGRADE=flask --app manage.py db upgrade
```

`EMAIL_SENDER` і `PASSWORD_KEY` потрібні для надсилання листа підтвердження. Для Gmail використовуйте пароль застосунку, а не звичайний пароль від акаунта.

</details>

## Running

Start the application:

```bash
python manage.py
```

After startup, the project will be available at:

```text
http://127.0.0.1:7060
```

<details>
<summary>Українською</summary>

Запустіть застосунок:

```bash
python manage.py
```

Після запуску проєкт буде доступний за адресою:

```text
http://127.0.0.1:7060
```

</details>

## Main Routes

- `/register/` - user registration;
- `/login/` - account login;
- `/success/` - page shown after sending the verification email;
- `/check_email/` - email verification;
- `/` - main chats page;
- `/create-chat/` - chat creation;
- `/search/` - chat search;
- `/add-chat/` - add a user to a chat;
- `/del-chat/` - delete the created chat;
- `/get-data/` - update profile data;
- `/del-user/` - delete account.

<details>
<summary>Українською</summary>

- `/register/` - реєстрація користувача;
- `/login/` - вхід в акаунт;
- `/success/` - сторінка після надсилання листа підтвердження;
- `/check_email/` - підтвердження email;
- `/` - основна сторінка чатів;
- `/create-chat/` - створення чату;
- `/search/` - пошук чатів;
- `/add-chat/` - додавання користувача до чату;
- `/del-chat/` - видалення створеного чату;
- `/get-data/` - оновлення даних профілю;
- `/del-user/` - видалення акаунта.

</details>

## Database

The project uses SQLite. The database file is created at `project/instance/data.db`, and migrations are stored in `project/migrations/`.

Main models:

- `User` - user, profile data, and chat list;
- `Chat` - chat, creator, members, and last message;
- `Message` - message, send time, author, and chat;
- `UserChat` - relation between users and chats.

<details>
<summary>Українською</summary>

Проєкт використовує SQLite. Файл бази даних створюється в `project/instance/data.db`, а міграції зберігаються в `project/migrations/`.

Основні моделі:

- `User` - користувач, дані профілю та список чатів;
- `Chat` - чат, автор, учасники та останнє повідомлення;
- `Message` - повідомлення, час надсилання, автор і чат;
- `UserChat` - зв'язок користувачів і чатів.

</details>

## Notes

- On the first run, migrations are executed through commands from `.env`.
- `Flask-SocketIO` must be installed for real-time messaging to work correctly.
- For development email sending, a separate test Gmail account can be used.

<details>
<summary>Українською</summary>

- Під час першого запуску міграції виконуються через команди з `.env`.
- Для коректної роботи повідомлень у реальному часі потрібен встановлений `Flask-SocketIO`.
- Для надсилання email у режимі розробки можна використовувати окремий тестовий Gmail-акаунт.

</details>
