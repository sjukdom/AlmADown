from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import subprocess
import sys
import re


class MainWindow(QMainWindow):

   def __init__(self):

      super().__init__()
      
      ### Useful attributes
      self.download_mode = 'Video'

      ### Window configs
      self.setWindowTitle('AlmADown')
      self.setFixedSize(400, 500)

      ### Status bar
      self.statusBar()

      ### Widgets
      self.text_edit = QTextEdit()
      self.button = QPushButton('Download')
      self.progress_bar = QProgressBar()
      self.check_box = QCheckBox('Video')
      # Widget's handlers
      self.button.pressed.connect(self.download)
      self.check_box.stateChanged.connect(self.change_download_mode)

      ### Actions (for the menu bar items)
      openAction = QAction('Open', self)
      openAction.setShortcut('Ctrl+O')
      openAction.triggered.connect(self.open_file)
      exitAction = QAction('Exit', self)
      exitAction.setShortcut('Ctrl+Q')
      exitAction.triggered.connect(qApp.quit)
      modeAction = QAction('Video', self, checkable=True, checked=True)
      modeAction.setShortcut('Ctrl+D')
      modeAction.triggered.connect(self.change_download_mode)

      ### Menubar and its elements
      menubar = self.menuBar()
      menubar.setNativeMenuBar(False)
      # Adding items to the menu
      fileMenu = menubar.addMenu('&File')
      settingsMenu = menubar.addMenu('&Settings')
      # Adding actions to the items
      fileMenu.addAction(openAction)
      fileMenu.addAction(exitAction)
      settingsMenu.addAction(modeAction)

      ### Layouts
      layout_main = QVBoxLayout()
      layout_bottom = QHBoxLayout()
      # Adding widgets to layouts
      layout_main.addWidget(self.text_edit)
      layout_bottom.addWidget(self.progress_bar)
      layout_bottom.addWidget(self.button)
      # Adding layouts to the main layout
      layout_main.addLayout(layout_bottom)

      ### Main widget
      widget = QWidget()
      widget.setLayout(layout_main)
      self.setCentralWidget(widget)

   def open_file(self):
      file_name = QFileDialog.getOpenFileName(self, 'Open File')
      if file_name[0] != "":
         with open(file_name[0], 'r') as f:
            text = f.read()
            self.text_edit.setText(text)

   def download(self):
      media_list = self.text_edit.toPlainText().split()
      total = len(media_list)
      for index, media in enumerate(media_list, 1):
         if self.download_mode == "Video":
            command = subprocess.run(["youtube-dl", "--quiet", media], capture_output=True)
            if command.returncode == 1:
               QMessageBox().about(self, "Error", "The link is not valid")
            else:
               self.update_progress_bar(index, total)
         else:    
            command = subprocess.run(["youtube-dl", "--quiet", "--extract-audio", "--audio-format", "mp3", media], capture_output=True)
            if command.returncode == 1:
               QMessageBox().about(self, "Error", "The link is not valid")
            else:
               self.update_progress_bar(index, total)
      self.statusBar().showMessage("All the media was downloaded")

   def update_progress_bar(self, current, total):
      percentage = current/total * 100
      self.progress_bar.setValue(percentage)

   def change_download_mode(self, state):
      if state == True:
         self.download_mode = 'Video'
      else:
         self.download_mode = 'Audio'
      self.statusBar().showMessage(self.download_mode + ' download mode selected')

if __name__ == '__main__':
   app = QApplication([])
   window = MainWindow()
   window.show()
   sys.exit(app.exec_())