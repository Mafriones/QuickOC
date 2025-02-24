# ⚙️ Configuración de QuickOC

Este documento explica cómo configurar **QuickOC** para su correcto funcionamiento dentro de la empresa.

---

## 📂 Archivos de Configuración

QuickOC utiliza dos archivos JSON para gestionar la información de los locales y los productos:

### 1️⃣ `locales.json`
- **Ubicación**: Se encuentra en la carpeta raíz del proyecto.
- **Propósito**: Contiene la información de los locales donde se entregan las órdenes de compra.
- **Estructura**:
  ```json
  [
    {
      "Cliente": "CD SANTIAGO LDT CARNES",
      "Nombre Local": "Centro de Distribución Santiago Carnes"
    },
    {
      "Cliente": "429 - Ice Star",
      "Nombre Local": "Ice Star Avenida Américo Vespucio"
    }
  ]
- Cómo modificarlo:
    - Seguir el paso **5** de [guía de uso](usage.md)

### :two: `productos.json`
- **Ubicación**: Se encuentra en la carpeta raíz del proyecto.
- **Propósito**: Contiene la información de los productos que contienen las ordenes de compra.
- **Estructura**:
  ```json
  [
  {
    "Codigo UPC": "07800145000575",
    "Codigo Cedar Creek": "1001001",
    "Nombre del producto": "TARTARO 4% TOTTUS 500 GR",
    "Unidades por caja": 8,
    "Kgs por caja": 2.5,
    "UM": "KGS"
  },
  {
    "Codigo UPC": "07800145000568",
    "Codigo Cedar Creek": "1002001",
    "Nombre del producto": "CARNE MOLIDA 7% TOTTUS 500 GR",
    "Unidades por caja": 8,
    "Kgs por caja": 2.0,
    "UM": "KGS"
  }
  ]
- Cómo modificarlo:
    - Seguir el paso **5** de [guía de uso](usage.md)

---

## 📑 Configuración de Parámetros de Procesamiento

### 🔄 Ajuste de Fechas de Entrega

El procesamiento de las órdenes de compra incluye reglas para calcular las fechas de entrega y fechas de productos. Estas reglas están en `OC_excel_processor.py` y pueden modificarse según sea necesario:

```python
# Ajuste de fechas basado en el local
if "CD COQUIMBO" in local:
    fecha_entrega = fecha_entrega - timedelta(days=1)
    fecha_producto = fecha_entrega
elif "CD SANTIAGO LDT CARNES" in local:
    fecha_producto = fecha_entrega - timedelta(days=1)
elif "429 - Ice Star" in local:
    fecha_producto = fecha_entrega - timedelta(days=1)
```

**Cómo modificar:**

- Ajustar los valores de timedelta(days=X) según las políticas de la empresa.
- Agregar más locales si se requieren reglas específicas

---

## 🏷️ Conversión de Unidades
QuickOC convierte productos en kilogramos a cajas cuando es necesario. Este cálculo puede modificarse en `OC_excel_processor.py:`
```python
if producto[3] == "Kilogramo":
    divisor = next((l["Kgs por caja"] for l in productos_json if int(l["Codigo UPC"]) == int(producto[0])), "No encontrado")
    cantidad = float(producto[2].replace(",", ".")) / float(divisor)
    cantidad = math.ceil(cantidad)
```
**Cómo modificar:**

- Ajustar la lógica de conversión si la empresa cambia su política de ventas.
- Agregar más condiciones según los tipos de productos.

---
## 🎨 Personalización de la Interfaz

Los colores y estilos de la interfaz gráfica de QuickOC están definidos en `OC_excel_processor.py`. Se pueden modificar para adaptarlos a la imagen corporativa.

### 🖌️ Colores principales

```python
COLOR_FONDO = '#2c2c2c'  # Color de fondo oscuro
COLOR_PANEL = '#d75e3b'  # Color logo
COLOR_TEXTO = '#ebf5fb'  # Texto blanco
COLOR_BOTON_FONDO = '#000000'  # Fondo negro para los botones
COLOR_BOTON_BORDE = '#FFD700'  # Borde dorado para los botones
COLOR_HOVER = '#d75e3b'        # Color logo para hover
```
### 🛠️ Cómo personalizar
Cambiar los valores hexadecimales de los colores para modificar la apariencia de la aplicación.
Modificar los estilos de botones y etiquetas según sea necesario.

---

## 🔄 Mantenimiento y Actualizaciones
### 📌 Mantener actualizados los archivos JSON
- Revisar periódicamente locales.json y productos.json para asegurarse de que contienen información actualizada.
### 📝 Registro de Cambios
- Cada vez que se actualiza la aplicación, es recomendable llevar un registro de cambios para que los empleados estén informados.