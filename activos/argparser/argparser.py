import sys # O confiamos que el script padre ya lo haya importado

class Err_NoVar(Exception):
	# Esta exception es devuelta si no existe la variable destino
	pass

class Err_ArgNoExiste(Exception):
	# Esta exception es devuelta si no existe un argumento
	pass

class Err_FaltaArg(Exception): # WHOOPS
	pass

class Err_FaltaArg2(Exception): # => array de lo que falta
	pass




debug = False # MUY VERBOSE


final = {}
argumentos = {} # Llenarlo abajo
sk_pos = []
args_requeridos = []



def ponerargumento(arg, variable, tipo, unico = False, requerido = False):
	for argum in arg:
		argumentos[argum] = { 'var':variable, 'tipo':tipo }
		if unico:
			argumentos[argum]["unico"] = True
		else:
			argumentos[argum]["unico"] = False

	if requerido:
		args_requeridos.append(arg)

	if debug: print(f"\n + {arg} =?> {variable} | tipo ? {tipo or None} | bool ? {unico} | requerido ? {requerido}\n")


def buscarargumento():
	contador = 0
	for arg in sys.argv:
		if debug: print(f"ARGUMENTO {contador}: ", end="")
		if not contador in sk_pos:
			if not contador == 0:
				try:
					if debug: print(arg)
					lineaDEBUG = f"{arg}: {argumentos[arg]}; posicion {contador}"
					if not argumentos[arg]["unico"]:
						arg2var(argumentos[arg]["var"], sys.argv[contador+1])
						lineaDEBUG += f"; siguiente valor: {sys.argv[contador+1]}"
						sk_pos.append(contador+1)
					else:
						arg2var(argumentos[arg]["var"], True)
						lineaDEBUG += f"; argumento unico"
					if debug: print(lineaDEBUG)
					buscar_en_vistos(arg)
				except IndexError:
					raise Err_FaltaArg(arg) # from None # PON ESTO SI QUIERES MAS INFO
				except Exception as e:
					if debug: print(e) # MAS INFO
					raise Err_ArgNoExiste(arg)

			else:
				if debug: print(f"{arg} (0)")
		else:
			if debug: print(f"[Saltando, tomado como valor para el argumento {contador-1}]")
		contador+=1

def arg2var(variable, valor, forzartipo = None):
	if debug: print(f"{variable}=>{valor} | {forzartipo}")
	final[variable] = valor

def devolver_args():
	if len(args_requeridos) == 0:
		if debug: print("Todos los argumentos requeridos necesarios")
		return final
	else:
		if debug: print(f"FALTAN ARGUMENTOS REQUERIDOS: {args_requeridos}")
		raise Err_FaltaArg2(args_requeridos) # Devuelve un array
		return {}

def buscar_en_vistos(arg):
	for arr in args_requeridos:
		if debug: print(f"Empezando busqueda array {arr}")
		for argsub in arr:
			if debug: print(f"{argsub} ?= {arg}")
			if arg == argsub:
				if debug: print(f"Sat. Dep. Arr. {arr}")
				args_requeridos.remove(arr)
