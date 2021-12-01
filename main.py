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
        data.addColumn('string', 'Name');
        data.addColumn('string', 'Salary');
        data.addColumn('string', 'Full Time Employee');
        data.addRows([
	"""

	# p = ejecutar_subproceso("sudo docker stats")
	table += "['Mike',  {v: 10000, f: '$10,000'}, true],"


	table += """
	]);

        var table = new google.visualization.Table(document.getElementById('table_div'));

        table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});
      }
    </script>
	"""

	return table

def get_time():
	time_cmd = ejecutar_subproceso("top -bn1")

	top = time_cmd.stdout.readlines()[0].decode()

	time = top.split(" ")

	return time[2]

def generar_grafica_memoria():

	inicio = """ <script type="text/javascript">
      google.charts.load('current', {'packages':['gauge']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {

        var data = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Memory', """

	fin = """]
        ]);

        var options = {
          width: 400, height: 120,
          redFrom: 90, redTo: 100,
          yellowFrom:75, yellowTo: 90,
          minorTicks: 5
        };

        var chart = new google.visualization.Gauge(document.getElementById('chart_div'));

        chart.draw(data, options);
      }
    </script>"""

	free = ejecutar_subproceso("free -m")
	info_memoria = free.stdout.readlines()[1].decode()
	info_memoria = re.sub(" +", " ", info_memoria)

	campos_memoria = info_memoria.split(" ") 
	total_memoria = campos_memoria[1]
	uso_memoria = campos_memoria[2]

	porcentaje = float(float(uso_memoria) / float(total_memoria)) * 100.0
	porcentaje = round(porcentaje, 2)

	return inicio + str(porcentaje) + fin

# Generate the html page
def generate_html():
	html = f"""<html>
	<head>
		{styles}
		<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
		{generar_grafica_memoria()}	
	</head>
	<body>
		<div class="container">
			<div class="header">
				<h1>Docker dashboard</h1>
			</div>

			<div class="data">
				<h1>{get_time()}</h1>
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




