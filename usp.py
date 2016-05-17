from xml.etree import ElementTree
import csv
import io
import os
import mechanize
from bs4 import BeautifulSoup

files = []
for file in os.listdir('BDTD_USP/'):
    if file.endswith(".xml"):
        files.append(file)

def escrever_arquivo(array):
		with io.open ('3/tesL22.csv', 'ab') as fp:
		    writer = csv.writer(fp, delimiter=';')
		    writer.writerow(array)

errors = []
filesxml = []

estrutura = ['{http://oai.ibict.br/mtd2-br/}Nome' , '{http://oai.ibict.br/mtd2-br/}Citacao' , '{http://oai.ibict.br/mtd2-br/}Lattes' , '{http://oai.ibict.br/mtd2-br/}CPF'
,'{http://oai.ibict.br/mtd2-br/}CPF']
formats = dict()
for filexml in files:
	with open('BDTD_USP/' + filexml, 'rt') as f:
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
		div = soup.find('div', {'class': 'DocumentoTituloTexto2'})
		div = div.findNext('div' , {'class' : 'DocumentoTituloTexto2'})
		div = div.findNext('div' , {'class' : 'DocumentoTituloTexto2'})
		if (div.findNext('div' , {'class' : 'DocumentoTituloTexto2'}) != None):
			div = div.findNext('div' , {'class' : 'DocumentoTituloTexto2'})

		texto = div.text.split('.')
		texto = texto[1].split('(')
		texto = texto[0]
		if formats.has_key(texto):
			formats[texto] +=  1
		else:
			formats[texto] = 1
		#print texto


	except:
		print 'error ->' , url , "---" , filexml
		errors.append(url)
		filesxml.append(filexml)



#sem documento - 629
#PDF: 45359