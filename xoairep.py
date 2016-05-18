from xml.etree import ElementTree
import csv
import io
import os
import mechanize
from bs4 import BeautifulSoup

#pasta onde encontra os xmls
diretorio = 'xoai/'

#array para armazenar todos os arquivos encontrado no diretorio
files = []
for file in os.listdir(diretorio):
    if file.endswith(".xml"):
        files.append(file)

def escrever_arquivo(array):
		with io.open ('repositorios.csv', 'ab') as fp:
		    writer = csv.writer(fp, delimiter=';')
		    writer.writerow(array)

#dicionario para armazernar todos os diferentes tipos de formatos encontrados
formats = dict()
for filexml in files:
	with open(diretorio + filexml, 'rt') as f:
	    tree = ElementTree.parse(f)
	
	universidade = ''
	root = tree.getroot()

	for records in root.findall('{http://www.lyncode.com/xoai}element'):
		for child in records:
			for r in child.findall("[@name='bundle']"):
				for child in r.getchildren():
					if (child.attrib == {'name': 'bitstreams'}) :
						for child in child.getchildren():
							for child in child.getchildren():
								if (child.attrib == {'name': 'format'}) :
								 	tipo = child.text

	for indentifier in root.findall("{http://www.lyncode.com/xoai}identifier"):
			id = indentifier.text[23:].split(':')
			id = id[0]
			universidade = id
	if universidade != '' and tipo != '':
		print universidade
		if formats.has_key(universidade):
			if formats[universidade].has_key(tipo):
				formats[universidade][tipo] +=  1
			else:
				formats[universidade][tipo] = 1
		else:
			formats[universidade] = dict()
			formats[universidade][tipo] = 1

		print tipo

	elif tipo =='':
		if formats[universidade].has_key('sem documento'):
			formats[universidade]['sem documento'] +=  1
		else:
			formats[universidade]['sem documento'] = 1

#Percore o fomats e vai salvando em um arquivo .csv
for i in formats.keys():
    a = []
    a.append(i)
    for j in formats[i]:
    	a.append(unicode(j.decode('utf-8')))
    	a.append(formats[i][j])
    escrever_arquivo(a)
