import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import json
import os

class GestionarLocales:
    def __init__(self, root): 
        self.root = root # Crea la raiz de la App
        self.ventana_locales = tk.Toplevel(root) # Crea la ventana
        self.ventana_locales.title("Gestionar Locales") # Titulo de la ventana
        self.ventana_locales.geometry("800x400") # Tamaño de la ventana
        self.ventana_locales.configure(bg='#2c2c2c') # color de fondo de la ventana
        
        self.archivo_locales = 'locales.json' # Establece el archivo_locales como el archivo lcoales.json
        self.locales = [] # Crea una lista vacia para almacenar los locales

        # Lista de locales
        self.tree = ttk.Treeview(self.ventana_locales, columns=("Rut", "Cliente", "Nombre Local"), show='headings') # Crea el arbol con los titulos
                                                                                                                    # De las columnas de las tablas
        self.tree.heading("Rut", text="Rut") # Establece el titulo de la columna
        self.tree.heading("Cliente", text="Cliente") # Establece el titulo de la columna
        self.tree.heading("Nombre Local", text="Nombre Local") # Establece el titulo de la columna
        self.tree.column("Rut", width=100) # Establece el ancho de la columna
        self.tree.column("Cliente", width=100) # Establece el ancho de la columna
        self.tree.column("Nombre Local", width=200) # Establece el ancho de la columna
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True) # pady agrega un espacio de 10 pixeles alrededor del widget
                                                           # fill = tk.BOTH hace que el widget se expanda vertical y horizontalmente para
                                                           # usar el espacio disponible
                                                           # expand = true permite que el widget crezca cuando la ventana se redimensiona

        # Botones de acción
        # Para cada uno de los 3 botones, se les adjunta la funcion que ejercen al ser apretados, la posicion, lo colores y la disposicion en la
        # ventana
        btn_agregar = tk.Button(self.ventana_locales, text="Agregar", command=self.agregar_local, bg='#1f1f1f', fg='#ffffff')
        btn_modificar = tk.Button(self.ventana_locales, text="Modificar", command=self.modificar_local, bg='#1f1f1f', fg='#ffffff')
        btn_eliminar = tk.Button(self.ventana_locales, text="Eliminar", command=self.eliminar_local, bg='#1f1f1f', fg='#ffffff')

        btn_agregar.pack(side=tk.LEFT, padx=10, pady=10)
        btn_modificar.pack(side=tk.LEFT, padx=10, pady=10)
        btn_eliminar.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.cargar_locales() # Llama a la funcion cargar_locales
        
    # Esta función llama a los locales del archivo json y los inserta en la tabla de la ventana
    def cargar_locales(self):
        if os.path.exists(self.archivo_locales): # Si el archivo existe en la carpeta
            with open(self.archivo_locales, 'r', encoding='utf-8') as file: # Lee el archivo json
                self.locales = json.load(file) # Carga el json en la variable locales
                for local in self.locales: # Inserta cada local en el arbol de la tabla
                    self.tree.insert("", tk.END, values = (local['Rut'], local['Cliente'], local['Nombre Local']))

    # Esta funcion abre el archivo json con los locales y guarda los locales en la variable de archivo_locales
    def guardar_locales(self):
        with open(self.archivo_locales, 'w', encoding='utf-8') as file:
            json.dump(self.locales, file, indent=4)

    # Esta funcion genera una ventana donde permite al usuario ingresar un nuevo local
    def agregar_local(self):
        # Solicitar información al usuario
        ventana_ingreso = tk.Toplevel(self.root) # Crea el tipo de ventana
        ventana_ingreso.title("Agregar Local") # Escribe el titulo de la ventana
        ventana_ingreso.geometry("400x200") # Le da tamaño a la ventana
        ventana_ingreso.configure(bg='#2c2c2c') # Le pone color al fondo de la ventana 

        # Etiquetas y campos de entrada
        tk.Label(ventana_ingreso, text="Rut:", bg='#2c2c2c', fg='#ffffff').grid(row=0, column=0, padx=10, pady=10) # Posiciona los campos donde se van
                                                                                                                   # a escribir los nuevos datos 
        tk.Label(ventana_ingreso, text="Cliente", bg='#2c2c2c', fg='#ffffff').grid(row=1,column=0, padx=10, pady=10)
        tk.Label(ventana_ingreso, text="Nombre Local:", bg='#2c2c2c', fg='#ffffff').grid(row=2, column=0, padx=10, pady=10)

        entrada_rut = tk.Entry(ventana_ingreso, width=30) # crea la caja de texto donde el usuario va a escribir los nuevos datos
        combobox_cliente = tk.Entry(ventana_ingreso, width=30) # ==
        entrada_nombre = tk.Entry(ventana_ingreso, width=30) # ==
        entrada_rut.grid(row=0, column=1, padx=10, pady=10) # posiciona la caja de texto
        combobox_cliente.grid(row=1, column=1, padx=10, pady=10) # ==
        entrada_nombre.grid(row=2, column=1, padx=10, pady=10)# ==

        # Esta funcion extrae la informacion de las cajas de texto creadas anteriormente, y las guarda en la variable de los locales
        # y llama a la funcion guardar locales para añadir el nuevo local al archivo json
        def guardar_nuevo_local():
            rut = entrada_rut.get() # obtiene los datos de rut
            nombre_cliente = combobox_cliente.get() # obtiene los datos de nombre de cliente
            nombre_local = entrada_nombre.get() # obtiene el nombre del local
            if rut and nombre_local and nombre_cliente:
                nuevo_local = {'Rut': rut, 'Cliente': nombre_cliente,'Nombre Local': nombre_local} # crea un diccionario con los datos de las cajas
                self.locales.append(nuevo_local) # añade el nuevo diccionario a la variable de locales
                self.tree.insert("", tk.END, values=(rut, nombre_cliente, nombre_local)) # inserta los valores nuevos en el arbol
                self.guardar_locales() # llama a la funcion de guardar locales
                ventana_ingreso.destroy() # destruye la ventana donde se ponen los datos
            else:
                messagebox.showwarning("Datos incompletos", "Debe ingresar todos los datos para agregar un local.")

        # Botón para guardar el nuevo local
        btn_guardar = tk.Button(ventana_ingreso, text="Guardar", command=guardar_nuevo_local, bg='#1f1f1f', fg='#ffffff') # Con este boton se llama
                                                                                                                          # a la funcion de guardar
                                                                                                                          # locales
        btn_guardar.grid(row=3, column=0, columnspan=2, pady=10) # crea una cuadricula

        

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