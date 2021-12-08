<html>
	<head>
		<style>
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
    </style>
		<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
		<!-- <script>setTimeout(function () {window.location.reload(1);}, 3000);</script> -->
		 <script type="text/javascript">
      google.charts.load('current', {'packages':['gauge']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {

        var data = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Memory', 26.14]
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
                
	['test', 'latest', '820f9c5a108f', '17 hours ago', '469MB'],
['<none>', '<none>', '68e7bb411506', '17 hours ago', '469MB'],
['winterhat/dashboard_proyecto_final', 'v1', '9a65cb03bc84', '17 hours ago', '54.9MB'],
['<none>', '<none>', 'cc3871e4c89c', '4 days ago', '54.9MB'],
['php', '7.4-apache', 'e66e0a2a90b2', '6 days ago', '469MB'],
['php', 'latest', '9dc9a6284b9b', '6 days ago', '484MB'],
['graph_stats', 'latest', '59e715a9f1ca', '7 days ago', '54.9MB'],
['httpd', 'alpine', 'da799a8c8856', '8 days ago', '54.9MB'],
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
	
	]);

        var table = new google.visualization.Table(document.getElementById('table_div2'));

        table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});
      }
    </script>
	
	</head>
	<body>
		<div class="container">
			<form action="" method="post">
				<input type="text" name="command-input" />
				<button type="submit">Ejecutar</button>
			</form>
			<div id="command-log" style="background-color: #808080; color: white">
				<?php
					if (isset($_POST['command-input'])) {                    
						$salida = shell_exec($_POST['command-input']);
						echo "<pre>$salida</pre>";
					}
				?>
			</div>

			<br/>

			<div class="header">
				<h1>Docker dashboard</h1>
			</div>

			<div class="data">
				<h2>Total tasks: 430, Running: 1, Sleeping: 429 | 13:50:23</h2>
			</div>

			<h1>List de imagenes</h1>
			<div class="table-container">
				<div id="table_div"></div>
			</div>

			<h1>Estadísticas de los contenedores es ejecución</h1>
			<div class="table-container">
				<div id="table_div2"></div>
			</div>

			<h1>Uso de memoria ram</h1>
			<div id="chart_div" style="width: 400px; height: 120px;"></div>
    	</div>
	</body>
	</html>