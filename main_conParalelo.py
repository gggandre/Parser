from concurrent.futures import ProcessPoolExecutor
from tkinter import W
from typing import NamedTuple
import re
import time
import os

inicio = time.time()
#Creamos una clase token que tendra los parametros de type y value
class Token(NamedTuple):
    type: str
    value: str

def tokenize(code): #Función que sirve para asignar el tipo de token a cada uno de los valores
    #print(code)
    token_specification = [ #Lista de expresiones regulares de nuestros tokens
        ('variableNoValida', r'\d+[A-Za-z]+([\d_A-Za-z]*)+'),
        ('numero', r'\d+(\.\d*)?'),
        ('asignacion', r'\='),
        ('suma', r'\+'),
        ('resta', r'\-'),
        ('multiplicacion', r'\*'),
        ('Comentario', r'(\/{2}.*)'),
        ('division', r'\/'),
        ('potencia', r'\^'),
        ('variable', r'[A-Za-z]+([\d_A-Za-z]*)+'),
        ('parentesisQueAbre', r'\('),
        ('parentesisQueCierra', r'\)'),
        ('EMPTY', r'\b'),
        ('NEWLINE', r'\n'),
        ('SKIP', r'[ \t]+'),
        ('MISMATCH', r'.'),
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
  #Clasificación de los valores con su token
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'numero':
            if '.' in value:
                kind = 'decimal'
                value = float(value)
            else:
                kind = 'entero'
                value = int(value)
        elif kind == 'SKIP':
            continue
        elif kind == 'EMPTY':
            continue
        elif kind == 'NEWLINE':
            line_num += 1
            continue
        elif kind == 'MISMATCH':
            kind = 'caracterNoIdentificado'
    
        #print(kind, "      ", value)
        yield Token(kind, value)
     
#Función que define nuestra gramatica
def gramatica():
  #Primer condicionar que haya variable y asignación.  Posterior checa la expresión y si hay comentarios o no

  if tokens[ite].type == "variable" and tokens[ite+1].type == "asignacion":
    match("variable")
    match("asignacion")
    V()
    if contParentesis != 0:
      raise Exception
    else:
      Co()
  #Puede que la linea sea solo un comentario
  elif tokens[ite].type == "Comentario":
    match("Comentario")
  else: #Si no cumple con alguna manda error
    raise Exception

def E(): #Función para definir las expresiones, es recursiva
  global contParentesis
  #Arreglar la expresión para que siempre empiece por numero o variable y las expresiones tengan sentido
  if (ite >= len(tokens)):
    pass
  else:
    if tokens[ite].type == "suma":
      match("suma")
      V()
    elif tokens[ite].type == "resta":
      match("resta")
      V()
    elif tokens[ite].type == "multiplicacion":
      match("multiplicacion")
      V()
    elif tokens[ite].type == "division":
      match("division")
      V()
    elif tokens[ite].type == "potencia":
      match("potencia")
      V()
    elif tokens[ite].type == "parentesisQueCierra":
      contParentesis -= 1
      match("parentesisQueCierra")
      E()
    elif tokens[ite].type == "caracterNoIdentificado" or tokens[ite].type == "variableNoValida":
	    raise Exception
    
def V():
  global contParentesis

  if (ite >= len(tokens)):
    pass
  else:
    if tokens[ite].type == "parentesisQueAbre":
      match("parentesisQueAbre")
      contParentesis += 1
      E()
      V()
      
    elif tokens[ite].type == "entero":
      match("entero")
      E()
    elif tokens[ite].type == "decimal":
      match("decimal")
      E()
    elif tokens[ite].type == "variable":
      match("variable")
      E()
    else:
      raise Exception  
    

def Co():#Función para definir si hay comentario
  if (ite >= len(tokens)):
    pass
  else:
    if tokens[ite].type == "Comentario":
      match("Comentario")
    else:
      pass
  
def match(c): #Verificamos que concida el parametro dado con el tipo del token
  global ite
  
  if tokens[ite].type == c:
    ite +=1
  else:
    raise Exception

def devolverArchivos(carpeta):
  for archivo in os.listdir(carpeta):
      if os.path.isdir(os.path.join(carpeta,archivo)):
            devolverArchivos(os.path.join(carpeta,archivo))    
      else:
        ingreso = os.path.join(carpeta,archivo)
        files.append(ingreso)

def evidencia(ingreso):
  global ite
  global contParentesis
  global tokens

  lista =[]
  file = open(ingreso, 'r')
  lineas = file.readlines()

  for elemento in lineas:
    tokens = []
    expresion = []
    ite = 0
    contParentesis = 0
    try:             
        for token in tokenize(elemento):
            tokens.append(token)
        if len(tokens) >=3:
            gramatica()
            #print(elemento.strip(), "Correct")
            for token in range (len(tokens)):
              clase = tokens[token].type
              value = tokens[token].value

              data = [clase, value]
              expresion.append(data)
            lista.append(expresion)
              
        else:
            raise Exception
    except Exception:
      #print(elemento.strip(), "Error!")
      for token in range (len(tokens)):
        clase = 'ERROR'
        value = tokens[token].value

        data = [clase, value]
        expresion.append(data)
      lista.append(expresion)
  viewHtml(ingreso, lista)
      
def viewHtml(ingreso, lista):
  inicio = []
  archivo = re.sub("\.txt", "", ingreso)
  stylecss = os.path.basename(archivo)
  with open(f'{archivo}.html', "w+") as Indexhtml:
    Indexhtml.write(f'''
    <!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="{stylecss}.css">
    <title>Evidencia 1</title>
</head>
	<body>
		<h1>Etapa 2 - Situación Problema 1: Analizador Sintáctico Paralelo</h1>
        <h2>Indice de Color</h2>
        <p>Variable: <span class="variable"> azul rey </span></p>
        <p>Asignacion: <span class="asignacion"> naranja </span></p>
        <p>Entero: <span class="entero"> cafe </span></p>
        <p>Decimal: <span class="float"> verde </span></p>
        <p>Suma: <span class="suma"> fuchsia </span></p>
        <p>Resta: <span class="resta"> azul claro </span></p>
        <p>Multiplicacion: <span class="multiplicacion"> amarillo </span></p>
        <p>Division: <span class="division"> morado </span></p>
        <p>Raiz: <span class="raiz"> verde amarillo </span></p>
        <p>Potencia: <span class="potencia"> azul  </span></p>
        <p>Parentesis que abre: <span class="parentesisQueAbre"> ocre </span></p>
        <p>Parentesis que cierra: <span class="parentesisQueCierra"> rosa claro </span></p>
        <p>Comentario: <span class="Comentario"> coral </span></p>
        <p>Error: <span class="ERROR">rojo </span></p> 
    ''')
    for exp in lista:
      Indexhtml.write("<p>")
      for item in exp:
        Indexhtml.write(f"""<span class="{item[0]}">{item[1]}</span>""")
      Indexhtml.write("</p>\n")
    Indexhtml.write('''
</body>
</html>''')
    
    with open(f'{archivo}.css', "w+") as css:
      css.write('''
.entero{
    color: brown;
    background-color: white;
}

.asignacion{
    color: orange;
    background-color: white;
}


.decimal{
    color: green;
    background-color: white;
}

.variable{
    color: blue;
    background-color: white;
}

.suma{
    color: fuchsia;
    background-color: white;
}

.resta{
    color: lightskyblue;
    background-color: white;
}

.multiplicacion{
    color: yellow;
    background-color: white;
}

.division{
    color: purple;
    background-color: white;
}

.raiz{
    color: greenyellow;
    background-color: white;
}


.potencia{
    color: rgb(0, 153, 255);
    background-color: white;
}


.parentesisQueAbre{
    color: darkgoldenrod;
    background-color: white;
}


.parentesisQueCierra{
    color: lightpink;
    background-color: white;
}


.Comentario{
    color:lightcoral ;
    background-color: white;
}

h1{
    color: brown;
    font-size: 23;
    font-weight: bolder;
}

.ERROR{
    background-color: red;
}''')
  
def main(): #Función main para correr el programa
    global files

    files = []
    devolverArchivos("C:\\Users\\gggan\\Desktop\\Parser\\Test")
    with ProcessPoolExecutor(max_workers = 6) as executor:
      executor.map(evidencia, files, chunksize = 10)
    fin = time.time()
    print(fin-inicio)

if __name__ == '__main__':
  main()