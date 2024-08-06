from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QVBoxLayout, QPushButton, QWidget, QLabel
from PyQt6.QtGui import QKeyEvent, QTextCursor, QFont, QAction
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import sys, os
import configparser

from bettersearch.src.pipeline import BetterSearchPipeline
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

option_to_cfg_file = {
    "CPU-Only": "cpu_only.json",
    "GPU VRAM < 10GB": "budget_gpu_config.json",
    "GPU VRAM < 16GB": "normal_gpu_config.json",
    "GPU VRAM > 16GB": "overkill_gpu_config.json"
}

class PipelineWorker(QThread):
    """
    Worker thread to run the pipeline setup without blocking the main UI.
    """
    finished = pyqtSignal()
    
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app
    
    def run(self):
        self.app.get_pipeline()
        self.finished.emit()
        
class AnswerWorker(QThread):
    """
    Worker thread to generate answers without blocking the main UI.
    """
    answer_ready = pyqtSignal(str)

    def __init__(self, pipeline, question, parent=None):
        super().__init__(parent)
        self.pipeline = pipeline
        self.question = question

    def run(self):
        answer = self.pipeline.answer(user_question=self.question)
        self.answer_ready.emit(answer)

class CustomLineEdit(QLineEdit):
    """
    Custom QLineEdit that triggers the main window's send_message method
    when the Enter key is pressed.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent  # Store a reference to the main window

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Return:  # Check if Enter key is pressed
            if self.main_window:  # Ensure that the reference to the main window is valid
                self.main_window.send_message()  # Call the main window's send_message method
        else:
            super().keyPressEvent(event)

class BetterSearchApp(QMainWindow):
    """
    Main application window for the BetterSearch App. Handles user interactions,
    settings management, and communication with the backend pipeline.
    """
    def __init__(self) -> None:
        super().__init__()
        
        self.default_settings = os.path.join(BASE_DIR, "settings.cfg")
        self.pipeline = None

        self.setWindowTitle("BetterSearch App")
        self.setGeometry(100, 100, 900, 600)

        # Initialize the central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Initialize chat display area
        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Arial",14))
        self.layout.addWidget(self.chat_display)

        # Add an initial welcome message
        self.append_message("BetterSearch", "Hi! I'm BetterSearch, and I can help you find information regarding your files. Let me finish setting up...", "green")

        # Initialize user input field
        self.user_input = CustomLineEdit(self)
        self.layout.addWidget(self.user_input)

        # Initialize Send button
        self.send_button = QPushButton("Send", self)
        self.layout.addWidget(self.send_button)
        self.send_button.clicked.connect(self.send_message)

        # Initialize status label
        self.status_label = QLabel(self)
        self.layout.addWidget(self.status_label)

        # Create menu for compute mode settings        
        self.create_menu()
        
        # Load default configuration
        self.get_default_config()
        self.get_compute_mode()
        
        # Start pipeline in separate thread
        self.start_pipeline_thread()
        
    def start_pipeline_thread(self):
        if self.pipeline:
            # Clean up old pipeline if it exists
            del self.pipeline
            self.pipeline = None
        
        # Start pipeline setup in a separate thread
        self.pipeline_worker = PipelineWorker(self)
        self.pipeline_worker.finished.connect(self.pipeline_ready)
        self.pipeline_worker.start()
        
    def pipeline_ready(self):
        """
        Handle tasks to be done after the pipeline is ready.
        """
        self.status_label.setText("Pipeline is ready")
        self.append_message("BetterSearch", "I'm ready to answer your queries. What would you like to know?", "green")
        
        # Re-enable input and send button after processing
        self.user_input.setEnabled(True)
        self.send_button.setEnabled(True)
        self.user_input.setFocus()
        
    def get_pipeline(self):
        """
        Load and configure the pipeline based on the selected compute mode.
        """
        with open(os.path.join(BASE_DIR, option_to_cfg_file.get(self.selected_option)), 'r') as file:
            config = json.load(file)
        self.pipeline = BetterSearchPipeline(**config)
    
    def get_default_config(self):
        """
        Load the default configuration from the settings file.
        """
        self.default_config = configparser.ConfigParser()
        self.default_config.read(self.default_settings)
        
    def set_default_config(self):
        """
        Save the currently selected option to the configuration file.
        """
        self.default_config['Compute Mode']['config_file'] = self.selected_option
        with open(self.default_settings, 'w') as configfile:
            self.default_config.write(configfile)
        
    def create_menu(self):
        """
        Create the menu bar and add actions for selecting compute modes.
        """
        self.menu_bar = self.menuBar()
        settings_menu = self.menu_bar.addMenu("Compute Mode")
        
        # Define actions for each compute mode
        self.cpu_only_action = QAction("CPU-Only", self, checkable=True)
        self.gpu_vram_less_10gb_action = QAction("GPU VRAM < 10GB", self, checkable=True)
        self.gpu_vram_less_16gb_action = QAction("GPU VRAM < 16GB", self, checkable=True)
        self.gpu_vram_more_16gb_action = QAction("GPU VRAM > 16GB", self, checkable=True)

        # Add actions to the menu
        settings_menu.addAction(self.cpu_only_action)
        settings_menu.addAction(self.gpu_vram_less_10gb_action)
        settings_menu.addAction(self.gpu_vram_less_16gb_action)
        settings_menu.addAction(self.gpu_vram_more_16gb_action)
        
        # Connect actions to the method that handles option selection
        self.cpu_only_action.triggered.connect(self.set_option)
        self.gpu_vram_less_10gb_action.triggered.connect(self.set_option)
        self.gpu_vram_less_16gb_action.triggered.connect(self.set_option)
        self.gpu_vram_more_16gb_action.triggered.connect(self.set_option)
        
    def set_option(self):
        """
        Handle the selection of a compute mode option and update the configuration.
        """
        action = self.sender()
        if action:
            self.deselect_all()
            action.setChecked(True)
            self.selected_option = action.text()
            self.set_default_config()
            self.start_pipeline_thread()
            
    def get_compute_mode(self):
        """
        Set the initial state of the menu based on the saved configuration.
        """
        if self.default_config['Compute Mode']['config_file'] == "CPU-Only":
            self.cpu_only_action.setChecked(True)
            self.selected_option = self.cpu_only_action.text()
        elif self.default_config['Compute Mode']['config_file'] == "GPU VRAM < 10GB":
            self.gpu_vram_less_10gb_action.setChecked(True)
            self.selected_option = self.gpu_vram_less_10gb_action.text()
        elif self.default_config['Compute Mode']['config_file'] == "GPU VRAM < 16GB":
            self.gpu_vram_less_16gb_action.setChecked(True)
            self.selected_option = self.gpu_vram_less_16gb_action.text()
        elif self.default_config['Compute Mode']['config_file'] == "GPU VRAM > 16GB":
            self.gpu_vram_more_16gb_action.setChecked(True)
            self.selected_option = self.gpu_vram_more_16gb_action.text()
        
    def send_message(self):
        """
        Handle sending of a user message. Append the message to the chat display
        and get a response from the backend.
        """
        user_question = self.user_input.text()
        if user_question:
            self.append_message("You", user_question, "blue")
            self.user_input.clear()
            
            # Disable input and send button while processing
            self.user_input.setEnabled(False)
            self.send_button.setEnabled(False)

            # Start the answer worker thread
            if self.pipeline:  # Ensure pipeline is not None
                self.answer_worker = AnswerWorker(self.pipeline, user_question)
                self.answer_worker.answer_ready.connect(self.display_answer)
                self.status_label.setText("Pipeline is running")
                self.answer_worker.start()
            else:
                self.append_message("BetterSearch", "Pipeline is not ready yet. Please wait.", "red")

    def display_answer(self, answer):
        """
        Display the generated answer in the chat display.
        """
        self.append_message("BetterSearch", answer, "green")
        
        # Re-enable input and send button after processing
        self.user_input.setEnabled(True)
        self.send_button.setEnabled(True)
        self.user_input.setFocus()
        
        self.status_label.setText("Pipeline is ready")
    
    
    def deselect_all(self):
        """
        Deselect all compute mode options in the menu.
        """
        self.cpu_only_action.setChecked(False)
        self.gpu_vram_less_10gb_action.setChecked(False)
        self.gpu_vram_less_16gb_action.setChecked(False)
        self.gpu_vram_more_16gb_action.setChecked(False)

    def append_message(self, sender, message, color):
        """
        Append a message to the chat display with the specified sender and color.

        :param sender: The name of the sender (e.g., "You" or "BetterSearch")
        :param message: The message text
        :param color: The color to use for the sender's name
        """
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)

        cursor.insertHtml(f'<b style="color: {color};">{sender}:</b><br>')
        cursor.insertHtml(f'{message}<br><br>')

        self.chat_display.setTextCursor(cursor)
        self.chat_display.ensureCursorVisible()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    chat_app = BetterSearchApp()
    chat_app.show()
    sys.exit(app.exec())