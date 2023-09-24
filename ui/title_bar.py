from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QWindowStateChangeEvent, QFont, QMouseEvent
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSpacerItem, QSizePolicy, \
    QLabel, QPushButton, QApplication, QVBoxLayout, QDialog
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget


class TitleBar(QWidget):
    Radius = 38

    def __init__(self, *args, title='PyPlans', **kwargs):
        super(TitleBar, self).__init__(*args, **kwargs)
        self.setupUi()

        # Поддержка настройки фона
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.mPos = None
        # Найти родительский элемент управления self.parent() (или self)
        self._root = self.window()
        font = QtGui.QFont()
        font.setFamily("Bauhaus 93")
        font.setPointSize(13)
        self.labelTitle.setFont(font)
        self.labelTitle.setText(title)
        self.labelTitle.setStyleSheet("color: #CBAB4A;")

        # Вам нужно скрыть кнопку свернуть или развернуть
        self.showMinimizeButton(self.isMinimizeable())
        self.showNormalButton(False)
        self.showMaximizeButton(self.isMaximizeable())

        # Связывающий сигнал
        # windowTitleChanged сигнал испускается при изменении заголовка окна
        # с новым заголовком в качестве аргумента.
        self._root.windowTitleChanged.connect(self.setWindowTitle)
        self.buttonMinimum.clicked.connect(self.showMinimized)
        self.buttonMaximum.clicked.connect(self.showMaximized)
        self.buttonNormal.clicked.connect(self.showNormal)
        self.buttonClose.clicked.connect(self._root.close)

        # Установите фильтр событий на родительский элемент управления (или на себя)
        self._root.installEventFilter(self)

    def showMinimized(self):
        self._root.showMinimized()
        QApplication.sendEvent(self.buttonMinimum, QMouseEvent(
            QMouseEvent.Leave, QPointF(), Qt.LeftButton, Qt.NoButton, Qt.NoModifier))

    def showNormal(self):
        ''' Восстанавливает виджет после того, как он был развернут или свернут. '''
        self._root.showNormal()
        QApplication.sendEvent(self.buttonMaximum, QMouseEvent(
            QMouseEvent.Leave, QPointF(), Qt.LeftButton, Qt.NoButton, Qt.NoModifier))

    def showMaximized(self):
        self._root.showMaximized()
        QApplication.sendEvent(self.buttonNormal, QMouseEvent(
            QMouseEvent.Leave, QPointF(), Qt.LeftButton, Qt.NoButton, Qt.NoModifier))

    def isMinimizeable(self):
        return self.testWindowFlags(Qt.WindowMinimizeButtonHint)

    def isMaximizeable(self):
        return self.testWindowFlags(Qt.WindowMaximized)

    def isResizable(self):
        return self._root.minimumSize() != self._root.maximumSize()

    def showMinimizeButton(self, show=True):
        """ Показать скрытую кнопку сворачивания """
        self.buttonMinimum.setVisible(show)
        self.widgetMinimum.setVisible(show)

    def showMaximizeButton(self, show=True):
        """ Показать скрытую кнопку максимизации """
        self.buttonMaximum.setVisible(show)
        self.widgetMaximum.setVisible(show)

    def showNormalButton(self, show=True):
        """ Показать скрытую кнопку восстановления """
        self.buttonNormal.setVisible(show)
        self.widgetNormal.setVisible(show)

    def showEvent(self, event):
        super(TitleBar, self).showEvent(event)
        if not self.isResizable():
            self.showMaximizeButton(False)
            self.showNormalButton(False)
        else:
            self.showMaximizeButton(
                self.isMaximizeable() and not self._root.isMaximized())
            self.showNormalButton(self.isMaximizeable()
                                  and self._root.isMaximized())

    def eventFilter(self, target, event):
        if isinstance(event, QWindowStateChangeEvent):
            if self._root.isVisible() and not self._root.isMinimized() and \
                    self.testWindowFlags(Qt.WindowMinMaxButtonsHint):
                maximized = self._root.isMaximized()
                self.showMaximizeButton(not maximized)
                self.showNormalButton(maximized)

                if maximized:
                    self._oldMargins = self._root.layout().getContentsMargins()
                    self._root.layout().setContentsMargins(0, 0, 0, 0)
                else:
                    if hasattr(self, '_oldMargins'):
                        self._root.layout().setContentsMargins(*self._oldMargins)
        return super(TitleBar, self).eventFilter(target, event)

    def mouseDoubleClickEvent(self, event):
        """ Дважды щелкните строку заголовка
        :param event:
        """
        if not self.isMaximizeable() or not self.isResizable():
            return
        if self._root.isMaximized():
            self._root.showNormal()
        else:
            self._root.showMaximized()

    def mousePressEvent(self, event):
        """ Координаты записи нажатия мышью
        :param event:
        """
        if event.button() == Qt.LeftButton:
            self.mPos = event.pos()

    def mouseReleaseEvent(self, event):
        """ Мышь отпущена, удалить координаты
        :param event:
        """
        self.mPos = None

    def mouseMoveEvent(self, event):
        """ Мышь двигает окно
        :param event:
        """
        if self._root.isMaximized():
            # Не двигается при максимизации
            return
        if event.buttons() == Qt.LeftButton and self.mPos:
            pos = event.pos() - self.mPos
            self._root.move(self._root.pos() + pos)

    def testWindowFlags(self, windowFlags):
        """ Определите, есть ли у текущего окна флаги
        :param windowFlags:
        """
        return bool(self._root.windowFlags() & windowFlags)

    def setWindowTitle(self, title):
        """ Установка заголовка
        :param title:
        """
        self.labelTitle.setText(title)

    def setupUi(self):
        """ Создать пользовательский интерфейс """
        self.setMinimumSize(0, self.Radius)
        self.setMaximumSize(0xFFFFFF, self.Radius)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        for name in ('widgetMinimum', 'widgetMaximum', 'widgetNormal', 'widgetClose'):
            widget = QWidget(self)
            widget.setMinimumSize(self.Radius, self.Radius)
            widget.setMaximumSize(self.Radius, self.Radius)
            widget.setObjectName('TitleBar_%s' % name)
            setattr(self, name, widget)
            layout.addWidget(widget)

        layout.addItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Название
        self.labelTitle = QLabel(self, alignment=Qt.AlignCenter)
        self.labelTitle.setObjectName('TitleBar_labelTitle')
        layout.addWidget(self.labelTitle)
        layout.addItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Свернуть, развернуть, восстановить, кнопкa закрыть
        for name, text in (('buttonMinimum', '0'), ('buttonMaximum', '1'),
                           ('buttonNormal', '2'), ('buttonClose', 'r')):
            button = QPushButton(text, self, font=QFont('Webdings'))
            button.setMinimumSize(self.Radius, self.Radius)
            button.setMaximumSize(self.Radius, self.Radius)
            button.setObjectName('TitleBar_%s' % name)
            setattr(self, name, button)
            layout.addWidget(button)
