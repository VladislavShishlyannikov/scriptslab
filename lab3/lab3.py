import sqlite3
import requests

# 1. Создание базы данных
def create_database():
    conn = sqlite3.connect('database.db')  # Подключение к базе данных
    cursor = conn.cursor()
    # Создание таблицы
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            title TEXT,
            body TEXT
        )
    ''')   
    conn.commit()
    conn.close()
    print("Таблица posts успешно создана")

# 2. Получение данных с сервера
def fetch_data():
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)
    
    if response.status_code == 200:
        print("Данные успешно получены")
        return response.json()  # Возвращаем JSON-данные
    else:
        print("Ошибка при получении данных:", response.status_code)
        return []

# 3. Сохранение данных в базу данных
def save_data_to_database(posts):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Добавляем каждый пост в таблицу
    for post in posts:
        cursor.execute('''
            INSERT OR REPLACE INTO posts (id, user_id, title, body)
            VALUES (?, ?, ?, ?)
        ''', (post['id'], post['userId'], post['title'], post['body']))
    
    conn.commit()
    conn.close()
    print("Данные успешно сохранены в базу данных")

# 4. Чтение данных из базы данных
def get_posts_by_user(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Получаем все посты принадлежащие конкретному пользователю
    cursor.execute('SELECT * FROM posts WHERE user_id = ?', (user_id,))
    posts = cursor.fetchall()
    
    conn.close()
    return posts

# Основная программа
if __name__ == "__main__":
    # Создаем базу данных и таблицу
    create_database()

    # Получаем данные с сервера
    posts_data = fetch_data()

    # Сохраняем данные в базу данных
    if posts_data:
        save_data_to_database(posts_data)

    # Чтение данных из базы по user_id
    user_id = 1
    user_posts = get_posts_by_user(user_id)
    for post in user_posts:
        print(post)
