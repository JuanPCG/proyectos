#!/usr/bin/env python
# Un script que uso personalmente para alinear videos con audios
# ... Si, tiene que ver con Padre de Familia
import argparser as args
import sys, os, subprocess

args.ponerargumento(["-vi","--video-in","--audio"], 'video', None, False, True)
args.ponerargumento(["-ai","--audio-in","--audio"], 'audio', None, False, True)
args.ponerargumento(["-n", "--nombre"], 'nombre', None, False, False)
args.ponerargumento(["-e","--episodio"], 'ep', None, False, False)
args.ponerargumento(["-t","-s","--temporada"], 'temp', None, False, False)



try:
	args.buscarargumento()
	argumentos = args.devolver_args()
	a_300 = argumentos["audio"]
	v_1080 = argumentos['video']
except args.Err_ArgNoExiste as argumento:
	print(f"Has pasado un argumento que no existe\nEl argumento que ha fallado ha sido: {argumento}")
	sys.exit(-1)
except args.Err_FaltaArg as argumento:
	print(f"Requiere un valor: {argumento}")
	sys.exit(-2)
except args.Err_FaltaArg2 as faltas:
	print(f"Falta(n) argumento(s) requeridos:")
	print("Se requiere satisfacer al menos un elemento de cada lista")
	for grupo in faltas.args[0]:
		print(f"\t- Debes usar al menos uno de estos: {grupo}")
	sys.exit(-3)

nombre, temporada, episodio = "Test", 1, 1

if 'nombre' in argumentos:
	nombre = argumentos['nombre']
if 'temp' in argumentos:
	temporada = argumentos['temp']
if 'ep' in argumentos:
	episodio = argumentos['ep']


if not os.path.exists(nombre):
	os.makedirs(nombre)
if not os.path.exists(f"{nombre}/Temporada {temporada}"):
	os.makedirs(f"{nombre}/Temporada {temporada}")
final = f"{nombre}/Temporada {temporada}/Episodio {episodio}.mkv"


tiempo_inicio = "00:10:00" # Para la preview
offset = -1.16
tmp = "tmp.mkv"
repro = "vlc"

modo_carpeta = (os.path.isdir(v_1080) and os.path.isdir(a_300))



# ¿Has pensando alguna vez como seria la vida si no aceptaras las cosas tal y como son?
# En plan, si decides ir a la calle con ropa del otro genero? O si decides aprender a volar aviones y robas uno y vuelas?
# Pues deberias, es un buen planteamiento y nunca, NUNCA dejes que nada te detenga



def proc(v,a,e):
	global offset
	while True:
		cmd_base = ["ffmpeg", "-ss", tiempo_inicio, "-i", v, "-ss", tiempo_inicio, "-itsoffset", str(offset), "-i", a, "-t", "15", "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-y", tmp]
		cmd_fin =  ["ffmpeg", "-i", v, "-itsoffset", str(offset), "-i", a, "-map", "0:v:0", "-map", "1:a:0", "-c", "copy", "-y", final]
		print(f"\nProbando con offset de: {offset} segundos...")
		subprocess.run(cmd_base, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		subprocess.run([repro, tmp], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		opcion = input("¿Cómo ha ido? [s] OK, [f] Fino (+0.1s), [r] Retrasar (-0.1s), [manual] Escribe el número: ").lower() or "s"
		if opcion == 's':
			print(f"¡Perfecto! El offset final es: {offset}")
			print(f"Ahora se generara el archivo '{final}'...")
			subprocess.run(cmd_fin, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			break
		elif opcion == 'f':
			offset += 0.1
		elif opcion == 'r':
			offset -= 0.1
		else:
			try:
				offset = float(opcion)
			except ValueError:
				print("Introduce un numero o una opcion valida.")




if modo_carpeta:
	def natural_sort_key(path): # Copiado
		return [int(text) if text.isdigit() else text.lower()
			for text in re.split('([0-9]+)', str(path))]
	from pathlib import Path
	import re
	videos = Path(v_1080)
	audios = Path(a_300)
	videosF = sorted([f for f in videos.iterdir() if f.is_file()], key=natural_sort_key)
	audiosF = sorted([f for f in audios.iterdir() if f.is_file()], key=natural_sort_key)
	actual = 1
	for video, audio in zip(videosF, audiosF):
		final = f"{nombre}/Temporada {temporada}/Episodio {actual}.mkv"
		print(f"Video: {video.name}")
		print(f"Audio: {audio.name}")
		proc(f'{v_1080}/{video.name}',f'{a_300}/{audio.name}', actual)
		print("-" * 20)
		actual += 1

if (__name__ == "__main__" and not modo_carpeta) or not modo_carpeta: proc(v_1080,a_300,episodio)
