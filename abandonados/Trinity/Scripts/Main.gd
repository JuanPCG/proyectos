extends Control

func _init():
	# Esto esta aqui para que llame cuando pueda a la funcion de conf_ventana
	# Que si no, puede que 'arranque' demasiado rapido y la ventana no este cargada.
	call_deferred("conf_ventana")
func conf_ventana():
	get_window().connect("files_dropped",proc_archivos)

func Saltar_Cancion():
	$Audio.stop()
	emit_signal("Fin_Cancion")

func proc_archivos(Archivos:Array):
	global.Cola.clear()
	for i in Archivos:
		# Solo abrir el puntero del archivo
		var f = FileAccess.open(i, FileAccess.READ)
		if f:
		# ID3 siempre empieza con "ID3" (bytes 73, 68, 51)
			var header = f.get_buffer(3).get_string_from_ascii()
			if header == "ID3":
				global.Cola.append(i)
		f.close()



		#var DatosCancion : PackedByteArray = FileAccess.get_file_as_bytes(i)
		## Igual puedo asignar los datos directamente la propiedad 'data' en un AudioStreamMP3.
		## Asi evitaria cargar la cancion dos veces.
		#var HeaderID3 : PackedByteArray = [73,68,51,4]
		## El 'header' de una cancion con ID3.
		#if DatosCancion.slice(0,4) == HeaderID3:
		## Del n1 al n4, si es un header ID3, (intentamos) cargar.
			#global.Cola.append(i)

	act_cola()


func PlayPause():
	$Audio.Repr()


func act_cola():
	$Lista_Repr.clear()
	for i : String in global.Cola:
		var Portada : Texture2D = load("res://icon.svg")
		# Si tenemos la portada, la ponemos, si no, pasamos
		# Igual podemos hacer que se lea el primer medio megabyte de informacion
		# (O lo que pese la imagen??) y guardarla en algun tipo de base de datos??
		$Lista_Repr.add_item(i.get_basename().get_file(),imagen.TieneIMG(UUID.check(i)))
