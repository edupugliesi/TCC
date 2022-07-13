from tkinter import *
from tkinter import ttk
import sqlite3



################### >>>>> BACK-END / BANCO DE DADOS <<<<< ###################
class Funcs():




    # Criação e Conexão com o Banco de Dados
    def conecta_bd(self):
        self.conn = sqlite3.connect("AutoTrip.bd")
        self.cursor = self.conn.cursor(); print("Conectando ao Banco de Dados")
    
    
    
    
    def desconecta_bd(self):
        self.conn.close(); print("Desconectando Banco de Dados")
    
    
    
    
    def montaTabelaVeiculo(self):
        self.conecta_bd()
        
        # Criar Tabela do Banco de Dados
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS veiculos (
                vei_id INTEGER primary key,
                placa CHAR(8) NOT NULL,
                marca CHAR(20) NOT NULL,
                modelo CHAR(10) NOT NULL,
                ano CHAR(4) NOT NULL,
                status CHAR(15),
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

        """)
        self.conn.commit(); print("Banco de dados criado")
        self.desconecta_bd()




    def montaTabelaManutencao(self):
        self.conecta_bd()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS manutencao (
                man_id INTEGER primary key,
                placa CHAR(8) NOT NULL,
                manutencao CHAR(30),
                km_atual CHAR(8),
                km_prox_manutencao CHAR(8),
                data_prox_manutencao DATE,
                obs CHAR(100),
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

        """)
        self.conn.commit(); print("Banco de dados criado")
        self.desconecta_bd()




    # Função para captura das variáveis das entrys de cadastro/edição de veículos.
    def variaveis(self):
        self.placa = self.entry_Placa_cadastrar.get()
        self.marca = self.entry_Marca_cadastrar.get()
        self.modelo = self.entry_Modelo_cadastrar.get()
        self.ano = self.entry_Ano_cadastrar.get()
        self.status = self.entry_Status_cadastrar.get()
    


    # Função para captura das variáveis das entrys de cadastro/edição de manutenções.
    def variaveis_manutencao(self):
        self.manutencao = self.entry_manutencao_editar.get()
        self.km_atual = self.entry_km_atual_editar.get()
        self.km_prox_manutencao = self.entry_km_prox_manutencao_editar.get()
        self.data_prox_manutencao = self.entry_data_prox_manutencao_editar.get()
        self.man_id = self.entry_Man_ID_manutencao_editar.get()
        self.obs = self.entry_obs_editar.get()




    # Função para adicionar veículo na tabela.
    def add_veiculo(self):
        self.variaveis()
        self.conecta_bd()

        self.cursor.execute(""" INSERT INTO veiculos (placa, marca, modelo, ano, status)
            VALUES (?, ?, ?, ?, ?) """, (self.placa, self.marca, self.modelo, self.ano, self.status))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpar_campos()




    # Função para mostrar veículos na janela Consultar
    def select_lista(self):
        self.lista_veiculos.delete(* self.lista_veiculos.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT vei_id, placa, marca, modelo, ano, status, data_cadastro FROM veiculos
            ORDER BY marca ASC; """)
        for i in lista:
            self.lista_veiculos.insert("", END, values=i)
        self.desconecta_bd()
    


    def select_lista_manutencao(self):
        self.lista_manutencao.delete(* self.lista_manutencao.get_children())
        self.conecta_bd()
        lista_historico = self.cursor.execute(""" SELECT man_id, placa, manutencao, km_atual, km_prox_manutencao, data_prox_manutencao, obs, data_atualizacao FROM manutencao
            ORDER BY placa ASC; """)
        for i in lista_historico:
            self.lista_manutencao.insert("", END, values=i)
        self.desconecta_bd()
    

 
    
    # Função para limpar entrys nas janelas correspondentes a adicionar/editar veículos
    def limpar_campos(self):
        self.entry_Placa_cadastrar.delete(0, END)
        self.entry_Modelo_cadastrar.delete(0, END)
        self.entry_Ano_cadastrar.delete(0, END)



    # Função para limpar entrys nas janelas correspondentes a adicionar/editar manutenções
    def limpa_campos_manutencao(self):
        self.entry_Man_ID_manutencao_editar.delete(0, END)
        self.entry_km_atual_editar.delete(0, END)
        self.entry_km_prox_manutencao_editar.delete(0, END)
        self.entry_data_prox_manutencao_editar.delete(0, END)
        self.entry_obs_editar.delete(0, END)



    # Função para deletar os veíuclos da Treeview e do Banco de Dados
    def deleta(self):

        self.itemSelecionado = self.lista_veiculos.selection()[0]
        self.lista_veiculos.delete(self.itemSelecionado)
            

        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM veiculos WHERE placa = ?""", [self.placa] )
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpar_campos() 
    




    def att_veiculo(self):
        self.placa = self.entry_Placa_cadastrar.get()
        self.manutencao = self.entry_manutencao.get()
        self.km_atual = self.entry_km_atual.get()
        self.km_prox_manutencao = self.entry_km_prox_manutencao.get()
        self.data_prox_manutencao = self.entry_data_prox_manutencao.get()
        self.obs = self.entry_obs.get()

        self.conecta_bd()
        #self.cursor.execute("""UPDATE veiculos SET marca = ?, 
        #modelo = ?, ano = ? WHERE placa = ?""", (self.marca, self.modelo, self.ano, self.placa))

        self.cursor.execute(""" INSERT INTO manutencao (placa, manutencao, km_atual, km_prox_manutencao, data_prox_manutencao, obs)
        VALUES (?, ?, ?, ?, ?, ?) """, (self.placa, self.manutencao, self.km_atual, self.km_prox_manutencao, self.data_prox_manutencao, self.obs))
        
        self.conn.commit()

        self.desconecta_bd()
        self.select_lista()

        
        self.limpar_campos()
        self.entry_km_atual.delete(0, END)
        self.entry_km_prox_manutencao.delete(0, END)
        self.entry_data_prox_manutencao.delete(0, END)
        self.entry_obs.delete(0, END)




    def busca_veiculo(self):
        self.conecta_bd()
        self.lista_veiculos.delete(* self.lista_veiculos.get_children())
        self.entry_campoBuscar.insert(END, '%')
        buscar = self.entry_campoBuscar.get()
        self.cursor.execute(
            """SELECT vei_id, placa, marca, modelo, ano, status, data_cadastro FROM veiculos
            WHERE placa LIKE '%s' ORDER BY placa, modelo ASC""" % buscar)
        buscarPlaca = self.cursor.fetchall()
        for i in buscarPlaca:
            self.lista_veiculos.insert("", END, values=i)
        
        self.entry_campoBuscar.delete(0, END)
        self.desconecta_bd()
    



    def busca_manutencao(self):
        self.conecta_bd()
        self.lista_manutencao.delete(* self.lista_manutencao.get_children())
        self.entry_campoBuscar_historico.insert(END, '%')
        buscar_historico = self.entry_campoBuscar_historico.get()
        self.cursor.execute(
            """SELECT man_id, placa, manutencao, km_atual, km_prox_manutencao, data_prox_manutencao, obs, data_atualizacao FROM manutencao
            WHERE placa LIKE '%s' ORDER BY placa ASC""" % buscar_historico)
        buscarPlaca_historico = self.cursor.fetchall()
        for x in buscarPlaca_historico:
            self.lista_manutencao.insert("", END, values=x)
        
        self.entry_campoBuscar_historico.delete(0, END)
        self.desconecta_bd()




    def edita_veiculo(self):
        self.variaveis()
        self.vei_id = self.entry_Vei_ID_cadastrar.get()

        self.conecta_bd()


        self.cursor.execute("""UPDATE veiculos SET placa = ?, marca = ?, modelo = ?, ano = ?, status = ? WHERE vei_id = ?""", 
            (self.placa, self.marca, self.modelo, self.ano, self.status, self.vei_id))

        self.limpar_campos()
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        
        
        



    def edita_manutencao(self):
        self.variaveis_manutencao()

        self.conecta_bd()

        self.cursor.execute("""UPDATE manutencao SET manutencao = ?, km_atual = ?, km_prox_manutencao = ?, data_prox_manutencao = ?, obs = ? WHERE man_id = ?""",
            (self.manutencao, self.km_atual, self.km_prox_manutencao,self.data_prox_manutencao, self.obs, self.man_id))

        self.conn.commit()
        self.desconecta_bd()
        self.limpa_campos_manutencao()
        self.select_lista_manutencao()







