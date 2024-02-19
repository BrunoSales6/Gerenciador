import sqlite3  # importa sqlite
from PyQt5.QtWidgets import *  # importa todos os widgets
from PyQt5.QtGui import *  # importa todos os recursos gráficos
import sys  # importa algumas variavies
import os 
from os import path  # importa o módulo pathpara manipular caminho de arquivos
from PyQt5.uic import loadUiType  # classe que carrega um arquivo de extensão .ui
def resource_path(relative_path): #função do py-to-exe
    '''GET absolute path to resource, works for dev and for PyInstaller'''
    base_path=getattr(sys,'_MEIPASS',os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path,relative_path)

# Carregando Interface e criando uma classe a parti dela
FORM_CLASS, _ = loadUiType(resource_path("GUI.ui"))


# Classe Main que define tudo da interface.
class Main(QMainWindow, FORM_CLASS):
    def __init__(self):
        super(Main, self).__init__()
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_Buttons()
        self.NAVEGAR()

    def Handel_Buttons(self):  # Trnasmite os sinais dos botões da interface para os slots
        self.atualizar.clicked.connect(self.GET_DATA)
        self.procura_botao.clicked.connect(self.PROCURAR)
        self.verificar_inventario.clicked.connect(self.VERIFICAR)
        self.update_btn.clicked.connect(self.UPDATE)
        self.delete_btn.clicked.connect(self.DELETAR)
        self.add_btn.clicked.connect(self.ADICIONAR)
        self.next_btn.clicked.connect(self.PROXIMO)
        self.previous_btn.clicked.connect(self.ANTERIOR)
        self.first_btn.clicked.connect(self.PRIMEIRO)
        self.last_btn.clicked.connect(self.ULTIMO)

    # Se conecta com o SQL lite database e adiciona as informações da batabase na interface.
    def GET_DATA(self):
        db = sqlite3.connect(resource_path("peças.db"))
        cursor = db.cursor()
        comand = '''SELECT * from peças_carro'''
        result = cursor.execute(comand)
        self.tabela.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tabela.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tabela.setItem(row_number, column_number,
                                    QTableWidgetItem(str(data)))

        # Mostra quantas peças diferentes tem no sistema e quantas referências únicad tem na database
        cursor2 = db.cursor()
        cursor3 = db.cursor()
        pecas_diferentes = '''SELECT COUNT(DISTINCT Peça) from peças_carro'''
        ref = '''SELECT COUNT (DISTINCT Referência) from peças_carro '''

        result_pecas_diferentes = cursor2.execute(pecas_diferentes)
        result_ref = cursor3.execute(ref)

        self.lbl_ref.setText(str(result_ref.fetchone()[0]))
        self.lbl_peca.setText(str(result_pecas_diferentes.fetchone()[0]))

        # Mostra a peça mais cara e a mais barata com suas respectivas referências

        cursor4 = db.cursor()
        cursor5 = db.cursor()

        min_valor = '''SELECT MIN(Preço), Referência from peças_carro'''
        max_valor = '''SELECT MAX(Preço), Referência from peças_carro'''

        result_min_valor = cursor4.execute(min_valor)
        result_max_valor = cursor5.execute(max_valor)

        r1 = result_min_valor.fetchone()
        r2 = result_max_valor.fetchone()

        self.lbl_menor.setText(str(r1[0]))
        self.lbl_maior.setText(str(r2[0]))
        self.lbl_ref_menor.setText(str(r1[1]))
        self.lbl_ref_maior.setText(str(r2[1]))

    def PROCURAR(self):  # Mostra na interface o filtro de bsuca
        db = sqlite3.connect(resource_path("peças.db"))
        cursor = db.cursor()
        filtro = int(self.numero_botao.text())
        comand = '''SELECT * from peças_carro WHERE Quantidade<=?'''
        result = cursor.execute(comand, [filtro])
        self.tabela.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tabela.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tabela.setItem(row_number, column_number,
                                    QTableWidgetItem(str(data)))

    # Verifica os 3 itens em menor quantidade em estoque

    def VERIFICAR(self):
        db = sqlite3.connect(resource_path("peças.db"))
        cursor = db.cursor()
        comand2 = '''SELECT Referência, Peça, Quantidade from peças_carro order by Quantidade asc LIMIT 3'''
        result = cursor.execute(comand2)
        self.tabela2.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tabela2.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tabela2.setItem(row_number, column_number,
                                     QTableWidgetItem(str(data)))

    def NAVEGAR(self):  # Essa função alimenta a interface na aba editar inventário
        db = sqlite3.connect(resource_path("peças.db"))
        cursor = db.cursor()
        comand = '''SELECT * from peças_carro'''
        result = cursor.execute(comand)
        val = result.fetchone()
        self.id.setText(str(val[0]))
        self.ref.setText(str(val[1]))
        self.peca.setText(str(val[2]))
        self.quantidade.setValue(val[3])
        self.preco.setText(str(val[4]))
        self.marca.setText(str(val[5]))

    def UPDATE(self):  # Atualiza o banco de dados
        db = sqlite3.connect(resource_path("peças.db"))
        cursor = db.cursor()
        id_ = int(self.id.text())
        ref_ = self.ref.text()
        peca_ = self.peca.text()
        quantidade_ = str(self.quantidade.value())
        preco_ = self.preco.text()
        marca_ = self.marca.text()

        row = (ref_, peca_, quantidade_, preco_, marca_, id_)

        comand = '''UPDATE peças_carro SET Referência=?, Peça=?, Quantidade=?,Preço=?,Marca=? WHERE ID=? '''
        cursor.execute(comand, row)
        db.commit()

    def DELETAR(self):  # Deleta do banco de dados
        db = sqlite3.connect(resource_path("peças.db"))
        cursor = db.cursor()
        d = self.id.text()
        comand = '''DELETE from peças_carro WHERE ID=?'''
        cursor.execute(comand, d)
        db.commit()

    def ADICIONAR(self):  # Adiciona no banco de dados
        db = sqlite3.connect(resource_path("peças.db"))
        cursor = db.cursor()
        ref_ = self.ref.text()
        peca_ = self.peca.text()
        quantidade_ = str(self.quantidade.value())
        preco_ = self.preco.text()
        marca_ = self.marca.text()

        row = (ref_, peca_, quantidade_, preco_, marca_)

        comand = '''INSERT INTO peças_carro (Referência, Peça, Quantidade,Preço,Marca) VALUES(?,?,?,?,?) '''
        cursor.execute(comand, row)
        db.commit()

    def PROXIMO(self):  # Move a exibição na interface
        db = sqlite3.connect(resource_path("peças.db"))
        cursor = db.cursor()
        id_atual = int(self.id.text())
        id_atual += 1
        comand = '''SELECT * from peças_carro WHERE ID=?'''
        result = cursor.execute(comand, (id_atual,))
        val = result.fetchone()
        if val is not None:
            self.id.setText(str(val[0]))
            self.ref.setText(str(val[1]))
            self.peca.setText(str(val[2]))
            self.quantidade.setValue(val[3])
            self.preco.setText(str(val[4]))
            self.marca.setText(str(val[5]))
        else:
            print("Você está visualizando o último ID")

    def ANTERIOR(self):  # Move a exibição na interface
        db = sqlite3.connect(resource_path("peças.db"))
        cursor = db.cursor()
        id_atual = int(self.id.text())
        id_atual -= 1
        comand = '''SELECT * from peças_carro WHERE ID=?'''
        result = cursor.execute(comand, (id_atual,))
        val = result.fetchone()
        if val is not None:
            self.id.setText(str(val[0]))
            self.ref.setText(str(val[1]))
            self.peca.setText(str(val[2]))
            self.quantidade.setValue(val[3])
            self.preco.setText(str(val[4]))
            self.marca.setText(str(val[5]))

    def PRIMEIRO(self): #Move para o primeiro ID
        db = sqlite3.connect(resource_path("peças.db"))
        cursor = db.cursor()
        comand = '''SELECT * FROM peças_carro ORDER BY ID ASC LIMIT 1 '''
        result=cursor.execute(comand)
        val=result.fetchone()
        self.id.setText(str(val[0]))
        self.ref.setText(str(val[1]))
        self.peca.setText(str(val[2]))
        self.quantidade.setValue(val[3])
        self.preco.setText(str(val[4]))
        self.marca.setText(str(val[5]))

    def ULTIMO(self): #Move para o último ID
        db = sqlite3.connect(resource_path("peças.db"))
        cursor = db.cursor()
        comand = '''SELECT * FROM peças_carro ORDER BY ID DESC LIMIT 1 '''
        result=cursor.execute(comand)
        val=result.fetchone()
        self.id.setText(str(val[0]))
        self.ref.setText(str(val[1]))
        self.peca.setText(str(val[2]))
        self.quantidade.setValue(val[3])
        self.preco.setText(str(val[4]))
        self.marca.setText(str(val[5]))



def main():  # Esta função instância a classe Main e roda o app ela num loop.
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec()


if __name__ == "__main__":  # garante que o script só rode no arquivo princiapl.
    main()
