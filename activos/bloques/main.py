#!/usr/bin/env python3
import argparser as args
import os, sys

args.debug = True

args.ponerargumento(["-n","--nombre"], 'nombre', None, False, True)
args.ponerargumento(["-a","--album"], 'album', None, False, True)
args.ponerargumento(["-g","--grupo","--artista",], 'artista', None, False, True)
args.ponerargumento(["--ancho"], 'ancho', None, False)
args.ponerargumento(["-l","--largo"], 'largo', None, False)
args.ponerargumento(["-h","--help","--ayuda"], 'ayuda', None, True)
args.ponerargumento(["-o", "-s","--salida","--out"], 'salida', None, False)
args.ponerargumento(["-f","--fps"], 'fps', None, False)
args.ponerargumento(["-i","--imagen"], 'imagen', None, False)



nombre = ""
artista = ""
ancho = 800
largo = 120
salida = "OUT.webm"
fps = 30
imagen = ""
album = ""

def mostrar_ayuda():
	print(f"Uso: {sys.argv[0]} \n\t-n 'Nombre de la Cancion' \n\t-g 'Grupo que la Canta'\n\t-a 'Album'\n\t[--ancho 800] \n\t[-l 120] \n\t[-h]\n\t[-s 'archivo de video.webm']\n\t[--fps 30]\n\t[-i (imagen.webp)]")
	print(f"Ejemplo: {sys.argv[0]} -n 'Every Breath You Take' -g 'The Police' -a 600 -l 150 -f 27 -i Synchronicity.jpg -s everybreathyoutake.webm")

try:
	args.buscarargumento()
	argumentos = args.devolver_args()
	if "ayuda" in argumentos:
		mostrar_ayuda()
		sys.exit(0)
	nombre = argumentos["nombre"]
	artista = argumentos['artista']
	album = argumentos['album']
	if 'ancho' in argumentos:
		ancho = int(argumentos['ancho']) or 800
	if 'largo' in argumentos:
		largo = int(argumentos['largo']) or 120
	if 'fps' in argumentos:
		fps = int(argumentos['fps']) or 30
	if 'salida' in argumentos:
		salida = argumentos['salida'] or 'OUT.webm'
	if "imagen" in argumentos:
		imagen = argumentos['imagen']
	else:
		imagen = None
except args.Err_ArgNoExiste as argumento:
	print(f"Has pasado un argumento que no existe\nEl argumento que ha fallado ha sido: {argumento}")
	sys.exit(-1)
except args.Err_FaltaArg as argumento:
	print(f"Requiere un valor: {argumento}")
	sys.exit(-2)
except args.Err_FaltaArg2 as faltas:
	for i in ['-h','--ayuda','--help']:
		if i in sys.argv:
			mostrar_ayuda()
			sys.exit(0)

	print(f"Falta(n) argumento(s) requeridos:")
	print("Se requiere satisfacer al menos un elemento de cada lista")
	for grupo in faltas.args[0]:
		print(f"\t- Debes usar al menos uno de estos: {grupo}")
	sys.exit(-3)

print(f"Generando titulo para {nombre} de {artista}")


from moviepy import ColorClip, TextClip, CompositeVideoClip, ImageClip # Importar despues, para que no cargue todo al principio


def create_song_card(color=(50, 150, 255), duration=5.0):
	width, height = 800, 120
	target_x = 50
	start_x = -ancho
	speed = 1500
	slide_duration = (target_x - start_x) / speed


	padding = 10
	img_size = largo - (padding * 2)


	block = ColorClip(size=(ancho, largo), color=color).with_duration(duration).with_opacity(0.8)


	if imagen == None:
		print("No añadiendo una imagen...")
	else:
		try:
			album_art = (ImageClip(imagen)
				.with_duration(duration)
				.resized(height=img_size)
				.with_position((padding, "center")))
		except Exception as e:
			print(f"Error cargando imagen: {e}")
			album_art = ColorClip(size=(img_size, img_size), color=(100,100,100)).with_duration(duration)




	full_text = f"{artista}\n{album}\n{nombre}" # Usar salto de línea queda mejor con imagen
	text = TextClip(
		text=full_text,
		font_size=30,
		color='white',
		text_align="left"
	).with_duration(duration).with_position((img_size + padding * 2, "center"))

	array_card = [block]
	if imagen != None:
		array_card.append(album_art)
	array_card.append(text)


	card = CompositeVideoClip(array_card, size=(ancho, largo)).with_duration(duration)

	def anim_pos(t):
		if t < slide_duration:
			current_x = start_x + (speed * t)
			return (min(current_x, target_x), "center")
		elif t > (duration - slide_duration):
			time_spent_sliding_out = t - (duration - slide_duration)
			current_x = target_x - (speed * time_spent_sliding_out)
			return (current_x, "center")
		else:
			return (target_x, "center")

	animated_card = card.with_position(anim_pos)
	final_canvas = CompositeVideoClip([animated_card], size=(1920, 1080))
	return final_canvas




VIDEO = create_song_card()

VIDEO.write_videofile(
	salida,
	fps=globals()["fps"],
	codec="libvpx-vp9",
	ffmpeg_params=["-pix_fmt", "yuva420p"]
)

