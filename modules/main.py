from PyQt5.QtWidgets import QApplication
from MainController import MainController
from MainWindow import MainWindow


if __name__ == "__main__":
    app = QApplication([])
    main_controller = MainController()
    window = MainWindow(main_controller)
    window.show()
    app.exec_()
