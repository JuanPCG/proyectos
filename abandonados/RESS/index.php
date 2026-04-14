<html>
	<head>
		<meta charset="UTF-8">
		<title>Intentando redirigirte...</title>
		<meta name="description" content="Pagina de redireccion">
	</head>
	<body>

<?php
$servername = "localhost";
$username = "usuario";
$password = "contra";
$DB = "recortes";
$conn = new mysqli($servername, $username, $password, $DB);

if ($conn->connect_error) {
	die("No se puede conectar a la base de datos: " . $conn->connect_error);
}

$urlfinal = explode("?", $_SERVER['REQUEST_URI'])[1];

if ($urlfinal === NULL) {
	echo "Url esta vacia";
	exit(1);
}

$cmdprueba = "SELECT id, URL_ORG FROM urls WHERE ID = $urlfinal";
$resultado = $conn->query($cmdprueba);
if ($resultado === FALSE) {
	die("El valor de resultado era FALSE, esta funcionando bien la base de datos?");
} else {
	if ($resultado->num_rows > 0) {
		$fila = $resultado->fetch_assoc();
		$url_obtenida = $fila['URL_ORG'];
		header("Location: " . htmlspecialchars($url_obtenida));
		$resultado->free();
	} else {
		echo "No se encontro el registro con ID = $urlfinal.";
	}
}
$conn->close();
?>
	</body>
</html>
