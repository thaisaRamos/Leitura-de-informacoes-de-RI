from xml.etree import ElementTree
import csv
import io
import os
import re
import mechanize
import cookielib
from bs4 import BeautifulSoup

def escrever_arquivo(array):
	with io.open ('repositorios.csv', 'ab') as fp:
	    writer = csv.writer(fp, delimiter=';')
	    writer.writerow(array)

diretorio = 'xoai/'
#array para armazenar todos os arquivos encontrado no diretorio
files = []
for file in os.listdir(diretorio):
    if file.endswith(".xml"): 
        files.append(file)

#dicionario para armazernar todos os diferentes tipos de formatos encontrados
formats = dict()
errors = []
for filexml in files:
	with open(diretorio + filexml, 'rt') as f:
	    tree = ElementTree.parse(f)
	    root = tree.getroot()
	    id = ''
	    tipo = ''
	    urlenc = False
	    for indentifier in root.findall("{http://www.loc.gov/METS/}identifier"):
	    	id = indentifier.text[23:].split(':')
	    	id = id[0]
	    	#print id

		for records in root.findall('{http://www.loc.gov/METS/}fileSec'):
		    for n,child in enumerate(records):
		    	urlenc = True
		    	if n==0:
			    	for child in child.getchildren():
			    		tipo = child.attrib['MIMETYPE']

		if id != '' and tipo != '' and urlenc:
			if formats.has_key(id):
				if formats[id].has_key(tipo):
					formats[id][tipo] +=  1
				else:
					formats[id][tipo] = 1
			else:
				formats[id] = dict()
				formats[id][tipo] = 1

			print tipo
		elif not urlenc:
			if formats[id].has_key('sem documento'):
				formats[id]['sem documento'] +=  1
			else:
				formats[id]['sem documento'] = 1
			errors.append(filexml)
