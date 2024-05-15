from PyQt5 import uic, QtWidgets
import mysql.connector

from reportlab.pdfgen import canvas
app = QtWidgets.QApplication([])

agenda = uic.loadUi('Agenda.ui')
listarContatos = uic.loadUi("ListaCadastro.ui")

banco = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_agenda"
)

if(banco):
    print("Estamos dentro do cu do guilherme")

# 
    
def Cadastro():
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

def Consultar ():
    print("Entramos no cu do guilherme dnv")
    listarContatos.show()
    agenda.hide()
    cursor = banco.cursor()
    
    cursor.execute('select * from tbl_contatos')
    dados = cursor.fetchall()
    listarContatos.tabelaContatos.setRowCount(len(dados))
    listarContatos.tabelaContatos.setColumnCount(5)
    
    for i in range(0, len(dados)):
        for f in range (0,5):
            listarContatos.tabelaContatos.setItem(i, f, QtWidgets.QTableWidgetItem(str(dados[i][f])))

def Excluir():
    row = listarContatos.tabelaContatos.clicked()
    cursor = banco.cursor()
    cursor.execute(f'delete from tbl_contatos where id = {row[0]}')

    
def EsconderJanela():
    listarContatos.hide()
    agenda.show()
    

listarContatos.voltarButton.clicked.connect(EsconderJanela)

agenda.cadButton.clicked.connect(Cadastro)
agenda.consButton.clicked.connect(Consultar)
agenda.show()
app.exec()