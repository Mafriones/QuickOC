import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import json
import os

class GestionarLocales:
    def __init__(self, root):
        self.root = root
        self.ventana_locales = tk.Toplevel(root)
        self.ventana_locales.title("Gestionar Locales")
        self.ventana_locales.geometry("800x400")
        self.ventana_locales.configure(bg='#2c2c2c')
        
        self.archivo_locales = 'locales.json'
        self.locales = []

        # Lista de locales
        self.tree = ttk.Treeview(self.ventana_locales, columns=("Rut", "Cliente", "Nombre Local"), show='headings')
        self.tree.heading("Rut", text="Rut")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Nombre Local", text="Nombre Local")
        self.tree.column("Rut", width=100)
        self.tree.column("Cliente", width=100)
        self.tree.column("Nombre Local", width=200)
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        # Botones de acción
        btn_agregar = tk.Button(self.ventana_locales, text="Agregar", command=self.agregar_local, bg='#1f1f1f', fg='#ffffff')
        btn_modificar = tk.Button(self.ventana_locales, text="Modificar", command=self.modificar_local, bg='#1f1f1f', fg='#ffffff')
        btn_eliminar = tk.Button(self.ventana_locales, text="Eliminar", command=self.eliminar_local, bg='#1f1f1f', fg='#ffffff')

        btn_agregar.pack(side=tk.LEFT, padx=10, pady=10)
        btn_modificar.pack(side=tk.LEFT, padx=10, pady=10)
        btn_eliminar.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.cargar_locales()
        
    def cargar_locales(self):
        if os.path.exists(self.archivo_locales):
            with open(self.archivo_locales, 'r', encoding='utf-8') as file:
                self.locales = json.load(file)
                for local in self.locales:
                    self.tree.insert("", tk.END, values = (local['Rut'], local['Cliente'], local['Nombre Local']))

    def guardar_locales(self):
        with open(self.archivo_locales, 'w', encoding='utf-8') as file:
            json.dump(self.locales, file, indent=4)

    def agregar_local(self):
        # Solicitar información al usuario
        ventana_ingreso = tk.Toplevel(self.root)
        ventana_ingreso.title("Agregar Local")
        ventana_ingreso.geometry("400x200")
        ventana_ingreso.configure(bg='#2c2c2c')

        # Etiquetas y campos de entrada
        tk.Label(ventana_ingreso, text="Rut:", bg='#2c2c2c', fg='#ffffff').grid(row=0, column=0, padx=10, pady=10)
        tk.Label(ventana_ingreso, text="Cliente", bg='#2c2c2c', fg='#ffffff').grid(row=1,column=0, padx=10, pady=10)
        tk.Label(ventana_ingreso, text="Nombre Local:", bg='#2c2c2c', fg='#ffffff').grid(row=2, column=0, padx=10, pady=10)

        entrada_rut = tk.Entry(ventana_ingreso, width=30)
        # combobox_cliente = ttk.Combobox(ventana_ingreso, values=["Tottus","Unimarc"], state="readonly",width=28)
        combobox_cliente = tk.Entry(ventana_ingreso, width=30)
        entrada_nombre = tk.Entry(ventana_ingreso, width=30)
        entrada_rut.grid(row=0, column=1, padx=10, pady=10)
        combobox_cliente.grid(row=1, column=1, padx=10, pady=10)
        entrada_nombre.grid(row=2, column=1, padx=10, pady=10)

        def guardar_nuevo_local():
            rut = entrada_rut.get()
            nombre_cliente = combobox_cliente.get()
            nombre_local = entrada_nombre.get()
            if rut and nombre_local and nombre_cliente:
                nuevo_local = {'Rut': rut, 'Cliente': nombre_cliente,'Nombre Local': nombre_local}
                self.locales.append(nuevo_local)
                self.tree.insert("", tk.END, values=(rut, nombre_cliente, nombre_local))
                self.guardar_locales()
                ventana_ingreso.destroy()
            else:
                messagebox.showwarning("Datos incompletos", "Debe ingresar todos los datos para agregar un local.")

        # Botón para guardar el nuevo local
        btn_guardar = tk.Button(ventana_ingreso, text="Guardar", command=guardar_nuevo_local, bg='#1f1f1f', fg='#ffffff')
        btn_guardar.grid(row=3, column=0, columnspan=2, pady=10)

    def modificar_local(self):
        seleccion = self.tree.selection()
        if seleccion:
            indice = self.tree.index(seleccion[0])
            local_actual = self.locales[indice]
            ventana_editar = tk.Toplevel(self.root)
            ventana_editar.title("Modificar Local")
            ventana_editar.geometry("400x200")
            ventana_editar.configure(bg='#2c2c2c')

            tk.Label(ventana_editar, text="Rut:", bg='#2c2c2c', fg='#ffffff').grid(row=0, column=0, padx=10, pady=10)
            tk.Label(ventana_editar, text="Cliente:", bg='#2c2c2c', fg='#ffffff').grid(row=1, column=0, padx=10, pady=10)
            tk.Label(ventana_editar, text="Nombre Local:", bg='#2c2c2c', fg='#ffffff').grid(row=2, column=0, padx=10, pady=10)

            entrada_rut = tk.Entry(ventana_editar, width=30)
            # combobox_cliente = ttk.Combobox(ventana_editar, values=["Tottus","Unimarc"], state="readonly", width=30)
            combobox_cliente = tk.Entry(ventana_editar, width=30)
            entrada_nombre = tk.Entry(ventana_editar, width=30)
            entrada_rut.grid(row=0, column=1, padx=10, pady=10)
            combobox_cliente.grid(row=1, column=1,padx=10,pady=10)
            entrada_nombre.grid(row=2, column=1, padx=10, pady=10)

            entrada_rut.insert(0, local_actual['Rut'])
            combobox_cliente.insert(0, local_actual['Cliente'])
            entrada_nombre.insert(0, local_actual['Nombre Local'])

            def guardar_modificacion():
                nuevo_rut = entrada_rut.get()
                nuevo_cliente = combobox_cliente.get()
                nuevo_nombre_local = entrada_nombre.get()
                if nuevo_rut and nuevo_nombre_local:
                    self.locales[indice] = {'Rut': nuevo_rut, 'Cliente': nuevo_cliente, 'Nombre Local': nuevo_nombre_local}
                    self.tree.item(seleccion[0], values=(nuevo_rut, nuevo_cliente, nuevo_nombre_local))
                    self.guardar_locales()
                    ventana_editar.destroy()
                else:
                    messagebox.showwarning("Datos incompletos", "Debe ingresar todos los datos para modificar el local.")

            btn_guardar = tk.Button(ventana_editar, text="Guardar", command=guardar_modificacion, bg='#1f1f1f', fg='#ffffff')
            btn_guardar.grid(row=3, column=0, columnspan=2, pady=10)


    def eliminar_local(self):
        seleccion = self.tree.selection()
        if seleccion:
            indice = self.tree.index(seleccion[0])
            self.locales.pop(indice)
            self.tree.delete(seleccion[0])
            self.guardar_locales()