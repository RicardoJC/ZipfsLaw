# -*- coding: utf-8 -*-
# Primer programa de Procesamiento de Lenguaje Natural
# Programa que realiza:
#    * Quita los signos de puntuación del corpus
#    * Obtiene el stem de cada token del corpus
#    * Obtiene el número de tokens y tipos
#    * Obtiene el parámero Beta de la ley de Herdan
#    * Obtiene la gráfica con las estadísticas de la ley de Zipf
#    * Obtiene la curva de Zipf
# Por Jimenez Cruz Ricardo


import codecs
import sys
import re
import snowballstemmer
import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter
import math

reload(sys)
sys.setdefaultencoding('utf8')


NAME_FILE = 'quijote.txt'

# Función que sustituye caracteres especiales y sustituye acentos
def parser(line):
    line = line.replace(',','')
    line = line.replace('.','')
    line = line.replace(':','')
    line = line.replace(';','')
    line = line.replace('—','')
    line = line.replace('-','')
    line = line.replace('!','')
    line = line.replace('¡','')
    line = line.replace('¿','')
    line = line.replace('?','')
    line = line.replace('«','')
    line = line.replace('»','')
    line = line.replace('(','')
    line = line.replace(')','')
    line = line.replace('\'','')
    line = line.replace('\"','')
    line = line.replace('\n','')
    line = line.replace('á','a')
    line = line.replace('é','e')
    line = line.replace('í','i')
    line = line.replace('ó','o')
    line = line.replace('ú','u')
    line = line.replace('Á','A')
    line = line.replace('É','E')
    line = line.replace('Í','I')
    line = line.replace('Ó','O')
    line = line.replace('Ú','U')
    return line

# Función que sustituye caracteres especiales y no sustituye acentos
def parserRegex(line):
    line = line.replace('\n',' ')
    line = re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ ]', '',line)
    return line

# Función que sustituye caracteres especiales y sí sustituye acentos
def parserRegexA(line):
    line = line.replace('á','a')
    line = line.replace('é','e')
    line = line.replace('í','i')
    line = line.replace('ó','o')
    line = line.replace('ú','u')
    line = line.replace('Á','A')
    line = line.replace('É','E')
    line = line.replace('Í','I')
    line = line.replace('Ó','O')
    line = line.replace('Ú','U')
    line = line.replace('\n',' ')
    line = re.sub(u'[^a-zA-Z0-9ñÑ ]', '',line)
    return line


def zetaRiemann(n):
    # a un valor entre 0 y 1
    a = 0.69
    r = 0
    for i in range(1,n+1):
        r += 1/pow(i,a)
    return r

def chartZipf(diccionario):

    fig, ax = plt.subplots()
    x = np.arange(0, len(diccionario), 1)
    y = sorted(diccionario.values(),reverse=True)

    ax.plot(x, y, marker='o')
        # Modificar los valores del segundo parametro para generar imagenes con un rango más o de menor amplitud
    ax.set_xlim((0, 100))
    ax.set_ylim((0, 22000))
    plt.title('Ley de Zipf')
    plt.xlabel('Rango de 100 palabras')
    plt.ylabel('Frecuencia')
    plt.savefig("zipf.png")


def curveChartZipf(diccionario):

    fig,ax = plt.subplots()
    x = []
    ylog = []
    y = sorted(diccionario.values(),reverse=True)
    for i in range(0,len(diccionario)):
        x.append(math.log10(i+1))
        ylog.append(math.log10(y[i]))
    ax.plot(x, ylog, marker='o')
    plt.title('Curva de Zipf')
    plt.xlabel('Logaritmo del rango')
    plt.ylabel('Logaritmo de la frecuencia')
    plt.savefig('curva_zipf.png')



print "Este programa genera archivos txt con los resultados"
print "Espere un momento ..."
quijote = codecs.open(NAME_FILE,'r',encoding='utf-8')

# Se crea un nuevo archivo
archivo = open('free_'+NAME_FILE,'w')
stemmer = snowballstemmer.stemmer('Spanish')


# Se hizo con la función parser
for line in quijote:
    archivo.write(parser(line))
quijote.close()
archivo.close()

archivo = codecs.open('free_'+NAME_FILE,'r',encoding='utf-8')
stemmer = snowballstemmer.stemmer('Spanish')
frecuencia = {}
herdan = {}
n_tokens = 0

for line in archivo:
    palabras = line.split()
    for palabra in palabras:
        n_tokens += 1
        original = palabra.lower()
        conteo = frecuencia.get(original,0)
        frecuencia[original] = conteo + 1
        conteo2 = herdan.get(stemmer.stemWord(original),0)
        herdan[stemmer.stemWord(original)] = conteo2 + 1

archivo.close()

print 'Total de tokens -> %d' % n_tokens
print 'Total de tipos  -> %d' % len(herdan)
print 'El parámetro Beta de la ley de Herdan por la relación Tipo - Token es: %.3f' % (math.log10(n_tokens)/math.log10(len(herdan)))


zipf = open('zipf.txt','w')
i=0
for key, value in reversed(sorted(frecuencia.items(), key = itemgetter(1))):
    i+=1
    rango = 'Rango -> %d' %i
    palabra = 'Palabra -> %s' %key
    repeticion = 'Aparece %d veces' %value
    frase = "%s %s %s \n" %(rango.ljust(20,' '), palabra.ljust(30,' '),repeticion.ljust(25,' '))
    zipf.write(frase)

zipf.close()



# Crea una imagen con la estadísticas de Zipf
chartZipf(frecuencia)
# Crea una image con la curva de Zip
curveChartZipf(frecuencia)

print 'Listo!'
