extends AudioStreamPlayer

func _init():
	if ! DirAccess.dir_exists_absolute("user://albums"):
		DirAccess.make_dir_absolute("user://albums")

func FIN_NATURAL():
	global.emit_signal("Fin_Cancion") # Llama al global para que emita final de la cancion


func iniciar_c(c:int):
	var DatosID = UUID.check(global.Cola[c])
	global.PosCola = c
	global.Estado = global.Estados.reproduciendo
	var Audio_Cargado : AudioStream = AudioStreamMP3.new()
	Audio_Cargado.data = FileAccess.get_file_as_bytes(global.Cola[c])
	stream = Audio_Cargado
	if not ID3Utils.datos(DatosID):
		ID3Utils.PonerDatos(DatosID,generar_id3(global.Cola[c]))
	play()
	PonerDatos(DatosID)
	$"/root/Main/Img".texture = imagen.TieneIMG(UUID.check(global.Cola[c]))

func Repr():
	if ! global.Cola.is_empty():
		match global.Estado:
			-1:
				iniciar_c(0)
			0:
				stream_paused = true
				global.Estado = global.Estados.pausado
			1:
				stream_paused = false
				global.Estado = global.Estados.reproduciendo


func generar_id3(ruta) -> Dictionary:
	var f = FileAccess.open(ruta, FileAccess.READ)
	if not f: # Si no hay archivo
		return {}
	if f.get_buffer(3).get_string_from_ascii() != "ID3": # Si no es ID3
		return {} # Esto no deberia pasar, si pasa, estamos JODIDISIMOS

	var version = f.get_8()
	f.seek(6) # Saltamos flags
	
	# Tamaño total (Syncsafe 7-bits) EXCEPTO si es V4 (¿Quien leches usa V4?)
	var b = f.get_buffer(4)
	var tamano_total = (b[0] << 21) | (b[1] << 14) | (b[2] << 7) | b[3]
	
	var resultados = {
		"TIT2": "Desconocido",
		"TPE1": "Artista Desconocido",
		"TALB": "Album Desconocido",
		"TDRC": "",
		"TCON": ""
	}

	while f.get_position() < tamano_total:
		var pos_actual = f.get_position()
		var id_buffer = f.get_buffer(4)
		
		# ¿Han acabado los tags?
		if id_buffer.size() < 4 or id_buffer[0] == 0:
			break

		var frame_id = id_buffer.get_string_from_ascii()
		var s = f.get_buffer(4)
		var frame_size : int
		
		if version == 4: # ID3v2.4 usa syncsafe
			frame_size = (s[0] << 21) | (s[1] << 14) | (s[2] << 7) | s[3]
		else: # ID3v2.3 usa 8-bits normales pero en Big Endian
			frame_size = (s[0] << 24) | (s[1] << 16) | (s[2] << 8) | s[3]

		f.get_16() # Pasamos los flags (Que son 2 bytes (16 bits))

		if frame_id in resultados:
			if frame_size > 0:
				var encoding = f.get_8()
				var contenido = f.get_buffer(frame_size - 1)
				if encoding == 0:
					resultados[frame_id] = contenido.get_string_from_ascii().strip_edges()
				else:
					resultados[frame_id] = contenido.get_string_from_utf16().strip_edges()
		elif frame_id == "APIC":
			var pos_antes = f.get_position()
			var encoding = f.get_8()

			# MIME
			var mime_type = ""
			while true:
				var bp = f.get_8()
				if bp == 0: 
					break
				mime_type += char(bp)

			# El tipo de imagen, que segun el estandar de ID3, tiene
			# varios tipos, como "poster", "posterior", etc... Aun no hacemos nada
			# pero en el futuro, quien sabe.
			var tipoimg = f.get_8()

			# JUSTO despues de la imagen, tenemos un campo de "descripcion"
			# Lo que vendria a ser 'alt text'. Para quien no sea capaz
			# De ver la imagen, por el motivo que sea.
			var Desc : String = ""
			while true:
				var bp = f.get_8()
				Desc+char(bp)
				if bp == 0:
					break # Como aun no hago nada con la descripcion, pasando de largo.

			# AHORA si que vienen los datos.
			var bytesleidos = f.get_position() - pos_antes
			var tamimagen = frame_size - bytesleidos
			var datos_imagen = f.get_buffer(tamimagen)


			var path_portada = "user://albums/" + UUID.check(ruta)
			var file = FileAccess.open(path_portada, FileAccess.WRITE)
			file.store_buffer(datos_imagen)


			# Guardamos la ruta, aunque no deberia hacer falta
			# Quiero decir, tenemos una carpeta comun, y un generador
			# De UUID, simplemente tomamos user + albums + uuid
			resultados["PORTADA"] = path_portada
		else:
			f.seek(f.get_position() + frame_size)
		if f.get_position() == pos_actual:
			break

	f.close()
	return resultados

func PonerDatos(datos):
	var DAT : Dictionary = ID3Utils.datos(datos)
	get_node("/root/Main/Infor").text = str( # Esto se podria hacer 'mas bonito' creo.
		"Nombre : ", DAT["TIT2"],
		"\nAlbum : ", DAT["TALB"],
		"\nGenero : ", DAT["TCON"],
		"\nArtista : ", DAT["TPE1"],
		"\nAño : ", DAT["TDRC"],
	)
