import os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from ui.main_window import MainWindow
from ui.title_bar import TitleBar
from dotenv import load_dotenv
from back.database import Database


class RegistrationWindow:
    def __init__(self, *args, **kwargs):
        super(RegistrationWindow, self).__init__(*args, **kwargs)

        if not os.path.exists("back"):
            os.mkdir("back")

        self.resize(850, 700)

        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)

        self.layout.addWidget(TitleBar(self))

        self.widget = QWidget(self, objectName='bottomWidget')
        self.layout.addWidget(self.widget)
        self.widget.setStyleSheet("background-color: #18292C")

        self.central_widget = QtWidgets.QFrame(self.widget)
        self.central_widget.setStyleSheet("background-color: #18292C")
        self.central_widget.setObjectName("central_widget")
        self.central_widget.resize(850, 700)

        self.username_enter = QtWidgets.QTextEdit(self.central_widget)
        self.username_enter.setFocus()
        self.username_enter.setGeometry(QtCore.QRect(200, 220, 400, 50))
        self.username_enter.setStyleSheet('''
                                                                 QWidget{
                                                                     background-color: #35514B;}
                                                                 QTextEdit{  
                                                                     background-color: #35514B; 
                                                                     font: 20 10pt \"Zen Kurenaido\"; 
                                                                     padding: 8px; 
                                                                     color: #F5D56B; 
                                                                     border-radius: 10px;}''')
        self.username_enter.setPlaceholderText("Enter username")

        self.password_enter = QtWidgets.QTextEdit(self.central_widget)
        self.password_enter.setFocus()
        self.password_enter.setGeometry(QtCore.QRect(200, 320, 400, 50))
        self.password_enter.setStyleSheet('''
                                                                         QWidget{
                                                                             background-color: #35514B;}
                                                                         QTextEdit{
                                                                             background-color: #35514B; 
                                                                             font: 20 10pt \"Zen Kurenaido\"; 
                                                                             padding: 8px; 
                                                                             color: #F5D56B; 
                                                                             border-radius: 10px;}''')
        self.password_enter.setPlaceholderText("Enter password")

        self.enter_button = QtWidgets.QPushButton(self.central_widget)
        self.enter_button.setGeometry(670, 260, 60, 60)
        font = QtGui.QFont()
        font.setFamily("Bauhaus 93")
        font.setPointSize(16)
        self.enter_button.setFont(font)
        self.enter_button.setStyleSheet("QPushButton {\n"
                                              "    transition-duration: 0.4s;\n"
                                              "    color: #CBAB4A;\n"
                                              "    background-color: #2F4A42;\n"
                                              "    border-radius: 30;\n"
                                              "}\n"
                                              "\n"
                                              "QPushButton:hover {\n"
                                              "    border-radius: 25;\n"
                                              "    box-shadow: 8px;\n"
                                              "}\n"
                                              "\n"
                                              "QPushButton:pressed {\n"
                                              "    background-color: #18292C;\n"
                                              "}")
        self.enter_button.setObjectName("add_project_button")
        self.enter_button.setText(">")
        self.enter_button.clicked.connect(lambda: self.create_user(self.username_enter.toPlainText(),
                                                                   self.password_enter.toPlainText()))
        load_dotenv(dotenv_path="back/user.env")

        if os.getenv("USER_NAME") and os.getenv("PASSWORD"):
            self.move_to_main_window(Database(os.getenv("USER_NAME"), os.getenv("PASSWORD")))

    def create_user(self, username, password):

        if (username is not None and password is not None) and (username != " " and password != " "):
            with open("back/user.env", "w") as file:
                file.write(f"USER_NAME={username}\nPASSWORD={password}")

            load_dotenv(dotenv_path="back/user.env")
            self.move_to_main_window(Database(os.getenv("USER_NAME"), os.getenv("PASSWORD")))

    def move_to_main_window(self, database):
        self.widget.hide()
        self.main_window = MainWindow(self, database)
        self.layout.addWidget(self.main_window)
