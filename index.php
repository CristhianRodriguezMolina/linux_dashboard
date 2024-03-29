<html>
	<head>
		<style>
			@import url('https://fonts.googleapis.com/css2?family=Inconsolata:wght@500&display=swap');
		</style> 

		<style>
		body {
			margin: 0;
		}

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

		h1, h2, p {
			font-family: 'Inconsolata', monospace;
		}

		

		.form-command {
			width: 100%;
			display: flex;
			align-items: center;
			justify-content: center;
			height: auto;
			
		}

		.form-cammand form {
			width: 100%;
			height: auto;
		}

		.form-command button {
			width: 7em;
			height: auto;
		}

		.form-command input {
			width: 52.5em;	
			height: auto;
		}

		#command-log {
			padding: 0.5em;
			background-color: #01048a;
			color: white;
		}

		#command-log pre{
			margin: 0;
			padding: 0;
			font-family: 'Inconsolata', monospace;
		}

    </style>
		<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
		<!-- <script>setTimeout(function () {window.location.reload(1);}, 3000);</script> -->
		 <script type="text/javascript">
      google.charts.load('current', {'packages':['gauge']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {

        var data = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Memory', 20.39]
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
    </script>
		
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
                
	['dashboard-proyecto-final', 'latest', '37884f4780e2', '5 minutes ago', '469MB'],
['winterhat/dashboard-proyecto-final', 'latest', '37884f4780e2', '5 minutes ago', '469MB'],
['php', '7.4-apache', 'e66e0a2a90b2', '6 days ago', '469MB'],
            ]);

            var table = new google.visualization.Table(document.getElementById('table_div'));

            table.draw(data, { showRowNumber: true, width: '100%', height: '100%' });
        }
    </script>
	
		
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
	["df95c3a59e95", "practical_villani", "0.00%", "15.05MiB", "0.06%"],
	]);

        var table = new google.visualization.Table(document.getElementById('table_div2'));

        table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});
      }
    </script>
	
	</head>
	<body>
		<div class="container">
			<div class="header">
				<h1>Docker dashboard</h1>
			</div>

			<div class="data">
				<h2>Total tasks: 412, Running: 1, Sleeping: 411 | 20:40:03</h2>
			</div>

			<h1>Consola virtual</h1>
			<div class="form-command">
				<form action="" method="post">
					<input type="text" name="command-input" />
					<button type="submit">Ejecutar</button>
				</form>
			</div>
			
			<div id="command-log">
				<?php
					if (isset($_POST['command-input'])) {                    
						$salida = shell_exec($_POST['command-input']);
						echo "<pre>Virtual terminal powered by Docker dashboard
==================================================================================================
==================================================================================================
$salida</pre>";
					}
				?>
			</div>

			<h1>Lista de imágenes</h1>
			<div class="table-container">
				<div id="table_div"></div>
			</div>

			<h1>Estadísticas de los contenedores en ejecución</h1>
			<div class="table-container">
				<div id="table_div2"></div>
			</div>

			<h1>Uso de memoria ram</h1>
			<div id="chart_div" style="width: 400px; height: 120px;"></div>			
    	</div>
	</body>
	</html>