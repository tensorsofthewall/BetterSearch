# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'home_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
    QLabel, QLayout, QSizePolicy, QSpacerItem,
    QToolButton, QVBoxLayout, QWidget)
import resource_rc

class Ui_home_widget(object):
    def setupUi(self, home_widget):
        if not home_widget.objectName():
            home_widget.setObjectName(u"home_widget")
        home_widget.resize(1117, 922)
        home_widget.setStyleSheet(u"#home_widget QLabel{\n"
"	background: #f7f7f8; \n"
"	border-radius: 8px;\n"
"	padding: 10px;\n"
"}\n"
"\n"
"#home_widget,\n"
"#app_frame QLabel{\n"
"	background: #fff\n"
"}\n"
"\n"
"#app_frame {\n"
"	background: #fff\n"
"}")
        self.gridLayout = QGridLayout(home_widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer = QSpacerItem(233, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 0, 1, 2)

        self.app_frame = QFrame(home_widget)
        self.app_frame.setObjectName(u"app_frame")
        self.app_frame.setMaximumSize(QSize(1000, 270))
        self.app_frame.setFrameShape(QFrame.StyledPanel)
        self.app_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.app_frame)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(2, 5, 2, 5)
        self.app_logo = QLabel(self.app_frame)
        self.app_logo.setObjectName(u"app_logo")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.app_logo.sizePolicy().hasHeightForWidth())
        self.app_logo.setSizePolicy(sizePolicy)
        self.app_logo.setMaximumSize(QSize(175, 175))
        self.app_logo.setAutoFillBackground(False)
        self.app_logo.setTextFormat(Qt.AutoText)
        self.app_logo.setPixmap(QPixmap(u":/imgs/images/logo.svg"))
        self.app_logo.setScaledContents(True)
        self.app_logo.setAlignment(Qt.AlignCenter)
        self.app_logo.setWordWrap(False)

        self.horizontalLayout_2.addWidget(self.app_logo)

        self.app_name = QLabel(self.app_frame)
        self.app_name.setObjectName(u"app_name")
        self.app_name.setMaximumSize(QSize(500, 16777215))
        font = QFont()
        font.setFamilies([u"Pristina"])
        font.setPointSize(72)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        self.app_name.setFont(font)
        self.app_name.setTextFormat(Qt.AutoText)
        self.app_name.setScaledContents(False)
        self.app_name.setAlignment(Qt.AlignCenter)
        self.app_name.setWordWrap(False)

        self.horizontalLayout_2.addWidget(self.app_name)


        self.gridLayout.addWidget(self.app_frame, 0, 2, 1, 3)

        self.horizontalSpacer_2 = QSpacerItem(233, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 5, 1, 2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.toolButton = QToolButton(home_widget)
        self.toolButton.setObjectName(u"toolButton")
        font1 = QFont()
        font1.setFamilies([u"Poppins"])
        font1.setPointSize(18)
        self.toolButton.setFont(font1)
        icon = QIcon()
        icon.addFile(u":/icons/icons/venn-diagram-svgrepo-com.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.toolButton.setIcon(icon)
        self.toolButton.setIconSize(QSize(28, 28))
        self.toolButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.toolButton.setAutoRaise(True)

        self.horizontalLayout_3.addWidget(self.toolButton)

        self.horizontalSpacer_4 = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.label = QLabel(home_widget)
        self.label.setObjectName(u"label")
        font2 = QFont()
        font2.setFamilies([u"Poppins"])
        font2.setPointSize(11)
        self.label.setFont(font2)
        self.label.setScaledContents(False)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.label_2 = QLabel(home_widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font2)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_2)

        self.label_3 = QLabel(home_widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font2)
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_3.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_3)


        self.gridLayout.addLayout(self.verticalLayout, 1, 1, 2, 2)

        self.horizontalSpacer_8 = QSpacerItem(150, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_8, 1, 3, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_6 = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_6)

        self.toolButton_3 = QToolButton(home_widget)
        self.toolButton_3.setObjectName(u"toolButton_3")
        self.toolButton_3.setFont(font1)
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/perimeter-limit-svgrepo-com.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.toolButton_3.setIcon(icon1)
        self.toolButton_3.setIconSize(QSize(28, 28))
        self.toolButton_3.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.toolButton_3.setAutoRaise(True)

        self.horizontalLayout_4.addWidget(self.toolButton_3)

        self.horizontalSpacer_5 = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_5)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.label_6 = QLabel(home_widget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font2)
        self.label_6.setAlignment(Qt.AlignCenter)
        self.label_6.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_6)

        self.label_5 = QLabel(home_widget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font2)
        self.label_5.setAlignment(Qt.AlignCenter)
        self.label_5.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_5)

        self.label_4 = QLabel(home_widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font2)
        self.label_4.setAlignment(Qt.AlignCenter)
        self.label_4.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_4)


        self.gridLayout.addLayout(self.verticalLayout_2, 1, 4, 2, 2)

        self.horizontalSpacer_7 = QSpacerItem(81, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_7, 2, 0, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(82, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_9, 2, 6, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 100, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer, 3, 2, 1, 1)


        self.retranslateUi(home_widget)

        QMetaObject.connectSlotsByName(home_widget)
    # setupUi

    def retranslateUi(self, home_widget):
        home_widget.setWindowTitle(QCoreApplication.translate("home_widget", u"Form", None))
        self.app_logo.setText("")
        self.app_name.setText(QCoreApplication.translate("home_widget", u"BetterSearch", None))
        self.toolButton.setText(QCoreApplication.translate("home_widget", u"Examples", None))
        self.label.setText(QCoreApplication.translate("home_widget", u"\"What are the largest PDF files on this machine?\"\u23ce", None))
        self.label_2.setText(QCoreApplication.translate("home_widget", u"\"Summarize the specifications of this system.\"\u23ce", None))
        self.label_3.setText(QCoreApplication.translate("home_widget", u"\"How many unique users have logged in on this machine since 10:00 AM?\"\u23ce", None))
        self.toolButton_3.setText(QCoreApplication.translate("home_widget", u"Limitations", None))
        self.label_6.setText(QCoreApplication.translate("home_widget", u"\"What are the largest PDF files on this machine?\"", None))
        self.label_5.setText(QCoreApplication.translate("home_widget", u"\"Summarize the specifications of this system.\"", None))
        self.label_4.setText(QCoreApplication.translate("home_widget", u"\"How many unique users have logged in on this machine since 10:00 AM?\"", None))
    # retranslateUi

