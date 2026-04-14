extends Node
func _init():
	# Borramos la lista y salimos
	global.Cola.clear()
	global.PosCola=0
	queue_free()
