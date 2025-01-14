# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainitWAay.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QListView, QMainWindow, QMenuBar, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QTextEdit,
    QVBoxLayout, QWidget)
from .static import resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1612, 847)
        font = QFont()
        font.setFamilies([u"MS Serif"])
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(u"#sidebar_widget QPushButton {\n"
"	text-align: left;\n"
"	background: transparent;\n"
"}\n"
"\n"
"#options_frame {\n"
"	border-top: 0.5px solid #4d4d4f;\n"
"}\n"
"\n"
"#options_frame QPushButton {\n"
"	color: #fff;\n"
"	border:none;\n"
"	padding: 10px;\n"
"	border-radius:5px;\n"
"	background: none;\n"
"}\n"
"\n"
"#options_frame QFrame {\n"
"	border-radius: 5px;\n"
"}\n"
"\n"
"#new_chat, #settings {\n"
"	border: 1px solid #4d4d4f;\n"
"	color: #fff;\n"
"	border-radius: 5px;\n"
"	padding: 10px;\n"
"}\n"
"\n"
"#sidebar_widget,\n"
"#chat_list {\n"
"	background: #202313;\n"
"}\n"
"\n"
"#chat_list {\n"
"	border: none;\n"
"}\n"
"\n"
"chat_list::item {\n"
"	color: #fff;\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	margin-top: 5px;\n"
"	\n"
"}\n"
"\n"
"#sidebar_widget QPushButton:hover,\n"
"#chat_list::item:hover,\n"
"#menu_frame QFrame:hover {\n"
"	background: #2a2b32;\n"
"}\n"
"\n"
"#input_frame {\n"
"	border: 1px solid #e5e5e5;\n"
"	background: #fff;\n"
"	border-radius: 1.5px;\n"
"}\n"
"\n"
"#text_input_area {\n"
""
                        "	border: 1px solid #f5f5f5;\n"
"	background: #fff;\n"
"	color: #1d1d1d;\n"
"}\n"
"\n"
"#send_btn {\n"
"	border: none;\n"
"}\n"
"\n"
"#send_btn:hover {\n"
"	background: #f3f3f3;\n"
"}\n"
"\n"
"#output_area {\n"
"	border: none;\n"
"}\n"
"\n"
"#main_widget,\n"
"#output_area_widget {\n"
"	background: #fff;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.sidebar_widget = QWidget(self.centralwidget)
        self.sidebar_widget.setObjectName(u"sidebar_widget")
        self.sidebar_widget.setMaximumSize(QSize(278, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.sidebar_widget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.settings_frame = QFrame(self.sidebar_widget)
        self.settings_frame.setObjectName(u"settings_frame")
        self.settings_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.settings_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.settings_frame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 8, -1, 8)
        self.new_chat = QPushButton(self.settings_frame)
        self.new_chat.setObjectName(u"new_chat")
        font1 = QFont()
        font1.setFamilies([u"Poppins Medium"])
        font1.setPointSize(11)
        self.new_chat.setFont(font1)
        icon = QIcon()
        icon.addFile(u":/icons/icons/new-indicator-svgrepo-com.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.new_chat.setIcon(icon)
        self.new_chat.setIconSize(QSize(26, 26))

        self.horizontalLayout_3.addWidget(self.new_chat)

        self.settings = QPushButton(self.settings_frame)
        self.settings.setObjectName(u"settings")
        self.settings.setFont(font1)
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/setting-5-svgrepo-com.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.settings.setIcon(icon1)
        self.settings.setIconSize(QSize(26, 26))

        self.horizontalLayout_3.addWidget(self.settings)


        self.verticalLayout_2.addWidget(self.settings_frame)

        self.chat_list_frame = QFrame(self.sidebar_widget)
        self.chat_list_frame.setObjectName(u"chat_list_frame")
        self.chat_list_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.chat_list_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.chat_list_frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(3)
        self.gridLayout.setContentsMargins(-1, 4, -1, 5)
        self.chat_list = QListView(self.chat_list_frame)
        self.chat_list.setObjectName(u"chat_list")
        font2 = QFont()
        font2.setPointSize(10)
        self.chat_list.setFont(font2)

        self.gridLayout.addWidget(self.chat_list, 0, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.chat_list_frame)

        self.options_frame = QFrame(self.sidebar_widget)
        self.options_frame.setObjectName(u"options_frame")
        self.options_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.options_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.options_frame)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 5, -1, 5)
        self.clear_chats_frame = QFrame(self.options_frame)
        self.clear_chats_frame.setObjectName(u"clear_chats_frame")
        self.clear_chats_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.clear_chats_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.clear_chats_frame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 0, -1, 2)
        self.clear_chats = QPushButton(self.clear_chats_frame)
        self.clear_chats.setObjectName(u"clear_chats")
        self.clear_chats.setFont(font1)
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/trash3-fill.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.clear_chats.setIcon(icon2)
        self.clear_chats.setIconSize(QSize(26, 26))

        self.horizontalLayout.addWidget(self.clear_chats)


        self.verticalLayout.addWidget(self.clear_chats_frame)

        self.dark_mode_frame = QFrame(self.options_frame)
        self.dark_mode_frame.setObjectName(u"dark_mode_frame")
        self.dark_mode_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.dark_mode_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.dark_mode_frame)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, 2)
        self.dark_mode = QPushButton(self.dark_mode_frame)
        self.dark_mode.setObjectName(u"dark_mode")
        self.dark_mode.setEnabled(True)
        self.dark_mode.setFont(font1)
        icon3 = QIcon()
        icon3.addFile(u":/icons/icons/moon-stars.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.dark_mode.setIcon(icon3)
        self.dark_mode.setIconSize(QSize(26, 26))

        self.horizontalLayout_2.addWidget(self.dark_mode)


        self.verticalLayout.addWidget(self.dark_mode_frame)


        self.verticalLayout_2.addWidget(self.options_frame)


        self.gridLayout_3.addWidget(self.sidebar_widget, 0, 0, 1, 1)

        self.main_widget = QWidget(self.centralwidget)
        self.main_widget.setObjectName(u"main_widget")
        self.gridLayout_5 = QGridLayout(self.main_widget)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(0)
        self.gridLayout_5.setVerticalSpacing(5)
        self.gridLayout_5.setContentsMargins(1, 0, 0, 10)
        self.horizontalSpacer = QSpacerItem(30, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.input_frame = QFrame(self.main_widget)
        self.input_frame.setObjectName(u"input_frame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_frame.sizePolicy().hasHeightForWidth())
        self.input_frame.setSizePolicy(sizePolicy)
        self.input_frame.setMinimumSize(QSize(650, 0))
        self.input_frame.setMaximumSize(QSize(1000, 120))
        self.input_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.input_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.input_frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(1)
        self.gridLayout_2.setVerticalSpacing(0)
        self.gridLayout_2.setContentsMargins(10, 5, 4, 5)
        self.verticalSpacer = QSpacerItem(20, 68, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_2.addItem(self.verticalSpacer, 0, 1, 1, 1)

        self.text_input_area = QTextEdit(self.input_frame)
        self.text_input_area.setObjectName(u"text_input_area")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.text_input_area.sizePolicy().hasHeightForWidth())
        self.text_input_area.setSizePolicy(sizePolicy1)
        self.text_input_area.setMaximumSize(QSize(900, 115))
        self.text_input_area.setFont(font1)
        self.text_input_area.setTabChangesFocus(False)

        self.gridLayout_2.addWidget(self.text_input_area, 0, 0, 3, 1)

        self.send_btn = QPushButton(self.input_frame)
        self.send_btn.setObjectName(u"send_btn")
        sizePolicy1.setHeightForWidth(self.send_btn.sizePolicy().hasHeightForWidth())
        self.send_btn.setSizePolicy(sizePolicy1)
        self.send_btn.setMinimumSize(QSize(0, 0))
        self.send_btn.setMaximumSize(QSize(40, 40))
        icon4 = QIcon()
        icon4.addFile(u":/icons/icons/send-svgrepo-com.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.send_btn.setIcon(icon4)
        self.send_btn.setIconSize(QSize(22, 22))

        self.gridLayout_2.addWidget(self.send_btn, 1, 1, 2, 1)


        self.gridLayout_5.addWidget(self.input_frame, 1, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(30, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)

        self.output_area = QScrollArea(self.main_widget)
        self.output_area.setObjectName(u"output_area")
        self.output_area.setAutoFillBackground(False)
        self.output_area.setFrameShape(QFrame.Shape.StyledPanel)
        self.output_area.setLineWidth(0)
        self.output_area.setWidgetResizable(True)
        self.output_area_widget = QWidget()
        self.output_area_widget.setObjectName(u"output_area_widget")
        self.output_area_widget.setGeometry(QRect(0, 0, 1333, 679))
        self.gridLayout_4 = QGridLayout(self.output_area_widget)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.verticalSpacer_2 = QSpacerItem(20, 777, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_2, 0, 0, 1, 1)

        self.output_area.setWidget(self.output_area_widget)

        self.gridLayout_5.addWidget(self.output_area, 0, 0, 1, 3)


        self.gridLayout_3.addWidget(self.main_widget, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1612, 33))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.new_chat.setText(QCoreApplication.translate("MainWindow", u"New Chat", None))
        self.settings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.clear_chats.setText(QCoreApplication.translate("MainWindow", u"  Clear Chats", None))
        self.dark_mode.setText(QCoreApplication.translate("MainWindow", u"  Dark Mode", None))
        self.send_btn.setText("")
    # retranslateUi

