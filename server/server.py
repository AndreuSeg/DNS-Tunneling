import os

import socket
import dns.message
import dns.name
import dns.rdata
import dns.rdataclass
import dns.rdatatype
import dns.rrset

server = "0.0.0.0"          # Escucha en todos los adaptadores
port = 53                   # Puerto 53 DNS
buffer = 4096               # Tamaño buffer
domain = "ass.com."         # Nombre de dominio absoluto para la respuesta (acaba con punto)
response_ip = "2.2.2.2"     # IP falsa de respuesta de ejemplo
subdomains = []             # Lista para almacenar los subdominios
inicio = "----INICIO----"
fin = "----FIN----"


def main():
    # Primero limpiamos la pantalla.
    os.system("clear")
    print(inicio)
    # Creamos el socket para la transmision DNS
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((server, port))
    print("Esperando peticiones DNS...\n")
    # Creamos un bucle que no se acabe a no ser que pulsemos ctrl+c
    while True:
        print("-------------------------------")
        # Recibimos las peticiones del cliente.
        request_data, client_address = server_socket.recvfrom(buffer)
        # Deserializar las peticiónes.
        request = dns.message.from_wire(request_data)
        print("Recibida petición DNS")
        print(request)
        # Extraes el dominio entero.
        full_domain_name = request.question[0].name.to_text()
        print("Nombre dominio completo: ", full_domain_name)
        # Extraes el subdominio.
        subdomain = full_domain_name.split(".")[0]
        print("Subdominio recibido: "+ subdomain)
        # Prepara la respuesta DNS
        response = dns.message.make_response(request)   # Crea respuesta vacía
        response.id = request.id                        # ID de la respuesta igual al de la petición
        response.set_rcode(dns.rcode.NOERROR)           # Establecer el campo rcode como NOERROR
        # Añade la respuesta a la petición con el dato del dominio ficticio
        # Es importante tener en cuenta que aquí el nombre del dominio es absoluto,
        # eso significa que el nombre de dominio acaba con un punto.
        response.answer.append(dns.rrset.from_text(domain, 300, dns.rdataclass.IN, dns.rdatatype.A, response_ip))
        # Serializar la respuesta
        response_data = response.to_wire()
        # Enviar la respuesta al cliente
        server_socket.sendto(response_data, client_address)
        # Si el subdominio es no igual a la variable fin, añadimos a una lista previamente creada
        # todos los subdominios para almacenarlos y posteriormente usarlos.
        if subdomain != fin:
            subdomains.append(subdomain)
        # Si la cadena es par se ejecuta todo lo que haya dentro del if.
        if len(subdomain) % 2 == 0:
            # Descodificamos el subdominio para posteriormente compararlo con la cadena de fin.
            subdomain_fin = bytes.fromhex(subdomain).decode()
            # Si el subdominio es igual a la variable fin, juntar todos los subdominios.
            if subdomain_fin == fin:
                # Juntamos todos los arrays de la lista.
                subdomains_unidos = "".join(subdomains)
                # Y crear el archivo y escribir dentro de el la cadena.
                with open("mensaje_recibido.txt", "wb") as archivo:
                    subdomains_unidos_en_bytes = bytes(subdomains_unidos, "utf8")
                    archivo.write(subdomains_unidos_en_bytes)
                try:
                    # Convertimos la cadena de hexadecimal a texto plano y la mostramos por pantalla.
                    real_data = bytes.fromhex(subdomains_unidos).decode()
                    real_data = real_data[:-len(fin)]
                    print("\nEl mensaje enviado desde el cliente es:")
                    print(real_data)
                    break
                except Exception as e:
                    print("No hay datos en hexadecimal")
                    break


if __name__ == "__main__":
    main()
