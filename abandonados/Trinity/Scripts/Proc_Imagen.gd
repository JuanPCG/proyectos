extends Node
var PorDefecto = preload("res://icon.svg")
func TieneIMG(uuid:String) -> Texture2D:
	var dat = ID3Utils.datos(uuid)
	if typeof(dat) == TYPE_DICTIONARY:
		if dat.has("PORTADA"):
			var img = Image.new()
			var error = img.load_jpg_from_buffer(FileAccess.get_file_as_bytes(dat["PORTADA"])) # O load_png_from_buffer
			var textura : Texture2D = ImageTexture.create_from_image(img)
			if error == OK:
				return textura
			else:
				return PorDefecto
		else:
			return PorDefecto
	return PorDefecto
