# 6 bits para la operacion, 4 bits para el modo, 22 bits para las memorias
from modes import mode
from operations import operations

#entrada salida
es = {}
#acumulador
ac = 0
#registros de memoria
valores = {}

needToJump = False

lineToJump = 0
#Funciones que ejecuta el programa

#1- Carga de memoria hacia AC
def load(register):
  global ac
  ac = register
  print("Acumulador es: " + str(ac))

#2- Almacenar en memoria desde AC
def save():
    global ac
    return ac

#3- Suma: memoria + AC
def sum(register):
  global ac
  ac = ac +register
  print("Acumulador es: " + str(ac))

#4- Suma: memoria1 + memoria2 + AC
def sum2(register1, register2):
  global ac
  ac = ac + register1 + register2
  print("Acumulador es: " + str(ac))

#10- Suma: memoria 1 + memoria 2, almacena en memoria 1
def sum3(register1, register2):
    return register1 + register2

#5- Resta: AC - memoria1, almacena en AC
def sub1(register):
  global ac
  ac = ac - register
  print("Acumulador es: " + str(ac))

#6- Resta: AC - memoria1,  almacena en memoria2
def sub2(register1):
  global ac
  return ac - register1

#7- Multiplicación: memoria x AC, almacena en AC
def mult(register1):
  global ac
  ac = ac * register1
  print("Acumulador es: " + str(ac))

#11- Multiplicación: memoria 1 x AC, almacena en memoria 2
def mult2(register1):
    global ac
    ac = ac * register1
    print("Acumulador es: " + str(ac))

#12- División: AC / memoria 1, almacena en AC 
def div(register1):
  global ac
  ac = ac // register1
  print("Acumulador es: " + str(ac))
  return ac

#13- División: AC / memoria 1, almacena en memoria 2
def div2(register1): #dividir el acumulador entre el registro se almacena en el registro2
  global ac
  return ac // register1


def ifOp(mode, valor1):
   match mode:
      case "=":
         if ac == valor1 : return True
         return False
      case "<":
         if ac < valor1 : return True
         return False
      case ">":
         if ac > valor1 : return True
         return False
      case "<=":
         if ac <= valor1 : return True
         return False
      case ">=":
         if ac >= valor1 : return True
         return False
      case "!=":
         if ac != valor1: return True
         return False
   pass
 
#Guardar en E/S desde AC, almacena el contenido de AC en un dispositivo de E/S
# retorna el registro ES donde se guardó el valor
def load_to_es(register):
    global ac
    es[register] = ac

    
# lee el dato de E/S y lo almacena en AC
def load_from_es(es_direction):
    global ac
    ac = es[es_direction]
    print("Acumulador es: " + str(ac))
    
  
# Escribir al archivo la informacion
def write_to_es_file():
  es_file = open('./es.txt', 'w')
  es_record = ''
  for x in es.keys():
    es_record += str(x) + '/' + str(convertToBinary(es[x])) + '\n' 
  es_file.write(es_record)
  es_file.close()

# lee el archivo y carga la variable es
def load_es_variable():
  es_file = open('./es.txt', 'r')
  for value in es_file.readlines():
    data = value.split('/')
    es[int(data[0])] = int(data[1],2)
  print(es)
  
#-------Funciones de lectura y ejecucion de instrucciones-----------------

#lee la instruccion y retorna la accion
def read_action(instruction):
    return operations[instruction[0:6]]
#0000001111
#lee la instruccion y retorna el modo
def read_mode(instruction):
   print(mode[instruction[6:10]])
   return  mode[instruction[6:10]]

#lee la instruccion y retorna los registros
def read_register(instruction):
    return  int(instruction[10:21], 2), int(instruction[21:32], 2)

#ejecuta la accion
def execute_action(action, register1, register2, mode):
    valor1 = valores.get(register1)
    valor2 = valores.get(register2)

    match action:
      case "load":
        load(valor1)
      case "save":
        write_register(register1, save())
      case "sum1":
        sum(valor1)
      case "sum2":
        sum2(valor1, valor2)
      case "sum3":
        write_register(register2, sum3(valor1, valor2))
      case "sub1":
        sub1(valor1)
      case "sub2":
        write_register(register2, sub2(valor1))
      case "mul":
        mult(valor1)
      case "mul2":
        mult2(valor1)
      case "div":
        div(valor1)
      case "div2":
        write_register(register2, div2(valor1))
      case "load2":
          load_from_es(register1)
      case "save2":
          load_to_es(register1)
      case "if":
          global needToJump
          needToJump = ifOp(mode, valor1)
    pass

#guarda el valor en el registro
def write_register(register,valor): #guarda el valor en el registro
    if(register in valores.keys()):
        valores[register] = valor

    else: valores[int(register)] = int(valor,2)

#convierte el numero a binario
def convertToBinary(num):
    return bin(num).replace("0b", "")
# ------ Pruebas a funciones ----------


# ins = "700/00000100011001110001010011100100"

# data = ins.split("/")
# print(data[1][0:6])
# print(data[1][6:10])
# print(data[1][10:21])
# print(data[1][21:32])
# print(read_action(data[1]))
# print(read_mode(data[1]))
# print(read_register(data[1]))
#-------Ejecucion del programa-----------------
f = open("./datos.txt", "r")
#leer el archivo de datos
for r in f :
    data = r.split("/")
    write_register(data[0], data[1])
    print(valores)
    
print(valores)
f.close()

#ejecutar las instrucciones
g = open("./Instrucciones.txt", "r")
load_es_variable()
counter = 0
for x in g:
  #00011001110010000000000000
  data = x.split("/")
  if needToJump and data[0] != lineToJump: 
     pass
  print(len(data[1]))
  print(data[1][0:6])
  print(data[1][6:10])
  print(data[1][10:21])
  print(data[1][21:32])
  print(str(counter) + " CONTADOR")
  counter+= 1
#ya no seria necesario el if en el caso en que trabajemos con archivos distintos
  accion = read_action(data[1])
  print(accion)
  register1, register2 = read_register(data[1])
  mode = read_mode(data[1])
  execute_action(accion, register1, register2, mode)
  if needToJump: 
     lineToJump =  int(register2, 2)
     print(lineToJump)
  if lineToJump == data[0]: 
     needToJump = False
g.close()

#guardar los datos en el archivo de datos asi como el de E/S
h = open("./datos.txt", "w")
for x in valores:
    h.write(str(x) + "/" + str(convertToBinary(valores[x])) + "\n")
h.close()
write_to_es_file()

#leer los datos del archivo
print("Acumulador finalizado: " + str(ac))
print("\nDatos del archivo")
h = open("./datos.txt", "r")
result = h.read()
print(result)
h.close()


