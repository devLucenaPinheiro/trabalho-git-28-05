import tkinter
from tkinter import messagebox as mb
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import sqlite3

connection = sqlite3.connect("teste.db")

cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS Tabela1 (nome TEXT, cpf TEXT, estado TEXT)")

def VerificarCPF(CPF):
    partes = CPF.split("-")
    if len(partes) != 2 or len(partes[1]) != 2:
        return False
    if len(partes[0].split(".")) != 3:
        return False
    for trecho in partes[0].split("."):
        if len(trecho) != 3:
            return False
        try:
            int(trecho) 
        except ValueError:
            return False
    return True

def ler_estados_config():
    estados = []
    try:
        with open("config.txt", "r") as file:
            estados = file.read().strip().split(";")
    except FileNotFoundError:
        mb.showerror("Erro", "Arquivo config.txt não encontrado!")
    return estados

def inserevalores(nome, cpf, estado):
    cursor.execute("INSERT INTO Tabela1 VALUES (?, ?, ?)", (nome, cpf, estado))
    connection.commit()
    mb.showinfo("Info", "Dados salvos com sucesso!")

def pegavalores():
    rows = cursor.execute("SELECT * FROM Tabela1").fetchall()
    print(rows)

def Main():
    root = tkinter.Tk()
    root.title("Trabalho RAD")
    root.resizable(False, False)
    root.geometry("600x400")

    image = Image.open("background-azul.jpg")
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

    estados = ler_estados_config()

    estado_var = tkinter.StringVar()
    estado_combo = ttk.Combobox(frame, textvariable=estado_var, values=estados)
    estado_combo.grid(row=2, column=1)

    def salvar():
        nome = nome_var.get()
        cpf = cpf_var.get()
        estado = estado_var.get()
        if VerificarCPF(cpf):
            if estado in estados:
                inserevalores(nome, cpf, estado)
            else:
                mb.showerror("Erro", "Estado inválido!")
        else:
            mb.showerror("Erro", "CPF inválido!")

    salvar_btn = tkinter.Button(frame, text="Salvar", command=salvar)
    salvar_btn.grid(row=3, columnspan=2)

    root.mainloop()

Main()
