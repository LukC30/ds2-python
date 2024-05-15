from PyQt5 import uic, QtWidgets
import mysql.connector

from reportlab.pdfgen import canvas
app = QtWidgets.QApplication([])

agenda = uic.loadUi('Agenda.ui')
listarContatos = uic.loadUi("ListaCadastro.ui")
agenda.btnConsultar.clicked

banco = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_agenda"
)

if(banco):
    print("Estamos dentro do cu do guilherme")

# def main():
#     nome = agenda.
    
def main():
    name = agenda.textNome.text()
    email = agenda.textEmail.text()
    telefone = agenda.textTelefone.text()
    
    isChecked = ""
    
    if agenda.checkedResidencial.isChecked():
        isChecked = "Residencial"
    elif agenda.checkedCasa.isChecked():
        isChecked = "celular"
    else:
        isChecked = 'comi o do meu lado esquerdo'
        isChecked = "não informado"
    
    try:
        cursor =  banco.cursor()
        cursor.execute(f"Insert into tbl_contatos(nome, email, telefone, tipo_telefone)values('{name}','{email}','{telefone}','{isChecked}')")    
        banco.commit()
        print("O cadastro da sua agenda foi feito!")
    except Exception as e:
        print(f"Sua requisição nao deu certo veja: {e}")    

agenda.cadButton.clicked.connect(main)

agenda.show()
app.exec()