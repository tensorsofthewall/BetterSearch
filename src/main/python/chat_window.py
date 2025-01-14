from PySide6.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy

from ui.widgets.input_widget import Ui_Form as InputForm
from ui.widgets.output_widget import Ui_Form as OutputForm

class InputWidget(QWidget):
    def __init__(self, parent=None, chat_obj=None):
        super().__init__(parent)
        self.ui = InputForm()
        self.ui.setupUi(self)
        
        self.chat_obj = chat_obj
        
        self.input_label = self.ui.textlabel
        self.edit_btn = self.ui.edit_btn
        
        self.edit_btn.clicked.connect(self.set_edit_text)
        
    def set_input_text(self, input_str):
        self.input_label.setText(input_str)
        
    def set_edit_text(self):
        text = self.input_label.text()
        self.chat_obj.setPlainText(text)
        
class OutputWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.ui = OutputForm()
        self.ui.setupUi(self)
        
        self.out_label = self.ui.textlabel
        
    def set_output_text(self, out_str):
        self.out_label.setText(out_str)
        

class ChatWindow(QWidget):
    def __init__(self, parent=None, chat_obj=None, chat_data=None):
        super().__init__(parent)
        
        self.chat_obj = chat_obj
        self.chat_data = chat_data
        
        self.main_vLayout = QVBoxLayout(self)
        self.main_vLayout.setContentsMargins(0,0,0,0)
        self.main_vLayout.setSpacing(0)
        self.main_vLayout.setObjectName("main_vLayout")
        
        self.style_str = """
        QPushButton,
            QLabel {
                border: none;
                padding: 5px;
            }
            
            QWidget {
                background: #fff;
            }
        """
        
        self.setStyleSheet(self.style_str)
        
        self.chats_data = {
            "title": "",
            "messages": []
        }
        
        if self.chat_data:
            self.chats_data["title"] = self.chat_data["title"]
            self.chats_data["messages"] += self.chat_data["messages"]
            
        print(self.chats_data)
        
        self.show_chats()
        
    def show_chats(self):
        chat_list = self.chats_data.get("messages")
        for chat in chat_list:
            input_str = chat.get("input_str")
            input_widget = InputWidget(chat_obj=self.chat_obj)
            input_widget.set_input_text(input_str)
            self.main_vLayout.addWidget(input_widget)
            
            out_str = chat.get("out_str")
            out_widget = OutputWidget()
            out_widget.set_output_text(out_str)
            self.main_vLayout.addWidget(out_widget)
            
        spacerItem = QSpacerItem(20,400,QSizePolicy.Minimum,QSizePolicy.Expanding)
        self.main_vLayout.addItem(spacerItem)
        self.setLayout(self.main_vLayout)
        