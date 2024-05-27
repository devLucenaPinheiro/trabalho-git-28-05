import tkinter
from tkinter import messagebox as mb
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import sqlite3

#Criar uma branch em que le um config.txt com uma lista de 5 estados possiveis separados por pular linha - x1
#Mudar o separador para ; e adicionar mais 5 estados - x2
#Voltar para main, criar outra branch e criar um dropdown com 3 opções (clt, mei, socio) - y1
#Voltar para main, Corrigir o bug da função de cpf - v5
#Merge de x com v - v6
#Adicionar verificação de CPF e de estado, com base na função cpf e na lista de estados .txt antes de adicionar no sqlite v7

# Cria conexão
connection = sqlite3.connect("teste.db")

# Cria o cursor e a tabela
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS Tabela1 (nome TEXT, cpf TEXT, estado TEXT)")

def VerificarCPF(CPF):
    # CPF deve ser na forma "123.456.789-10"
    partes = CPF.split("-")
    if len(partes) != 2 or len(partes[1]) != 2:
        return False
    if len(partes[0].split(".")) != 3:
        return False
    for trecho in partes[0].split("."):
        if len(trecho) != 3:
            return False
    return True

def inserevalores(nome, cpf, estado):
    # Insere linha na tabela
    cursor.execute("INSERT INTO Tabela1 VALUES (?, ?, ?)", (nome, cpf, estado))
    connection.commit()
    mb.showinfo("Info", "Dados salvos com sucesso!")

def pegavalores():
    # Pega valores da tabela
    rows = cursor.execute("SELECT * FROM Tabela1").fetchall()
    print(rows)

def Main():
    root = tkinter.Tk()
    root.title("Trabalho RAD")
    root.resizable(False, False)
    root.geometry("600x400")

    # Adicionando a imagem de fundo
    image = Image.open("ceuazul.png")
    photo = ImageTk.PhotoImage(image)
    background_label = ttk.Label(root, image=photo)
    background_label.place(relwidth=1, relheight=1)

    frame = tkinter.Frame(root, bg='white')
    frame.place(relx=0.5, rely=0.5, anchor='center')

    label = tkinter.Label(frame, text="Nome")
    label.grid(row=0, column=0)

    nome_var = tkinter.StringVar()
    nome_entry = tkinter.Entry(frame, textvariable=nome_var)
    nome_entry.grid(row=0, column=1)

    label = tkinter.Label(frame, text="Cpf")
    label.grid(row=1, column=0)

    cpf_var = tkinter.StringVar()
    cpf_entry = tkinter.Entry(frame, textvariable=cpf_var)
    cpf_entry.grid(row=1, column=1)

    label = tkinter.Label(frame, text="Estado")
    label.grid(row=2, column=0)

    estado_var = tkinter.StringVar()
    estado_entry = tkinter.Entry(frame, textvariable=estado_var)
    estado_entry.grid(row=2, column=1)

    def salvar():
        nome = nome_var.get()
        cpf = cpf_var.get()
        estado = estado_var.get()
        if VerificarCPF(cpf):
            inserevalores(nome, cpf, estado)
        else:
            mb.showerror("Erro", "CPF inválido!")

    salvar_btn = tkinter.Button(frame, text="Salvar", command=salvar)
    salvar_btn.grid(row=3, columnspan=2)

    root.mainloop()

Main()