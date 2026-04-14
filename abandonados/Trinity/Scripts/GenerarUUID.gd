extends Node

var tabla : Dictionary = {}

func _ready():
	if FileAccess.file_exists("user://tablauuid.json"):
		tabla = JSON.parse_string(FileAccess.get_file_as_string("user://tablauuid.json"))
	else:
		var aTabla = FileAccess.open("user://tablauuid.json",FileAccess.WRITE)
		var ini = JSON.stringify({},"\t")
		aTabla.store_string(ini)

func check(archivo : String):
	var md5 = FileAccess.get_md5(archivo)
	if md5 in tabla:
		return tabla[md5]
	else: # Generamos un UUID (Y lo guardamos)
		var b = []
		for i in range(16):
			b.append(randi() % 256)
		b[6] = (b[6] & 0x0f) | 0x40
		b[8] = (b[8] & 0x3f) | 0x80
		var BFin = "%02x%02x%02x%02x-%02x%02x-%02x%02x-%02x%02x-%02x%02x%02x%02x%02x%02x" % [
			b[0], b[1], b[2], b[3],
			b[4], b[5],
			b[6], b[7],
			b[8], b[9],
			b[10], b[11], b[12], b[13], b[14], b[15]
		]
		tabla[md5] = BFin
		guardar_tabla()
		return BFin

func guardar_tabla():
	var aTabla = FileAccess.open("user://tablauuid.json",FileAccess.WRITE)
	var ini = JSON.stringify(tabla,"\t")
	aTabla.store_string(ini)
