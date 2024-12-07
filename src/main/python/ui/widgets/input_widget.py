# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'input_widget.ui'
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
from .static import resource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(846, 123)
        Form.setStyleSheet(u"#Form {\n"
"	background: #fff;\n"
"}")
        self.gridLayout_3 = QGridLayout(Form)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.input_frame = QFrame(Form)
        self.input_frame.setObjectName(u"input_frame")
        self.input_frame.setFrameShape(QFrame.StyledPanel)
        self.input_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.input_frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.textlabel = QLabel(self.input_frame)
        self.textlabel.setObjectName(u"textlabel")
        self.textlabel.setMinimumSize(QSize(700, 0))

        self.gridLayout_2.addWidget(self.textlabel, 0, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.frame_2 = QFrame(self.input_frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.input_icon = QLabel(self.frame_2)
        self.input_icon.setObjectName(u"input_icon")
        self.input_icon.setMaximumSize(QSize(32, 32))
        self.input_icon.setFrameShape(QFrame.NoFrame)
        self.input_icon.setPixmap(QPixmap(u":/icons/icons/user-circle-svgrepo-com.svg"))
        self.input_icon.setScaledContents(True)
        self.input_icon.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.input_icon)

        self.verticalSpacer = QSpacerItem(20, 42, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.gridLayout_2.addWidget(self.frame_2, 0, 2, 1, 1)

        self.frame_3 = QFrame(self.input_frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_3)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 1, 0, 1, 2)

        self.edit_btn = QPushButton(self.frame_3)
        self.edit_btn.setObjectName(u"edit_btn")
        self.edit_btn.setStyleSheet(u"border: none;")
        icon = QIcon()
        icon.addFile(u":/icons/icons/edit-3-svgrepo-com.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.edit_btn.setIcon(icon)
        self.edit_btn.setIconSize(QSize(14, 14))

        self.gridLayout.addWidget(self.edit_btn, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_3, 0, 4, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_3, 0, 5, 1, 1)


        self.gridLayout_3.addWidget(self.input_frame, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.textlabel.setText(QCoreApplication.translate("Form", u"Text", None))
        self.input_icon.setText("")
        self.edit_btn.setText("")
    # retranslateUi