################### >>>>> JANELAS <<<<< ###################
class App(Funcs):




    # Função de inicialização
    def __init__(self):

        # Chamada para funções do Banco de Dados
        self.montaTabelaVeiculo()
        self.montaTabelaManutencao()

        self.Login()
        self.Cadastrar()
        self.Consultar()
        self.Atualizar()
        self.Manutencoes()




    ################### >>>>> JANELA DE LOGIN <<<<< ###################
    def Login(self):




        # Configurações visuais e comportamentais da Janela
        root = Tk()
        self.root = root    
        self.root.title("Login")
        self.root.configure(background = '#4F4F4F')
        self.root.geometry('800x600')
        self.root.resizable(True, True)
        self.root.maxsize(width=1280, height=720)
        self.root.minsize(width=800, height=600)


        ############################## LABELS


        #Logo
        self.lb_logo = Label(self.root, text="AutoTrip")
        self.lb_logo.place(relx=0.35, rely=0.05, relwidth=0.3, relheight=0.1)
        self.lb_logo.configure(font='Arial 40 bold' ,background='#4F4F4F', foreground='white')

        #Boas Vindas
        self.lb_boasVindas = Label(self.root, text="Bem Vindo")
        self.lb_boasVindas.place(relx=0.4, rely=0.15, relwidth=0.2, relheight=0.05)
        self.lb_boasVindas.configure(font='Arial 15 bold' ,background='#4F4F4F', foreground='white')

        #Usuário
        self.lb_usuario = Label(self.root, text="Usuário *")
        self.lb_usuario.place(relx=0.37, rely=0.35, relwidth=0.267, relheight=0.03)
        self.lb_usuario.configure(font='Arial 15 bold' ,background='#4F4F4F', foreground='white')

        #Senha
        self.lb_senha = Label(self.root, text="Senha *")
        self.lb_senha.place(relx=0.37, rely=0.45, relwidth=0.267, relheight=0.03)
        self.lb_senha.configure(font='Arial 15 bold' ,background='#4F4F4F', foreground='white')


        ############################## ENTRYS


        #Usuário
        self.entry_usuario = Entry(self.root)
        self.entry_usuario.place(relx=0.37, rely=0.38, relwidth=0.26, relheight=0.04)
        self.entry_usuario.configure(bg='#eeeeee')

        #Senha
        self.entry_senha = Entry(self.root)
        self.entry_senha.place(relx=0.37, rely=0.48, relwidth=0.26, relheight=0.04)
        self.entry_senha.configure(bg='#eeeeee')


        ############################## BOTÕES
    

        #Entrar
        self.bt_entrar = Button(self.root, text="Entrar", command = self.Consultar) #Botão chamando a Janela Consultar
        self.bt_entrar.place(relx= 0.422, rely=0.75, relwidth=0.15, relheight=0.05)
        self.bt_entrar.configure(font='Arial 12 bold', bd=2, bg='#eeeeee')


        root.mainloop()




    ################### >>>>> JANELA CONSULTAR VEÍCULOS <<<<< ###################
    def Consultar(self):

        


        # Configurações visuais e comportamentais da Janela
        self.root2 = Toplevel()
        self.root2.title("Consultar Veículos")
        self.root2.configure(background = '#4F4F4F')
        self.root2.geometry('1280x720')
        self.root2.resizable(True, True)
        self.root2.maxsize(width=1920, height=1080)
        self.root2.minsize(width=1280, height=720)
        self.root2.transient(self.root)
        self.root2.focus_force()
        self.root2.grab_set()


        ############################## FRAME


        self.mostraVeiculo = Frame(self.root2)
        self.mostraVeiculo.place(relx= 0.05, rely=0.21, relwidth=0.9, relheight=0.7) ##Posicionamento do frame_mostra_veiculo


        ############################## LABELS


        #Logo
        self.lb_logo = Label(self.root2, text="AutoTrip")
        self.lb_logo.place(relx=0.345, rely=0.06, relwidth=0.8, relheight=0.1)
        self.lb_logo.configure(font='Arial 50 bold', background='#4F4F4F', foreground='white')


        #Buscar
        self.lb_campoBuscar = Label(self.root2, text="Digite a placa do veículo")
        self.lb_campoBuscar.place(relx=0.05, rely=0.10, relwidth=0.267, relheight=0.03)
        self.lb_campoBuscar.configure(font='Arial 15 bold', background='#4F4F4F', foreground='white')


        ############################## ENTRYS


        #Buscar
        self.entry_campoBuscar = Entry(self.root2)
        self.entry_campoBuscar.place(relx=0.05, rely=0.15, relwidth=0.28, relheight=0.04)
        self.entry_campoBuscar.configure(bg='#eeeeee')


        ############################## LISTBOX


        #Criando lista dos veículos
        self.lista_veiculos = ttk.Treeview(self.mostraVeiculo, height=1, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8"))

        #Atributos da Lista

        self.lista_veiculos.heading("#0", text="")
        self.lista_veiculos.column("#0", minwidth=0, width=0, stretch=NO)

        #ID
        self.lista_veiculos.heading("#1", text="ID")
        self.lista_veiculos.column("#1", minwidth=40, width=40, stretch=NO, anchor=CENTER)

        #Placa
        self.lista_veiculos.heading("#2", text="Placa")
        self.lista_veiculos.column("#2", minwidth=120, width=120, stretch=NO, anchor=CENTER)

        #Marca
        self.lista_veiculos.heading("#3", text="Marca")
        self.lista_veiculos.column("#3", minwidth=220, width=220, stretch=NO, anchor=CENTER)

        #Modelo
        self.lista_veiculos.heading("#4", text="Modelo")
        self.lista_veiculos.column("#4", minwidth=220, width=220, stretch=NO, anchor=CENTER)

        #Ano
        self.lista_veiculos.heading("#5", text="Ano")
        self.lista_veiculos.column("#5", minwidth=100, width=100, stretch=NO, anchor=CENTER)

        #Status
        self.lista_veiculos.heading("#6", text="Status")
        self.lista_veiculos.column("#6", minwidth=160, width=160, stretch=NO, anchor=CENTER)

        #Data Cadastro
        self.lista_veiculos.heading("#7", text="Data Cadastro")
        self.lista_veiculos.column("#7", minwidth=250, width=250, stretch=NO, anchor=CENTER)
  
        
        #Posicionamento da lista
        self.lista_veiculos.place(relx=0, rely=0, relwidth=1.05, relheight=1.05)


        ############################## SCROLLBAR


        self.scrolllista_veiculos = Scrollbar(self.lista_veiculos, orient='vertical')
        self.lista_veiculos.configure(yscroll=self.scrolllista_veiculos.set)
        self.scrolllista_veiculos.place(relx=0.935, rely=0, relwidth=0.02, relheight=0.96)


        ############################## BOTÕES


        #Buscar
        self.bt_buscar_funcional = Button(self.root2, text="Buscar", command = self.busca_veiculo)
        self.bt_buscar_funcional.place(relx= 0.35, rely=0.15, relwidth=0.08, relheight=0.04)
        self.bt_buscar_funcional.configure(font='Arial 12 bold', bd=2, bg='#eeeeee')

        #Cadastrar
        self.bt_cadastrar_consultar = Button(self.root2, text="Cadastrar Veículo", command = self.Cadastrar)
        self.bt_cadastrar_consultar.place(relx= 0.05, rely=0.93, relwidth=0.12, relheight=0.04)
        self.bt_cadastrar_consultar.configure(font='Arial 12 bold', bd=2, bg='#eeeeee')

        #Editar
        self.bt_editar_consultar = Button(self.root2, text="Editar Veículo", command = self.Janela_Editar_Veiculos)
        self.bt_editar_consultar.place(relx= 0.18, rely=0.93, relwidth=0.12, relheight=0.04)
        self.bt_editar_consultar.configure(font='Arial 12 bold', bd=2, bg='#eeeeee')

        #Atualizar
        self.bt_atualizar_consultar = Button(self.root2, text="Inserir Manutenção", command = self.Atualizar)
        self.bt_atualizar_consultar.place(relx= 0.31, rely=0.93, relwidth=0.13, relheight=0.04)
        self.bt_atualizar_consultar.configure(font='Arial 12 bold', bd=2, bg='#eeeeee')

        #Manutenções
        self.bt_manutencoes_funcional = Button(self.root2, text="Ver Manutenções", command = self.Manutencoes)
        self.bt_manutencoes_funcional.place(relx= 0.45, rely=0.93, relwidth=0.12, relheight=0.04)
        self.bt_manutencoes_funcional.configure(font='Arial 12 bold', bd=2, bg='#eeeeee')

        #Sair
        self.bt_sair = Button(self.root2, text="Sair", command = self.root.destroy)
        self.bt_sair.place(relx= 0.05, rely=0.02, relwidth=0.08, relheight=0.05)
        self.bt_sair.configure(font='Arial 12 bold', bd=2, bg='#eeeeee')

        
        #Janela Consultar já aparece com todos os veículos na tela.
        self.select_lista()




    ################### >>>>> JANELA CADASTRAR VEÍCULOS <<<<< ###################
    def Cadastrar(self):




        # Para corrigir BUG que ficavam abrindo multiplas janelas Consultar
        self.root2.focus_force()

        # Configurações visuais e comportamentais da Janela
        self.root3 = Toplevel()
        self.root3.title("Cadastrar Veículo")
        self.root3.configure(background = '#4F4F4F')
        self.root3.geometry('1280x720')
        self.root3.resizable(True, True)
        self.root3.maxsize(width=1920, height=1080)
        self.root3.minsize(width=1280, height=720)
        self.root3.transient(self.root2)
        self.root3.focus_force()
        self.root3.grab_set()


        ############################## LABELS


        #Logo
        self.lb_logo_cadastrar = Label(self.root3, text="AutoTrip")
        self.lb_logo_cadastrar.place(relx=0.345, rely=0.03, relwidth=0.3, relheight=0.1)
        self.lb_logo_cadastrar.configure(font='Arial 40 bold' ,background='#4F4F4F', foreground='white')

        #Boas Vindas
        self.lb_boasVindas_cadastrar = Label(self.root3, text="Cadastrar")
        self.lb_boasVindas_cadastrar.place(relx=0.395, rely=0.11, relwidth=0.2, relheight=0.05)
        self.lb_boasVindas_cadastrar.configure(font='Arial 15 italic' ,background='#4F4F4F', foreground='white')


        #Placa
        self.lb_campoPlaca_cadastrar = Label(self.root3, text="Placa *")
        self.lb_campoPlaca_cadastrar.place(relx=0.362, rely=0.25, relwidth=0.267, relheight=0.04)
        self.lb_campoPlaca_cadastrar.configure(font='Arial 15 bold' ,background='#4F4F4F', foreground='white')

        #Marca
        self.lb_campoMarca_cadastrar = Label(self.root3, text="Marca *")
        self.lb_campoMarca_cadastrar.place(relx=0.362, rely=0.35, relwidth=0.267, relheight=0.04)
        self.lb_campoMarca_cadastrar.configure(font='Arial 15 bold' ,background='#4F4F4F', foreground='white')

        #Modelo
        self.lb_campoModelo_cadastrar = Label(self.root3, text="Modelo *")
        self.lb_campoModelo_cadastrar.place(relx=0.362, rely=0.45, relwidth=0.267, relheight=0.04)
        self.lb_campoModelo_cadastrar.configure(font='Arial 15 bold' ,background='#4F4F4F', foreground='white')

        #Ano
        self.lb_campoAno_cadastrar = Label(self.root3, text="Ano *")
        self.lb_campoAno_cadastrar.place(relx=0.362, rely=0.55, relwidth=0.267, relheight=0.04)
        self.lb_campoAno_cadastrar.configure(font='Arial 15 bold' ,background='#4F4F4F', foreground='white')

        #Status
        self.lb_campoStatus_cadastrar = Label(self.root3, text="Status *")
        self.lb_campoStatus_cadastrar.place(relx=0.362, rely=0.65, relwidth=0.267, relheight=0.04)
        self.lb_campoStatus_cadastrar.configure(font='Arial 15 bold' ,background='#4F4F4F', foreground='white')

        #Aviso Pequeno
        self.lb_avisoPequeno_cadastrar = Label(self.root3, text="Campos destacados são obrigatórios.")
        self.lb_avisoPequeno_cadastrar.place(relx=0.55, rely=0.92, relwidth=0.5, relheight=0.03)
        self.lb_avisoPequeno_cadastrar.configure(font='Arial 12 italic' ,background='#4F4F4F', foreground='white')

        
        ############################## ENTRYS


        #Placa
        self.entry_Placa_cadastrar = Entry(self.root3)
        self.entry_Placa_cadastrar.place(relx=0.36, rely=0.28, relwidth=0.28, relheight=0.04)
        self.entry_Placa_cadastrar.configure(bg='#eeeeee')

        #Marca
        self.entry_Marca_cadastrar = StringVar(self.root3)
        self.entry_Marca_cadastrar_options = ("Scania", "Volvo", "Mercedes-Benz", "Volkswagen", "DAF", "MAN")
        #self.entry_MArca_cadastrar.set("Ativo")
        self.popupMenu = OptionMenu(self.root3, self.entry_Marca_cadastrar, *self.entry_Marca_cadastrar_options)
        self.popupMenu.place(relx=0.36, rely=0.38, relwidth=0.28, relheight=0.04)

        #self.entry_Marca_cadastrar = Entry(self.root3)
        #self.entry_Marca_cadastrar.place(relx=0.36, rely=0.38, relwidth=0.28, relheight=0.04)
        #self.entry_Marca_cadastrar.configure(bg='#eeeeee')

        #Modelo
        self.entry_Modelo_cadastrar = Entry(self.root3)
        self.entry_Modelo_cadastrar.place(relx=0.36, rely=0.48, relwidth=0.28, relheight=0.04)
        self.entry_Modelo_cadastrar.configure(bg='#eeeeee')

        #Ano
        self.entry_Ano_cadastrar = Entry(self.root3)
        self.entry_Ano_cadastrar.place(relx=0.36, rely=0.58, relwidth=0.28, relheight=0.04)
        self.entry_Ano_cadastrar.configure(bg='#eeeeee')

        #Status - Drop Down Button
        self.entry_Status_cadastrar = StringVar(self.root3)
        self.entry_Status_cadastrar_options = ("Ativo", "Inativo")
        #self.entry_Status_cadastrar.set("Ativo")
        self.popupMenu = OptionMenu(self.root3, self.entry_Status_cadastrar, *self.entry_Status_cadastrar_options)
        self.popupMenu.place(relx=0.36, rely=0.68, relwidth=0.28, relheight=0.04)


        ############################## BOTÕES


        #Cadastrar
        self.bt_cadastrar_funcional = Button(self.root3, text="Cadastrar", command = self.add_veiculo)
        self.bt_cadastrar_funcional.place(relx= 0.422, rely=0.9, relwidth=0.15, relheight=0.05)
        self.bt_cadastrar_funcional.configure(font='Arial 12 bold', bd=2, bg='#eeeeee')

        #Voltar
        self.bt_voltar_cadastrar = Button(self.root3, text="Voltar", command = self.root3.destroy)
        self.bt_voltar_cadastrar.place(relx= 0.02, rely=0.02, relwidth=0.08, relheight=0.05)
        self.bt_voltar_cadastrar.configure(font='Arial 12 bold', bd=2, bg='#eeeeee')   




    ################### >>>>> JANELA INSERIR MANUTENÇÃO <<<<< ###################
    def Atualizar(self):



        # Para corrigir BUG que ficavam abrindo multiplas janelas Consultar
        self.root2.focus_force()

        # Configurações visuais e comportamentais da Janela
        self.root4 = Toplevel()
        self.root4.title("Inserir Manutenção")
        self.root4.configure(background = '#4F4F4F')
        self.root4.geometry('1280x720')
        self.root4.resizable(True, True)
        self.root4.maxsize(width=1920, height=1080)
        self.root4.minsize(width=1280, height=720)
        self.root4.transient(self.root2)
        self.root4.focus_force()
        self.root4.grab_set()



        ############################## LABELS


        #Atualizar
        self.lb_logo_atualizar = Label(self.root4, text="AutoTrip")
        self.lb_logo_atualizar.place(relx=0.345, rely=0.01, relwidth=0.3, relheight=0.12)
        self.lb_logo_atualizar.configure(font='Arial 45 bold' ,background='#4F4F4F', foreground='white')

        #Boas Vindas
        self.lb_boasVindas_atualizar = Label(self.root4, text="Inserir Manutenção")
        self.lb_boasVindas_atualizar.place(relx=0.395, rely=0.12, relwidth=0.2, relheight=0.02)
        self.lb_boasVindas_atualizar.configure(font='Arial 11 italic' ,background='#4F4F4F', foreground='white')

        #Placa
        self.lb_campoPlaca_atualizar = Label(self.root4, text="Placa")
        self.lb_campoPlaca_atualizar.place(relx=0.13, rely=0.20, relwidth=0.267, relheight=0.03)
        self.lb_campoPlaca_atualizar.configure(font='Arial 15 bold' ,background='#4F4F4F', foreground='white')

        #Marca
        self.lb_campoMarca_atualizar = Label(self.root4, text="Marca")
        self.lb_campoMarca_atualizar.place(relx=0.13, rely=0.30, relwidth=0.267, relheight=0.03)
        self.lb_campoMarca_atualizar.configure(font='Arial 15 bold' ,background='#4F4F4F', foreground='white')

        #Modelo
        self.lb_campoModelo_atualizar = Label(self.root4, text="Modelo")
        self.lb_campoModelo_atualizar.place(relx=0.13, rely=0.40, relwidth=0.267, relheight=0.03)
        self.lb_campoModelo_atualizar.configure(font='Arial 15 bold' ,background='#4F4F4F', foreground='white')

        #Ano
        self.lb_campoAno_atualizar = Label(self.root4, text="Ano")
        self.lb_campoAno_atualizar.place(relx=0.13, rely=0.50, relwidth=0.267, relheight=0.03)
        self.lb_campoAno_atualizar.configure(font='Arial 15 bold' ,background='#4F4F4F', foreground='white')

        #Manutenção Realizada
        self.lb_manutencaoRealizada = Label(self.root4, text="Manutenção")
        self.lb_manutencaoRealizada.place(relx=0.60, rely=0.20, relwidth=0.267, relheight=0.03)
        self.lb_manutencaoRealizada.configure(font='Arial 15 bold' ,background='#4F4F4F', foreground='white')

        #KM Atual
        self.lb_km_atual = Label(self.root4, text="KM Atual")
        self.lb_km_atual.place(relx=0.60, rely=0.30, relwidth=0.267, relheight=0.03)
        self.lb_km_atual.configure(font='Arial 15 bold' ,background='#4F4F4F', foreground='white')

        #KM Próxima Manutenção
        self.lb_km_prox_manutencao = Label(self.root4, text="Próxima Manutenção (KM)")
        self.lb_km_prox_manutencao.place(relx=0.60, rely=0.40, relwidth=0.267, relheight=0.03)
        self.lb_km_prox_manutencao.configure(font='Arial 15 bold' ,background='#4F4F4F', foreground='white')

        #Data Próxima Manutenção
        self.lb_data_prox_manutencao = Label(self.root4, text="Próxima Manutenção (Data)")
        self.lb_data_prox_manutencao.place(relx=0.60, rely=0.50, relwidth=0.267, relheight=0.03)
        self.lb_data_prox_manutencao.configure(font='Arial 15 bold' ,background='#4F4F4F', foreground='white')

        #Observação
        self.lb_obs = Label(self.root4, text="Observação")
        self.lb_obs.place(relx=0.363, rely=0.70, relwidth=0.267, relheight=0.03)
        self.lb_obs.configure(font='Arial 15 bold' ,background='#4F4F4F', foreground='white')

        
        ############################## ENTRYS


        #Placa
        self.entry_Placa_cadastrar = Entry(self.root4)
        self.entry_Placa_cadastrar.place(relx=0.13, rely=0.23, relwidth=0.26, relheight=0.04)
        self.entry_Placa_cadastrar.configure(bg='#eeeeee')

        #Marca
        self.entry_Marca_cadastrar = Entry(self.root4)
        self.entry_Marca_cadastrar.place(relx=0.13, rely=0.33, relwidth=0.26, relheight=0.04)
        self.entry_Marca_cadastrar.configure(bg='#eeeeee')

        #Modelo
        self.entry_Modelo_cadastrar = Entry(self.root4)
        self.entry_Modelo_cadastrar.place(relx=0.13, rely=0.43, relwidth=0.26, relheight=0.04)
        self.entry_Modelo_cadastrar.configure(bg='#eeeeee')

        #Ano
        self.entry_Ano_cadastrar = Entry(self.root4)
        self.entry_Ano_cadastrar.place(relx=0.13, rely=0.53, relwidth=0.26, relheight=0.04)
        self.entry_Ano_cadastrar.configure(bg='#eeeeee')

        #Manutenção
        self.entry_manutencao = StringVar(self.root4)
        self.entry_manutencao_options = ("Abastecimento", "Troca de Óleo", "Troca de Mangueiras", "Troca de Correias", "Bronzinamento", "Retífica", "Troca de Pneus")
        #self.entry_MArca_cadastrar.set("Ativo")
        self.popupMenu = OptionMenu(self.root4, self.entry_manutencao, *self.entry_manutencao_options)
        self.popupMenu.place(relx=0.605, rely=0.23, relwidth=0.26, relheight=0.04)

        #KM Atual
        self.entry_km_atual = Entry(self.root4)
        self.entry_km_atual.place(relx=0.605, rely=0.33, relwidth=0.26, relheight=0.04)
        self.entry_km_atual.configure(bg='#eeeeee')

        #KM Próxima Manutenção
        self.entry_km_prox_manutencao = Entry(self.root4)
        self.entry_km_prox_manutencao.place(relx=0.605, rely=0.43, relwidth=0.26, relheight=0.04)
        self.entry_km_prox_manutencao.configure(bg='#eeeeee')

        #DATA Próxima Manutenção
        self.entry_data_prox_manutencao = Entry(self.root4)
        self.entry_data_prox_manutencao.place(relx=0.605, rely=0.53, relwidth=0.26, relheight=0.04)
        self.entry_data_prox_manutencao.configure(bg='#eeeeee')

        #Observação
        self.entry_obs = Entry(self.root4)
        self.entry_obs.place(relx=0.347, rely=0.73, relwidth=0.30, relheight=0.04)
        self.entry_obs.configure(bg='#eeeeee')


        ############################## BOTÕES


        #Atualizar
        self.bt_atualizar_funcional = Button(self.root4, text="Atualizar", command = self.att_veiculo)
        self.bt_atualizar_funcional.place(relx= 0.422, rely=0.9, relwidth=0.15, relheight=0.05)
        self.bt_atualizar_funcional.configure(font='Arial 12 bold', bd=2, bg='#eeeeee')

        #Voltar
        self.bt_voltar_atualizar = Button(self.root4, text="Voltar", command = self.root4.destroy)
        self.bt_voltar_atualizar.place(relx= 0.02, rely=0.02, relwidth=0.08, relheight=0.05)
        self.bt_voltar_atualizar.configure(font='Arial 12 bold', bd=2, bg='#eeeeee')


        ############################## Função para inserir os dados do veículo selecionado automaticamente na janela atualizar


        self.lista_veiculos.selection()

        for n in self.lista_veiculos.selection():
            col3, col4, col5, col6, col7, col8, col9 = self.lista_veiculos.item(n, 'values')
            self.entry_Placa_cadastrar.insert(END, col4)
            self.entry_Marca_cadastrar.insert(END, col5)
            self.entry_Modelo_cadastrar.insert(END, col6)
            self.entry_Ano_cadastrar.insert(END, col7)




    ################### >>>>> JANELA HISTORICO DE VEÍCULOS <<<<< ###################
    def Manutencoes(self):




        #Para corrigir BUG que ficavam abrindo multiplas janelas Consultar
        self.root2.focus_force()
        

        # Configurações visuais e comportamentais da Janela
        self.root5 = Toplevel()
        self.root5.title("Manutenções")
        self.root5.configure(background = '#4F4F4F')
        self.root5.geometry('1366x768')
        self.root5.resizable(True, True)
        self.root5.maxsize(width=1920, height=1080)
        self.root5.minsize(width=1366, height=768)
        self.root5.transient(self.root2)
        self.root5.focus_force()
        self.root5.grab_set()


        ############################## FRAME


        self.mostraManutencao = Frame(self.root5)
        self.mostraManutencao.place(relx= 0.05, rely=0.21, relwidth=0.9, relheight=0.7) ##Posicionamento do frame_mostra_veiculo


        ############################## LABELS

        #Logo
        self.lb_logo_historico = Label(self.root5, text="Manutenções")
        self.lb_logo_historico.place(relx=0.345, rely=0.06, relwidth=0.8, relheight=0.1)
        self.lb_logo_historico.configure(font='Arial 50 bold', background='#4F4F4F', foreground='white')

        #Buscar
        self.lb_campoBuscar_historico = Label(self.root5, text="Digite a placa do veículo")
        self.lb_campoBuscar_historico.place(relx=0.05, rely=0.10, relwidth=0.267, relheight=0.03)
        self.lb_campoBuscar_historico.configure(font='Arial 15 bold', background='#4F4F4F', foreground='white')


        ############################## ENTRYS

        #Buscar
        self.entry_campoBuscar_historico = Entry(self.root5)
        self.entry_campoBuscar_historico.place(relx=0.05, rely=0.15, relwidth=0.28, relheight=0.04)
        self.entry_campoBuscar_historico.configure(bg='#eeeeee')


        ############################## LISTBOX

        #Criando a lista dos veículos
        self.lista_manutencao = ttk.Treeview(self.mostraManutencao, height=1, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8"))

        #Atributos da Lista

        self.lista_manutencao.heading("#0", text="")
        self.lista_manutencao.column("#0", minwidth=0, width=0, stretch=NO)

        #ID
        self.lista_manutencao.heading("#1", text="ID")
        self.lista_manutencao.column("#1", minwidth=40, width=40, stretch=NO, anchor=CENTER)

        #Placa
        self.lista_manutencao.heading("#2", text="Placa")
        self.lista_manutencao.column("#2", minwidth=80, width=80, stretch=NO, anchor=CENTER)

        #Manutenção
        self.lista_manutencao.heading("#3", text="Manutenção")
        self.lista_manutencao.column("#3", minwidth=200, width=200, stretch=NO, anchor=CENTER)

        #KM Atual
        self.lista_manutencao.heading("#4", text="KM Atual")
        self.lista_manutencao.column("#4", minwidth=140, width=140, stretch=NO, anchor=CENTER)

        #KM Próx Manutenção
        self.lista_manutencao.heading("#5", text="KM Px Manutenção")
        self.lista_manutencao.column("#5", minwidth=140, width=140, stretch=NO, anchor=CENTER)

        #DATA Próx Manutenção
        self.lista_manutencao.heading("#6", text="Data Px Manutenção")
        self.lista_manutencao.column("#6", minwidth=160, width=160, stretch=NO, anchor=CENTER)

        #Observação
        self.lista_manutencao.heading("#7", text="Observação")
        self.lista_manutencao.column("#7", minwidth=290, width=290, stretch=NO, anchor=CENTER)

        #Data da Atualização
        self.lista_manutencao.heading("#8", text="Data da Atualização")
        self.lista_manutencao.column("#8", minwidth=160, width=160, stretch=NO, anchor=CENTER)


        #Posicionamento da lista
        self.lista_manutencao.place(relx=0, rely=0, relwidth=1.05, relheight=1.05)


        ############################## SCROLLBAR


        self.scrollLista_manutencao = Scrollbar(self.lista_manutencao, orient='vertical')
        self.lista_manutencao.configure(yscroll=self.scrollLista_manutencao.set)
        self.scrollLista_manutencao.place(relx=0.935, rely=0, relwidth=0.02, relheight=0.96)


        ############################## BOTÕES


        #Buscar
        self.bt_buscar_funcional_historico = Button(self.root5, text="Buscar", command = self.busca_manutencao)
        self.bt_buscar_funcional_historico.place(relx= 0.35, rely=0.15, relwidth=0.08, relheight=0.04)
        self.bt_buscar_funcional_historico.configure(font='Arial 12 bold', bd=2, bg='#eeeeee')

        #Editar
        self.bt_editar_manutencoes = Button(self.root5, text="Editar Manutenção", command = self.Janela_Editar_Manutencoes)
        self.bt_editar_manutencoes.place(relx= 0.05, rely=0.93, relwidth=0.12, relheight=0.04)
        self.bt_editar_manutencoes.configure(font='Arial 12 bold', bd=2, bg='#eeeeee')

        #Sair
        self.bt_sair_historico = Button(self.root5, text="Voltar", command = self.root5.destroy)
        self.bt_sair_historico.place(relx= 0.05, rely=0.02, relwidth=0.08, relheight=0.05)
        self.bt_sair_historico.configure(font='Arial 12 bold', bd=2, bg='#eeeeee')


        #Janela Consultar já aparece com todos os veículos na tela.
        self.select_lista_manutencao()





    def Janela_Editar_Veiculos(self):




        # Para corrigir BUG que ficavam abrindo multiplas janelas Consultar
        self.root2.focus_force()

        # Configurações visuais e comportamentais da Janela
        self.root8 = Toplevel()
        self.root8.title("Editar Veículo")
        self.root8.configure(background = '#4F4F4F')
        self.root8.geometry('1280x720')
        self.root8.resizable(True, True)
        self.root8.maxsize(width=1920, height=1080)
        self.root8.minsize(width=1280, height=720)
        self.root8.transient(self.root2)
        self.root8.focus_force()
        self.root8.grab_set()


        ############################## LABELS


        #Logo
        self.lb_logo_editar = Label(self.root8, text="AutoTrip")
        self.lb_logo_editar.place(relx=0.345, rely=0.03, relwidth=0.3, relheight=0.1)
        self.lb_logo_editar.configure(font='Arial 40 bold' ,background='#4F4F4F', foreground='white')

        #Boas Vindas
        self.lb_boasVindas_editar = Label(self.root8, text="Editar Veículo")
        self.lb_boasVindas_editar.place(relx=0.395, rely=0.11, relwidth=0.2, relheight=0.05)
        self.lb_boasVindas_editar.configure(font='Arial 15 italic' ,background='#4F4F4F', foreground='white')

        #Placa
        self.lb_campoPlaca_editar = Label(self.root8, text="Placa *")
        self.lb_campoPlaca_editar.place(relx=0.362, rely=0.25, relwidth=0.267, relheight=0.04)
        self.lb_campoPlaca_editar.configure(font='Arial 15 bold' ,background='#4F4F4F', foreground='white')

        #Marca
        self.lb_campoMarca_editar = Label(self.root8, text="Marca *")
        self.lb_campoMarca_editar.place(relx=0.362, rely=0.35, relwidth=0.267, relheight=0.04)
        self.lb_campoMarca_editar.configure(font='Arial 15 bold' ,background='#4F4F4F', foreground='white')

        #Modelo
        self.lb_campoModelo_editar = Label(self.root8, text="Modelo *")
        self.lb_campoModelo_editar.place(relx=0.362, rely=0.45, relwidth=0.267, relheight=0.04)
        self.lb_campoModelo_editar.configure(font='Arial 15 bold' ,background='#4F4F4F', foreground='white')

        #Ano
        self.lb_campoAno_editar = Label(self.root8, text="Ano *")
        self.lb_campoAno_editar.place(relx=0.362, rely=0.55, relwidth=0.267, relheight=0.04)
        self.lb_campoAno_editar.configure(font='Arial 15 bold' ,background='#4F4F4F', foreground='white')

        #Status
        self.lb_campoStatus_editar = Label(self.root8, text="Status *")
        self.lb_campoStatus_editar.place(relx=0.362, rely=0.65, relwidth=0.267, relheight=0.04)
        self.lb_campoStatus_editar.configure(font='Arial 15 bold' ,background='#4F4F4F', foreground='white')

        #Aviso Pequeno
        self.lb_avisoPequeno_editar = Label(self.root8, text="Campos destacados são obrigatórios.")
        self.lb_avisoPequeno_editar.place(relx=0.55, rely=0.92, relwidth=0.5, relheight=0.03)
        self.lb_avisoPequeno_editar.configure(font='Arial 12 italic' ,background='#4F4F4F', foreground='white')

        
        ############################## ENTRYS

        #ID
        self.entry_Vei_ID_cadastrar = Entry(self.root8)
        self.entry_Vei_ID_cadastrar.place(relx=0.31, rely=0.28, relwidth=0.04, relheight=0.04)
        self.entry_Vei_ID_cadastrar.configure(bg='#eeeeee')

        #Placa
        self.entry_Placa_cadastrar = Entry(self.root8)
        self.entry_Placa_cadastrar.place(relx=0.36, rely=0.28, relwidth=0.28, relheight=0.04)
        self.entry_Placa_cadastrar.configure(bg='#eeeeee')

        #Marca
        self.entry_Marca_cadastrar = StringVar(self.root8)
        self.entry_Marca_cadastrar_options = ("Scania", "Volvo", "Mercedes-Benz", "Volkswagen", "DAF", "MAN")
        #self.entry_MArca_cadastrar.set("Ativo")
        self.popupMenu = OptionMenu(self.root8, self.entry_Marca_cadastrar, *self.entry_Marca_cadastrar_options)
        self.popupMenu.place(relx=0.36, rely=0.38, relwidth=0.28, relheight=0.04)

        #self.entry_Marca_cadastrar = Entry(self.root8)
        #self.entry_Marca_cadastrar.place(relx=0.36, rely=0.38, relwidth=0.28, relheight=0.04)
        #self.entry_Marca_cadastrar.configure(bg='#eeeeee')

        #Modelo
        self.entry_Modelo_cadastrar = Entry(self.root8)
        self.entry_Modelo_cadastrar.place(relx=0.36, rely=0.48, relwidth=0.28, relheight=0.04)
        self.entry_Modelo_cadastrar.configure(bg='#eeeeee')

        #Ano
        self.entry_Ano_cadastrar = Entry(self.root8)
        self.entry_Ano_cadastrar.place(relx=0.36, rely=0.58, relwidth=0.28, relheight=0.04)
        self.entry_Ano_cadastrar.configure(bg='#eeeeee')

        #Status
        self.entry_Status_cadastrar = StringVar(self.root8)
        self.entry_Status_cadastrar_options = ("Ativo", "Inativo")
        self.entry_Status_cadastrar.set("Ativo")
        self.popupMenu = OptionMenu(self.root8, self.entry_Status_cadastrar, *self.entry_Status_cadastrar_options)
        self.popupMenu.place(relx=0.36, rely=0.68, relwidth=0.28, relheight=0.04)


        ############################## BOTÕES


        #Editar
        self.bt_editar_funcional = Button(self.root8, text="Editar", command = self.edita_veiculo)
        self.bt_editar_funcional.place(relx= 0.422, rely=0.9, relwidth=0.15, relheight=0.05)
        self.bt_editar_funcional.configure(font='Arial 12 bold', bd=2, bg='#eeeeee')

        #Voltar
        self.bt_voltar_editar = Button(self.root8, text="Voltar", command = self.root8.destroy)
        self.bt_voltar_editar.place(relx= 0.02, rely=0.02, relwidth=0.08, relheight=0.05)
        self.bt_voltar_editar.configure(font='Arial 12 bold', bd=2, bg='#eeeeee')

        self.lista_veiculos.selection()

        for n in self.lista_veiculos.selection():
            col2, col3, col4, col5, col6, col7, col8 = self.lista_veiculos.item(n, 'values')
            self.entry_Vei_ID_cadastrar.insert(END, col2)
            self.entry_Placa_cadastrar.insert(END, col3)
            self.entry_Modelo_cadastrar.insert(END, col5)
            self.entry_Ano_cadastrar.insert(END, col6)




    def Janela_Editar_Manutencoes(self):




        # Para corrigir BUG que ficavam abrindo multiplas janelas Consultar
        self.root2.focus_force()

        # Configurações visuais e comportamentais da Janela
        self.root9 = Toplevel()
        self.root9.title("Editar Veículo")
        self.root9.configure(background = '#4F4F4F')
        self.root9.geometry('1280x720')
        self.root9.resizable(True, True)
        self.root9.maxsize(width=1920, height=1080)
        self.root9.minsize(width=1280, height=720)
        self.root9.transient(self.root2)
        self.root9.focus_force()
        self.root9.grab_set()


        ############################## LABELS


        #Editar
        self.lb_logo_editar_manutencao = Label(self.root9, text="AutoTrip")
        self.lb_logo_editar_manutencao.place(relx=0.345, rely=0.01, relwidth=0.3, relheight=0.12)
        self.lb_logo_editar_manutencao.configure(font='Arial 45 bold' ,background='#4F4F4F', foreground='white')

        #Boas Vindas
        self.lb_boasVindas_editar_manutencao = Label(self.root9, text="Editar Manutenção")
        self.lb_boasVindas_editar_manutencao.place(relx=0.395, rely=0.11, relwidth=0.2, relheight=0.05)
        self.lb_boasVindas_editar_manutencao.configure(font='Arial 15 italic' ,background='#4F4F4F', foreground='white')

        #Manutenção Realizada
        self.lb_manutencaoRealizada_editar = Label(self.root9, text="Manutenção")
        self.lb_manutencaoRealizada_editar.place(relx=0.363, rely=0.25, relwidth=0.267, relheight=0.03)
        self.lb_manutencaoRealizada_editar.configure(font='Arial 15 bold' ,background='#4F4F4F', foreground='white')

        #KM Atual
        self.lb_km_atual_editar = Label(self.root9, text="KM Atual")
        self.lb_km_atual_editar.place(relx=0.363, rely=0.35, relwidth=0.267, relheight=0.03)
        self.lb_km_atual_editar.configure(font='Arial 15 bold' ,background='#4F4F4F', foreground='white')

        #KM Próxima Manutenção
        self.lb_km_prox_manutencao_editar = Label(self.root9, text="Próxima Manutenção (KM)")
        self.lb_km_prox_manutencao_editar.place(relx=0.363, rely=0.45, relwidth=0.267, relheight=0.03)
        self.lb_km_prox_manutencao_editar.configure(font='Arial 15 bold' ,background='#4F4F4F', foreground='white')

        #Data Próxima Manutenção
        self.lb_data_prox_manutencao_editar = Label(self.root9, text="Próxima Manutenção (Data)")
        self.lb_data_prox_manutencao_editar.place(relx=0.363, rely=0.55, relwidth=0.267, relheight=0.03)
        self.lb_data_prox_manutencao_editar.configure(font='Arial 15 bold' ,background='#4F4F4F', foreground='white')

        #Observação
        self.lb_obs_editar = Label(self.root9, text="Observação")
        self.lb_obs_editar.place(relx=0.363, rely=0.75, relwidth=0.267, relheight=0.03)
        self.lb_obs_editar.configure(font='Arial 15 bold' ,background='#4F4F4F', foreground='white')

        
        ############################## ENTRYS

        #ID
        self.entry_Man_ID_manutencao_editar = Entry(self.root9)
        self.entry_Man_ID_manutencao_editar.place(relx=0.315, rely=0.28, relwidth=0.04, relheight=0.04)
        self.entry_Man_ID_manutencao_editar.configure(bg='#eeeeee')

        #Manutenção Realizada
        self.entry_manutencao_editar = StringVar(self.root9)
        self.entry_manutencao_editar_options = ("Abastecimento", "Troca de Óleo", "Troca de Mangueiras", "Troca de Correias", "Bronzinamento", "Retífica", "Troca de Pneus")
        #self.entry_MArca_cadastrar.set("Ativo")
        self.popupMenu = OptionMenu(self.root9, self.entry_manutencao_editar, *self.entry_manutencao_editar_options)
        self.popupMenu.place(relx=0.365, rely=0.28, relwidth=0.26, relheight=0.04)


        #KM Atual
        self.entry_km_atual_editar = Entry(self.root9)
        self.entry_km_atual_editar.place(relx=0.365, rely=0.38, relwidth=0.26, relheight=0.04)
        self.entry_km_atual_editar.configure(bg='#eeeeee')

        #KM Próxima Manutenção
        self.entry_km_prox_manutencao_editar = Entry(self.root9)
        self.entry_km_prox_manutencao_editar.place(relx=0.365, rely=0.48, relwidth=0.26, relheight=0.04)
        self.entry_km_prox_manutencao_editar.configure(bg='#eeeeee')

        #DATA Próxima Manutenção
        self.entry_data_prox_manutencao_editar = Entry(self.root9)
        self.entry_data_prox_manutencao_editar.place(relx=0.365, rely=0.58, relwidth=0.26, relheight=0.04)
        self.entry_data_prox_manutencao_editar.configure(bg='#eeeeee')

        #Observação
        self.entry_obs_editar = Entry(self.root9)
        self.entry_obs_editar.place(relx=0.345, rely=0.78, relwidth=0.30, relheight=0.04)
        self.entry_obs_editar.configure(bg='#eeeeee')


        ############################## BOTÕES


        #Editar
        self.bt_editar_funcional = Button(self.root9, text="Editar", command = self.edita_manutencao)
        self.bt_editar_funcional.place(relx= 0.422, rely=0.9, relwidth=0.15, relheight=0.05)
        self.bt_editar_funcional.configure(font='Arial 12 bold', bd=2, bg='#eeeeee')

        #Voltar
        self.bt_voltar_editar = Button(self.root9, text="Voltar", command = self.root9.destroy)
        self.bt_voltar_editar.place(relx= 0.02, rely=0.02, relwidth=0.08, relheight=0.05)
        self.bt_voltar_editar.configure(font='Arial 12 bold', bd=2, bg='#eeeeee')

        self.lista_veiculos.selection()

        for n in self.lista_manutencao.selection():
            col2, col4, col5, col6, col7, col8, col9, col10 = self.lista_manutencao.item(n, 'values')
            self.entry_Man_ID_manutencao_editar.insert(END, col2)
            self.entry_km_atual_editar.insert(END, col6)
            self.entry_km_prox_manutencao_editar.insert(END, col7)
            self.entry_data_prox_manutencao_editar.insert(END, col8)
            self.entry_obs_editar.insert(END, col9)      



App()