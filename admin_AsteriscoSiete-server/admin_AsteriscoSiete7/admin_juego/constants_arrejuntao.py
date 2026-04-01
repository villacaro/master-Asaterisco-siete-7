# -*- coding: utf-8 -*-
"""
constants_arrejuntao.py — Sistema Asterisco Siete (*7)
=======================================================
Tabla de 77 animalitos/figuras y constantes del producto EL ARREJUNTAO.
"""

# ─────────────────────────────────────────────────────────────────────────────
# 1. TABLA DE 77 ANIMALITOS — EL ARREJUNTAO
#    Clave: número de figura (str) → nombre del animal
#    Figuras especiales: "00" (Ballena) y "0" (Delfín)
# ─────────────────────────────────────────────────────────────────────────────

ANIMALITOS_ARREJUNTAO = {
    "00": "Ballena",
    "0":  "Delfín",
    "1":  "Carnero",
    "2":  "Toro",
    "3":  "Ciempiés",
    "4":  "Alacrán",
    "5":  "León",
    "6":  "Rana",
    "7":  "Perico",
    "8":  "Ratón",
    "9":  "Águila",
    "10": "Tigre",
    "11": "Gato",
    "12": "Caballo",
    "13": "Mono",
    "14": "Paloma",
    "15": "Zorro",
    "16": "Oso",
    "17": "Pavo",
    "18": "Burro",
    "19": "Loro",
    "20": "Cochino",
    "21": "Gallo",
    "22": "Camello",
    "23": "Cebra",
    "24": "Iguana",
    "25": "Gallina",
    "26": "Vaca",
    "27": "Perro",
    "28": "Zamuro",
    "29": "Elefante",
    "30": "Caiman",
    "31": "Lapa",
    "32": "Ardilla",
    "33": "Pescado",
    "34": "Venado",
    "35": "Jirafa",
    "36": "Conejo",
    "37": "Mariposa",
    "38": "Serpiente",
    "39": "Cocodrilo",
    "40": "Pelícano",
    "41": "Murciélago",
    "42": "Pato",
    "43": "Pantera",
    "44": "Dinosaurio",
    "45": "Tortuga",
    "46": "Lobo",
    "47": "Guacamaya",
    "48": "Flamenco",
    "49": "Langosta",
    "50": "Pulpo",
    "51": "Tiburón",
    "52": "Cangrejo",
    "53": "Garza",
    "54": "Lechuza",
    "55": "Puma",
    "56": "Manatí",
    "57": "Cóndor",
    "58": "Avestruz",
    "59": "Pingüino",
    "60": "Rinoceronte",
    "61": "Hipopótamo",
    "62": "Gorila",
    "63": "Mapache",
    "64": "Armadillo",
    "65": "Nutria",
    "66": "Colibrí",
    "67": "Halcón",
    "68": "Búfalo",
    "69": "Llama",
    "70": "Canguro",
    "71": "Koala",
    "72": "Panda",
    "73": "Hipopótamo",   # figura 73 de la tabla original
    "74": "Turpial",
    "75": "Bestia Ganadora",
}

# Rango numérico válido de figuras (como enteros)
ANIMALITO_MIN = 0
ANIMALITO_MAX = 75

# Lista ordenada de figuras para validación rápida
ANIMALITO_FIGURAS_VALIDAS = set(ANIMALITOS_ARREJUNTAO.keys())

# ─────────────────────────────────────────────────────────────────────────────
# 2. SIGNOS ZODIACALES — Para jugadas con signo
# ─────────────────────────────────────────────────────────────────────────────

SIGNOS_ZODIACALES = [
    'ARIES', 'TAURO', 'GEMINIS', 'CANCER',
    'LEO', 'VIRGO', 'LIBRA', 'ESCORPIO',
    'SAGITARIO', 'CAPRICORNIO', 'ACUARIO', 'PISCIS',
]

# ─────────────────────────────────────────────────────────────────────────────
# 3. TIPOS DE JUGADA — EL ARREJUNTAO
#    Cada entrada define:
#      código        → identificador interno del tipo
#      nombre        → nombre visible en UI
#      digitos       → cantidad de dígitos del número apostado
#      factor_pago   → multiplicador base (ejemplo: 400x para Triple)
#      usa_signo     → si requiere signo zodiacal
#      es_terminal   → si la validación es sobre los últimos N dígitos
# ─────────────────────────────────────────────────────────────────────────────

