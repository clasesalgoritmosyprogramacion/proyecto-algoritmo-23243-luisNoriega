#importar paquetes
import json
import requests
import uuid


#Clases
from Client import Client
#from Order import Order
from Product import Product
from Restaurant import Restaurant
from Stadium import Stadium
from Team import Team
from Ticket import Ticket
from Match import Match

class App():
    def __init__(self):
        self.Lista_Client = []
        self.Lista_Match = []
        self.Lista_order = []
        self.Lista_Product = []
        self.Lista_Restaurant = []
        self.Lista_Stadium = []
        self.Lista_Team = []
        self.Lista_Ticket = []

    def menu(self, opciones):
        for i, opcion in enumerate(opciones):
            print(f"{i+1}. {opcion}")
        
        opcion = input("ingrese el numero de la opcion que desea elegir: ")
        while not opcion.isnumeric() or not int(opcion) in range(1, len(opciones)+1):
            opcion = input("Error, ingrese el numero de la opcion que desea elegir: ")

        opcion = int(opcion)-1

        return opcion

    def run(self):
        self.API()

        opciones = ["Gestión de partidos y estadios", "Gestión de venta de entradas", "Gestión de asistencia a partidos", "Gestión de restaurantes", "Gestión de venta de restaurantes", "Indicadores de gestión (estadísticas)", "salir"]
        print("Bienvenido")
        
        while True:
            opcion = self.menu(opciones)

            if opcion == 0:
                self.modulo_1()
            elif opcion == 1:
                self.modulo_2()
            elif opcion == 2:
                self.modulo_3()
            elif opcion == 3:
                self.modulo_4()
            elif opcion == 4:
                self.modulo_5()
            elif opcion == 5:
                self.modulo_6()
            else:
                print("Hasta luego")
                break

    #Carga del apis en los objetos
    def API(self):
        self.API_Teams()
        self.API_Stadiums()
        self.API_Matches()

    #Carga del apis Teams en los objetos
    def API_Teams(self):
        api_teams = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json").json()
        
        for team in api_teams:
            new= Team(team["id"], team["code"], team["name"], team["group"])
            self.Lista_Team.append(new)
    #Carga del apis Stadiums en los objetos
    def API_Stadiums(self):
        api_stadiums = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json").json()

        #Recorrer Lista de estadios y guardar su informacion
        for stadium in api_stadiums:
            new_stadium = Stadium(stadium['id'], stadium['name'], stadium['city'], stadium['capacity'], stadium['restaurants'])
            
            #Recorrer Lista de restaurantes y guardar su informacion dentro de su estadio pertinente
            restaurants = []
            for restaurant in stadium['restaurants']:
                new_restaurant = Restaurant(restaurant['name'], restaurant['products'])


                #Recorrer Lista de productos y guardar su informacion dentro de su restaurantes pertinente
                products = []
                for product in restaurant['products']:
                    new_product = Product(product['name'], product['quantity'], product['price'], product['adicional'], product['stock'])
                    products.append(new_product)
                    self.Lista_Product.append(new_product)
                #Guardamos lista de productos dentro del restaurantes
                new_stadium.restaurants = restaurants



                restaurants.append(new_restaurant)
                self.Lista_Restaurant.append(new_restaurant)
            #Guardamos lista de restaurantes dentro del estadio
            new_stadium.restaurants = restaurants



            self.Lista_Stadium.append(new_stadium )
    #Carga del apis Stadiums en los objetos
    def API_Matches(self):
        api_matches = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json").json()

        for match in api_matches:
            
            for team in self.Lista_Team:
                if match["home"]["id"] == team.id:
                    local = team
                if match["away"]["id"] == team.id:
                    away = team

            for stadium in self.Lista_Stadium:
                if stadium.id == match["stadium_id"]:
                    stadium_match = stadium

            new = Match(match["id"], match["number"], local, away, match["date"], match["group"], stadium_match)

            self.Lista_Match.append(new)

    #Gestión de partidos y estadios
    def modulo_1(self):
        opciones = ["Buscar todos los partidos de un país", "Buscar todos los partidos que se jugarán en un estadio específico", "Buscar todos los partidos que se jugarán en una fecha determinada"]
        opcion = self.menu(opciones)

        if opcion == 0:
            self.search_match_country()
        elif opcion == 1:
            self.search_match_stadiums()
        elif opcion == 2:
            self.search_match_date()

    def search_match_country(self):
        match_search =input("Ingresa el pais por el que desea buscar el partido: ").lower()
        find = False
        for match in self.Lista_Match:
            if match_search in match.home.name.lower() or match_search in match.away.name.lower():
                find = True
                print(match.show())
        
        if not find:
            print("No se encontraron resultados")
            
    def search_match_stadiums(self):
        match_search =input("Ingresa el stadium por el que desea buscar el partido: ").lower()
        find = False
        for match in self.Lista_Match:
            if match_search in match.stadium.lower():
                find = True
                print(match.show())
        
        if not find:
            print("No se encontraron resultados")
            
    def search_match_date(self):
        match_search =input("Ingresa la fecha por el que desea buscar el partido (Ej: 2024-06-14): ").lower()
        find = False
        for match in self.Lista_Match:
            if match_search == match.date.lower():
                find = True
                print(match.show())
        
        if not find:
            print("No se encontraron resultados")


    #Gestión de venta de entradas
    def modulo_2(self):
        cedula = input("Ingresa tu cedula (sin puntos): ")
        while not cedula.replace(".", "").isnumeric() or 7 > len(cedula.replace(".", "")) > 8:
            cedula = input("Error, Ingresa la cedula: ")
        cedula = int(cedula.replace(".", ""))

        data_client = self.validate_dni(cedula)
        if data_client == False:
            name = input("Ingresa tu nombre: ")
            while not name.isalpha():
                name = input("Error, Ingresa el nombre: ")

            age = input("Ingresa tu edad: ")
            while not age.isnumeric() or int(age) < 1:
                age = input("Error, Ingresa la edad: ")
            age = int(age)

            data_client = Client(name, age, cedula)
            self.Lista_Client.append(data_client)
        
        for index, match in enumerate(self.Lista_Match):
            print(f"        ----------{index+1}----------")
            print(match.show())
        
        match_number = input("Ingrese el numero del partido que desea escoger: ")
        while not match_number.isnumeric() or not int(match_number) in range(1, len(self.Lista_Match)+1):
            match_number = input("Ingrese el numero del partido que desea escoger: ")
        
        type_ticket = input("Ingrese el numero del tipo de entrada que desea: \n1. General \n2. VIP \n")
        while not type_ticket.isnumeric() or not int(type_ticket) in range(1, 3):
            type_ticket = input("Ingrese el numero del tipo de entrada que desea: \n1. General \n2. VIP \n")

        match = self.Lista_Match[int(match_number)-1]
        match_capacity = match.stadium.capacity
        price = 0 
        if type_ticket == "1":
            match_capacity = match_capacity[0]
            price = 35
        else:
            match_capacity = match_capacity[1]
            price = 75
        
        row = match_capacity//10

        seating = []
        for i in range(1, row+1):
            row_seating = []
            for j in range(1, 11):
                if len(str(i)) == 1:
                    i = "0"+str(i)
                seat = f"{i}-{j}"
                row_seating.append(seat)
            seating.append(row_seating)
        
        for seat in seating:
            seat = " | ".join(seat)
            print(seat)

        if type_ticket == "1":
            ticket_bought = match.tickets_general
        else:
            ticket_bought = match.tickets_vip

        
        print("formato del codigo fila-columna")
        seat_row = input("Ingresa la fila del asiento: ")
        while not seat_row.isnumeric() or not int(seat_row) in range(1, row+1):
            seat_row = input("Ingresa la fila del asiento: ")

        print("formato del codigo fila-columna")
        seat_column = input("Ingresa la columna del asiento: ")
        while not seat_column.isnumeric() or not int(seat_column) in range(1, 11):
            seat_column = input("Ingresa la columna del asiento: ")
        
        seat = f"{seat_column}-{seat_column}"

        while seat in ticket_bought:
            print("Ticket ocupado ingrese otro")

            print("formato del codigo fila-columna")
            seat_row = input("Ingresa la fila del asiento: ")
            while not seat_row.isnumeric() or not int(seat_row) in range(1, row+1):
                seat_row = input("Ingresa la fila del asiento: ")

            print("formato del codigo fila-columna")
            seat_column = input("Ingresa la columna del asiento: ")
            while not seat_column.isnumeric() or not int(seat_column) in range(1, 11):
                seat_column = input("Ingresa la columna del asiento: ")
            
            seat = f"{seat_column}-{seat_column}"

        
        subtotal = price
        descuento = 0
        if vampiro(cedula):
            descuento = subtotal*0.5
        IVA = subtotal*0.16
        total = subtotal - descuento + IVA
        

        print("-------Resumen-------")
        print("---------------------------")
        print(f"-Asiento: {seat}")
        print(f"-Subtotal: {subtotal}")
        print(f"-descuento {descuento}")
        print(f"-IVA: {IVA}")
        print(f"-total: {total}")

        shopping = input("Desea comprar la entrada? \n1. si\n2. no \n>")
        while not shopping.isnumeric() or not int(shopping) in range(1,3):
            shopping = input("Desea comprar la entrada? \n1. si\n2. no \n>")
        
        if shopping == "1":
            id_unico = uuid.uuid4()
            print(f"Gracias por su compra, este el codig de tu entrada: {id_unico}")
            data_client.balance += total
            data_client.type_ticket = type_ticket
            match.ticket_bought.append(seat)
            new_ticket = Ticket(id_unico, cedula, type_ticket, seat, match)
            self.Lista_Ticket.append(new_ticket)

        else:
            print("Hasta luego")
    
    def vampiro(numero):
        digitos = list(str(numero))
        num_digitos = len(digitos)

        # Comprobación de los factores
        for i in range(1, int(numero**0.5)+1):
            if numero % i == 0:
                factor1 = str(i)
                factor2 = str(numero // i)
                factores = factor1 + factor2

                # Comprobación de la permutación
                if sorted(digitos) == sorted(factores) and len(factor1) == len(factor2):
                    return True

        return False

    def validate_dni(self, cedula):
        for client in self.Lista_Client:
            if int(client.dni) == int(cedula):
                return client
        
        return False

    #Gestión de asistencia a partidos
    def modulo_3(self):
        code = input("Ingrese el numero del codigo que desea revisar: ")
        if self.validate_ticket():
            print("Entrada Valida")
        else:
            print("Esta entrada no es valida")
        
    def validate_ticket(self, code):
        for ticket in self.Lista_Ticket():
            if ticket.id.lower() == code.lower() or ticket.attendance != False:
                match.attendance += 1
                return True
        
        return False

    #Gestión de restaurantes
    def modulo_4(self):
        opciones = ["Buscar producto por nombre", "Buscar producto por tipo", "Buscar producto por rango"]
        opcion = self.menu(opciones)

        if opcion == 0:
            self.search_product_name()
        elif opcion == 1:
            self.search_product_type()
        elif opcion == 2:
            self.search_product_range()

    def search_product_name(self):
        product_search =input("Ingresa el nombre del producto que desea buscar: ").lower()
        find = False
        for product in self.Lista_Product:
            if product_search == product.name.lower():
                find = True
                print(product.show())
        
        if not find:
            print("No se encontraron resultados")

    def search_product_type(self):
        product_search =input("Ingresa el numero de la opcion que desee buscar: \n1. De Paquete \n2. De Plato \n3. Con Alcohol: \4. Sin Alcohol: ")
        find = True
        for product in self.Lista_Product:
            if product_search == "1" and product.adicional == "package":
                print(product.show())
            elif product_search == "1" and product.adicional == "plate":
                print(product.show())
            elif product_search == "1" and product.adicional == "alcoholic":
                print(product.show())
            elif product_search == "1" and product.adicional == "non-alcoholic":
                print(product.show())
            elif not product_search in "1234":
                find = False

        if find:
            print("Dato invalido")

    def search_product_range(self):
        product_search_min =input("Ingresa el numero minimo del precio: ")
        while not product_search_min.isnumeric():
            product_search_min =input("Ingresa el numero minimo del precio: ")
        
        product_search_max =input("Ingresa el numero maximo del pecio: ")
        while not product_search_max.isnumeric() and float(product_search_max) < float(product_search_min):
            product_search_max =input("Ingresa el numero maximo del precio: ")
        
        find = False
        for product in self.Lista_Product:
            if float(product_search_min) < product.price < float(product_search_max):
                find = True
                print(product.show())
        
        if not find:
            print("No hay resultados en este rango")

    #Gestión de venta de restaurantes
    def modulo_5(self):
        cedula = input("Ingresa tu cedula (sin puntos): ")
        while not cedula.replace(".", "").isnumeric() or 7 > len(cedula.replace(".", "")) > 8:
            cedula = input("Error, Ingresa la cedula: ")
        cedula = int(cedula.replace(".", ""))

        data_client = self.validate_dni(cedula)

        if data_cliente == False:
            print("Usted no es cliente")
        else:
            if data_cliente != 2:
                print("Usted no es cliente VIP")
            else:
                stadium = data_client.tickets[-1].partido.stadium
                restaurants = stadium.restaurants

                for index, restaurant in enumerate(restaurants):
                    print(f"        ----------{index+1}----------")
                    print(restaurant.show())
                
                opcion = input("Ingrese el numero del restaurante que desea escoger: ")
                while not opcion.isnumeric() or not int(opcion) in range(1, len(restaurants)+1):
                    opcion = input("Ingrese el numero del restaurante que desea escoger: ")
                
                restaurant = restaurants[int(opcion)-1]
                products = restaurant.products

                for index, product in enumerate(products):
                    print(f"        ----------{index+1}----------")
                    print(product.show())
                
                opcion = input("Ingrese el numero del producto que desea comprar: ")
                while (not opcion.isnumeric() or not int(opcion) in range(1, len(products)+1)) or (data_client.age < 18):
                    opcion = input("Ingrese el numero del producto que desea comprar, recuerda que si eres menor no puede comprar alcohol: ")
                
                product = products[int(opcion)]

                quantity = input("Ingresa la cantidad de productos que desea comprar")
                while not quantity.isnumeric():
                    quantity = input("Ingresa la cantidad de productos que desea comprar")
                
                subtotal = product.price* int(quantity)
                descuento = 0
                if perfecto(data_client.dni):
                    descuento = subtotal*0.15
                IVA = subtotal*0.16
                total = subtotal - descuento + IVA

                print("-------Resumen-------")
                print("---------------------------")
                print(f"-Producto: {product.name}")
                print(f"-Cantidad: {quantitye}")
                print(f"-Subtotal: {subtotal}")
                print(f"-descuento {descuento}")
                print(f"-IVA: {IVA}")
                print(f"-total: {total}")

                shopping = input("Desea realizar la compra? \n1. si\n2. no \n>")
                while not shopping.isnumeric() or not int(shopping) in range(1,3):
                    shopping = input("Desea realizar la compra? \n1. si\n2. no \n>")
                
                if shopping == "1":
                    print("compra exitosa")
                    data_client.balance += total
                    product.quantity -= quantity
                    product.sold += quantity
                else:
                    print("Gracias por visitar")

    def perfecto(numero):
        suma_divisores = 0
        for i in range(1, numero):
            if numero % i == 0:
                suma_divisores += i
        return suma_divisores == numero

    #Indicadores de gestión (estadísticas)
    def modulo_6(self):
        opciones = ["promedio de gasto de un cliente VIP en un partido", "tabla con la asistencia a los partidos de mejor a peor", "partido con mayor asistencia", "el partido con mayor boletos vendidos", "Top 3 productos más vendidos en el restaurante.", "Top 3 de clientes (clientes que más compraron boletos)"]
        opcion = self.menu(opciones)

        if opcion == 0:
            print("promedio de gasto de un cliente VIP en un partido")

            balance = 0
            aux = 0
            for client in self.Lista_Client:
                if client.type_ticket = "2":
                    balance += client.balance
                    aux += 1

            print(f"El promedio de gasto de un cliente VIP es de: {balance/aux}$")
        elif opcion == 1:
            print("tabla con la asistencia a los partidos de mejor a peor")
            print("local, estadio, boletos vendidos, personas que asistieron, la relación asistencia/venta")
            
            matchs = []
            for match in self.Lista_Match:
                total = len(match.tickets_general)+len(match.tickets_vip)
                relacion = total-match.attendance
                matchs.append([match.home, match.away, total,match.attendance, relacion])
            lista_ordenada = sorted(matchs, key=comparar_por_total, reverse=True)

            for match in matchs:
                print(match)

        elif opcion == 2:
            print("partido con mayor asistencia")

            partido_max = self.Lista_Match[0]
            for match in range(1, len(self.Lista_Match)):
                if partido_max.attendance < match.attendance:
                    partido_max = match

            partido_max.show()


        elif opcion == 3:
            print("el partido con mayor boletos vendidos")
            partido_max = self.Lista_Match[0]
            for match in range(1, len(self.Lista_Match)):
                if partido_max.attendance < match.attendance:
                    partido_max = match

            partido_max.show()
            
        elif opcion == 4:
            print("Top 3 productos más vendidos en el restaurante.")
        elif opcion == 5:
            print("Top 3 de clientes (clientes que más compraron boletos)")

    def comparar_por_total(lista1, lista2):
        if lista1[2] > lista2[2]:
            return 1
        elif lista1[2] < lista2[2]:
            return -1
        else:
            return 0        


    #Guardar informacion en Archivo.txt
    def txt(self):
        pass
