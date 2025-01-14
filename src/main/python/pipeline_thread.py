from PySide6.QtCore import QThread, Signal


class PipelineStarter(QThread):
    """
    Worker thread to run the pipeline setup without blocking the main UI.
    """
    # finished = Signal()
    
    def __init__(self, app, parent=None, **kwargs):
        super().__init__(parent)
        self.app = app
        self.kwargs = {**kwargs}
    
    def run(self):
        """
        Run the pipeline setup in the background.

        The finished signal is emitted after the pipeline setup is complete.
        """
        self.app.get_pipeline(**self.kwargs)
        self.finished.emit()


class PipelineExecutor(QThread):
    """
    Worker thread to generate answers without blocking the main UI.
    """
    finished = Signal(str)
    
    def __init__(self, pipeline, parent=None):
        super().__init__(parent)
        self.pipeline = pipeline
    
    def run(self):
        output = self.pipeline(user_question=self.prompt)
        self.finished.emit(output)
        
    def start(self, prompt):
        self.prompt = prompt
        super().start()
        
    