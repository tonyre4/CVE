import logging
from Tkinter import *

class logO(logging.Handler):

    def __init__(self, textwdg):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.textwdg = textwdg
        # Logging configuration
        logging.basicConfig(filename='test.log',
                            level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        # Add the handler to logger
        logger = logging.getLogger()
        logger.addHandler(self)

    def emit(self, record):
        msg = self.format(record)

        def append():
            self.textwdg.configure(state='normal')
            self.textwdg.insert(END, msg + '\n')
            self.textwdg.configure(state='disabled')
            # Autoscroll to the bottom
            self.textwdg.yview(END)
        # This is necessary because we can't modify the Text from other threads
        self.textwdg.after(0, append)

    def printlog(self,msg):
        logging.info(msg)
