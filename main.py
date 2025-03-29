# main.py
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import smtplib
from email.message import EmailMessage

# --------------------
# 1) BANCO DE DADOS
# --------------------
def conectar_banco():
    """
    Cria (se não existir) e conecta ao banco de dados SQLite,
    criando as tabelas necessárias.
    """
    conn = sqlite3.connect("garden_center.db")
    cursor = conn.cursor()
    
    # Tabela de clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT,
            email TEXT,
            endereco TEXT
        )
    ''')

    # Tabela de orçamentos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orcamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            data TEXT,
            valor_total REAL,
            status TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )
    ''')

    # Tabela de serviços
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS servicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            preco REAL NOT NULL
        )
    ''')

    # Tabela que relaciona orçamentos com serviços
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS itens_orcamento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            orcamento_id INTEGER,
            servico_id INTEGER,
            quantidade INTEGER,
            preco_unitario REAL,
            FOREIGN KEY (orcamento_id) REFERENCES orcamentos(id),
            FOREIGN KEY (servico_id) REFERENCES servicos(id)
        )
    ''')

    conn.commit()
    conn.close()

# --------------------
# 2) FUNÇÕES DE E-MAIL
# --------------------
def enviar_email_confirmacao(nome, email):
    """
    Envia um e-mail de boas-vindas ao novo cliente.
    Substitua remetente e senha com suas credenciais reais.
    """
    remetente = "seuemail@gmail.com"  # Seu e-mail
    senha = "SENHA_DE_APLICATIVO"     # Senha de aplicativo do Gmail
    assunto = "Bem-vindo ao Garden Center"
    corpo = f"""
Olá {nome},

Seja bem-vindo ao Garden Center! Estamos muito felizes em tê-lo conosco.

Nosso compromisso é oferecer os melhores serviços de paisagismo e jardinagem 
para transformar seu espaço em um verdadeiro paraíso verde.

Se precisar de qualquer suporte, entre em contato conosco.

Atenciosamente,
Equipe Garden Center
"""

    msg = EmailMessage()
    msg.set_content(corpo)
    msg["Subject"] = assunto
    msg["From"] = remetente
    msg["To"] = email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(remetente, senha)
            server.send_message(msg)
        print(f"E-mail enviado com sucesso para {email}")
    except Exception as e:
        print(f"Erro ao enviar e-mail para {email}: {e}")

# --------------------
# 3) LÓGICA DE CLIENTES
# --------------------
def cadastrar_cliente():
    """
    Cadastra um novo cliente no banco de dados,
    enviando e-mail de confirmação se houver e-mail.
    """
    nome = entry_nome.get()
    telefone = entry_telefone.get()
    email = entry_email.get()
    endereco = entry_endereco.get()

    if nome and email:  # nome e e-mail obrigatórios
        conn = sqlite3.connect("garden_center.db")
        cursor = conn.cursor()
        # Inserir na tabela de clientes
        cursor.execute("""
            INSERT INTO clientes (nome, telefone, email, endereco) 
            VALUES (?, ?, ?, ?)
        """, (nome, telefone, email, endereco))
        conn.commit()
        conn.close()

        # Mensagem de sucesso no Tkinter
        messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")

        # Enviar e-mail de boas-vindas
        enviar_email_confirmacao(nome, email)

        # Limpar campos
        entry_nome.delete(0, tk.END)
        entry_telefone.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_endereco.delete(0, tk.END)
    else:
        messagebox.showerror("Erro", "O nome e o e-mail são obrigatórios!")

# --------------------
# 4) INTERFACE TKINTER
# --------------------
def main():
    # Conectar/Inicializar o banco
    conectar_banco()

    # Criar janela principal
    root = tk.Tk()
    root.title("Garden Center - Orçamentos")
    root.geometry("500x450")
    root.configure(bg="#DFF0D8")

    # Seção de Cadastro de Clientes
    tk.Label(root, text="Cadastro de Cliente", font=("Arial", 12, "bold"), bg="#DFF0D8").pack(pady=10)

    frame_cliente = tk.Frame(root, bg="#DFF0D8")
    frame_cliente.pack()

    tk.Label(frame_cliente, text="Nome:", bg="#DFF0D8").grid(row=0, column=0, sticky="w")
    global entry_nome
    entry_nome = tk.Entry(frame_cliente)
    entry_nome.grid(row=0, column=1)

    tk.Label(frame_cliente, text="Telefone:", bg="#DFF0D8").grid(row=1, column=0, sticky="w")
    global entry_telefone
    entry_telefone = tk.Entry(frame_cliente)
    entry_telefone.grid(row=1, column=1)

    tk.Label(frame_cliente, text="E-mail:", bg="#DFF0D8").grid(row=2, column=0, sticky="w")
    global entry_email
    entry_email = tk.Entry(frame_cliente)
    entry_email.grid(row=2, column=1)

    tk.Label(frame_cliente, text="Endereço:", bg="#DFF0D8").grid(row=3, column=0, sticky="w")
    global entry_endereco
    entry_endereco = tk.Entry(frame_cliente)
    entry_endereco.grid(row=3, column=1)

    # Botão de cadastro
    tk.Button(root, text="Cadastrar Cliente", command=cadastrar_cliente,
              bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), 
              padx=10, pady=5).pack(pady=10)

    # Rodar a aplicação
    root.mainloop()

# Execução do programa
if __name__ == "__main__":
    main()
