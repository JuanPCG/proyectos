extends Node

var tabla : Dictionary = {}

func _ready():
	if FileAccess.file_exists("user://ID3.json"):
		tabla = JSON.parse_string(FileAccess.get_file_as_string("user://ID3.json"))
	else:
		var aTabla = FileAccess.open("user://ID3.json",FileAccess.WRITE)
		var ini = JSON.stringify({},"\t")
		aTabla.store_string(ini)

func datos(uuid:String):
	if uuid in tabla:
		return tabla[uuid]
	else:
		false

func guardar_tabla():
	var aTabla = FileAccess.open("user://ID3.json",FileAccess.WRITE)
	var ini = JSON.stringify(tabla,"\t")
	aTabla.store_string(ini)

func PonerDatos(uuid:String,Datos:Dictionary):
	tabla[uuid] = Datos
	guardar_tabla()
