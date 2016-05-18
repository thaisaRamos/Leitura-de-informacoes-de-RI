from xml.etree import ElementTree
import csv
import io
import os
import mechanize
from bs4 import BeautifulSoup

#pasta onde encontra os xmls
diretorio = 'mtd2-br/'

#array para armazenar todos os arquivos encontrado no diretorio
files = []
for file in os.listdir(diretorio):
    if file.endswith(".xml"):
        files.append(file)

def escrever_arquivo(array):
		with io.open ('repositorios.csv', 'ab') as fp:
		    writer = csv.writer(fp, delimiter=';')
		    writer.writerow(array)

#array para armazernar os arquivo nao encontrados
errors = dict()
#dicionario para armazernar todos os diferentes tipos de formatos encontrados
formats = dict()
for filexml in files:
	print filexml
	with open(diretorio + filexml, 'rt') as f:
	    tree = ElementTree.parse(f)
	id = ''
	tipo = {}
	urlenc = False
	root = tree.getroot()
	for arquivo in root.findall('{http://oai.ibict.br/mtd2-br/}Arquivo'):
		info = arquivo.getchildren()
		for i in info:
			if not i.getchildren():
				if i.text != None:
					if i.tag == '{http://oai.ibict.br/mtd2-br/}URL':
						urlenc = True
						tipo = i.attrib
						if tipo != {}:
							tipo = tipo['Formato']
	
	for dados in root.findall('{http://oai.ibict.br/mtd2-br/}InstituicaoDefesa'):
		info = dados.getchildren()
		for i in info:
			if i.tag == '{http://oai.ibict.br/mtd2-br/}Sigla':
				if i.text != None:
					id = i.text

	
	if id != '' and tipo != {} and urlenc:
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

