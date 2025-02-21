import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import json
import os

class GestionarProductos:
    def __init__(self, root):
        self.root = root
        self.ventana_productos = tk.Toplevel(root)
        self.ventana_productos.title("Gestionar Productos")
        self.ventana_productos.geometry("900x400")
        self.ventana_productos.configure(bg='#2c2c2c')
        
        self.archivo_productos = 'productos.json'
        self.productos = []
        self.orden_tipo_precio = False

        # Lista de productos
        self.tree = ttk.Treeview(self.ventana_productos, columns=("Codigo Cedar Creek", "Nombre del producto","Unidades por caja","UM","Codigo UPC","Tipo de precio","Kgs por caja"), show='headings')
        self.tree.heading("Codigo Cedar Creek", text="Codigo Cedar Creek")
        self.tree.heading("Nombre del producto", text="Nombre del producto")
        self.tree.heading("Unidades por caja",text="Unidades por caja")
        self.tree.heading("UM",text="Unidad de medida")
        self.tree.heading("Codigo UPC",text="Codigo UPC")
        self.tree.heading("Tipo de precio",text="Tipo de precio", command=self.sort_by_tipo_precio)
        self.tree.heading("Kgs por caja",text="Kgs por caja")
        self.tree.column("Codigo Cedar Creek", width=100)
        self.tree.column("Nombre del producto", width=200)
        self.tree.column("Unidades por caja",width=100)
        self.tree.column("UM",width=50)
        self.tree.column("Codigo UPC",width=100)
        self.tree.column("Tipo de precio",width=100)
        self.tree.column("Kgs por caja",width=50)        
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        # Botones de acción
        btn_agregar = tk.Button(self.ventana_productos, text="Agregar", command=self.agregar_producto, bg='#1f1f1f', fg='#ffffff')
        btn_modificar = tk.Button(self.ventana_productos, text="Modificar", command=self.modificar_producto, bg='#1f1f1f', fg='#ffffff')
        btn_eliminar = tk.Button(self.ventana_productos, text="Eliminar", command=self.eliminar_producto, bg='#1f1f1f', fg='#ffffff')

        btn_agregar.pack(side=tk.LEFT, padx=10, pady=10)
        btn_modificar.pack(side=tk.LEFT, padx=10, pady=10)
        btn_eliminar.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.cargar_productos()
        
    def cargar_productos(self):
        if os.path.exists(self.archivo_productos):
            with open(self.archivo_productos, 'r', encoding='utf-8') as file:
                self.productos = json.load(file)
                #for producto in self.productos:
                #    self.tree.insert("",tk.END, values = (producto['Codigo Cedar Creek'], producto['Nombre del producto'], producto['Unidades por caja'], producto['UM'], producto['Codigo UPC'], producto['Tipo de precio'] ,producto['Kgs por caja']))
                self.actualizar_treeview()

    def actualizar_treeview(self):
        """ Refresh the Treeview with current data """
        # First, clear the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert all products into the Treeview
        for producto in self.productos:
            self.tree.insert("", tk.END, values=(producto['Codigo Cedar Creek'], producto['Nombre del producto'], producto['Unidades por caja'], producto['UM'], producto['Codigo UPC'], producto['Tipo de precio'], producto['Kgs por caja']))

    def sort_by_tipo_precio(self):
        """ Sort products by 'Tipo de precio' """
        self.productos = sorted(self.productos, key=lambda x: x['Tipo de precio'], reverse=self.orden_tipo_precio)
        self.orden_tipo_precio = not self.orden_tipo_precio  # Toggle sorting order
        self.actualizar_treeview()


    def guardar_productos(self):
        with open(self.archivo_productos, 'w', encoding='utf-8') as file:
            json.dump(self.productos, file, indent=4)

    def agregar_producto(self):
        ventana_ingreso = tk.Toplevel(self.root)
        ventana_ingreso.title("Agregar Producto")
        ventana_ingreso.geometry("400x400")
        ventana_ingreso.configure(bg='#2c2c2c')

        # Etiquetas y campos de entrada
        tk.Label(ventana_ingreso, text="Codigo Cedar Creek:", bg='#2c2c2c', fg='#ffffff').grid(row=0, column=0, padx=10, pady=10)
        tk.Label(ventana_ingreso, text="Nombre del producto:", bg='#2c2c2c', fg='#ffffff').grid(row=1, column=0, padx=10, pady=10)
        tk.Label(ventana_ingreso, text="Unidades por caja:", bg='#2c2c2c', fg='#ffffff').grid(row=2, column=0, padx=10, pady=10)
        tk.Label(ventana_ingreso, text="UM:", bg='#2c2c2c', fg='#ffffff').grid(row=3, column=0, padx=10, pady=10)
        tk.Label(ventana_ingreso, text="Codigo UPC:", bg='#2c2c2c', fg='#ffffff').grid(row=4, column=0, padx=10, pady=10)
        tk.Label(ventana_ingreso, text="Tipo de precio:", bg='#2c2c2c', fg='#ffffff').grid(row=5, column=0, padx=10, pady=10)
        tk.Label(ventana_ingreso, text="Kgs por caja:", bg='#2c2c2c', fg='#ffffff').grid(row=6, column=0, padx=10, pady=10)


        entrada_codigo_cedar_creek = tk.Entry(ventana_ingreso, width=30)
        entrada_nombre_producto = tk.Entry(ventana_ingreso, width=30)
        entrada_unidades_por_caja = tk.Entry(ventana_ingreso, width=30)
        combobox_um = ttk.Combobox(ventana_ingreso, values=["CTN","KGS"], state="readonly", width=28)
        entrada_codigo_upc = tk.Entry(ventana_ingreso, width=30)
        combobox_tipo_de_precio = ttk.Combobox(ventana_ingreso, values=["Carniceria Tottus", "Carniceria Unimarc", "Molidas Tottus y Unimarc"], state="readonly", width=30)
        entrada_kgs_por_caja = tk.Entry(ventana_ingreso, width=30)
        
        
        entrada_codigo_cedar_creek.grid(row=0, column=1, padx=10, pady=10)
        entrada_nombre_producto.grid(row=1, column=1, padx=10, pady=10)
        entrada_unidades_por_caja.grid(row=2, column=1, padx=10, pady=10)
        combobox_um.grid(row=3, column=1, padx=10, pady=10)
        entrada_codigo_upc.grid(row=4, column=1, padx=10, pady=10)
        combobox_tipo_de_precio.grid(row=5, column=1, padx=10, pady=10)
        entrada_kgs_por_caja.grid(row=6, column=1, padx=10, pady=10)
        
        def guardar_nuevo_producto():
            codigo_cedar_creek = entrada_codigo_cedar_creek.get()
            nombre_producto = entrada_nombre_producto.get()
            unidades_por_caja = entrada_unidades_por_caja.get()
            um = combobox_um.get()
            codigo_upc = entrada_codigo_upc.get()
            tipo_de_precio = combobox_tipo_de_precio.get()
            kgs_por_caja = entrada_kgs_por_caja.get()
            
            
            if codigo_cedar_creek and nombre_producto and unidades_por_caja and um and codigo_upc and tipo_de_precio and kgs_por_caja:
                nuevo_producto = {'Codigo Cedar Creek': codigo_cedar_creek, 'Nombre del producto': nombre_producto, 'Unidades por caja': unidades_por_caja, 'UM': um, 'Codigo UPC': codigo_upc, 'Tipo de precio': tipo_de_precio, 'Kgs por caja': kgs_por_caja}
                self.productos.append(nuevo_producto)
                self.tree.insert("", tk.END, values=(codigo_cedar_creek, nombre_producto, unidades_por_caja, um, codigo_upc, tipo_de_precio, kgs_por_caja))
                self.guardar_productos()
                ventana_ingreso.destroy()
            else:
                messagebox.showwarning("Datos incompletos", "Debe ingresar todos los datos para agregar un producto.")

        # Botón para guardar el nuevo local
        btn_guardar = tk.Button(ventana_ingreso, text="Guardar", command=guardar_nuevo_producto, bg='#1f1f1f', fg='#ffffff')
        btn_guardar.grid(row=7, column=0, columnspan=2, pady=10)

    def modificar_producto(self):
        # Lógica para modificar un producto existente
        seleccion = self.tree.selection()
        if seleccion:
            indice = self.tree.index(seleccion[0])
            producto_actual = self.productos[indice]

            ventana_editar = tk.Toplevel(self.root)
            ventana_editar.title("Modificar Producto")
            ventana_editar.geometry("400x400")
            ventana_editar.configure(bg='#2c2c2c')

            tk.Label(ventana_editar, text="Codigo Cedar Creek:", bg='#2c2c2c', fg='#ffffff').grid(row=0, column=0, padx=10, pady=10)
            tk.Label(ventana_editar, text="Nombre Producto:", bg='#2c2c2c', fg='#ffffff').grid(row=1, column=0, padx=10, pady=10)
            tk.Label(ventana_editar, text="Unidades por caja:", bg='#2c2c2c', fg='#ffffff').grid(row=2, column=0, padx=10, pady=10)
            tk.Label(ventana_editar, text="UM:", bg='#2c2c2c', fg='#ffffff').grid(row=3, column=0, padx=10, pady=10)
            tk.Label(ventana_editar, text="Codigo UPC:", bg='#2c2c2c', fg='#ffffff').grid(row=4, column=0, padx=10, pady=10)
            tk.Label(ventana_editar, text="Tipo de precio:", bg='#2c2c2c', fg='#ffffff').grid(row=5, column=0, padx=10, pady=10)
            tk.Label(ventana_editar, text="Kgs por caja:", bg='#2c2c2c', fg='#ffffff').grid(row=6, column=0, padx=10, pady=10)
                      
            
            entrada_codigo_cedar_creek = tk.Entry(ventana_editar, width=30)
            entrada_nombre_producto = tk.Entry(ventana_editar, width=30)
            entrada_unidades_por_caja = tk.Entry(ventana_editar, width=30)
            combobox_um = ttk.Combobox(ventana_editar, value=["KGS","CTN"], state="readonly", width=28)
            entrada_codigo_upc = tk.Entry(ventana_editar, width=30)
            combobox_tipo_de_precio = ttk.Combobox(ventana_editar, value=["Carniceria Tottus", "Carniceria Unimarc", "Molidas Tottus y Unimarc"], state="readonly", width=30)
            entrada_kgs_por_caja = tk.Entry(ventana_editar, width=30)
            
            
            
            entrada_codigo_cedar_creek.grid(row=0, column=1, padx=10, pady=10)
            entrada_nombre_producto.grid(row=1, column=1, padx=10, pady=10)
            entrada_unidades_por_caja.grid(row=2, column=1, padx=10, pady=10)
            combobox_um.grid(row=3, column=1, padx=10, pady=10)
            entrada_codigo_upc.grid(row=4, column=1, padx=10, pady=10)
            combobox_tipo_de_precio.grid(row=5, column=1, padx=10, pady=10)
            entrada_kgs_por_caja.grid(row=6, column=1, padx=10, pady=10)

            entrada_codigo_cedar_creek.insert(0, producto_actual['Codigo Cedar Creek'])
            entrada_nombre_producto.insert(0, producto_actual['Nombre del producto'])
            entrada_unidades_por_caja.insert(0, producto_actual['Unidades por caja'])
            combobox_um.set(producto_actual['UM'])
            entrada_codigo_upc.insert(0, producto_actual['Codigo UPC'])
            combobox_tipo_de_precio.insert(0, producto_actual['Tipo de precio'])
            entrada_kgs_por_caja.insert(0, producto_actual['Kgs por caja'])

            def guardar_modificacion():
                nuevo_codigo_cedar_creek = entrada_codigo_cedar_creek.get()
                nuevo_nombre_producto = entrada_nombre_producto.get()
                nuevo_unidades_por_caja = entrada_unidades_por_caja.get()
                nuevo_um = combobox_um.get()
                nuevo_codigo_upc = entrada_codigo_upc.get()
                nuevo_tipo_de_precio = combobox_tipo_de_precio.get()
                nuevo_kgs_por_caja = entrada_kgs_por_caja.get()
                
                
                
                if nuevo_codigo_cedar_creek and nuevo_nombre_producto and nuevo_unidades_por_caja and nuevo_um and nuevo_codigo_upc and nuevo_tipo_de_precio and nuevo_kgs_por_caja:
                    self.productos[indice] = {'Codigo Cedar Creek': nuevo_codigo_cedar_creek, 'Nombre del producto': nuevo_nombre_producto, 'Unidades por caja': nuevo_unidades_por_caja, 'UM': nuevo_unidades_por_caja, 'Codigo UPC': nuevo_codigo_upc, 'Tipo de precio': nuevo_tipo_de_precio, 'Kgs por caja': nuevo_kgs_por_caja}
                    self.tree.item(seleccion[0], values=(nuevo_codigo_cedar_creek, nuevo_nombre_producto, nuevo_unidades_por_caja, nuevo_um, nuevo_codigo_upc, nuevo_tipo_de_precio, nuevo_kgs_por_caja))
                    self.guardar_productos()
                    ventana_editar.destroy()
                else:
                    messagebox.showwarning("Datos incompletos", "Debe ingresar todos los datos para modificar el producto.")

            btn_guardar = tk.Button(ventana_editar, text="Guardar", command=guardar_modificacion, bg='#1f1f1f', fg='#ffffff')
            btn_guardar.grid(row=7, column=0, columnspan=2, pady=10)

    def eliminar_producto(self):
        seleccion = self.tree.selection()
        if seleccion:
            indice = self.tree.index(seleccion[0])
            self.productos.pop(indice)
            self.tree.delete(seleccion[0])
            self.guardar_productos()  

    