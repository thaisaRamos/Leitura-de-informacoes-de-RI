from xml.etree import ElementTree
import csv
import io
import os
import mechanize
from bs4 import BeautifulSoup

#array para armazenar todos os arquivos encontrado no diretorio
diretorio = 'BDTD_USP/'
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
		#leitura do html da pagina da usp para encontrar o formato do documento
		div = soup.find('div', {'class': 'DocumentoTituloTexto2'})
		div = div.findNext('div' , {'class' : 'DocumentoTituloTexto2'})
		div = div.findNext('div' , {'class' : 'DocumentoTituloTexto2'})
		if (div.findNext('div' , {'class' : 'DocumentoTituloTexto2'}) != None):
			div = div.findNext('div' , {'class' : 'DocumentoTituloTexto2'})
		texto = div.text.split('.')
		texto = texto[1].split('(')
		texto = texto[0]
		#se o formato ja existir no dicionario soma mais um
		if formats.has_key(texto):
			formats[texto] +=  1
		#senao cria o novo formato no dicionario
		else:
			formats[texto] = 1

	except:
		print 'Documento sem arquivo associado' , url , "---" , filexml
		errors.append(url)

print formats
print 'Sem documento: ' , len(errors)
