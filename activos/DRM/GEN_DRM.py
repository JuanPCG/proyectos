import secrets
import base64

def clave():
	raw_kid = secrets.token_bytes(16)
	raw_key = secrets.token_bytes(16)
	def b64_url(b):
		return base64.urlsafe_b64encode(b).decode('utf-8').rstrip('=')
	# Tal y como se hace de verdad
	return {
		"kid_hex": raw_kid.hex(),
		"key_hex": raw_key.hex(),
		"jwk": {
			"kty": "oct",
			"k": b64_url(raw_key),
			"kid": b64_url(raw_kid)
		}
	}
	# Pues eso, llama a esta cosa para que te de un keypair 'valido'.
