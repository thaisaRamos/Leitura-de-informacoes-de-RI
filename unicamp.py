from xml.etree import ElementTree
import csv
import io
import os
import mechanize
from bs4 import BeautifulSoup

#pasta onde encontra os xmls
diretorio = 'BDTD_UNICAMP/'
#array para armazenar todos os arquivos encontrado no diretorio
files = []
for file in os.listdir(diretorio):
    if file.endswith(".xml"):
        files.append(file)

#array para armazernar os arquivo nao encontrados
errors = []
#dicionario para armazernar todos os diferentes tipos de formatos encontrados
formats = dict()
for filexml in files:
	with open(diretorio + filexml, 'rt') as f:
	    tree = ElementTree.parse(f)
	
	root = tree.getroot()
	for arquivo in root.findall('{http://oai.ibict.br/mtd2-br/}Arquivo'):
		info = arquivo.getchildren()
		for i in info:
			if not i.getchildren():
				if i.text != None:
					if i.tag == '{http://oai.ibict.br/mtd2-br/}URL':
						url =  i.text		
	try:
		br = mechanize.Browser()
		page = br.open(url)
		html = page.read()
		soup = BeautifulSoup(html)
		table = soup.find('table', {'id': 'tabela-bases'})
		td = table.find('td')
		td = td.findNext('td')
		#se o formato ja existir no dicionario soma mais um
		if formats.has_key(td.text):
			formats[td.text] +=  1
		#senao cria o novo formato no dicionario
		else:
			formats[td.text] = 1
		print td.text


	except:
		print 'error ->' , url
		errors.append(url)
		
print formats
print 'Sem documento: ' , len(errors)