TIPOS_JUGADA_ARREJUNTAO = {
    # ── Triple ──────────────────────────────────────────────────────────────
    'TRIPLE_A': {
        'nombre':      'Triple A',
        'digitos':     3,
        'factor_pago': 400,
        'usa_signo':   False,
        'es_terminal': False,
        'resultado_key': 'triple_a',
    },
    'TRIPLE_B': {
        'nombre':      'Triple B',
        'digitos':     3,
        'factor_pago': 400,
        'usa_signo':   False,
        'es_terminal': False,
        'resultado_key': 'triple_b',
    },

    # ── Terminal ─────────────────────────────────────────────────────────────
    'TERMINAL_A': {
        'nombre':      'Terminal A',
        'digitos':     2,
        'factor_pago': 40,
        'usa_signo':   False,
        'es_terminal': True,    # compara con últimos 2 dígitos de triple_a
        'resultado_key': 'triple_a',
    },
    'TERMINAL_B': {
        'nombre':      'Terminal B',
        'digitos':     2,
        'factor_pago': 40,
        'usa_signo':   False,
        'es_terminal': True,
        'resultado_key': 'triple_b',
    },

    # ── Triple con Signo ──────────────────────────────────────────────────────
    'TRIPLE_SIGNO_A': {
        'nombre':      'Triple Signo A',
        'digitos':     3,
        'factor_pago': 100,
        'usa_signo':   True,
        'es_terminal': False,
        'resultado_key': 'triple_a',
    },
    'TRIPLE_SIGNO_B': {
        'nombre':      'Triple Signo B',
        'digitos':     3,
        'factor_pago': 100,
        'usa_signo':   True,
        'es_terminal': False,
        'resultado_key': 'triple_b',
    },

    # ── Terminal con Signo ────────────────────────────────────────────────────
    'TERMINAL_SIGNO_A': {
        'nombre':      'Terminal Signo A',
        'digitos':     2,
        'factor_pago': 25,
        'usa_signo':   True,
        'es_terminal': True,
        'resultado_key': 'triple_a',
    },
    'TERMINAL_SIGNO_B': {
        'nombre':      'Terminal Signo B',
        'digitos':     2,
        'factor_pago': 25,
        'usa_signo':   True,
        'es_terminal': True,
        'resultado_key': 'triple_b',
    },

    # ── El Arrimao (4 dígitos) ────────────────────────────────────────────────
    'ARRIMAO': {
        'nombre':      'El Arrimao',
        'digitos':     4,
        'factor_pago': 3000,
        'usa_signo':   False,
        'es_terminal': False,
        'resultado_key': 'cuatro_digitos',
    },

    # ── El Pegadito / Pagadito (5 dígitos) ───────────────────────────────────
    'PAGADITO': {
        'nombre':      'El Pegadito',
        'digitos':     5,
        'factor_pago': 60000,
        'usa_signo':   False,
        'es_terminal': False,
        'resultado_key': 'cinco_digitos',
    },

    # ── Animalitos / Figuras ──────────────────────────────────────────────────
    'ANIMALITO': {
        'nombre':      'Animalito',
        'digitos':     2,       # se acepta '0', '00' o '01'..'75'
        'factor_pago': 8,
        'usa_signo':   False,
        'es_terminal': False,
        'resultado_key': 'animalito',
    },
}

# Conjunto de tipos de jugada válidos para validación rápida
TIPOS_VALIDOS = set(TIPOS_JUGADA_ARREJUNTAO.keys())


# ─────────────────────────────────────────────────────────────────────────────
# 4. CLAVES DE RESULTADO ESPERADAS EN UN SORTEO COMPLETO
#    Diccionario de ejemplo para la función liquidar_arrejuntao()
# ─────────────────────────────────────────────────────────────────────────────

RESULTADO_ARREJUNTAO_EJEMPLO = {
    'triple_a':      '123',   # Triple A  (3 dígitos)
    'triple_b':      '456',   # Triple B  (3 dígitos)
    'signo':         'ARIES', # Signo zodiacal
    'cuatro_digitos':'1234',  # El Arrimao (4 dígitos)
    'cinco_digitos': '12345', # El Pegadito (5 dígitos)
    'animalito':     '37',    # Figura ganadora (0-75 o '00')
}


def get_nombre_animalito(figura):
    """Retorna el nombre del animal dado su número de figura (str o int)."""
    return ANIMALITOS_ARREJUNTAO.get(str(figura), 'Figura desconocida')


def get_factor_pago(tipo_jugada):
    """Retorna el factor de pago base para un tipo de jugada."""
    config = TIPOS_JUGADA_ARREJUNTAO.get(tipo_jugada)
    return config['factor_pago'] if config else 0


def es_tipo_valido(tipo_jugada):
    """Verifica si el string es un tipo de jugada del Arrejuntao."""
    return tipo_jugada in TIPOS_VALIDOS


def es_figura_valida(figura):
    """Verifica si la figura está dentro del rango de animalitos."""
    return str(figura) in ANIMALITO_FIGURAS_VALIDAS
