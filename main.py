#!/usr/bin/python3
#-*- coding: utf-8 -*-

import subprocess
import re
import os

styles = """<style>
        .container {
            width: 50em;
            margin: auto;
        }

        .header {
            display: flex;
            justify-content: center;
            background-color: #1c66a3;
            height: 5em;
        }

        .header h1 {
            color: white;
        }

        .data {
            text-align: right;
        }

        .table-container {
            margin-top: 1em;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        #table_div {
            width: 100%;
        }
    </style>"""

def ejecutar_subproceso(bash_command):
	"""Metodo que ejecuta un comando de bash en un subproceso

		Parameters
		----------
		bash_commnad : str
			instrucción del bash (Bourne-again shell) 

		Returns
		-------
		subprocess.Popen
			resultados del comando de bash


	"""
	p = subprocess.Popen(bash_command, 
							stdout = subprocess.PIPE, 
							stderr = subprocess.PIPE,
							shell = True
						)
	p.wait()
	return p


def generate_table_stats():
	table = """
	<script type="text/javascript">
      google.charts.load('current', {'packages':['table']});
      google.charts.setOnLoadCallback(drawTable);

      function drawTable() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Container ID');
        data.addColumn('string', 'Name');
        data.addColumn('string', 'CPU %');
		data.addColumn('string', 'RAM Usage');
		data.addColumn('string', 'RAM %');
        data.addRows([
	"""

	p = ejecutar_subproceso("sudo docker stats --no-stream")

	# Discarting the first line
	p.stdout.readline().decode()	

	while True:
		line = p.stdout.readline().decode()
		line = re.sub(" +", " ", line)

		if not line or line.strip() == '':
			break
		
		data = line.split(' ')

		table += f'["{data[0]}", "{data[1]}", "{data[2]}", "{data[3]}", "{data[6]}"],'

	table += """
	]);

        var table = new google.visualization.Table(document.getElementById('table_div'));

        table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});
      }
    </script>
	"""

	return table

# Generate the html page
def generate_html():
	html = f"""<html>
	<head>
		{styles}
		<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>      
		{generate_table_stats()}	
	</head>
	<body>
		<div class="container">
			<div class="header">
				<h1>Docker dashboard</h1>
			</div>

			<div class="data">
				<h1>20:23</h1>
			</div>

			<div class="table-container">
				<div id="table_div"></div>
			</div>
			<div id="chart_div" style="width: 400px; height: 120px;"></div>
    	</div>
	</body>
	</html>"""

	try:
		with open("shared/index.html", "w") as archivo:
			archivo.write(html)
			print("Se creó el archivo exitosamente")
	except:
		sys.stderr.write("Error escribiendo el archivo")
	
generate_html()
# generate_table_stats()