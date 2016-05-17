from xml.etree import ElementTree
import csv
import io
import os
import mechanize
from bs4 import BeautifulSoup

files = []
for file in os.listdir('BDTD_UNICAMP/'):
    if file.endswith(".xml"):
        files.append(file)

def escrever_arquivo(array):
		with io.open ('3/tesL22.csv', 'ab') as fp:
		    writer = csv.writer(fp, delimiter=';')
		    writer.writerow(array)

errors = []

estrutura = ['{http://oai.ibict.br/mtd2-br/}Nome' , '{http://oai.ibict.br/mtd2-br/}Citacao' , '{http://oai.ibict.br/mtd2-br/}Lattes' , '{http://oai.ibict.br/mtd2-br/}CPF'
,'{http://oai.ibict.br/mtd2-br/}CPF']
formats = dict()
for filexml in files:
	with open('BDTD_UNICAMP/' + filexml, 'rt') as f:
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
		if formats.has_key(td.text):
			formats[td.text] +=  1
		else:
			formats[td.text] = 1
		print td.text


	except:
		print 'error ->' , url
		errors.append(url)



#sem documento - 629
#PDF: 45359