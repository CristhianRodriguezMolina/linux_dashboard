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

		#table_div2 {
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

def generate_task_and_time_data():
	p = ejecutar_subproceso("top -n 1")

	time = p.stdout.readline().decode().strip()
	time = re.sub(" +", " ", time)
	
	tasks = p.stdout.readline().decode().strip()
	tasks = re.sub(" +", " ", tasks)

	data_tasks = tasks.split(' ')
	data_time = time.split(' ')

	return f"Total tasks: {data_tasks[1]}, Running: {data_tasks[3]}, Sleeping: {data_tasks[5]} | {data_time[2]}"

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

        var table = new google.visualization.Table(document.getElementById('table_div2'));

        table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});
      }
    </script>
	"""

	return table

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

def generate_docker_images_table():
	
	start = """
	<script type="text/javascript">
        google.charts.load('current', { 'packages': ['table'] });
        google.charts.setOnLoadCallback(drawTable);

        function drawTable() {
            var data = new google.visualization.DataTable();
            data.addColumn('string', 'Repository');
            data.addColumn('string', 'Tag');
            data.addColumn('string', 'Image id');
			data.addColumn('string', 'Created');
			data.addColumn('string', 'Size');
            data.addRows([
                
	"""

	fin = """
            ]);

            var table = new google.visualization.Table(document.getElementById('table_div'));

            table.draw(data, { showRowNumber: true, width: '100%', height: '100%' });
        }
    </script>
	"""

	command = ejecutar_subproceso("sudo docker image ls")

	content = ""

	line = command.stdout.readline().decode()
	while True:
		line = command.stdout.readline().decode()
		line = re.sub(" +", " ", line)
		
		if not line or line.strip() == '':
			break

		data = "["	

		#['Mike', { v: 10000, f: '$10,000' }, true],
		info = line.rstrip().split(" ")

		for i in range(len(info)):

			if(i == len(info) - 1 or i <= 2):
				data += f"'{info[i]}', "
			elif(i == 3):
				column = " ".join(info[i: len(info) - 1])
				data += f"'{column}', "
		


		data = data[0:-2]
		data += "],"

		content += data + "\n"
	
	return start + content[0:-1] + fin

# Generate the html page
def generate_html():
	html = f"""<html>
	<head>
		{styles}
		<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
		{generar_grafica_memoria()}
		{generate_docker_images_table()}
		{generate_table_stats()}
	</head>
	<body>
		<div class="container">
			<div class="header">
				<h1>Docker dashboard</h1>
			</div>

			<div class="data">
				<h2>{generate_task_and_time_data()}</h2>
			</div>

			<div class="table-container">
				<div id="table_div"></div>
			</div>

			<div class="table-container">
				<div id="table_div2"></div>
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
# print(generate_task_data())