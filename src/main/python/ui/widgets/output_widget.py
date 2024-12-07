# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'output_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
import resource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(995, 121)
        Form.setStyleSheet(u"#Form {\n"
"	background: #fff;\n"
"}")
        self.gridLayout_3 = QGridLayout(Form)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.output_frame = QFrame(Form)
        self.output_frame.setObjectName(u"output_frame")
        self.output_frame.setFrameShape(QFrame.StyledPanel)
        self.output_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.output_frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.frame_2 = QFrame(self.output_frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.output_icon = QLabel(self.frame_2)
        self.output_icon.setObjectName(u"output_icon")
        self.output_icon.setMaximumSize(QSize(32, 32))
        self.output_icon.setFrameShape(QFrame.NoFrame)
        self.output_icon.setPixmap(QPixmap(u":/imgs/images/logo.svg"))
        self.output_icon.setScaledContents(True)
        self.output_icon.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.output_icon)

        self.verticalSpacer = QSpacerItem(20, 24, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.gridLayout_2.addWidget(self.frame_2, 0, 2, 1, 1)

        self.textlabel = QLabel(self.output_frame)
        self.textlabel.setObjectName(u"textlabel")
        self.textlabel.setMinimumSize(QSize(700, 0))

        self.gridLayout_2.addWidget(self.textlabel, 0, 3, 1, 1)

        self.frame_3 = QFrame(self.output_frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_3)
        self.gridLayout.setObjectName(u"gridLayout")
        self.redo_btn = QPushButton(self.frame_3)
        self.redo_btn.setObjectName(u"redo_btn")
        self.redo_btn.setStyleSheet(u"border: none;")
        icon = QIcon()
        icon.addFile(u":/icons/icons/redo-svgrepo-com.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.redo_btn.setIcon(icon)
        self.redo_btn.setIconSize(QSize(14, 14))

        self.gridLayout.addWidget(self.redo_btn, 0, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 42, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 1, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 1, 2, 1, 1)


        self.gridLayout_2.addWidget(self.frame_3, 0, 4, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 1, 1, 1)


        self.gridLayout_3.addWidget(self.output_frame, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.output_icon.setText("")
        self.textlabel.setText(QCoreApplication.translate("Form", u"Text", None))
        self.redo_btn.setText("")
    # retranslateUi

