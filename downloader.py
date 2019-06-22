from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys


class MainWindow(QMainWindow):

   def __init__(self):

      super().__init__()
      
      ### Useful attributes
      self.download_mode = 'Video'

      ### Window configs
      self.setWindowTitle('YouDownMe')
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
      if file_name:
         with open(file_name[0], 'r') as f:
            text = f.read()
            self.text_edit.setText(text)

   def download(self):
      pass

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