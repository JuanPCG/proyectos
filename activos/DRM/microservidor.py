import socket, GEN_DRM

IP, PUERTO = '127.0.0.1', 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((IP, PUERTO))
	s.listen(5)
	print(f"Esperando conexiones en... {IP}:{PUERTO} (SOLO HTTP)")

	while True:
		conn , cliente = s.accept()
		with conn:
			DATOS = conn.recv(4096).decode('utf-8', errors='ignore')
			if not DATOS:
				continue
			PRIMERA_LINEA = DATOS.split('\n')[0]
			RUTA = PRIMERA_LINEA.split(' ')[1] if len(PRIMERA_LINEA.split(' ')) > 1 else "/"
			if RUTA == "/licencia":
				CLAVE = GEN_DRM.clave()
				CUERPO = f"{CLAVE}\n"
				ESTADO = "200 OK"
				CONTENIDO = "application/json"
			else:
				CUERPO = "Servidor licencias dummy, por favor, envia GET o POST a /licencia\n"
				ESTADO = "418 I'm a teapot"
				CONTENIDO = "text/plain"

			print(f"IP: {cliente[0]}\nURL: {RUTA}\n{f'CLAVES: {CLAVE}' if 'CLAVE' in vars() else 'Sin claves'} ")



			response = (
				f"HTTP/1.1 {ESTADO}\r\n"
				f"Content-Type: {CONTENIDO}\r\n"
				"Access-Control-Allow-Origin: *\r\n"
				f"Content-Length: {len(CUERPO)}\r\n"
				"Connection: close\r\n"
				"\r\n"
				f"{CUERPO}"
			)

			conn.sendall(response.encode('utf-8'))
