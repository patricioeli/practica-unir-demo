import csv
from collections import defaultdict
from datetime import datetime

def procesar_csv_deudas(nombre_archivo):
    """
    Procesa un archivo CSV de deudas con formato: Cliente,Fecha,Deuda,Concepto
    Maneja múltiples formatos de fecha y solo considera deudas del año actual.
    """
    deudas = defaultdict(float)
    transacciones = []
    año_actual = datetime.now().year
    formatos_fecha = ['%d/%m/%Y', '%d-%m-%Y', '%m/%d/%Y', '%Y-%m-%d']  # Formatos admitidos

    try:
        with open(nombre_archivo, mode='r', encoding='utf-8') as archivo:
            # Detecta automáticamente si tiene encabezados
            dialect = csv.Sniffer().sniff(archivo.read(1024))
            archivo.seek(0)
            lector = csv.DictReader(archivo, dialect=dialect)
            
            print(lector.fieldnames)
                
            if not {'Cliente', 'Fecha', 'Deuda'}.issubset(lector.fieldnames):
                print("Error: El archivo CSV debe contener columnas 'Cliente', 'Fecha' y 'Deuda'")
                return None, None
            
            for n_fila, fila in enumerate(lector, 1):
                try:
                    cliente = fila['Cliente'].strip()
                    valor_deuda = fila['Deuda'].replace(',', '')
                    deuda = float(valor_deuda)

                    print (cliente)
                    print (valor_deuda)

                    # Procesamiento flexible de fechas
                    fecha_str = fila['Fecha'].strip()
                    fecha = None
                    
                    print (fecha)

                    for formato in formatos_fecha:
                        try:
                            fecha = datetime.strptime(fecha_str, formato)
                            if fecha.year == año_actual:
                                break
                            else:
                                fecha = None
                        except ValueError:
                            print ('error Fecha')
                            continue
                    
                    if not fecha:
                        continue  # Salta fechas de otros años o formatos no reconocidos
                    
                    print ('datos ok')
                    
                    deudas[cliente] += deuda
                    transacciones.append({
                        'cliente': cliente,
                        'fecha': fecha.strftime('%d/%m/%Y'),
                        'deuda': deuda,
                        'concepto': fila.get('Concepto', '')
                    })
                    
                except ValueError as e:
                    print(f"Advertencia: Error en fila {n_fila} - {str(e)}")
                except KeyError as e:
                    print(f"Advertencia: Fila {n_fila} no tiene columna {str(e)}")
    
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{nombre_archivo}'")
        return None, None
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return None, None
    
    return dict(deudas), transacciones

def generar_reporte(deudas, transacciones):
    """Genera un reporte detallado de las deudas"""
    if not deudas:
        print("\nNo se encontraron deudas válidas del año actual para procesar.")
        print("Posibles causas:")
        print("- El archivo está vacío")
        print("- Las fechas no corresponden al año actual")
        print("- El formato de fechas no es reconocido (usar DD/MM/AAAA o DD-MM-AAAA)")
        print("- Los encabezados no coinciden (debe tener 'Cliente', 'Fecha', 'Deuda')")
        return
    
    print("\nREPORTE DE DEUDAS - AÑO ACTUAL")
    print("="*60)
    print(f"{'CLIENTE':<30} {'TOTAL DEUDA':>15}")
    print("-"*60)
    
    for cliente, total in sorted(deudas.items(), key=lambda x: x[1], reverse=True):
        print(f"{cliente:<30} ${total:>12,.2f}")
    
    print("\nDETALLE DE TRANSACCIONES:")
    print("="*60)
    print(f"{'FECHA':<12} {'CLIENTE':<25} {'DEUDA':>12} {'CONCEPTO':<20}")
    print("-"*60)
    
    for t in sorted(transacciones, key=lambda x: datetime.strptime(x['fecha'], '%d/%m/%Y')):
        print(f"{t['fecha']:<12} {t['cliente'][:24]:<25} ${t['deuda']:>11,.2f} {t['concepto'][:18]:<20}")

if __name__ == "__main__":
    print("PROCESADOR DE DEUDAS CSV")
    print("="*60)
    archivo_csv = input("Ingrese la ruta del archivo CSV: ").strip()
    
    deudas, transacciones = procesar_csv_deudas(archivo_csv)
    
    if deudas is not None:
        generar_reporte(deudas, transacciones)
    
    input("\nPresione Enter para salir...")