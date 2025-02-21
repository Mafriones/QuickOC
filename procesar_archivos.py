import re

def procesar_archivo_contenido(contenido):
    datos = []
    
    try:
        # Extraer número de orden de compra
        numero_orden = re.search(r'BGM\+220\+(\d{10})\+', contenido).group(1)
        
        # Extraer fecha de entrega
        fecha_entrega = re.search(r'DTM\+2:(\d+):203', contenido).group(1)
        
        # Extraer los productos
        productos = re.findall(r'LIN\+\d+\+\+(\d{12}):SRV.*?IMD\+F\+\+DU:::(.*?)\'QTY\+21:(\d+):CS.*?PRI\+AAA:(\d+)', contenido)

        for producto in productos:
            codigo_upc, descripcion, cantidad, precio = producto
            datos.append({
                "Numero Orden": numero_orden,
                "Fecha Entrega": fecha_entrega,
                "Codigo UPC": codigo_upc,
                "Descripcion": descripcion,
                "Cantidad": int(cantidad),
                "Precio": float(precio) / 100  # Convertir centavos a unidades monetarias
            })

        return datos
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        return None


def obtener_cedar_creek(codigo_upc, productos_json):
    for producto in productos_json:
        if producto['Codigo UPC'] == codigo_upc:
            return producto['Codigo Cedar Creek']
    return "N/A"  # Return "N/A" if no match is found



# Simulamos el contenido del archivo basado en las observaciones
#contenido_simulado = """
"""
UNB+UNOA:4+7808800008669:14+7808800121351:14+20240726:0649+20240726064955'UNH+001+ORDERS:D:01B:UN:EAN010'
BGM+220+0046213882+9'DTM+137:202407260640:203'DTM+2:202407310640:203'RFF+PL:000000000000000000000'NAD+BY+7808800008669::EN'
LOC+7+7804647170354'CTA+OC+:aearredond'NAD+SU+7808800121351::EN'CTA+OC+:Alexis Rodr guez'PAT+1++21::D:30'TOD++NC'
LIN+000001++07800145000575:SRV'IMD+F++DU:::TARTARO 4% TOTTUS 500 GR'QTY+21:21:CS'PRI+AAA:30408::LIU::CSC'
"""
"""
# Procesar el contenido simulado
resultados_simulados = procesar_archivo_contenido(contenido_simulado)
print(resultados_simulados)

"""
