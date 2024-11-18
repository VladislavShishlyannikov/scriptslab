import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableView, QVBoxLayout, QPushButton,
    QLineEdit, QWidget, QMessageBox, QDialog, QFormLayout, QDialogButtonBox
)
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery

os.environ["QT_PLUGIN_PATH"] = "C:/Users/Владислав/AppData/Local/Programs/Python/Python313/Lib/site-packages/PyQt5/Qt5/plugins"

# Создаем базу данных, если её не существует
def initialize_database():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("database.db")  
    if not db.open():
        QMessageBox.critical(None, "Ошибка, не удалось подключиться к базе данных")
        sys.exit(-1)

    # Создаем таблицу, если её не существует
    query = QSqlQuery(db) 
    query.exec(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            body TEXT NOT NULL
        )
        """
    )
    db.close()

class AddRecordDialog(QDialog):
    # Диалоговое окно для добавления новой записи
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить новую запись")
        self.resize(300, 200)

        self.layout = QFormLayout(self)

        self.user_id_input = QLineEdit()
        self.title_input = QLineEdit()
        self.body_input = QLineEdit()

        self.layout.addRow("User ID:", self.user_id_input)
        self.layout.addRow("Title:", self.title_input)
        self.layout.addRow("Body:", self.body_input)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.layout.addWidget(self.buttons)

    # Возвращаем данные из полей ввода
    def get_data(self):
        return {
            "user_id": self.user_id_input.text(),
            "title": self.title_input.text(),
            "body": self.body_input.text(),
        }

# Создаем главное окно
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Users")
        self.resize(800, 600)

        # Создаем центральный виджет и компоновку
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # создаем поле для поиска
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Введите текст для поиска")
        self.search_bar.textChanged.connect(self.search)
        layout.addWidget(self.search_bar)

        # Создаем кнопки
        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_record)
        self.delete_button = QPushButton("Удалить")
        self.delete_button.clicked.connect(self.delete_record)
        self.refresh_button = QPushButton("Обновить")
        self.refresh_button.clicked.connect(self.refresh_data)

        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.refresh_button)
        
        # Таблица для отображения данных
        self.table_view = QTableView()
        self.table_view.verticalHeader().setVisible(False)  # Убираем нумерацию строк (опционально)
        layout.addWidget(self.table_view)

        # Подключаемся к базе данных
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("database.db")
        if not self.db.open():
            QMessageBox.critical(self, "Ошибка, не удалось подключиться к базе данных")
            sys.exit(-1)

        # Настраиваем модель для QTableView
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable("users")
        self.model.select()
        self.table_view.setModel(self.model)

    # Функция фильтрации данных в таблице
    def search(self):
        filter_text = self.search_bar.text()
        self.model.setFilter(f"title LIKE '%{filter_text}%'")

    # Функция добавления новой записи
    def add_record(self):
        dialog = AddRecordDialog(self)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            query = QSqlQuery(self.db)
            query.prepare("INSERT INTO users (user_id, title, body) VALUES (?, ?, ?)")
            query.addBindValue(data['user_id'])
            query.addBindValue(data['title'])
            query.addBindValue(data['body'])
            if not query.exec():
                QMessageBox.critical(self, "Ошибка", f"Не удалось добавить запись: {query.lastError().text()}")
            else:
                self.refresh_data()

    # Функция удаления выбранной записи
    def delete_record(self):
        index = self.table_view.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления!")
            return

        record_id = self.model.data(self.model.index(index.row(), 0)) 
        confirm = QMessageBox.question(
            self, "Подтверждение", f"Удалить запись с ID {record_id}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            query = QSqlQuery(self.db)
            query.prepare("DELETE FROM users WHERE id = ?")
            query.addBindValue(record_id)
            if not query.exec():
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить запись: {query.lastError().text()}")
            self.refresh_data()

    # Функция обновления данных
    def refresh_data(self):
        self.model.select()

# Инициализируем базу данных
if __name__ == "__main__":
    initialize_database()

    # Создаем приложение и запускаем главное окно
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
