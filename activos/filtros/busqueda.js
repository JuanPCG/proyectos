// Inicializamos el almacen
window.exfiltrado = [];
const VISTOS = new Set();

// CAMBIA ESTO DE AQUI ABAJO!!! PROBABLEMENTE (ESTADISTICAMENTE NO ESTAS USANDO LA CUENTA CON ID '1', PROBABLEMENTE ESTO ES '0'
// NO es un INT, es un INT, asi que POR FAVOR **NO** lo cambies
const cuenta = "1"; // n donde 'n' es tu numero de cuenta (Aunque creo que se puede sacar por URL)

exfiltrado.push({idcuenta:cuenta}) // Por si acaso hago un script que tambien lo descargue o algo yo que se

// SVG para carpetas
const RUTA_CARPETA = "M20,6h-8l-2-2H4C2.9,4,2.01,4.9,2.01,6L2,18c0,1.1,0.9,2,2,2h16c1.1,0,2-0.9,2-2V8C22,6.9,21.1,6,20,6z M15,9 c1.1,0,2,0.9,2,2c0,1.1-0.9,2-2,2s-2-0.9-2-2C13,9.9,13.9,9,15,9z M19,17h-8v-0.57c0-0.81,0.48-1.53,1.22-1.85 C13.07,14.21,14.01,14,15,14c0.99,0,1.93,0.21,2.78,0.58C18.52,14.9,19,15.62,19,16.43V17z";
// Tambien se puede hacer lo mismo para SITES


console.log("%cIniciando búsqueda filtrada por filas (TR)...", "color: green");

const observer = new MutationObserver(() => {
	// Solo capturamos elementos <tr> que tengan un data-id
	const filas = document.querySelectorAll('tr[data-id]');

	filas.forEach(fila => {
		const id = fila.getAttribute('data-id');

		if (id && !VISTOS.has(id)) {
			VISTOS.add(id);

			// Identificar si es carpeta mirando SOLO la primera celda (el icono)
			// TODO: Mirar si es WEB (x-google-sites) o 'Google Sites Compartido' dentro del <div> de accesibilidad
			const celdaIcono = fila.querySelector('td');
			let esCarpeta = false;
			if (celdaIcono) {
				esCarpeta = Array.from(celdaIcono.querySelectorAll('path')) .some(p => p.getAttribute('d') === RUTA_CARPETA);
			}

			const nombreINT = fila.innerText.split('\n')[0] || "SINNOMBRE";
				// Hacer parser
			window.exfiltrado.push({
				tiempo: new Date().toISOString(),
				nombre: nombreINT,
				id: id,
				tipo: esCarpeta ? "CARPETA" : "ARCHIVO",
				links: {
					vista: `https://drive.google.com/open?id=${id}`,
					// NO se puede poner el u/${cuenta} (CREO) en este

					// SI NO ES CARPETA NO SE PUEDE HACER NADA
					descarga: esCarpeta ? null : `https://drive.google.com/u/${cuenta}/uc?id=${id}&export=download`
				}
			});

			console.log(`PILLADO: [${esCarpeta ? 'CARPETA' : 'ARCHIVO'}]: ${nombreINT}`);
		}
    });
});


// IDEA PARA ESCARPETA:

// Enviar un request a https://takeout-pa-qw.clients6.google.com/v1/exports?key={LLAVE}
// PERO esto tiene que ser anteriormente pedido por un servicio
// (Investigar sobre esto)


// Vigilar
observer.observe(document.body, { childList: true, subtree: true });


// Funcion que limpia todo
function LIMPIAR() {
	VISTOS.clear() // ESTO hace que SI seguimos en la misma vista de página se vuelve a llenar inmediatamente, arreglar ESTO (Prioritario)
	exfiltrado = []
}

// LA DESCARGA EN SI
window.DESCARGARJSON = (nombre) => {
	if (window.exfiltrado.length === 0) {
		return console.error("No se ha visto nada aun.");
	}
	const dataStr = JSON.stringify(window.exfiltrado, null, 4);
	const blob = new Blob([dataStr], { type: "application/json" });
	const url = URL.createObjectURL(blob);
	const link = document.createElement("a");
	link.href = url;
	if (nombre == undefined) {
		link.download = `AUDITORIA_DRIVE_${new Date().getTime()}.json`;
	} else {
		link.download = `${nombre}.json`
	}
	link.click();
	console.log("Archivo JSON generado con éxito.");
};
