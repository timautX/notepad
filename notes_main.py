import json
import datetime
import os

from PyQt5 import Qt, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
                            QLabel, QHBoxLayout, QVBoxLayout,
                            QTextEdit, QLineEdit, QListWidget)

class NotesApp(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.data = {}

        self.setWindowTitle("Заметки")

        # скелет приложения
        self.main_vbox = QVBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.control_panel_vbox = QVBoxLayout()

        # поле для ввода заметок
        self.note_text_edit = QTextEdit()
        self.hbox1.addWidget(self.note_text_edit)

        # список заметок
        self.list_of_notes = QListWidget()
        self.list_of_notes.setFixedWidth(150)
        self.fill_list_of_notes()
        self.list_of_notes.itemClicked.connect(self.select_note)
        self.control_panel_vbox.addWidget(self.list_of_notes)


        # кнопка для сохранения заметки
        self.save_note_button = QPushButton("Сохранить заметку")
        self.save_note_button.clicked.connect(self.save_note)
        self.control_panel_vbox.addWidget(self.save_note_button)

        # навешиваем шампуры друг на друга
        self.main_vbox.addLayout(self.hbox1)
        self.hbox1.addLayout(self.control_panel_vbox)
        self.setLayout(self.main_vbox)

    def save_note(self):
        if len(self.data) == 0:
            self.data["name"] = None
        self.data["text"] = self.note_text_edit.toPlainText()
        self.save_widget = SaveNoteWidget(self.data, self)

    def fill_list_of_notes(self):
        self.list_of_notes.clear()
        for name in os.listdir("notes"):
            if name[-5:] == ".json":
                self.list_of_notes.addItem(name.replace(".json", ""))

    def select_note(self, note):
        filename = f'notes/{note.text()}.json'

        try:
            with open(filename, "r") as file:
                self.data = json.load(file)
                self.note_text_edit.setText(self.data["text"])
                file.close()
        except:
            self.fill_list_of_notes()

class SaveNoteWidget(QWidget):
    def __init__(self, data, parent_win: NotesApp) -> None:
        super().__init__()
        self.parent_win = parent_win
        self.data = data

        self.main_vbox = QVBoxLayout()

        self.name_edit = QLineEdit()
        if data["name"]:
            self.name_edit.setText(data["name"][:-5])
        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save)
        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.close_window)

        self.main_vbox.addWidget(self.name_edit)
        self.main_vbox.addWidget(self.save_button)
        self.main_vbox.addWidget(self.cancel_button)
        self.setLayout(self.main_vbox)

        self.show()

    def save(self):
        if self.name_edit.text() not in ("", None):
            self.note_name = f'{self.name_edit.text()}.json'

        data = {
            "text":str(self.data["text"]),
            "name":str(self.note_name),
            "tags":[],
            "date": str(datetime.datetime.now())
        }
        
        with open(f'notes/{self.note_name}', "w+", encoding="utf-8") as file:
            json.dump(data, file)
            file.close()

        self.close_window()
        self.parent_win.fill_list_of_notes()


    def close_window(self):
        self.close()

app = QApplication([])
win = NotesApp()
win.show()
app.exec_()

