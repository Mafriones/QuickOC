# Código Fuente de QuickOC

Este documento proporciona una visión general del código fuente de QuickOC, explicando la funcionalidad de los módulos principales y cómo interactúan entre sí.

---

## 📂 Estructura del Código

El proyecto **QuickOC** sigue la siguiente estructura de archivos:

    QuickOC/
    ├── OC_excel_processor.py
    ├── gestionar_locales.py
    ├── gestionar_productos.py
    ├── productos.json
    ├── locales.json
    ├── OC_icon_v3.ico
    ├── licencia.txt
    ├── requirements.txt
    ├── mkdocs.yml
    └── docs/
        ├── index.md
        ├── installation.md
        ├── usage.md
        ├── development.md
        ├── code.md
        └── config.md

---

## 📜 Descripción de los Archivos Principales

### `OC_excel_processor.py`
- **Función**: Es el núcleo de la aplicación, maneja la interfaz gráfica de usuario con `Tkinter`, carga archivos de órdenes de compra y genera los archivos Excel procesados. Además contiene 2 botones conectados a `gestionar locales` y a `gestionar productos`.
- **Componentes principales**:
  - Carga y análisis de archivos `.xls`
  - Extracción de datos de órdenes de compra
  - Generación de archivos Excel con la información procesada

### `gestionar_locales.py`
- **Función**: Maneja la gestión de locales en la aplicación, permitiendo agregar, editar y eliminar locales desde una base de datos en `JSON`.

### `gestionar_productos.py`
- **Función**: Maneja la gestión de productos en la aplicación, permitiendo agregar, editar y eliminar productos desde una base de datos en `JSON`.
---

## 📌 Lógica de Procesamiento de Órdenes de Compra

1. **Carga de Archivos**: Se seleccionan los archivos `.xls` desde la interfaz gráfica.
2. **Extracción de Datos**:
   - Se analiza el contenido del archivo y se extraen los valores clave.
   - Se identifican productos, cantidades, precios y montos totales mediante expresiones regulares.
3. **Procesamiento de Datos**:
   - Se validan los datos extraídos.
   - Se aplican reglas de negocio (como la conversión de unidades y validación de productos).
4. **Generación de Excel**:
   - Se crea un archivo `Excel` con la información procesada.
   - Se solicita al usuario una ubicación para guardar el archivo generado.

---

## 🔧 Reglas de Procesamiento de Productos

- **Conversión de unidades**:
  - Si un producto se vende por `Kilogramos`, se busca la conversión a `Cajas` si es aplicable.
  - En el caso de `ESCALOPA`, se realizan ajustes según la cantidad total.
- **Asignación de códigos Cedar Creek**:
  - Se buscan los códigos en `productos.json` y se asignan al producto correspondiente.
- **Cálculo de montos**:
  - Se extraen precios unitarios y totales, aplicando conversión si es necesario.

---

## 🔗 Conexión entre Módulos

- **`OC_excel_processor.py`** llama a `gestionar_locales.py` y `gestionar_productos.py` para gestionar datos.
- **`utils.py`** proporciona funciones comunes reutilizadas en todo el código.
- **La base de datos en `JSON`** (`locales.json` y `productos.json`) actúa como almacenamiento de información de locales y productos.

---

## 🚀 Posibles Mejoras

- **Optimización del procesamiento de archivos**: Reducir el tiempo de carga y análisis.
- **Integración con bases de datos SQL**: Para reemplazar el uso de archivos JSON.
- **Automatización del procesamiento**: Opciones para ejecutar sin interfaz gráfica.

---

## 📚 Referencias

- **Tkinter**: [Documentación oficial](https://docs.python.org/3/library/tkinter.html)
- **Pandas**: [Documentación oficial](https://pandas.pydata.org/docs/)
- **BeautifulSoup**: [Documentación oficial](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)