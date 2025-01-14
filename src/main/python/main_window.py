from PySide6.QtWidgets import QMainWindow, QGridLayout, QLabel, QPushButton, QFrame, QLineEdit
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon

# Toast for showing messages
from pyqttoast import Toast, ToastPreset, ToastIcon

from pipeline_thread import PipelineStarter, PipelineExecutor
from ui.widgets.main import Ui_MainWindow

from home_window import HomeWindow
from chat_window import ChatWindow
from chat_db import ChatDB
from bettersearch.pipeline.pipeline import BetterSearchPipeline

from chat_block_widget import ChatBlockWidget


class MainWindow(QMainWindow):
    def __init__(self, **kwargs):
        super().__init__()
        self.pipeline=None
        
        # Initialize the Main Window
        self.ui= Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Init Chat DB and BetterSearch pipeline
        self.chat_db = ChatDB(**kwargs)
        
        # Start pipeline in a separate thread
        self._start_pipeline_thread(**kwargs)
        
        # Get objects available in Main Window
        self.message_input = self.ui.text_input_area
        self.new_chat_btn = self.ui.new_chat
        self.clear_chats_btn = self.ui.clear_chats
        self.output_scrollArea = self.ui.output_area
        self.input_frame = self.ui.input_frame
        self.send_msg_btn = self.ui.send_btn
        
        # Show scrollbar if needed
        self.output_scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Resize input frame and text input area
        self.message_input.setFixedHeight(48)
        self.input_frame.setFixedHeight(84)
        
        # Set data for chat list and current chat messages
        self.show_chat_list()
        self.show_home_window()
        
        # Set signals and slots
        self.send_msg_btn.clicked.connect(self.get_response)
        self.new_chat_btn.clicked.connect(self.create_new_chat)
        self.clear_chats_btn.clicked.connect(self.clear_chats)
        
    def get_response(self):
        msg_input = self.message_input.toMarkdown().strip()
        
        chat_db = self.chat_db.get_chat_data()
        
        if msg_input:
            self.pipeline_executor.finished.connect(lambda output: self.process_pipeline_output(output, chat_db))
            self.pipeline_executor.start(prompt=msg_input)
        else:
            return
    
    def process_pipeline_output(self, output, chat_db):
        if self.ui.chat_list.selectedIndexes():
            curr_idx = self.ui.chat_list.currentIndex()
            curr_row = curr_idx.row()+1
            
            chat_db[curr_row]["messages"] += [{"input_str": self.message_input.toMarkdown().strip(), "out_str": output}]
            
            chat_data = chat_db[curr_row]
            
            # Reload window
            self.chat_db.save_chat_data(**chat_db)
            self.show_chat_window(chat_data)
        
        else:
            chat_data = {
                "title": self.message_input.toPlainText().strip(),
                "messages": [
                    {
                        "input_str": self.message_input.toMarkdown().strip(),
                        "out_str": output
                    }
                ]
            }
            
            chat_db.update(chat_data)
            self.chat_db.save_chat_data(**chat_data)
            
            # Reload window
            self.show_chat_window(chat_data)
            self.show_chat_list(selected_index=0)
        
        self.message_input.clear()
        # self.message_input.setEnabled(True)
        # self.send_msg_btn.setEnabled(True)
    
    def _start_pipeline_thread(self, **kwargs):
        if self.pipeline is not None:
            # Clean up old pipeline if exists
            del self.pipeline
            self.pipeline = None
        
        # Start pipeline in a separate thread
        self.pipeline_starter = PipelineStarter(self, parent=None,**kwargs)
        self.pipeline_starter.started.connect(self._pipeline_starting)
        self.pipeline_starter.finished.connect(self._pipeline_ready)
        
        self.pipeline_starter.start()
    
    def _pipeline_starting(self):
        
        # Disable input and send button while waiting for pipeline to start
        self.message_input.setDisabled(True)
        self.send_msg_btn.setDisabled(True)
        
        # Display toast to show that pipeline is starting
        toast = Toast(self)
        toast.setDuration(15000)
        toast.setAlwaysOnMainScreen(True)
        toast.setShowDurationBar(False)
        toast.setIcon(ToastIcon.INFORMATION)
        toast.setShowIcon(True)
        toast.setText('Starting Pipeline...')
        toast.applyPreset(ToastPreset.INFORMATION)
        toast.show()
        
    def _pipeline_ready(self):
        toast = Toast(self)
        toast.setDuration(8000)
        toast.setAlwaysOnMainScreen(True)
        toast.setShowDurationBar(False)
        toast.setIcon(ToastIcon.SUCCESS)
        toast.setShowIcon(True)
        toast.setText('Pipeline is ready to use!')
        toast.applyPreset(ToastPreset.SUCCESS)
        toast.show()
        
        # Handle tasks to be done after pipeline is ready
        self.message_input.setEnabled(True)
        self.send_msg_btn.setEnabled(True)
        self.message_input.setFocus()
        
        # Setup executor
        self.pipeline_executor = PipelineExecutor(self.pipeline)
        self.pipeline_executor.started.connect(self._pipeline_execute_start)
        
    def _execute_pipeline_thread(self):
        pass
    def _pipeline_execute_start(self):
        # Display toast to show that pipeline is starting
        toast = Toast(self)
        toast.setDuration(5000)
        toast.setAlwaysOnMainScreen(True)
        toast.setShowDurationBar(False)
        toast.setIcon(ToastIcon.INFORMATION)
        toast.setShowIcon(True)
        toast.setText('BetterSearch is working on your request. Please wait...')
        toast.applyPreset(ToastPreset.INFORMATION)
        toast.show()
    
    def get_pipeline(self, **kwargs):
        self.pipeline = BetterSearchPipeline(**kwargs)
    
    # Show default window if no chat is selected
    def show_home_window(self):
        """
        Show the home window if no chat is selected.

        This method clears the QGridLayout inside the output scroll area and
        adds a new HomeWindow widget to the grid layout.

        """
        grid_layout = self.clear_output_scroll_area()
        home_window = HomeWindow()
        grid_layout.addWidget(home_window)
        
    def clear_output_scroll_area(self):
        # Get QGridLayout object
        """
        Clear the QGridLayout inside the output scroll area and remove all widgets from it.

        This method is used to clear the output window when a new chat is selected or when the
        "Clear Chats" button is clicked.

        :return: The cleared QGridLayout object
        """
        grid_layout = self.output_scrollArea.findChild(QGridLayout)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        
        # Get all objects in main chat window
        children_list = grid_layout.children()
        
        remove_widget_list = [QLabel, QPushButton, QFrame]
        
        # Add widgets to be removed from main chat window
        for remove_widget in remove_widget_list:
            children_list += self.output_scrollArea.findChildren(remove_widget)
        
        for child in children_list:
            child.deleteLater()
            
        for row in range(grid_layout.rowCount()):
            for col in range(grid_layout.columnCount()):
                item = grid_layout.itemAtPosition(row, col)
                if item:
                    grid_layout.removeItem(item)
                    
        return grid_layout
    
    # Show list of chats in sidebar
    def show_chat_list(self, selected_index=None):
        itemModel = QStandardItemModel()
        self.ui.chat_list.setModel(itemModel)
        
        chat_list = self.chat_db.get_chat_title_list()
        
        for chat in chat_list:
            item = QStandardItem()
            itemModel.appendRow(item)
            
            index = item.index()
            index_text = index.row()+1
            
            if index_text == selected_index:
                show_btn_flag = True
                self.ui.chat_list.setCurrentIndex(index)
            else:
                show_btn_flag = False
            
            # Create chat title widget    
            widget = ChatBlockWidget(chat, show_btn_flag)
            
            # Show chat title in sidebar
            self.ui.chat_list.setIndexWidget(index, widget)
            
            operation_btn = widget.findChildren(QPushButton)
            
            # Connect buttons to signals and methods
            edit_btn = operation_btn[2]
            edit_btn.clicked.connect(self.edit_chat)
            
            delete_btn = operation_btn[1]
            delete_btn.clicked.connect(self.delete_chat)
            
            
    @Slot()
    def edit_chat(self):
        currIndex = self.ui.chat_list.currentIndex()
        current_chat = self.ui.chat_list.indexWidget(currIndex)
        
        chat_title = current_chat.findChild(QLineEdit)
        
        # Get original chat title
        pre_chat_title = chat_title.text()
        
        chat_title.setReadOnly(False)
        
        # QLineEdit StyleSheet
        chat_title_style = """
            QLineEdit {
                background:transparent;
                border: 1px solid #2563eb;
                color: #fff;
                font-size: 15px;
                padding-left: 2px;
            }
        """
        
        chat_title.setStyleSheet(chat_title_style)
        
        operation_btns = current_chat.findChildren(QPushButton)
        confirm_btn = operation_btns[2]
        cancel_btn = operation_btns[1]
        
        confirm_btn.setIcon(QIcon(u':/icons/icons/check-svgrepo-com.svg'))
        cancel_btn.setIcon(QIcon(u':/icons/icons/cross-svgrepo-com.svg'))
        
        confirm_btn.clicked.disconnect()
        cancel_btn.clicked.disconnect()
        
        confirm_btn.clicked.connect(lambda: self.confirm_edit(chat_title))
        cancel_btn.clicked.connect(lambda: self.cancel_edit(pre_chat_title, chat_title))
    
    @Slot()
    def confirm_edit(self, chat_title):
        curr_index = self.ui.chat_list.currentIndex().row()+1
        
        chat_db = self.chat_db.get_chat_data()
        chat_db[curr_index]["title"] = chat_title.text()
        
        self.chat_db.save_chat_data(chat_db)
        self.on_chat_list_clicked()
        
    
    @Slot()
    def cancel_edit(self, pre_chat_title, chat_title):
        chat_title.setText(pre_chat_title)
        self.on_chat_list_clicked()
    
    
    @Slot()
    def delete_chat(self):
        # Get current selected chat index
        selected_chat_index = self.ui.chat_list.currentIndex()
        index = selected_chat_index.row()+1
        
        # Delete chat from database
        self.chat_db.delete_chat_data(index)
        
        # Reload window
        self.show_home_window()
        self.show_chat_list()
    
    # Signal and slot function for chat list modifications (QListView)
    def on_chat_list_clicked(self):
        chat_list = []
        
        # Clear input when change chat
        self.message_input.clear()
        
        # Get current selected chat index
        curr_index = self.ui.chat_list.currentIndex()
        curr_row = curr_index.row()+1
        
        # Get count of chat list
        chat_models = self.ui.chat_list.model()
        chat_count = chat_models.rowCount()
        
        # Traverse chat list
        for i in range(chat_count):
            row_idx = chat_models.index(i,0)
            curr_chat = self.ui.chat_list.indexWidget(row_idx)
            chat_title = curr_chat.findChild(QLineEdit)
            
            if chat_title:
                # Check if chat state is waiting to delete
                if i == curr_row and chat_title.text().startswith("Delete \""):
                    chat_list.append(chat_title.text().split('"')[1])
                else:
                    chat_list.append(chat_title.text())
            else:
                chat_list.append("")
        
        # Reload chats
        for row, chat in enumerate(chat_list):
            index = chat_models.index(row,0)
            
            # Check if the chat title is selected
            if row == curr_row:
                show_btn_flag = True
            else:
                show_btn_flag = False
            
            widget = ChatBlockWidget(chat, show_btn_flag)
            
            # Set and show chat title in chat list(QListView)
            self.ui.chat_list.setIndexWidget(index, widget)

            # Get QPushButton object in  chat title widget
            operation_btn = widget.findChildren(QPushButton)

            # Connect signal and slot for buttons
            edit_btn = operation_btn[2]
            edit_btn.clicked.connect(self.edit_chat)

            delete_btn = operation_btn[1]
            delete_btn.clicked.connect(self.delete_chat)
            
        # Get selected chat data and show in main output window
        chat_db = self.chat_db.get_chat_data()
        chat_data = chat_db[curr_row]
        print("Chat Data before display: ",chat_data)
        self.show_chat_window(chat_data)
    
    
    # Create new chat    
    def create_new_chat(self):
        self.show_home_window()
        self.show_chat_list(selected_index=None)
    
    # Delete all chats from chat list
    def clear_chats(self):
        self.chat_db.delete_all_data()
        self.show_home_window()
        self.show_chat_list()
        
    # Show the chat ddata in main output window
    def show_chat_window(self, chat_data):
        grid_layout = self.clear_output_scroll_area()
        
        # show new message
        chat_window = ChatWindow(chat_obj=self.message_input, chat_data=chat_data)
        grid_layout.addWidget(chat_window)
        
        