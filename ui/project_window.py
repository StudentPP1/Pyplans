from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QRect, QSize, QModelIndex, QEvent
from PyQt5.QtWidgets import QHeaderView, QAbstractItemView


class ProjectWindow(QtWidgets.QWidget):
    def __init__(self, window, project_name, database):
        super(ProjectWindow, self).__init__(parent=window)

        self.project_name = project_name
        self.window = window
        self.database = database
        self.is_task = True

        self.resize(850, 700)
        self.setStyleSheet("background-color: #18292C")

        self.main_frame = QtWidgets.QFrame(self)
        self.main_frame.setStyleSheet("background-color: #18292C")
        self.main_frame.resize(self.window.size())

        self.top_frame = QtWidgets.QFrame(self.main_frame)
        self.top_frame.setStyleSheet("background-color: #18292C")
        self.top_frame.setGeometry(0, 0, 850, 100)

        self.middle_frame = QtWidgets.QFrame(self.main_frame)
        self.middle_frame.setStyleSheet("background-color: #18292C")
        self.middle_frame.setGeometry(0, 100, 850, 500)

        rows, tasks = self.get_project_data()

        self.table = QtWidgets.QTableWidget(rows, 1)
        self.table.itemClicked.connect(self.item_clicked)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().hide()
        self.table.verticalHeader().hide()
        self.table.resizeRowsToContents()
        self.table.setShowGrid(False)
        self.table.setWordWrap(True)
        self.table.setStyleSheet("""
                QTableWidget { background-color: #18292C; font-size: 21px; color: #F5D56B;
                border: None;
                border-color:transparent; }

                QTableView::indicator { background-color: #35514B; border-radius: 7;}

                QTableView::indicator:checked { background-color: #35514B; }

                QTableView::item:selected:active {
                    background: #35514B;
                    color: #F5D56B;
                }

                QLineEdit {
                   background: #35514B;
                   color: #F5D56B;
                }

                QLineEdit:focus { 
                    background: #35514B;
                    color: #F5D56B;
                }
                """)
        self.update_table()

        layout = QtWidgets.QVBoxLayout(self.middle_frame)
        layout.addWidget(self.table)

        self.bottom_frame = QtWidgets.QFrame(self.main_frame)
        self.bottom_frame.setStyleSheet("background-color: #18292C")
        self.bottom_frame.setGeometry(0, 500, 850, 200)

        self.return_button = QtWidgets.QPushButton(self.top_frame)
        self.return_button.setGeometry(30, 30, 60, 60)
        font = QtGui.QFont()
        font.setFamily("Bauhaus 93")
        font.setPointSize(13)
        self.return_button.setFont(font)
        self.return_button.setStyleSheet("QPushButton {\n"
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
        self.return_button.setObjectName("add_project_button")
        self.return_button.setText("<")
        self.return_button.clicked.connect(self.back_to_main_window)

        # self.project_label = QtWidgets.QLabel(self.top_frame)
        # self.project_label.setGeometry(500, 30, 290, 60)
        # self.project_label.setFont(font)
        # self.project_label.setText(self.project_name)
        # self.project_label.setAlignment(Qt.AlignCenter)
        # self.project_label.setStyleSheet("QLabel { color: #CBAB4A; background-color: #2F4A42; border-radius: 15; }")

        self.add_task_button = QtWidgets.QPushButton(self.bottom_frame)
        self.add_task_button.setGeometry(30, 30, 60, 60)
        font.setPointSize(26)
        self.add_task_button.setFont(font)
        self.add_task_button.setStyleSheet("QPushButton {\n"
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
        self.add_task_button.setObjectName("add_task")
        self.add_task_button.setText("+")
        self.add_task_button.clicked.connect(self.add_task)

        self.edit_task_button = QtWidgets.QPushButton(self.bottom_frame)
        self.edit_task_button.setGeometry(400, 30, 60, 60)
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
        self.edit_task_button.clicked.connect(self.edit_task)

        self.back_from_edit = QtWidgets.QPushButton(self.bottom_frame)
        self.back_from_edit.setGeometry(30, 30, 60, 60)
        font.setPointSize(13)
        self.back_from_edit.setFont(font)
        self.back_from_edit.setStyleSheet("QPushButton {\n"
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
        self.back_from_edit.setObjectName("add_task")
        self.back_from_edit.setText("<")
        self.back_from_edit.clicked.connect(lambda: self.back(False, True))
        self.back_from_edit.setVisible(False)

        self.del_task_button = QtWidgets.QPushButton(self.bottom_frame)
        self.del_task_button.setGeometry(730, 30, 60, 60)
        font.setPointSize(26)
        self.del_task_button.setFont(font)
        self.del_task_button.setStyleSheet("QPushButton {\n"
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
        self.del_task_button.setObjectName("del_task")
        self.del_task_button.setText("-")
        self.del_task_button.clicked.connect(self.del_task)

        self.back_from_delete = QtWidgets.QPushButton(self.bottom_frame)
        self.back_from_delete.setGeometry(30, 30, 60, 60)
        font.setPointSize(13)
        self.back_from_delete.setFont(font)
        self.back_from_delete.setStyleSheet("QPushButton {\n"
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
        self.back_from_delete.setObjectName("add_task")
        self.back_from_delete.setText("<")
        self.back_from_delete.clicked.connect(lambda: self.back(True, False))
        self.back_from_delete.setVisible(False)

        self.input_task_name = QtWidgets.QPlainTextEdit(self)
        self.input_task_name.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.input_task_name.cursor()
        self.input_task_name.setGeometry(QtCore.QRect(200, 200, 450, 150))
        self.input_task_name.setStyleSheet('''QWidget {background-color: #35514B; color: #F5D56B; border-radius: 10px;
        font: 20px bold}''')

        self.enter_task_button = QtWidgets.QPushButton(self)
        self.enter_task_button.setGeometry(QtCore.QRect(700, 240, 60, 60))
        font = QtGui.QFont()
        font.setFamily("Bauhaus 93")
        font.setPointSize(13)
        self.enter_task_button.setFont(font)
        self.enter_task_button.setStyleSheet("QPushButton {\n"
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
        self.enter_task_button.setObjectName("enter_input_button")
        self.enter_task_button.setText(">")
        self.enter_task_button.clicked.connect(lambda: self.create_task(self.input_task_name.toPlainText()))

        self.back_button = QtWidgets.QPushButton(self)
        self.back_button.setGeometry(QtCore.QRect(90, 240, 60, 60))
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
        self.input_task_name.setVisible(False)
        self.enter_task_button.setVisible(False)
        self.back_button.setVisible(False)

    def update_table(self, add_row=False, set_items_editable=False):

        rows, tasks = self.get_project_data()

        not_done_tasks = {}
        done_tasks = {}

        for task in tasks.keys():
            if tasks[task]:
                done_tasks[task] = tasks[task]
            else:
                not_done_tasks[task] = tasks[task]

        print("not_done_tasks", not_done_tasks)
        print("done_tasks", done_tasks)

        not_done_tasks.update(done_tasks)
        tasks = not_done_tasks

        print("tasks", tasks)
        print()

        if add_row:
            self.table.setRowCount(self.table.rowCount() + 1)

        row = -1
        for task in tasks.keys():
            if tasks[task]:
                done_item = QtWidgets.QTableWidgetItem(f"{task}")
                done_item.setTextAlignment(Qt.AlignCenter | Qt.AlignHCenter)
                font = QtGui.QFont()
                font.setStrikeOut(True)
                done_item.setFont(font)

                if set_items_editable:
                    done_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
                else:
                    done_item.setFlags(Qt.ItemIsEnabled)

                self.table.setItem(row, 1, done_item)
            else:
                item = QtWidgets.QTableWidgetItem(f"{task}")
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignHCenter)

                if set_items_editable:
                    item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
                else:
                    item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)

                self.table.setItem(row, 1, item)
            row += 1

    def edit_task(self):
        self.edit_task_button.setVisible(False)
        self.return_button.setVisible(False)
        self.del_task_button.setVisible(False)
        self.add_task_button.setVisible(False)
        self.back_from_edit.setVisible(True)
        self.table.itemClicked.disconnect(self.item_clicked)
        self.table.itemDoubleClicked.connect(self.cell_double_clicked)
        self.update_table(False, True)

    def del_task(self):
        self.edit_task_button.setVisible(False)
        self.return_button.setVisible(False)
        self.del_task_button.setVisible(False)
        self.add_task_button.setVisible(False)
        self.back_from_delete.setVisible(True)

        self.table.itemClicked.disconnect(self.item_clicked)
        self.table.itemClicked.connect(self.delete_task)

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def delete_task(self, item):
        text = item.text()
        self.database.del_task(self.project_name, text)

        self.table.removeRow(item.row())
        self.update_table()

    def create_task(self, text):
        if text != '':
            self.database.add_new_task(self.project_name, text)
            self.back()
            self.update_table(True)

    def back(self, back_from_task_delete=False, back_from_task_edit=False):
        if back_from_task_edit:
            self.edit_task_button.setVisible(True)
            self.return_button.setVisible(True)
            self.del_task_button.setVisible(True)
            self.add_task_button.setVisible(True)
            self.back_from_edit.setVisible(False)
            self.table.itemClicked.connect(self.item_clicked)
            self.table.itemDoubleClicked.disconnect(self.cell_double_clicked)
            self.update_table()

        elif back_from_task_delete:
            self.edit_task_button.setVisible(True)
            self.return_button.setVisible(True)
            self.del_task_button.setVisible(True)
            self.add_task_button.setVisible(True)
            self.back_from_delete.setVisible(False)

            self.table.itemClicked.disconnect(self.delete_task)
            self.table.itemClicked.connect(self.item_clicked)
        else:
            self.edit_task_button.setVisible(True)
            for child in self.bottom_frame.children():
                child.setEnabled(True)

            for child in self.top_frame.children():
                if type(child) is QtWidgets.QPushButton:
                    child.setEnabled(True)

            self.table.itemClicked.connect(self.item_clicked)
            self.input_task_name.clear()
            self.blur_effect.setEnabled(False)
            self.input_task_name.setVisible(False)
            self.enter_task_button.setVisible(False)
            self.back_button.setVisible(False)

    def add_task(self):
        self.input_task_name.setVisible(True)
        self.enter_task_button.setVisible(True)
        self.back_button.setVisible(True)

        for child in self.bottom_frame.children():
            child.setEnabled(False)

        for child in self.top_frame.children():
            if type(child) is QtWidgets.QPushButton:
                child.setEnabled(False)

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.itemClicked.disconnect(self.item_clicked)

        self.blur_effect = QtWidgets.QGraphicsBlurEffect()
        self.main_frame.setGraphicsEffect(self.blur_effect)
        self.blur_effect.setEnabled(True)

    def back_to_main_window(self):
        self.hide()
        self.window.main_window.show()
        self.window.layout.addWidget(self.window.main_window)

    def item_clicked(self, item):
        font = QtGui.QFont()
        font.setStrikeOut(True)

        if item.font() != font:
            task_text = item.text()
            print(f"Item clicked: {task_text}")
            self.database.task_done(self.project_name, task_text)
            self.update_table()

    def cell_double_clicked(self, item):
        text = item.text()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.table.itemChanged.connect(lambda: self.cell_changed(item, text))

    def cell_changed(self, item, old_task):
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        new_task = item.text()

        if new_task != '' and not new_task.isdigit():
            self.database.edit_task(self.project_name, old_task, new_task)

        self.table.itemChanged.disconnect()

    def get_project_data(self):
        data = self.database.plans[self.project_name].items()
        print("data:", data)

        tasks = {}

        for text, flag in data:
            if text != '':
                is_done = bool(int(flag))
                tasks[text] = is_done

        return len(list(tasks.keys())), tasks
