from PySide6.QtWidgets import QPushButton, QWidget, QHBoxLayout, QLineEdit
from PySide6.QtGui import QIcon
from ui.widgets.static import resource_rc

class ChatBlockWidget(QWidget):
    """
    This widget creates chats in the chat list.
    """
    def __init__(self, text, show_btn_flag, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5,0,0,0)
        
        # Create Icon widget of the chat
        chat_icon = QIcon(u":/icons/icons/chat-round-dots-svgrepo-com.svg")
        chat_icon_btn = QPushButton(self)
        chat_icon_btn.setIcon(chat_icon)
        
        # create title widget to show chat title
        chat_title=QLineEdit(self)
        chat_title.setText(text)
        chat_title.setReadOnly(True)
        chat_title.home(False)
        # chat_title.textChanged.connect(lambda: chat_title.home(False))
        
        # Create delete and edit buttons for chat title
        delete_btn = QPushButton(self)
        delete_btn.setIcon(QIcon(u":/icons/icons/trash3-fill.svg"))

        edit_btn = QPushButton(self)
        edit_btn.setIcon(QIcon(u":/icons/icons/edit-3-svgrepo-com.svg"))
        
        # QPushButton and QTextEdit StyleSheets
        push_btn_style_str = """
            QPushButton {
                border: none;
                max-width: 30px;
                max-height: 30px;
                background:transparent;
            }
        """
        
        chat_title_style = """
            QLineEdit {
                background:transparent;
                border: none;
                color: #fff;
                font-size: 15px;
                padding-left: 2px;
            }
        """
        
        chat_title.setStyleSheet(chat_title_style)
        chat_icon_btn.setStyleSheet(push_btn_style_str)
        
        edit_btn.setStyleSheet(push_btn_style_str)
        delete_btn.setStyleSheet(push_btn_style_str)

        if not show_btn_flag:
            delete_btn.hide()
            edit_btn.hide()
        
        layout.addWidget(chat_icon_btn)
        layout.addWidget(chat_title)
        layout.addWidget(edit_btn)
        layout.addWidget(delete_btn)
    