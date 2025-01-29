# Orders Management System 🍽️

## Веб-приложение для управления заказами в кафе на Django ☕

---

## 🚀 Установка

### 1. Клонирование репозитория

```sh
git clone https://github.com/Yackov2004/Orders-managment.git
cd Orders-managment
```

### 2. Создание виртуального окружения 🛠️

```sh
python -m venv venv
```

### 3. Активация окружения 🔧

#### Для Linux/Mac:

```sh
source venv/bin/activate
```

#### Для Windows:

```sh
venv\Scripts\activate
```

### 4. Установка зависимостей 📦

```sh
pip install -r requirements.txt
```

---

## 🔧 Настройка

### 1. Создание файла окружения `.env` 📄

Создайте файл `.env` в корне проекта и добавьте в него:

```env
SECRET_KEY=ваш_секретный_ключ
DEBUG=True # Для разработки
```

### 2. Применение миграций 🔄

```sh
python manage.py migrate
```

### 3. Создание суперпользователя 👤

```sh
python manage.py createsuperuser
```

---

## ▶️ Запуск

### 1. Сборка статических файлов 📂

```sh
python manage.py collectstatic
```

### 2. Запуск сервера 🌐

```sh
python manage.py runserver
```

### 3. Доступ к веб-приложению 🔗

- Основное приложение: [http://localhost:8000](http://localhost:8000)
- Админ-панель: [http://localhost:8000/admin](http://localhost:8000/admin)

---

## 🎯 Использование

### Роли пользователей:

- **👑 Администратор** – управление пользователями, просмотр всех заказов
- **📋 Менеджер** – создание и редактирование заказов
- **👨‍🍳 Работник** – изменение статуса заказов

### Основные функции:

- ➕ Добавление/удаление заказов
- 🔎 Поиск по номеру стола и статусу
- 💰 Автоматический расчет суммы заказа
- ✅ Изменение статусов ("В ожидании", "Готово", "Оплачено")
- 📊 Расчет дневной выручки

---

## 🚢 Деплой в production

### 1. Установка WhiteNoise 🌬️

```sh
pip install whitenoise
```

### 2. Обновление `settings.py` ⚙️

```python
MIDDLEWARE = [
    ...
    'whitenoise.middleware.WhiteNoiseMiddleware',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### 3. Настройка веб-сервера (Nginx) 🖥️

Пример конфигурации для Nginx:

```nginx
location /static {
    alias /path/to/your/project/staticfiles;
}
```

---

## 📜 Лицензия

Проект распространяется под лицензией **MIT**. ✅

