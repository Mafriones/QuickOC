# Instalación de QuickOC

Este documento explica cómo instalar y ejecutar **QuickOC** en tu computadora.

---

## 📌 Requisitos previos

Antes de instalar QuickOC, asegúrate de cumplir con los siguientes requisitos:

### 🔹 Windows
- **Sistema operativo:** Windows 10 o superior
- **Python:** Versión 3.8 o superior (Descargar desde [Python.org](https://www.python.org/downloads/))
- **Git (opcional):** Para clonar el repositorio (Descargar desde [git-scm.com](https://git-scm.com/downloads))

### 🔹 Librerías necesarias
QuickOC depende de varias librerías de Python. Puedes instalarlas con el archivo `requirements.txt`.

---

## 🚀 Instalación

### 1️⃣ Clonar el repositorio
Si tienes Git instalado, puedes clonar el repositorio con:

```sh
git clone https://github.com/Mafriones/QuickOC.git
cd QuickOC
```

### 2️⃣ Instalar dependencias
Desde tu terminal ejecuta el siguiente comando para instalar las librerías necesarias:

```sh
pip install -r requirements.txt
```

### ▶️ Ejecución de QuickOC
Para iniciar la aplicación, ejecuta:
```sh
python OC_excel_processor.py
```

### 🔹 Generar el archivo ejecutable (.exe)
Si deseas crear un ejecutable para Windows:
    Asegúrate de estar en la carpeta del proyecto:
    ```sh 
    pyinstaller --noconsole --name "OC_excel_processor" --add-data "locales.json;." --add-data "productos.json;." --add-data "gestionar_locales.py;." --add-data "gestionar_productos.py;." --hidden-import=tkinter --hidden-import=pandas --hidden-import=bs4 --hidden-import=json --exclude-module matplotlib --icon=OC_icon_v3.ico OC_excel_processor.py
    ```