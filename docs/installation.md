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
1. Asegúrate de estar en la carpeta del proyecto:
```sh
cd QuickOC
```

2. Genera el .exe con PyInstaller:
```sh 
pyinstaller --noconsole --name "QuickOC" --add-data "locales.json;." --add-data "productos.json;." --add-data "gestionar_locales.py;." --add-data "gestionar_productos.py;." --hidden-import=tkinter --hidden-import=pandas --hidden-import=bs4 --hidden-import=json --exclude-module matplotlib --icon=OC_icon_v3.ico OC_excel_processor.py
```

3. Ahora se habran generado 2 carpetas, **dist** y **build**
A la carpeta dist *(que es la que importa)* le agregaremos los siguientes archivos de la carpeta principal:
    1. *gestionar_locales.py*
    2. *gestionar_productos.py*
    3. *procesar_archivos.py*
    4. *locales.json*
    5. *productos.json*
    6. *OC_icon_v3.ico*

4. El ejecutable estara en la carpeta **dist** con el nombre *QuickOC.exe*


## 📌 Solución de problemas

- **El comando `python` no funciona**
  - Prueba con `python3` o revisa si Python está correctamente instalado y en el PATH.

- **El ejecutable tarda mucho en abrir**
  - La primera ejecución puede demorar debido a la carga de dependencias.

- **Faltan archivos JSON en el `.exe`**
  - Asegúrate de usar `--add-data` en el comando de `pyinstaller`.

- **Error al abrir un archivo `.xls`**
  - Asegúrate de que el archivo no esté dañado y tenga el formato correcto.

---

## 🎯 Conclusión

QuickOC ya está listo para usarse en tu empresa. Si tienes dudas, contacta con el equipo de desarrollo *(Cristobal)*.  🚀


