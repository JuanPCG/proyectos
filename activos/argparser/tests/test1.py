import sys, argparser as args


args.ponerargumento(["-r","--recursivo"], 'recursivo', None, True)
args.ponerargumento(["-v","--valor"], 'valor', None, False)

recursivo = False
valor = 0


try:
	args.buscarargumento()
	argumentos = args.devolver_args()
	if "recursivo" in argumentos:
		recursivo = argumentos["recursivo"]
	if 'valor' in argumentos:
		valor = argumentos['valor']
	print(f"Modo recursivo (-r o --recursivo): {recursivo}")
	print(f"Valor de ejemplo (-v (valor) o --valor (valor)): {valor}")
except args.Err_ArgNoExiste as argumento:
	print(f"Has pasado un argumento que no existe\nEl argumento que ha fallado ha sido: {argumento}")
except args.Err_FaltaArg as argumento:
	print(f"Requiere un argumento: {argumento}")
