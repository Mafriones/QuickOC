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
        self.root = root # Crear raiz de la App
        self.root.title("Ordenes de Compra") # Titulo de la ventana
        self.root.configure(bg=COLOR_FONDO)  #Asigna color al fondo de la ventana
        self.root.geometry("500x250") # Le da el tamaño a la ventana
        self.root.resizable(False,False) # Bloquea la funcion de cambiar el tamaó de la ventana
        self.root.iconbitmap("OC_icon_v3.ico")  # Reemplaza con la ruta de tu archivo .ico

        self.locales = [] # Crea una lista vacia para almacenar los locales
        self.archivos = [] # Crea una lista vacia para almacenar los archivos
        self.df = pd.DataFrame()  # DataFrame para almacenar la información
        self.current_combobox = None  # Para manejar la edición de celdas

        self.cargar_locales() # Llama a la funcion cargar_locales

        # Formato del Título
        self.label_title = tk.Label(root, text="Procesador de Ordenes de Compra", # lo que dice el titulo 
                                    fg=COLOR_TEXTO, # color de la letra
                                    bg=COLOR_PANEL, # color del fondo
                                    font=('Arial', 18), # tipo de letra y tamaño
                                    bd=2, # borde
                                    relief='solid') # tipo de borde
        self.label_title.pack(side=tk.TOP, fill=tk.X, pady=10) # Posicion del titulo

        # Formato de los Botones principales
        self.btn_cargar_archivos = tk.Button(root, text="Cargar Archivos de Ordenes de Compra (.xls)",
                                            command=self.cargar_archivos, # Llama a la funcion cargar_archivos
                                            width=50, # ancho boton
                                            bg=COLOR_BOTON_FONDO, # color de fondo
                                            fg=COLOR_TEXTO, bd=3, # color de letra, borde
                                            relief='solid', # tipo de borde
                                            highlightbackground=COLOR_BOTON_BORDE, # color del borde
                                            highlightthickness=5, font=('Arial', 12)) # grosor del borde, tipo de letra y
        self.btn_cargar_archivos.pack(pady=10) # Posicion del boton

        self.buttons_frame = tk.Frame(root, bg=COLOR_FONDO) # Crea un marco para los botones

        self.buttons_frame.pack(pady=10) # Posicion del marco

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
                                           command=self.generar_excel, # Llama a la funcion generar_excel
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
        self.apply_hover_effects() # Llama a la funcion apply_hover_effects

    # Esta funcion aplica un cambio de color a los botones cuando el mouse pasa por encima
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
        archivo_locales = 'locales.json' # Nombre del archivo
        if os.path.exists(archivo_locales): # Si el archivo existe
            with open(archivo_locales, 'r', encoding='utf-8') as file: # Abre el archivo
                self.locales = json.load(file) # Carga los datos del archivo en la lista locales

    # Cargar archivos de ordenes de compra
    def cargar_archivos(self): 
        archivos = filedialog.askopenfilenames(filetypes=[("Archivos Excel/HTML", "*.xls")]) # Abre una ventana para seleccionar los archivos

        # Abre una ventana para seleccionar los archivos si se decide actualizar el formato de los archivos de ComercioNet
        # archivos = filedialog.askopenfilenames(filetypes=[("Archivos Excel/HTML", "*.xls;*.xlsx")]) 


        print("Archivos cargados") # Confirma que se cargaron los archivos en la consola
        if archivos:
            self.archivos = archivos # Guarda los archivos en la lista archivos
            self.procesar_archivos() # Llama a la funcion procesar_archivos

    # Verificar si el archivo es HTML
    def es_archivo_html(self, archivo):
        try: # Intenta hacer lo siguiente
            with open(archivo, 'r', encoding='utf-8', errors='ignore') as file: # Abre el archivo
                inicio = file.read(512).lower() # Lee los primeros 512 caracteres del archivo
                return '<html' in inicio or '<table' in inicio # Retorna verdadero si encuentra '<html' o '<table' en los primeros 512 caracteres
        except: # Si hay un error
            return False # Retorna falso si no encuentra '<html' o '<table' en los primeros 512 caracteres
    
    # Funcion que extrae el local desde el codigo extraido
    def extraer_local(self, contenido): 
        pattern = r"Por cuenta del vendedor\s*(.*?)\s*Información Comprador" # Patron para extraer el local entre el texto "Por cuenta del vendedor"
                                                                             # e "Información Comprador" 
        
        match = re.search(pattern, contenido, re.IGNORECASE | re.DOTALL) # Busca el patron en el contenido del archivo
        if match:
            print( f"📍 Lugar de entrega encontrado: {match.group(1).strip()}") # confirma que se encontró el local
            return match.group(1).strip() # Retorna el local encontrado
        else:
            return "⚠️ Lugar de entrega no encontrado" # Retorna un mensaje si no se encuentra el local
            
    # Procesar archivos de ordenes de compra (HTML y Excel) 
    def procesar_archivos(self):
            datos = [] # Crea una lista vacia para almacenar los datos
            for archivo in self.archivos: # Para cada archivo en la lista de archivos
                try:
                    if self.es_archivo_html(archivo): # Si el archivo es HTML
                        print(f"📄 Procesando como HTML: {archivo}") 
                        with open(archivo, 'r', encoding='utf-8', errors='ignore') as file: # Abre el archivo
                            soup = BeautifulSoup(file, 'html.parser') # Lee el archivo usando la extension BeautifulSoup

                        table = soup.find('table') # Busca una tabla en el archivo
                        if table: # Si encuentra una tabla
                            df = pd.read_html(StringIO(str(table)))[0] # Lee la tabla y la guarda en un DataFrame

                            if df.shape[0] >= 5 and df.shape[1] >= 5: # Si el DataFrame tiene al menos 5 filas y 5 columnas
                                numero_orden_raw = str(df.iat[4, 0]) # Extrae el numero de orden de la fila 4 columna 0
                                fecha_entrega_raw = str(df.iat[4, 4]) # Extrae la fecha de entrega de la fila 4 columna 4
                            else: # Si no tiene al menos 5 filas y 5 columnas
                                contenido = df.iat[0, 0] # Extrae el contenido de la fila 0 columna 0
                                numero_orden_raw = re.search(r'Número de Orden de Compra:\s*(\d+)', contenido) # Busca el numero de orden en el contenido
                                numero_orden_raw = numero_orden_raw.group(1) if numero_orden_raw else None # Extrae el numero de orden si lo encuentra
                                fecha_entrega_raw = re.search(r'Fecha de Entrega:\s*(\d{2}/\d{2}/\d{4})', contenido) # Busca la fecha de entrega en el contenido
                                fecha_entrega_raw = fecha_entrega_raw.group(1) if fecha_entrega_raw else None # Extrae la fecha de entrega si la encuentra
                                local = self.extraer_local(contenido) # Extrae el local del contenido
                        else:
                            print(f"⚠️ No se encontró una tabla en {archivo}") # Informa que no se encuentra una tabla en el archivo
                            continue
                    else: # Si el archivo no es HTML
                        # Esta parte no esta totalmente desarrollada porque actualmente ComercioNet da los archivos como html
                        print(f"📊 Procesando como Excel: {archivo}")
                        if archivo.endswith('.xls'):
                            df = pd.read_excel(archivo, engine='xlrd')
                        else:
                            df = pd.read_excel(archivo, engine='openpyxl')

                        numero_orden_raw = str(df.iat[4, 0])
                        fecha_entrega_raw = str(df.iat[4, 4])

                    numero_orden = re.search(r'\d+', numero_orden_raw) # Busca el numero de orden en el numero de orden extraido
                    numero_orden = numero_orden.group(0) if numero_orden else None # Extrae el numero de orden si lo encuentra

                    # Cambia la informacion de las fechas dependiendo del local al que se le haya hecho la orden
                    if "CD COQUIMBO" in local: # si el local es CD COQUIMBO
                        fecha_entrega = pd.to_datetime(fecha_entrega_raw, dayfirst=True, errors='coerce') # Convierte la fecha de entrega a un formato de fecha
                        fecha_entrega = fecha_entrega - timedelta(days=1) if pd.notnull(fecha_entrega) else None # Resta un dia a la fecha de entrega
                        fecha_producto = fecha_entrega if pd.notnull(fecha_entrega) else None # La fecha de producto es igual a la fecha de entrega
                    elif "CD SANTIAGO LDT CARNES" in local:
                        fecha_entrega = pd.to_datetime(fecha_entrega_raw, dayfirst=True, errors='coerce')
                        fecha_producto = fecha_entrega - timedelta(days=1) if pd.notnull(fecha_entrega) else None
                    elif "429 - Ice Star" in local:
                        fecha_entrega = pd.to_datetime(fecha_entrega_raw, dayfirst=True, errors='coerce')
                        fecha_producto = fecha_entrega - timedelta(days=1) if pd.notnull(fecha_entrega) else None

                    if numero_orden and pd.notnull(fecha_entrega): # Si el numero de orden y la fecha de entrega no son nulos
                        datos.append([ # Añade los datos a la lista de datos
                            numero_orden, # Numero de orden
                            fecha_entrega.strftime('%Y-%m-%d'),
                            fecha_producto.strftime('%Y-%m-%d'),
                            local
                        ])
                    else:
                        print(f"❌ Datos incompletos en el archivo: {archivo}") # Informa que los datos estan incompletos

                except Exception as e:
                    print(f"❌ Error procesando {archivo}: {e}") # Informa que hubo un error procesando el archivo

            self.df = pd.DataFrame(datos, columns=['Numero de Orden', 'Fecha Entrega', 'Fecha Producto', 'Local']) # Crea un DataFrame con los datos
            self.mostrar_tabla() # Llama a la funcion mostrar_tabla


    # Funcion que extrae el numero de orden de un archivo
    def extraer_numero_orden(self, contenido):
        try:
            match = re.search(r'BGM\+220\+(\d{10})(\d{10})', contenido) # Este regex busca un patrón específico en el string contenido,
                                                                        # con la estructura: BGM+220+XXXXXXXXXXYYYYYYYYYY
                                                                        # BGM\+220\+ → Busca literalmente la cadena "BGM+220+".
                                                                        # (\d{10}) → Captura un grupo de 10 dígitos (XXXXXXXXXX).
                                                                        # (\d{10}) → Captura otro grupo de 10 dígitos (YYYYYYYYYY).
            if match:
                numero_orden = match.group(2)  # Extract the order number
                return numero_orden # Devuelve el numero de orden
            else:
                messagebox.showerror("Error", "Número de orden no encontrado en el archivo.") # Muestra un mensaje de error si no se encuentra el
                                                                                              # numero de orden
                return None

        except Exception as e:
            print(f"Error extracting 'Numero de Orden': {e}") # Informa que hubo un error extrayendo el numero de orden
            messagebox.showerror("Error", f"No se pudo extraer el número de orden: {e}") # Muestra un mensaje de error en el computador
            return None
        
    # Esta funcion extrae la fecha de entrega de un archivo
    def extraer_fecha_entrega(self, contenido):
        try:
            # Intentar encontrar la fecha en diferentes formatos
            match = re.search(r'Fecha de Entrega:\s*(\d{2}/\d{2}/\d{4})', contenido) # Busca la fecha de entrega en el contenido del archivo
                                                                                     # con el formato dd/mm/yyyy 
            
            if match:
                fecha_entrega = match.group(1)
                return datetime.strptime(fecha_entrega, '%d/%m/%Y').strftime('%Y-%m-%d') # Devuelve la fecha de entrega en el formato yyyy-mm-dd
            else:
                print("⚠️ No se encontró 'Fecha de Entrega' en el contenido.") # Informa que no se encontró la fecha de entrega
                return None

        except Exception as e:
            print(f"❌ Error extrayendo 'Fecha de Entrega': {e}") # Informa que hubo un error extrayendo la fecha de entrega
            return None

    # Esta función muestra en la parte inferior de la ventana los datos numero de orden, fecha de entrega, fecha de producto y local
    def mostrar_tabla(self):
        if self.tree:
            self.tree.destroy() # Eliminar el árbol anterior si existe

        # Ajuste de tamaño de la ventana automáticamente
        local_mas_largo = max(self.df["Local"], key=len) # Encontrar el local más largo
        n_archivos = len(self.archivos) # Contar la cantidad de archivos
        alto_ventana = 300 + n_archivos * 20 # Calcular el alto de la ventana
        ancho_ventana = 500 + round(len(local_mas_largo) * 4.5) # Calcular el ancho de la ventana
        ancho_extra = ancho_ventana - 380 # Calcular el ancho extra
        str_geometria = f"{ancho_ventana}x{alto_ventana}" # Establece el nuevo tamaó de la ventana
        self.root.geometry(str_geometria) # Ajusta el nuevo tamaño de la ventana

        # Crear un árbol con las columnas Numero de Orden, Fecha Entrega, Fecha Producto y Local
        self.tree = ttk.Treeview(self.root, columns=('Numero de Orden',  
                                                    'Fecha Entrega',
                                                    'Fecha Producto',
                                                    'Local'),
                                                    show='headings') 
        self.tree.heading('Numero de Orden', text='Numero de Orden') # Encabezado de la columna Numero de Orden
        self.tree.heading('Fecha Entrega', text='Fecha Entrega') # Encabezado de la columna Fecha Entrega 
        self.tree.heading('Fecha Producto', text='Fecha Producto') # Encabezado de la columna Fecha Producto
        self.tree.heading('Local', text='Local') #Encaezado de la columna Local

        self.tree.column('Numero de Orden', width=140) # Ajusta el ancho de la columna Numero de Orden
        self.tree.column('Fecha Entrega', width=100) # Ajusta el ancho de la columna Fecha Entrega
        self.tree.column('Fecha Producto', width=100) # Ajusta el ancho de la columna Fecha
        self.tree.column('Local', width=ancho_extra) # Ajusta el ancho de la columna Local

        
        for index, row in self.df.iterrows(): # Para cada fila en el DataFrame
            # Insertar los datos en el árbol
            self.tree.insert('', 'end', values=(row['Numero de Orden'],
                                                row['Fecha Entrega'],
                                                row['Fecha Producto'],
                                                row['Local']))

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10) # Posiciona el arbol en la ventana


        
    # Esta funcion genera un archivo excel con los datos extraidos de los archivos de las ordenes de compra
    def generar_excel(self):
        datos = [] # Crea una lista vacia para almacenar los datos
        for archivo in self.archivos: # Para cada archivo en la lista de archivos
            try: # Intenta hacer lo siguiente
                if self.es_archivo_html(archivo): # Si el archivo es HTML
                    # print(f"Generando Excel a partir de HTML")
                    with open(archivo, 'r', encoding='utf-8', errors='ignore') as file: 
                        soup = BeautifulSoup(file, 'html.parser') # Lee el archivo usando la extension BeautifulSoup

                    table = soup.find('table') # Busca una tabla en el archivo
                    if table: # Si encuentra una tabla
                        df = pd.read_html(StringIO(str(table)))[0] # Lee la tabla y la guarda en un DataFrame

                        contenido = df.iat[0, 0]
                        # Crear json con los datos de la orden de compra
                        orden_compra = {
                            # 🔹 Extrae el nombre del "Emisor" ubicado entre "Emisor: " y "Receptor:"
                            "Emisor": re.search(r"Emisor: (.+?) Receptor:", contenido).group(1), 

                            # 🔹 Extrae el nombre del "Receptor" ubicado entre "Receptor:" y "Número de Orden"
                            "Receptor": re.search(r"Receptor: (.+?) Número de Orden", contenido).group(1),

                            # 🔹 Extrae el "Número de Orden de Compra" que es un número entero después de "Número de Orden de Compra: "
                            "Numero de Orden": re.search(r"Número de Orden de Compra: (\d+)", contenido).group(1),

                            # 🔹 Extrae la "Fecha de Generación" en formato dd/mm/yyyy después de "Fecha generación Mensaje: "
                            "Fecha Generacion": re.search(r"Fecha generación Mensaje: (\d{2}/\d{2}/\d{4})", contenido).group(1),

                            # 🔹 Extrae la "Fecha de Entrega" en formato dd/mm/yyyy después de "Fecha de Entrega: "
                            "Fecha de Entrega": re.search(r"Fecha de Entrega: (\d{2}/\d{2}/\d{4})", contenido).group(1),

                            # 🔹 Extrae el "Local" ubicado entre "Por cuenta del vendedor" e "Información Comprador"
                            "Local": re.search(r"Por cuenta del vendedor\s*(.*?)\s*Información Comprador", contenido).group(1).strip(),

                            # 🔹 Lista vacía donde se almacenarán los productos extraídos más adelante
                            "Productos": []
                        }
                        # 📆 Calcular "Fecha de producto" (un día antes de la fecha de entrega)
                        fecha_entrega_dt = datetime.strptime(orden_compra["Fecha de Entrega"], "%d/%m/%Y") # convierte el texto de la fecha en un 
                                                                                                           # formato de fecha
                        fecha_producto_dt = fecha_entrega_dt - timedelta(days=1) # Resta un dia a la fecha de entrega
                        fecha_entrega_arreglada = fecha_entrega_dt.strftime("%Y-%m-%d") # Convierte la fecha de entrega en el formato yyyy-mm-dd
                        if "CD COQUIMBO" in orden_compra["Local"]: # Si el local es CD COQUIMBO
                            fecha_entrega_dt = fecha_entrega_dt - timedelta(days=1) # Resta un dia a la fecha de entrega
                            fecha_entrega_arreglada = fecha_entrega_dt.strftime("%Y-%m-%d") # Convierte la fecha de entrega en el formato yyyy-mm-dd
                            orden_compra["Fecha de Producto"] = fecha_entrega_arreglada # La fecha de producto es igual a la fecha de entrega
                        elif "CD SANTIAGO LDT CARNES" in orden_compra["Local"]: 
                            fecha_producto_dt = fecha_entrega_dt - timedelta(days=1)
                            orden_compra["Fecha de Producto"] = fecha_producto_dt.strftime("%Y-%m-%d")
                        elif "429 - Ice Star" in orden_compra["Local"]:
                            fecha_producto_dt = fecha_entrega_dt - timedelta(days=1)
                            orden_compra["Fecha de Producto"] = fecha_producto_dt.strftime("%Y-%m-%d")


                        # 📝 Cortar el contenido para buscar solo los productos
                        if "Cargos y descuentos aplicables al documento" in contenido: # Si encuentra el contenido
                            contenido_cortado = contenido.split("Cargos y descuentos aplicables al documento", 1)[1] # Corta el contenido desde que
                                                                                                                     # empiezan los productos
                        else:
                            contenido_cortado = contenido  # Si no encuentra el contenido, deja el original

                        if "TOTTUS" not in orden_compra["Emisor"]: # Si el emisor no es Tottus
                            print("Orden de compra no es de Tottus") # Informa que la orden de compra no es de Tottus
                            productos = re.findall( # Busca los productos en el contenido
                                        (
                                            # Captura un código de producto de 11 a 14 dígitos seguidos.
                                            r"(\d{11,14})\s+" 

                                            # Captura la descripción del producto: letras, espacios y "%"
                                            # (lazy match para evitar capturar más de lo necesario).
                                            r"([\w\s%]+?)\s+" 

                                            # Captura la cantidad: un número de 1 a 3 dígitos seguido de posibles separadores (",", "." o más dígitos).
                                            r"(\d{1,3}[,.\d]+)\s+"

                                            # Captura la unidad de cantidad: puede ser "Cajas", "Kilogramo" o "Kg".
                                            r"(Cajas|Kilogramo|Kg)\s+"

                                            # Captura un separador numérico intermedio: una serie de dígitos y comas antes del tipo de unidad.
                                            r"[\d,]+\s+" 

                                            # Captura el tipo de unidad: "Unid." o "Kilogramo".
                                            r"(Unid\.|Kilogramo)\s+" 

                                            # Captura el precio unitario: número precedido por "$", con formato de miles opcional.
                                            r"\$(\d{1,3}(?:[.,]\d{3})*)\s+\(Precio neto por unidad\)\s+" 

                                            # Captura el monto total: número precedido por "$", con formato de miles opcional.
                                            r"\$(\d{1,3}(?:[.,]\d{3})*)"
                                        ),
                                        contenido
                                    )
                            print(f"📦 Productos encontrados: {len(productos)}")

                            # Aquí se agregan los datos de los productos al json de orden de compra
                            for producto in productos:
                                orden_compra["Productos"].append({
                                    "Codigo": producto[0],
                                    "Descripcion": producto[1].strip(),
                                    "Cantidad": producto[2],
                                    "Unidad": producto[3],
                                    "Precio Unitario": f"${producto[5]}",
                                    "Monto Total": f"${producto[6]}",
                                })
                        else: # Si el emisor es Tottus
                            print("Orden de compra es de Tottus")

                            # ---- PRUEBA POR SECCIONES ----

                            # 📌 Ver si encuentra códigos de productos
                            codigo_producto = re.findall(
                                r"\d{11,14}",  # Captura códigos de productos de 11 a 14 dígitos
                                contenido_cortado
                            )

                            # 📌 Ver si encuentra descripciones de productos
                            descripcion_producto = re.findall(
                                (
                                    r"\d{11,14}\s+"  # Código del producto
                                    r"([\w\s%.\-]+?)\s+"  # Descripción del producto
                                    r"\d{1,3}[,.\d]+(?:\s+Cajas|\s+Kilogramo|\s+Kg)"  # Cantidad seguida de la unidad
                                ),
                                contenido_cortado
                            )

                            # 📌 Ver si encuentra cantidades
                            cantidades = re.findall(
                                (
                                    r"(\d{1,3}[,.\d]+)"  # Cantidad (puede incluir coma o punto como separador)
                                    r"(?=\s+(?:Cajas|Kilogramo|Kg))"  # Debe estar seguida de la unidad especificada
                                ),
                                contenido_cortado
                            )

                            # 📌 Buscar un número entero entre "Cajas"/"Kilogramo" y "Unid."/"Kilogramo"
                            cantidad_unidad = re.findall(
                                (
                                    r"(?:Cajas|Kilogramo)\s+"  # Debe estar precedido por "Cajas" o "Kilogramo"
                                    r"(\d{1,3}[,.]?\d{0,3})\s+"  # Número de unidades, con o sin separador decimal
                                    r"(?:Unid\.|Kilogramo)"  # Debe estar seguido por "Unid." o "Kilogramo"
                                ),
                                contenido_cortado
                            )

                            # 📌 Ver si encuentra unidades (Cajas, Kilogramo, Kg)
                            unidades = re.findall(
                                r"(Cajas|Kilogramo|Kg)",  # Captura cualquiera de estas unidades
                                contenido_cortado
                            )

                            # 📌 Ver si encuentra el tipo de unidad (Unid. o Kilogramo) antes del precio
                            tipo_unidad = re.findall(
                                r"(Unid\.|Kilogramo)(?=\s+\$)",  # Busca "Unid." o "Kilogramo" justo antes de un precio
                                contenido_cortado
                            )

                            # 📌 Ver si encuentra precios unitarios
                            precios_unitarios = re.findall(
                                (
                                    r"\$(\d{1,3}(?:[.,]\d{3})*)"  # Precio con formato de separadores de miles
                                    r"(?=\s+\(Precio lista\))"  # Debe estar seguido de "(Precio lista)"
                                ),
                                contenido_cortado
                            )

                            # 📌 Ver si encuentra montos totales
                            monto_total = re.findall(
                                (
                                    r"(?<!TOTAL\s)"  # Asegura que no está precedido por la palabra "TOTAL"
                                    r"\$(\d{1,3}(?:[.,]\d{3})*)"  # Captura montos en formato correcto
                                    r"(?:\s+DESCUENTO|\s*$)"  # Debe estar seguido de "DESCUENTO" o final de línea
                                ),
                                contenido_cortado
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

                            # Aquí se agregan los datos de los productos al json de orden de compra
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
                                                "No encontrado") # Buscar el divisor de kilos por caja
                                
                                # Buscar la unidad de medida
                                UM = next((l["UM"] for l in productos_json if int(l["Codigo UPC"]) == int(producto[0])), "No encontrado") 
                                
                                if UM == "KGS": # Si la unidad de medida es KGS
                                    cantidad = float(producto[2].replace(",", ".")) / float(divisor) # Divide la cantidad por el divisor
                                    if "ESCALOPA" in producto[1]: # Si el producto es escalopa
                                        
                                        kilos = float(producto[2].replace(",", ".")) # Convierte la cantidad a kilos

                                        # Acá se especifica que cantidad de unidades se agregan dependiendo de la cantidad de kilos del producto
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
                                        
                                        precio_unidad = float(producto[5].replace(".", "")) * float(divisor) # Multiplica el precio por kilo a la 
                                                                                                             # Cantidad de kilos por caja
                                        precio_unidad = round(precio_unidad) # Redondea el precio a un numero entero


                                    else:
                                        precio_unidad = float(producto[5].replace(".", "")) * float(divisor) # Multiplica el precio por kilo a la 
                                                                                                             # Cantidad de kilos por caja  
                                else:
                                    cantidad = float(producto[7].replace(",", ".")) # Reemplaza la coma con un punto para obtener el formato correcto
                                    cantidad = math.ceil(cantidad) # Aproxima la cantidad hacia arriba
                                    precio_unidad = float(producto[5].replace(".", "")) # Reemplaza la coma con un punto para obtener el formato correcto

                            else:
                                cantidad = float(producto[2].replace(",", ".")) # Reemplaza la coma con un punto para obtener el formato correcto
                                cantidad = math.ceil(cantidad) # Aproxima la cantidad hacia arriba
                                precio_unidad = float(producto[5].replace(".", "")) # Reemplaza la coma con un punto para obtener el formato correcto

                            # Añade los productos actualizados a una lista "productos_lista" 
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

                        # Acá se revisa el documento con los locales y se confirma que el local encontrado pertenece a los existentes
                        with open("locales.json", "r", encoding="utf-8") as file:
                            locales = json.load(file)
                        nombre_local = next((l["Nombre Local"] for l in locales if l["Cliente"] == orden_compra["Local"]), "No encontrado")
                        # print(f"Este es el nombre de local: {nombre_local}")
                        
                        # Acá obtendo el numero de orden de compra en el formato correcto
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

            # 📝 Aplicar la eliminación de columnas duplicadas POR ORDEN DE COMPRA
            columnas_orden = ["Cliente", "Fecha de producto", "Fecha orden", "Fecha de entrega", "Orden de compra", "Tipo Documento"]
            # Para cada orden de compra, eliminamos los valores repetidos dejando solo el primero
            df_final[columnas_orden] = df_final.groupby("Orden de compra")[columnas_orden].transform(
                lambda x: x.mask(x.duplicated(), ""))
            
            # 📂 Esta función abre la ventana del explorador de archivos para guardar el excel generado
            nombre_archivo = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Archivos Excel", "*.xlsx")],
                title="Guardar archivo Excel"
            )
            if nombre_archivo: # Si se genera sa un nombre al archivo, se guarda en la ubicacion especificada
                df_final.to_excel(nombre_archivo, index=False)
                messagebox.showinfo("Éxito", f"Archivo Excel generado: {nombre_archivo}")
            else:
                print("⚠️ Operación cancelada, archivo no guardado.")

    def gestionar_locales(self): # invoca la funcion Gestionar Locales
        GestionarLocales(self.root)

    def gestionar_productos(self): # invoca la funcion Gestionar Productos
        GestionarProductos(self.root) 

if __name__ == "__main__": #Estas lineas hacen que si se corre el codigodesde esta ventana, se cree una instancia de aplicacion y empieze el programa
    root = tk.Tk()
    app = OrdenesCompraApp(root)
    root.mainloop()