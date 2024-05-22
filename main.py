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
    linhaContato = listarContatos.tabelaContatos.currentRow()
    listarContatos.tabelaContatos.removeRow(linhaContato)
    
    cursor = banco.cursor()
    cursor.execute(f"select id from tbl_contatos")
    contatos_lidos = cursor.fetchall()
    valorId= contatos_lidos[linhaContato][0]
    cursor.execute(f"Delete from tbl_contatos where id = {str(valorId)}")
    banco.commit()
    
    
    
def GerarPDF():
    cursor = banco.cursor()
    cursor.execute("Select * from tbl_contatos")
    contatosLidos = cursor.fetchall()
    
    y = 0
    pdf = canvas.Canvas("Lista_contatos.pdf")
    pdf.setFont("Times-Bold", 20)
    pdf.drawString(200,800, "Lista de contatos")
    pdf.setFont("Times-Bold", 10)
    pdf.drawString(10,750, "ID")
    pdf.drawString(110,750, "NOME")
    pdf.drawString(210,750, "EMAIL")
    pdf.drawString(410,750, "TELEFONE")
    pdf.drawString(490,750, "TIPO DE CONTATO")
    
    for i in range (0, len(contatosLidos)):
        y = y+50
        pdf.drawString(10,750 - y, str(contatosLidos[i][0]))
        pdf.drawString(110,750 - y, str(contatosLidos[i][1]))
        pdf.drawString(210,750 - y, str(contatosLidos[i][2]))
        pdf.drawString(410,750 - y, str(contatosLidos[i][3]))
        pdf.drawString(490,750 - y, str(contatosLidos[i][4]))
    pdf.save()
    print('PDF gerado com sucesso!')
    
def EsconderJanela():
    listarContatos.hide()
    agenda.show()
    

listarContatos.voltarButton.clicked.connect(EsconderJanela)
listarContatos.deleteButton.clicked.connect(Excluir)
listarContatos.pdfButton.clicked.connect(GerarPDF)
agenda.cadButton.clicked.connect(Cadastro)
agenda.consButton.clicked.connect(Consultar)
agenda.show()
app.exec()