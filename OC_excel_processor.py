import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import json
import os
import re
import math
from datetime import datetime, timedelta
from gestionar_locales import GestionarLocales
from gestionar_productos import GestionarProductos
from bs4 import BeautifulSoup
from io import StringIO

# Definición de colores
COLOR_FONDO = '#2c2c2c'  # Color de fondo oscuro
COLOR_PANEL = '#d75e3b'  # Color logo
COLOR_TEXTO = '#ebf5fb'  # Texto blanco
COLOR_BOTON_FONDO = '#000000'  # Fondo negro para los botones
COLOR_BOTON_BORDE = '#FFD700'  # Borde dorado para los botones
COLOR_HOVER = '#d75e3b'        # Color logo para hover

class OrdenesCompraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ordenes de Compra")
        self.root.configure(bg=COLOR_FONDO)
        self.root.geometry("500x250")
        self.root.resizable(False,False)
        self.root.iconbitmap("OC_icon_v3.ico")  # Reemplaza con la ruta de tu archivo .ico

        self.locales = []
        self.archivos = []
        self.df = pd.DataFrame()  # DataFrame para almacenar la información
        self.current_combobox = None  # Para manejar la edición de celdas

        self.cargar_locales()

        # Título
        self.label_title = tk.Label(root, text="Procesador de Ordenes de Compra",
                                    fg=COLOR_TEXTO,
                                    bg=COLOR_PANEL,
                                    font=('Arial', 18),
                                    bd=2,
                                    relief='solid')
        self.label_title.pack(side=tk.TOP, fill=tk.X, pady=10)

        # Botones principales
        self.btn_cargar_archivos = tk.Button(root, text="Cargar Archivos de Ordenes de Compra (.xls)",
                                            command=self.cargar_archivos,
                                            width=50,
                                            bg=COLOR_BOTON_FONDO,
                                            fg=COLOR_TEXTO, bd=3,
                                            relief='solid',
                                            highlightbackground=COLOR_BOTON_BORDE,
                                            highlightthickness=5, font=('Arial', 12))
        self.btn_cargar_archivos.pack(pady=10)

        self.buttons_frame = tk.Frame(root, bg=COLOR_FONDO)

        self.buttons_frame.pack(pady=10)

        self.btn_locales = tk.Button(self.buttons_frame, text="Locales",
                                    command=self.gestionar_locales,
                                    width=20,
                                    bg=COLOR_BOTON_FONDO,
                                    fg=COLOR_TEXTO,
                                    bd=3,
                                    relief='solid',
                                    highlightbackground=COLOR_BOTON_BORDE,
                                    highlightthickness=5,
                                    font=('Arial', 12))
        
        self.btn_locales.pack(side=tk.LEFT, padx=10)

        self.btn_productos = tk.Button(self.buttons_frame, text="Productos",
                                        command=self.gestionar_productos,
                                        width=20,
                                        bg=COLOR_BOTON_FONDO,
                                        fg=COLOR_TEXTO,
                                        bd=3,
                                        relief='solid',
                                        highlightbackground=COLOR_BOTON_BORDE,
                                        highlightthickness=5,
                                        font=('Arial', 12))
        
        self.btn_productos.pack(side=tk.LEFT, padx=10)

        self.btn_generar_excel = tk.Button(root, text="Generar Excel",
                                           command=self.generar_excel,
                                           width=50,
                                           bg=COLOR_BOTON_FONDO,
                                           fg=COLOR_TEXTO,
                                           bd=3,
                                           relief="solid",
                                           highlightbackground=COLOR_BOTON_BORDE,
                                           highlightthickness=5,
                                           font=('Arial', 12))
        self.btn_generar_excel.pack(pady=10)

        self.tree = None

        # Aplicar efecto hover a los botones
        self.apply_hover_effects()

    def apply_hover_effects(self):
        buttons = [
            self.btn_cargar_archivos,
            self.btn_locales,
            self.btn_productos,
            self.btn_generar_excel
        ]

        for button in buttons:
            button.bind("<Enter>", lambda event: event.widget.config(bg=COLOR_HOVER))
            button.bind("<Leave>", lambda event: event.widget.config(bg=COLOR_BOTON_FONDO))

    # Cargar locales desde locales.json
    def cargar_locales(self):
        archivo_locales = 'locales.json'
        if os.path.exists(archivo_locales):
            with open(archivo_locales, 'r', encoding='utf-8') as file:
                self.locales = json.load(file)

    def cargar_archivos(self):
        archivos = filedialog.askopenfilenames(filetypes=[("Archivos Excel/HTML", "*.xls")])
        # archivos = filedialog.askopenfilenames(filetypes=[("Archivos Excel/HTML", "*.xls;*.xlsx")])
        print("Archivos cargados")
        if archivos:
            self.archivos = archivos
            self.procesar_archivos()

    def es_archivo_html(self, archivo):
        try:
            with open(archivo, 'r', encoding='utf-8', errors='ignore') as file:
                inicio = file.read(512).lower()
                return '<html' in inicio or '<table' in inicio
        except:
            return False
        
    def extraer_local(self, content):
        pattern = r"Por cuenta del vendedor\s*(.*?)\s*Información Comprador"
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        if match:
            print( f"📍 Lugar de entrega encontrado: {match.group(1).strip()}")
            return match.group(1).strip()
        else:
            return "⚠️ Lugar de entrega no encontrado"
            

    def procesar_archivos(self):
            datos = []
            for archivo in self.archivos:
                try:
                    if self.es_archivo_html(archivo):
                        print(f"📄 Procesando como HTML: {archivo}")
                        with open(archivo, 'r', encoding='utf-8', errors='ignore') as file:
                            soup = BeautifulSoup(file, 'html.parser')

                        table = soup.find('table')
                        if table:
                            df = pd.read_html(StringIO(str(table)))[0]

                            if df.shape[0] >= 5 and df.shape[1] >= 5:
                                numero_orden_raw = str(df.iat[4, 0])
                                fecha_entrega_raw = str(df.iat[4, 4])
                            else:
                                content = df.iat[0, 0]
                                numero_orden_raw = re.search(r'Número de Orden de Compra:\s*(\d+)', content)
                                numero_orden_raw = numero_orden_raw.group(1) if numero_orden_raw else None

                                fecha_entrega_raw = re.search(r'Fecha de Entrega:\s*(\d{2}/\d{2}/\d{4})', content)
                                fecha_entrega_raw = fecha_entrega_raw.group(1) if fecha_entrega_raw else None

                                local = self.extraer_local(content)
                        else:
                            print(f"⚠️ No se encontró una tabla en {archivo}")
                            continue
                    else:
                        print(f"📊 Procesando como Excel: {archivo}")
                        if archivo.endswith('.xls'):
                            df = pd.read_excel(archivo, engine='xlrd')
                        else:
                            df = pd.read_excel(archivo, engine='openpyxl')

                        numero_orden_raw = str(df.iat[4, 0])
                        fecha_entrega_raw = str(df.iat[4, 4])

                    numero_orden = re.search(r'\d+', numero_orden_raw)
                    numero_orden = numero_orden.group(0) if numero_orden else None

                    # Filtro Fechas
                    if "CD COQUIMBO" in local:
                        fecha_entrega = pd.to_datetime(fecha_entrega_raw, dayfirst=True, errors='coerce')
                        fecha_entrega = fecha_entrega - timedelta(days=1) if pd.notnull(fecha_entrega) else None
                        fecha_producto = fecha_entrega if pd.notnull(fecha_entrega) else None
                    elif "CD SANTIAGO LDT CARNES" in local:
                        fecha_entrega = pd.to_datetime(fecha_entrega_raw, dayfirst=True, errors='coerce')
                        fecha_producto = fecha_entrega - timedelta(days=1) if pd.notnull(fecha_entrega) else None
                    elif "429 - Ice Star" in local:
                        fecha_entrega = pd.to_datetime(fecha_entrega_raw, dayfirst=True, errors='coerce')
                        fecha_producto = fecha_entrega - timedelta(days=1) if pd.notnull(fecha_entrega) else None

                    if numero_orden and pd.notnull(fecha_entrega):
                        datos.append([
                            numero_orden,
                            fecha_entrega.strftime('%Y-%m-%d'),
                            fecha_producto.strftime('%Y-%m-%d'),
                            local
                        ])
                    else:
                        print(f"❌ Datos incompletos en el archivo: {archivo}")

                except Exception as e:
                    print(f"❌ Error procesando {archivo}: {e}")

            self.df = pd.DataFrame(datos, columns=['Numero de Orden', 'Fecha Entrega', 'Fecha Producto', 'Local'])
            self.mostrar_tabla()


    # Extraer numero de orden
    def extraer_numero_orden(self, contenido):
        try:
            match = re.search(r'BGM\+220\+(\d{10})(\d{10})', contenido)
        
            if match:
                numero_orden = match.group(2)  # Extract the order number
                return numero_orden
            else:
                messagebox.showerror("Error", "Número de orden no encontrado en el archivo.")
                return None

        except Exception as e:
            print(f"Error extracting 'Numero de Orden': {e}")
            messagebox.showerror("Error", f"No se pudo extraer el número de orden: {e}")
            return None
        
        # Extraer fecha de entrega
    def extraer_fecha_entrega(self, contenido):
        try:

            # Intentar encontrar la fecha en diferentes formatos
            match = re.search(r'Fecha de Entrega:\s*(\d{2}/\d{2}/\d{4})', contenido)
            
            if match:
                fecha_entrega = match.group(1)
                return datetime.strptime(fecha_entrega, '%d/%m/%Y').strftime('%Y-%m-%d')
            else:
                print("⚠️ No se encontró 'Fecha de Entrega' en el contenido.")
                return None

        except Exception as e:
            print(f"❌ Error extrayendo 'Fecha de Entrega': {e}")
            return None

    def mostrar_tabla(self):
        if self.tree:
            self.tree.destroy()

        # Ajuste de tamaño de la ventana automáticamente
        local_mas_largo = max(self.df["Local"], key=len)
        n_archivos = len(self.archivos)
        alto_ventana = 300 + n_archivos * 20
        ancho_ventana = 500 + round(len(local_mas_largo) * 4.5)
        ancho_extra = ancho_ventana - 380
        str_geometria = f"{ancho_ventana}x{alto_ventana}"
        self.root.geometry(str_geometria)

        self.tree = ttk.Treeview(self.root, columns=('Numero de Orden',
                                                    'Fecha Entrega',
                                                    'Fecha Producto',
                                                    'Local'),
                                                    show='headings')
        self.tree.heading('Numero de Orden', text='Numero de Orden')
        self.tree.heading('Fecha Entrega', text='Fecha Entrega')
        self.tree.heading('Fecha Producto', text='Fecha Producto')
        self.tree.heading('Local', text='Local')

        self.tree.column('Numero de Orden', width=140)
        self.tree.column('Fecha Entrega', width=100)
        self.tree.column('Fecha Producto', width=100)
        self.tree.column('Local', width=ancho_extra)

        for index, row in self.df.iterrows():
            self.tree.insert('', 'end', values=(row['Numero de Orden'],
                                                row['Fecha Entrega'],
                                                row['Fecha Producto'],
                                                row['Local']))

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


        

    def generar_excel(self):
        datos = []
        for archivo in self.archivos:
            try:
                if self.es_archivo_html(archivo):
                    # print(f"Generando Excel a partir de HTML")
                    with open(archivo, 'r', encoding='utf-8', errors='ignore') as file:
                        soup = BeautifulSoup(file, 'html.parser')

                    table = soup.find('table')
                    if table:
                        df = pd.read_html(StringIO(str(table)))[0]

                        content = df.iat[0, 0]
                        # Crear json con los datos de la orden de compra
                        orden_compra = {
                            "Emisor": re.search(r"Emisor: (.+?) Receptor:", content).group(1),
                            "Receptor": re.search(r"Receptor: (.+?) Número de Orden", content).group(1),
                            "Numero de Orden": re.search(r"Número de Orden de Compra: (\d+)", content).group(1),
                            "Fecha Generacion": re.search(r"Fecha generación Mensaje: (\d{2}/\d{2}/\d{4})", content).group(1),
                            "Fecha de Entrega": re.search(r"Fecha de Entrega: (\d{2}/\d{2}/\d{4})", content).group(1),
                            # "Local": re.search(r"Información Comprador (.+?) Información Proveedor", content).group(1).strip(),
                            "Local": re.search(r"Por cuenta del vendedor\s*(.*?)\s*Información Comprador", content).group(1).strip(),
                            "Productos": []
                        }

                        # 📆 Calcular "Fecha de producto" (un día antes de la fecha de entrega)
                        fecha_entrega_dt = datetime.strptime(orden_compra["Fecha de Entrega"], "%d/%m/%Y")
                        fecha_producto_dt = fecha_entrega_dt - timedelta(days=1)
                        fecha_entrega_arreglada = fecha_entrega_dt.strftime("%Y-%m-%d")
                        if "CD COQUIMBO" in orden_compra["Local"]:
                            fecha_entrega_dt = fecha_entrega_dt - timedelta(days=1)
                            fecha_entrega_arreglada = fecha_entrega_dt.strftime("%Y-%m-%d")
                            orden_compra["Fecha de Producto"] = fecha_entrega_arreglada
                        elif "CD SANTIAGO LDT CARNES" in orden_compra["Local"]:
                            fecha_producto_dt = fecha_entrega_dt - timedelta(days=1)
                            orden_compra["Fecha de Producto"] = fecha_producto_dt.strftime("%Y-%m-%d")
                        elif "429 - Ice Star" in orden_compra["Local"]:
                            fecha_producto_dt = fecha_entrega_dt - timedelta(days=1)
                            orden_compra["Fecha de Producto"] = fecha_producto_dt.strftime("%Y-%m-%d")


                        # 📝 Cortar el contenido para buscar solo los productos
                        if "Cargos y descuentos aplicables al documento" in content:
                            content_cortado = content.split("Cargos y descuentos aplicables al documento", 1)[1]
                        else:
                            content_cortado = content  # Si no encuentra el content, deja el original

                        if "TOTTUS" not in orden_compra["Emisor"]:
                            print("Orden de compra no es de Tottus")
                            # 📝 Expresión regular mejorada para detectar todos los productos
                            productos = re.findall(
                                        (
                                            r"(\d{11,14})\s+"  # Código del producto
                                            r"([\w\s%]+?)\s+"  # Descripción del producto
                                            r"(\d{1,3}[,.\d]+)\s+"  # Cantidad
                                            r"(Cajas|Kilogramo|Kg)\s+"  # Unidad de cantidad
                                            r"[\d,]+\s+"  # Separador entre cantidad y tipo de unidad
                                            r"(Unid\.|Kilogramo)\s+"  # Tipo de unidad
                                            r"\$(\d{1,3}(?:[.,]\d{3})*)\s+\(Precio neto por unidad\)\s+"  # Precio unitario
                                            r"\$(\d{1,3}(?:[.,]\d{3})*)"  # Monto total
                                        ),
                                        content
                                    )
                            print(f"📦 Productos encontrados: {len(productos)}")

                            # 📊 Agregar productos al JSON
                            for producto in productos:
                                orden_compra["Productos"].append({
                                    "Codigo": producto[0],
                                    "Descripcion": producto[1].strip(),
                                    "Cantidad": producto[2],
                                    "Unidad": producto[3],
                                    "Precio Unitario": f"${producto[5]}",
                                    "Monto Total": f"${producto[6]}",
                                })
                        else:
                            print("Orden de compra es de Tottus")

                            # ---- PRUEBA POR SECCIONES ----

                            # 📌 Ver si encuentra códigos de productos
                            codigo_producto = re.findall(
                                r"\d{11,14}",  # Captura códigos de productos de 11 a 14 dígitos
                                content_cortado
                            )

                            # 📌 Ver si encuentra descripciones de productos
                            descripcion_producto = re.findall(
                                (
                                    r"\d{11,14}\s+"  # Código del producto
                                    r"([\w\s%.\-]+?)\s+"  # Descripción del producto
                                    r"\d{1,3}[,.\d]+(?:\s+Cajas|\s+Kilogramo|\s+Kg)"  # Cantidad seguida de la unidad
                                ),
                                content_cortado
                            )

                            # 📌 Ver si encuentra cantidades
                            cantidades = re.findall(
                                (
                                    r"(\d{1,3}[,.\d]+)"  # Cantidad (puede incluir coma o punto como separador)
                                    r"(?=\s+(?:Cajas|Kilogramo|Kg))"  # Debe estar seguida de la unidad especificada
                                ),
                                content_cortado
                            )

                            # 📌 Buscar un número entero entre "Cajas"/"Kilogramo" y "Unid."/"Kilogramo"
                            cantidad_unidad = re.findall(
                                (
                                    r"(?:Cajas|Kilogramo)\s+"  # Debe estar precedido por "Cajas" o "Kilogramo"
                                    r"(\d{1,3}[,.]?\d{0,3})\s+"  # Número de unidades, con o sin separador decimal
                                    r"(?:Unid\.|Kilogramo)"  # Debe estar seguido por "Unid." o "Kilogramo"
                                ),
                                content_cortado
                            )

                            # 📌 Ver si encuentra unidades (Cajas, Kilogramo, Kg)
                            unidades = re.findall(
                                r"(Cajas|Kilogramo|Kg)",  # Captura cualquiera de estas unidades
                                content_cortado
                            )

                            # 📌 Ver si encuentra el tipo de unidad (Unid. o Kilogramo) antes del precio
                            tipo_unidad = re.findall(
                                r"(Unid\.|Kilogramo)(?=\s+\$)",  # Busca "Unid." o "Kilogramo" justo antes de un precio
                                content_cortado
                            )

                            # 📌 Ver si encuentra precios unitarios
                            precios_unitarios = re.findall(
                                (
                                    r"\$(\d{1,3}(?:[.,]\d{3})*)"  # Precio con formato de separadores de miles
                                    r"(?=\s+\(Precio lista\))"  # Debe estar seguido de "(Precio lista)"
                                ),
                                content_cortado
                            )

                            # 📌 Ver si encuentra montos totales
                            monto_total = re.findall(
                                (
                                    r"(?<!TOTAL\s)"  # Asegura que no está precedido por la palabra "TOTAL"
                                    r"\$(\d{1,3}(?:[.,]\d{3})*)"  # Captura montos en formato correcto
                                    r"(?:\s+DESCUENTO|\s*$)"  # Debe estar seguido de "DESCUENTO" o final de línea
                                ),
                                content_cortado
                            )

                            # 📌 Unir todos los datos en una lista de tuplas (una por producto)
                            productos = list(zip(
                                codigo_producto,  # Código del producto
                                descripcion_producto,  # Descripción del producto
                                cantidades,  # Cantidad del producto
                                unidades,  # Unidad de medida (Cajas/Kilogramo)
                                tipo_unidad,  # Tipo de unidad (Unid./Kilogramo)
                                precios_unitarios,  # Precio unitario
                                monto_total,  # Monto total
                                cantidad_unidad  # Cantidad por unidad
                            ))


                            print(f"📦 Productos encontrados: {len(productos)}")

                            # 📊 Agregar productos al JSON
                            for producto in productos:
                                orden_compra["Productos"].append({
                                    "Codigo": producto[0],
                                    "Descripcion": producto[1].strip(),
                                    "Cantidad": producto[2],
                                    "Unidad": producto[3],
                                    "Precio Unitario": f"${producto[5]}",
                                    "Monto Total": f"${producto[6]}",
                                    "Cantidad Unidad": producto[7]
                                })
                        
                        productos_lista = []
                        with open("productos.json", "r", encoding="utf-8") as file:
                            productos_json = json.load(file)

                        # Filtros Productos
                        for producto in productos:

                            # Buscar el codigo de Cedar Creek
                            codigo_cedar = next((l["Codigo Cedar Creek"] for l in productos_json if int(l["Codigo UPC"]) == int(producto[0])),
                                                 "No encontrado")
                            # Filtro kilos escalopa
                            if producto[3] == "Kilogramo":
                                
                                divisor = next((l["Kgs por caja"] for l in productos_json if int(l["Codigo UPC"]) == int(producto[0])),
                                                "No encontrado")
                                UM = next((l["UM"] for l in productos_json if int(l["Codigo UPC"]) == int(producto[0])), "No encontrado")

                                if UM == "KGS":
                                    cantidad = float(producto[2].replace(",", ".")) / float(divisor)
                                    if "ESCALOPA" in producto[1]:
                                        
                                        kilos = float(producto[2].replace(",", "."))

                                        if kilos > 50  and kilos <= 100:
                                            cantidad = math.ceil(cantidad)
                                        elif kilos > 100 and kilos <= 150:
                                            cantidad = math.ceil(cantidad)
                                            cantidad += 1
                                        elif kilos > 150 and kilos <= 200:
                                            cantidad = math.ceil(cantidad)
                                            cantidad += 2
                                        elif kilos > 200 and kilos <= 300:
                                            cantidad = math.ceil(cantidad)
                                            cantidad += 3
                                        elif kilos > 300:
                                            c_extra = math.ceil(kilos/100)
                                            cantidad = math.ceil(cantidad) + c_extra
                                        else:
                                            cantidad = math.trunc(cantidad)
                                        
                                        precio_unidad = float(producto[5].replace(".", "")) * float(divisor)
                                        precio_unidad = round(precio_unidad)


                                    else:
                                        precio_unidad = float(producto[5].replace(".", "")) * float(divisor)
                                else:
                                    cantidad = float(producto[7].replace(",", "."))
                                    cantidad = math.ceil(cantidad)
                                    precio_unidad = float(producto[5].replace(".", "")) 

                            else:
                                cantidad = float(producto[2].replace(",", "."))
                                cantidad = math.ceil(cantidad)
                                precio_unidad = float(producto[5].replace(".", "")) 

                            productos_lista.append({
                                "Líneas del pedido/Producto/Referencia interna": codigo_cedar,
                                # "Codigo": producto[0],
                                # "Descripcion": producto[1].strip(),
                                "Líneas del pedido/Cantidad": cantidad,
                                # "Unidad": producto[3],
                                "Líneas del pedido/Precio un.": precio_unidad,
                                # "Monto Total": float(producto[6].replace(".", ""))
                            })

                        # 📂 Generar DataFrame para exportación a Excel
                        df_productos = pd.DataFrame(productos_lista)

                        with open("locales.json", "r", encoding="utf-8") as file:
                            locales = json.load(file)
                        nombre_local = next((l["Nombre Local"] for l in locales if l["Cliente"] == orden_compra["Local"]), "No encontrado")
                        # print(f"Este es el nombre de local: {nombre_local}")
                        
                        # Obtener numero de orden de compra correcto
                        N_O_C = int(orden_compra["Numero de Orden"])
                        N_O_C = str(N_O_C)[-11:]
                        N_O_C = str(N_O_C)[:10]
                        N_O_C = int(N_O_C)

                        # Añadir columnas de la orden a cada fila
                        df_productos.insert(0, "Cliente", nombre_local)
                        df_productos.insert(1, "Fecha de producto", orden_compra["Fecha de Producto"])
                        df_productos.insert(2, "Fecha orden", fecha_entrega_arreglada)
                        df_productos.insert(3, "Fecha de entrega", fecha_entrega_arreglada)
                        df_productos.insert(4, "Orden de compra", N_O_C)
                        df_productos.insert(5, "Tipo Documento", "FAC")
                        # df_productos.insert(3, "Orden de compra", N_O_C)
                        # df_productos.insert(4, "Tipo Documento", "FAC")

                        # display(df_productos)
                        
                        datos.append(df_productos)
                        print("✅ Datos guardados en DataFrame")
                        #messagebox.showinfo("Exito", "Datos guardados en DataFrame")

                    else:
                        print(f"⚠️ No se encontró una tabla en {archivo}")
                        continue
                else:
                    print(f"❌ El archivo actual no es un HTML")

            except Exception as e:
                print(f"❌ Error procesando {archivo}: {e}")

        # 📑 Guardar los datos en un archivo Excel
        if datos:
            df_final = pd.concat(datos, ignore_index=True)

            # 📝 Aplicar la eliminación de duplicados POR ORDEN DE COMPRA
            columnas_orden = ["Cliente", "Fecha de producto", "Fecha orden", "Fecha de entrega", "Orden de compra", "Tipo Documento"]
            # Para cada orden de compra, eliminamos los valores repetidos dejando solo el primero
            df_final[columnas_orden] = df_final.groupby("Orden de compra")[columnas_orden].transform(
                lambda x: x.mask(x.duplicated(), ""))
            
            # 📂 Pedir ubicación para guardar el archivo
            nombre_archivo = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Archivos Excel", "*.xlsx")],
                title="Guardar archivo Excel"
            )
            if nombre_archivo:
                df_final.to_excel(nombre_archivo, index=False)
                messagebox.showinfo("Éxito", f"Archivo Excel generado: {nombre_archivo}")
            else:
                print("⚠️ Operación cancelada, archivo no guardado.")

    def gestionar_locales(self):
        GestionarLocales(self.root)

    def gestionar_productos(self):
        GestionarProductos(self.root) 

if __name__ == "__main__":
    root = tk.Tk()
    app = OrdenesCompraApp(root)
    root.mainloop()