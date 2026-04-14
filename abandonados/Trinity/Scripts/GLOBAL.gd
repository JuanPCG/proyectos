extends Node
@export var Cola : Array = []
@export var PosCola : int = 0

enum Estados {
	ESTADO_INICIAL = -1,
	reproduciendo = 0,
	pausado = 1,
	final = 2
}



@export var Estado : Estados = Estados.ESTADO_INICIAL

signal Fin_Cancion
