from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication
from ui.project_window import ProjectWindow


class MainWindow(QtWidgets.QWidget):
    def __init__(self, window, database):
        super(MainWindow, self).__init__(parent=window)

        self.parent_window = window
        self.database = database
        self.resize(self.parent_window.size())

        self.widget = QWidget(self, objectName='bottomWidget')
        self.widget.setStyleSheet("background-color: #18292C")

        self.central_widget = QtWidgets.QFrame(self.widget)
        self.central_widget.setStyleSheet("background-color: #18292C")
        self.central_widget.setObjectName("central_widget")
        self.central_widget.resize(self.parent_window.size())

        self.central_frame = QtWidgets.QFrame(self.central_widget)
        self.central_frame.setStyleSheet("background-color: #18292C")

        self.projects_frame = QtWidgets.QFrame(self.central_frame)
        self.projects_frame.setStyleSheet("background-color: #18292C")
        self.scroll_area = QtWidgets.QScrollArea(self.projects_frame)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_content = QtWidgets.QWidget(self.projects_frame)
        self.grid_layout = QtWidgets.QGridLayout(self.scroll_area_content)
        self.scroll_area.setWidget(self.scroll_area_content)
        self.grid_layout.setAlignment(Qt.AlignCenter)
        self.projects_frame.setGeometry(0, 0, 850, 500)
        self.scroll_area.setGeometry(0, 0, 850, 500)

        self.scroll_area_content.setStyleSheet("background-color: #18292C")
        self.scroll_area.setStyleSheet("background-color: #18292C")
        self.setStyleSheet("""
        QWidget {        
            border: none;        
        }      

        QScrollArea QWidget QWidget:disabled {
            background-color: pink;          
        }


        QScrollBar:vertical {
            background: transparent;         
            width: 16px;
            margin: 16px 2px 16px 2px;       
            border: 0px solid #31363B;       
            border-radius: 4px;
        }

        QScrollBar::handle:vertical {
            background-color: pink;     
            border: 1px solid #544d4d;
            min-height: 8px;
            border-radius: 4px;
        }

        QScrollBar::handle:vertical:hover {
            background-color: pink;      
            border: 1px solid #544d4d;
            border-radius: 4px;
            min-height: 8px;
        }

        QScrollBar::sub-line:vertical {
            margin: 3px 0px 3px 0px;
            height: 10px;
            width: 10px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }

        QScrollBar::add-line:vertical {
            margin: 3px 0px 3px 0px;
            height: 10px;
            width: 10px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }

        QScrollBar::up-arrow:vertical,
        QScrollBar::down-arrow:vertical {
            background: none;                   
        }

        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical {
            background: none;                
        }""")

        self.buttons_frame = QtWidgets.QFrame(self.central_frame)
        self.buttons_frame.setStyleSheet("background-color: #18292C")
        self.buttons_frame.setGeometry(0, 500, 850, 150)

        self.add_project_button = QtWidgets.QPushButton(self.buttons_frame)
        self.add_project_button.setGeometry(30, 50, 60, 60)
        font = QtGui.QFont()
        font.setFamily("Bauhaus 93")
        font.setPointSize(26)
        self.add_project_button.setFont(font)
        self.add_project_button.setStyleSheet("QPushButton {\n"
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
        self.add_project_button.setObjectName("add_project_button")
        self.add_project_button.setText("+")
        self.add_project_button.clicked.connect(self.add_project)

        self.edit_task_button = QtWidgets.QPushButton(self.buttons_frame)
        self.edit_task_button.setGeometry(400, 50, 60, 60)
        font.setPointSize(20)
        self.edit_task_button.setFont(font)
        self.edit_task_button.setStyleSheet("QPushButton {\n"
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
        self.edit_task_button.setObjectName("edit_task")
        self.edit_task_button.setText("✎")
        self.edit_task_button.clicked.connect(self.edit_project)

        self.del_project_button = QtWidgets.QPushButton(self.buttons_frame)
        self.del_project_button.setGeometry(740, 50, 60, 60)
        font = QtGui.QFont()
        font.setFamily("Bauhaus 93")
        font.setPointSize(30)
        self.del_project_button.setFont(font)
        self.del_project_button.setStyleSheet("QPushButton {\n"
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
        self.del_project_button.setObjectName("del_project_button")
        self.del_project_button.setText("-")
        self.del_project_button.clicked.connect(self.del_project)

        self.load_project_names()

        self.input_project_name = QtWidgets.QTextEdit(self.central_widget)
        self.input_project_name.cursor()
        self.input_project_name.setGeometry(QtCore.QRect(225, 220, 400, 50))
        self.input_project_name.setStyleSheet('''
                                                         QWidget{
                                                             background-color: #35514B;}
                                                         QTextEdit{
                                                             color: #F5D56B;
                                                             background-color: #35514B;
                                                             font: 20 10pt \"Zen Kurenaido\"; 
                                                             padding: 8px; 
                                                             border-radius: 10px;}''')

        self.enter_input_button = QtWidgets.QPushButton(self.central_widget)
        self.enter_input_button.setGeometry(QtCore.QRect(660, 215, 60, 60))
        font = QtGui.QFont()
        font.setFamily("Bauhaus 93")
        font.setPointSize(13)
        self.enter_input_button.setFont(font)
        self.enter_input_button.setStyleSheet("QPushButton {\n"
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
        self.enter_input_button.setObjectName("enter_input_button")
        self.enter_input_button.setText(">")
        self.enter_input_button.clicked.connect(lambda: self.input_project(self.input_project_name.toPlainText(), True))

        self.back_button = QtWidgets.QPushButton(self.central_widget)
        self.back_button.setGeometry(QtCore.QRect(130, 215, 60, 60))
        font = QtGui.QFont()
        font.setFamily("Bauhaus 93")
        font.setPointSize(10)
        self.back_button.setFont(font)
        self.back_button.setStyleSheet("QPushButton {\n"
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
        self.back_button.setObjectName("back_button")
        self.back_button.setText("X")
        self.back_button.clicked.connect(self.back)

        self.input_project_name.setVisible(False)
        self.enter_input_button.setVisible(False)
        self.back_button.setVisible(False)

    def input_project(self, input_text, new_project=False):
        print(input_text)

        if new_project:
            project_names = self.database.plans.keys()

            if input_text != '':
                if input_text not in project_names:
                    self.database.add_new_project(input_text)

            self.input_project_name.clear()

            self.load_project_names()
            self.back()

        self.hide()
        self.project_window = ProjectWindow(self.parent_window, input_text, self.database)
        self.parent_window.layout.addWidget(self.project_window)

    def back(self, delete_check=False):
        self.edit_task_button.setVisible(True)
        self.input_project_name.setVisible(False)
        self.enter_input_button.setVisible(False)
        self.back_button.setVisible(False)
        self.input_project_name.clear()

        for child in self.buttons_frame.children():
            child.setEnabled(True)

        for child in self.scroll_area_content.children():
            if type(child) == QtWidgets.QPushButton:
                child.setEnabled(True)

        self.blur_effect.setEnabled(False)

        if delete_check:
            self.load_project_names()
            font = QtGui.QFont()
            font.setFamily("Bauhaus 93")
            font.setPointSize(26)
            self.add_project_button.setFont(font)
            self.add_project_button.setText("+")
            self.add_project_button.clicked.connect(self.add_project)
            self.del_project_button.setVisible(True)

            self.enter_input_button.clicked.disconnect()
            self.back_button.clicked.disconnect()
            self.enter_input_button.clicked.connect(
                lambda: self.input_project(self.input_project_name.toPlainText(), True))
            self.back_button.clicked.connect(self.back)

    def add_project(self):
        self.input_project_name.setVisible(True)
        self.enter_input_button.setVisible(True)
        self.back_button.setVisible(True)

        self.blur_effect = QtWidgets.QGraphicsBlurEffect()
        self.central_frame.setGraphicsEffect(self.blur_effect)
        self.blur_effect.setEnabled(True)

        for child in self.scroll_area_content.children():
            if type(child) == QtWidgets.QPushButton:
                child.setEnabled(False)

        for child in self.buttons_frame.children():
            child.setEnabled(False)

    def delete_row(self, project_name):
        print(f"Deleted: item = {project_name}")

        self.database.del_project(project_name)

        for i in range(self.grid_layout.count()):
            self.grid_layout.itemAt(i).widget().close()

        self.del_project()

    def del_project(self):
        self.load_project_names(change_connect=True)
        self.grid_layout.update()
        self.edit_task_button.setVisible(False)
        self.del_project_button.setVisible(False)
        font = QtGui.QFont()
        font.setFamily("Bauhaus 93")
        font.setPointSize(13)
        self.add_project_button.setFont(font)
        self.add_project_button.setText("<")
        self.add_project_button.clicked.connect(lambda: self.back(True))

    def edit_project(self):
        font = QtGui.QFont()
        font.setFamily("Bauhaus 93")
        font.setPointSize(13)
        self.add_project_button.setFont(font)
        self.add_project_button.setText("<")
        self.add_project_button.clicked.connect(lambda: self.back(True))
        self.del_project_button.setVisible(False)
        self.edit_task_button.setVisible(False)
        self.load_project_names(False, True)

    def change_project_name(self, old_name, new_name):

        project_names = list(self.database.plans.keys())

        if new_name != '' and new_name not in project_names:
            self.database.edit_project_name(old_name, new_name)

            self.input_project_name.clear()

            self.blur_effect.setEnabled(False)
            self.input_project_name.setVisible(False)
            self.enter_input_button.setVisible(False)
            self.back_button.setVisible(False)

            for child in self.scroll_area_content.children():
                if type(child) == QtWidgets.QPushButton:
                    child.setEnabled(True)

            for child in self.buttons_frame.children():
                child.setEnabled(True)

            self.edit_project()

    def edit_name(self, old_project_name):
        self.input_project_name.setVisible(True)
        self.enter_input_button.setVisible(True)
        self.back_button.setVisible(True)

        self.blur_effect = QtWidgets.QGraphicsBlurEffect()
        self.central_frame.setGraphicsEffect(self.blur_effect)
        self.blur_effect.setEnabled(True)

        for child in self.scroll_area_content.children():
            if type(child) == QtWidgets.QPushButton:
                child.setEnabled(False)

        for child in self.buttons_frame.children():
            child.setEnabled(False)

        self.back_button.clicked.connect(self.edit_project)
        self.enter_input_button.clicked.disconnect()
        self.enter_input_button.clicked.connect(lambda: self.change_project_name(
            old_project_name, self.input_project_name.toPlainText()))

    def load_project_names(self, change_connect: bool = False, change_project_name: bool = False):
        project_names = list(self.database.plans.keys())
        print(project_names)

        for name in project_names:
            font = QtGui.QFont()
            font.setFamily("Bauhaus 93")
            font.setPointSize(13)

            self.project_name_button = QtWidgets.QPushButton()
            self.project_name_button.setFixedSize(QSize(300, 50))
            self.project_name_button.setFont(font)
            self.project_name_button.setStyleSheet("QPushButton {\n"
                                                       "    transition-duration: 0.4s;\n"
                                                       "    color: #F5D56B;\n"
                                                       "    background-color: #35514B;\n"
                                                       "    border-radius: 25;\n"
                                                       "}\n"
                                                       "\n"
                                                       "QPushButton:hover {\n"
                                                       "    border-radius: 16;\n"
                                                       "    box-shadow: 8px;\n"
                                                       "}\n"
                                                       "\n"
                                                       "QPushButton:pressed {\n"
                                                       "    background-color: #18292C;\n"
                                                       "}")
            self.project_name_button.setObjectName(f"{name}")
            self.project_name_button.setText(f"{name}")

            if change_project_name:
                self.project_name_button.clicked.connect(lambda ch, name=name: self.edit_name(name))
            else:
                if change_connect:
                    self.project_name_button.clicked.connect(lambda ch, name=name: self.delete_row(name))
                else:
                    self.project_name_button.clicked.connect(lambda ch, name=name: self.input_project(name))

            self.grid_layout.addWidget(self.project_name_button, project_names.index(name), 0,
                                       alignment=Qt.AlignCenter)
