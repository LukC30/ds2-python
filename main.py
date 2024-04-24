from PyQt5 import uic, QtWidgets

def main():
    print("Etec")
    
app = QtWidgets.QApplication([])

agenda = uic.loadUi('Agenda.ui')
agenda.cadButton.clicked.connect(main)

agenda.show()
app.exec()