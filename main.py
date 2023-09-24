from PyQt5.QtWidgets import QApplication, QWidget
from ui.registration_window import RegistrationWindow


class ProgramWindow(QWidget, RegistrationWindow):
    pass


Style = """
TitleBar {
    background: #18292C;
    color: #CBAB4A;
}
TitleBar {
    border-top-right-radius: 20px;
    border-top-left-radius:  20px;
}
#TitleBar_buttonClose {
    border-top-right-radius: 20px;
}

#bottomWidget {
    background: #CBAB4A;
    border-bottom-right-radius: 10px;
    border-bottom-left-radius: 10px;
}

TitleBar > QPushButton {
    background: transparent;
}
TitleBar > QPushButton:hover {
    color: #CBAB4A;
    background: #2F4A42;
}

#TitleBar_buttonClose:hover {
    color: #CBAB4A;
    background: #2F4A42;
}

TitleBar > QPushButton:pressed {
    color: #CBAB4A;
    background: rgb(0, 0, 0);
}

TitleBar_buttonClose:pressed {
    color: #CBAB4A;
    background: rgb(0, 0, 0);
}

#TitleBar_buttonClose:pressed {
    color: #CBAB4A;
    background: rgb(0, 0, 0);
}
"""

if __name__ == '__main__':
    import sys

    # Back up the reference to the exceptionhook
    sys._excepthook = sys.excepthook


    def my_exception_hook(exctype, value, traceback):
        # Print the error and traceback
        print(exctype, value, traceback)
        # Call the normal Exception hook after
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)


    # Set the exception hook to our wrapping function
    sys.excepthook = my_exception_hook

    app = QApplication(sys.argv)
    app.setStyleSheet(Style)
    w = ProgramWindow()
    w.show()
    sys.exit(app.exec_())
