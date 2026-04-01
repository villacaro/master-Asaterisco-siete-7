#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
import_venezuela_geo.py
Importa estados, municipios y parroquias de Venezuela.
Uso: python manage.py shell < scripts/import_venezuela_geo.py
  o: python scripts/import_venezuela_geo.py (con DJANGO_SETTINGS_MODULE configurado)
"""
import os, sys, django

# ── Setup Django ─────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_asterisco7.settings_local')
django.setup()

from admin_profiles.models import Paises, Estados, Municipios, Parroquias

# ── Datos Venezuela ───────────────────────────────────────────
VENEZUELA = [
    {"iso_31662":"VE-X","estado":"Amazonas","capital":"Puerto Ayacucho","id_estado":1,"municipios":[{"municipio":"Alto Orinoco","capital":"La Esmeralda","parroquias":["Alto Orinoco La Esmeralda","Huachamacare Acanaña","Marawaka Toky Shamanaña","Mavaka Mavaka","Sierra Parima Parimabé"]},{"municipio":"Atabapo","capital":"San Fernando de Atabapo","parroquias":["Ucata Laja Lisa","Yapacana Macuruco","Caname Guarinuma"]},{"municipio":"Atures","capital":"Puerto Ayacucho","parroquias":["Fernando Girón Tovar","Luis Alberto Gómez","Pahueña Limón de Parhueña","Platanillal Platanillal"]},{"municipio":"Autana","capital":"Isla Ratón","parroquias":["Samariapo Samariapo","Sipapo Pendare","Munduapo Munduapo","Guayapo San Pedro del Orinoco"]},{"municipio":"Manapiare","capital":"San Juan de Manapiare","parroquias":["Alto Ventuari Cacurí","Medio Ventuari Manami","Bajo Ventuari Marueta"]},{"municipio":"Maroa","capital":"Maroa","parroquias":["Victorino","Comunidad"]},{"municipio":"Río Negro","capital":"San Carlos de Río Negro","parroquias":["Casiquiare Curimacare","Cocuy","San Carlos de Río Negro","Solano Solano"]}]},
    {"iso_31662":"VE-B","estado":"Anzoátegui","capital":"Barcelona","id_estado":2,"municipios":[{"municipio":"Anaco","capital":"Anaco","parroquias":["Anaco","San Joaquín"]},{"municipio":"Aragua","capital":"Aragua de Barcelona","parroquias":["Cachipo","Aragua de Barcelona"]},{"municipio":"Bolívar","capital":"Barcelona","parroquias":["Bergatín","Caigua","El Carmen.","El Pilar","Naricual.","San Cristóbal"]},{"municipio":"Bruzual","capital":"Clarines","parroquias":["Clarines","Guanape","Sabana de Uchire"]},{"municipio":"Cajigal","capital":"Onoto","parroquias":["Onoto","San Pablo"]},{"municipio":"Carvajal","capital":"Valle de Guanape","parroquias":["Valle de Guanape","Santa Bárbara"]},{"municipio":"Diego Bautista Urbaneja","capital":"Lechería","parroquias":["Lechería","El Morro"]},{"municipio":"Freites","capital":"Cantaura","parroquias":["Cantaura","Libertador","Santa Rosa","Urica"]},{"municipio":"Guanipa","capital":"San José de Guanipa","parroquias":["San José de Guanipa"]},{"municipio":"Guanta","capital":"Guanta","parroquias":["Guanta","Chorrerón"]},{"municipio":"Independencia","capital":"Soledad","parroquias":["Mamo","Soledad"]},{"municipio":"Libertad","capital":"San Mateo","parroquias":["San Mateo","El Carito","Santa Inés","La Romereña"]},{"municipio":"McGregor","capital":"El Chaparro","parroquias":["El Chaparro","Tomás Alfaro","Calatrava"]},{"municipio":"Miranda","capital":"Pariaguán","parroquias":["Atapirire","Boca del Pao","El Pao","Pariaguán"]},{"municipio":"Monagas","capital":"Mapire","parroquias":["Mapire","Piar","Santa Clara","San Diego de Cabrutica","Uverito","Zuata"]},{"municipio":"Peñalver","capital":"Puerto Píritu","parroquias":["Puerto Píritu","San Miguel","Sucre"]},{"municipio":"Píritu","capital":"Píritu","parroquias":["Píritu","San Francisco"]},{"municipio":"San Juan de Capistrano","capital":"Boca de Uchire","parroquias":["Boca de Uchire","Boca de Chávez"]},{"municipio":"Santa Ana","capital":"Santa Ana","parroquias":["Pueblo Nuevo","Santa Ana"]},{"municipio":"Simón Rodríguez","capital":"El Tigre","parroquias":["Edmundo Barrios","Miguel Otero Silva"]},{"municipio":"Sotillo","capital":"Puerto La Cruz","parroquias":["Puerto La Cruz","Pozuelos"]}]},
    {"iso_31662":"VE-C","estado":"Apure","capital":"San Fernando de Apure","id_estado":3,"municipios":[{"municipio":"Achaguas","capital":"Achaguas","parroquias":["Achaguas","Apurito","El Yagual","Guachara","Mucuritas","Queseras del medio"]},{"municipio":"Biruaca","capital":"Biruaca","parroquias":["Biruaca"]},{"municipio":"Muñoz","capital":"Bruzual","parroquias":["Bruzual","Mantecal","Quintero","Rincón Hondo","San Vicente"]},{"municipio":"Páez","capital":"Guasdualito","parroquias":["Guasdualito","Aramendi","El Amparo","San Camilo","Urdaneta"]},{"municipio":"Pedro Camejo","capital":"San Juan de Payara","parroquias":["San Juan de Payara","Codazzi","Cunaviche"]},{"municipio":"Rómulo Gallegos","capital":"Elorza","parroquias":["Elorza","La Trinidad"]},{"municipio":"San Fernando","capital":"San Fernando de Apure","parroquias":["San Fernando","El Recreo","Peñalver","San Rafael de Atamaica"]}]},
    {"iso_31662":"VE-D","estado":"Aragua","capital":"Maracay","id_estado":4,"municipios":[{"municipio":"Bolívar","capital":"San Mateo","parroquias":["Bolívar"]},{"municipio":"Camatagua","capital":"Camatagua","parroquias":["Camatagua","Carmen de Cura"]},{"municipio":"Girardot","capital":"Maracay","parroquias":["Pedro José Ovalles","Joaquín Crespo","José Casanova Godoy","Madre María de San José","Andrés Eloy Blanco","Los Tacarigua","Las Delicias","Choroní"]},{"municipio":"José Félix Ribas","capital":"La Victoria","parroquias":["José Félix Ribas","Castor Nieves Ríos","Las Guacamayas","Pao de Zárate","Zuata"]},{"municipio":"Santiago Mariño","capital":"Turmero","parroquias":["Turmero","Arevalo Aponte","Chuao","Samán de Güere","Alfredo Pacheco Miranda"]},{"municipio":"Sucre","capital":"Cagua","parroquias":["Cagua","Bella Vista"]},{"municipio":"Zamora","capital":"Villa de Cura","parroquias":["Zamora","Magdaleno","San Francisco de Asís","Valles de Tucutunemo","Augusto Mijares"]}]},
    {"iso_31662":"VE-E","estado":"Barinas","capital":"Barinas","id_estado":5,"municipios":[{"municipio":"Barinas","capital":"Barinas","parroquias":["Barinas","Alberto Arvelo Larriva","San Silvestre","Santa Inés","Santa Lucía","El Carmen","Rómulo Betancourt"]},{"municipio":"Bolívar","capital":"Barinitas","parroquias":["Barinitas","Altamira de Cáceres","Calderas"]},{"municipio":"Ezequiel Zamora","capital":"Santa Bárbara","parroquias":["Santa Bárbara","Pedro Briceño Méndez","Ramón Ignacio Méndez"]},{"municipio":"Rojas","capital":"Libertad","parroquias":["Libertad","Dolores","Santa Rosa","Palacio Fajardo","Simón Rodríguez"]}]},
    {"iso_31662":"VE-F","estado":"Bolívar","capital":"Ciudad Bolívar","id_estado":6,"municipios":[{"municipio":"Caroní","capital":"Ciudad Guayana","parroquias":["Cachamay","Chirica","Dalla Costa","Once de Abril","Simón Bolívar","Unare","Universidad","Vista al Sol","Pozo Verde","Yocoima","5 de Julio"]},{"municipio":"Gran Sabana","capital":"Santa Elena de Uairén","parroquias":["Gran Sabana","Ikabarú"]},{"municipio":"Heres","capital":"Ciudad Bolívar","parroquias":["Catedral","Zea","Orinoco","José Antonio Páez","Marhuanta","Agua Salada","Vista Hermosa","La Sabanita","Panapana"]},{"municipio":"Sifontes","capital":"El Dorado","parroquias":["Sifontes","Dalla Costa","San Isidro"]}]},
    {"iso_31662":"VE-G","estado":"Carabobo","capital":"Valencia","id_estado":7,"municipios":[{"municipio":"Guacara","capital":"Guacara","parroquias":["Ciudad Alianza","Guacara","Yagua"]},{"municipio":"Puerto Cabello","capital":"Puerto Cabello","parroquias":["Bartolomé Salóm","Democracia","Fraternidad","Goaigoaza","Juan José Flores","Unión","Borburata","Patanemo"]},{"municipio":"Valencia","capital":"Valencia","parroquias":["Urbana Candelaria","Urbana Catedral","Urbana El Socorro","Urbana Miguel Peña","Urbana Rafael Urdaneta","Urbana San Blas","Urbana San José","Urbana Santa Rosa","No Urbana Negro Primero"]}]},
    {"iso_31662":"VE-H","estado":"Cojedes","capital":"San Carlos","id_estado":8,"municipios":[{"municipio":"San Carlos","capital":"San Carlos","parroquias":["San Carlos de Austria","Juan Ángel Bravo","Manuel Manrique"]},{"municipio":"Tinaquillo","capital":"Tinaquillo","parroquias":["Tinaquillo"]}]},
    {"iso_31662":"VE-Y","estado":"Delta Amacuro","capital":"Tucupita","id_estado":9,"municipios":[{"municipio":"Tucupita","capital":"Tucupita","parroquias":["San José","José Vidal Marcano Caparal de Guara","Juan Millán","Leonardo Ruíz Pineda Paloma","Mariscal Antonio José de Sucre","San Rafael","Virgen del Valle"]}]},
    {"iso_31662":"VE-I","estado":"Falcón","capital":"Coro","id_estado":10,"municipios":[{"municipio":"Carirubana","capital":"Punto Fijo","parroquias":["Norte","Carirubana","Santa Ana","Urbana Punta Cardón"]},{"municipio":"Miranda","capital":"Santa Ana de Coro","parroquias":["Guzmán Guillermo","Mitare","Río Seco","Sabaneta","San Antonio","San Gabriel","Santa Ana"]},{"municipio":"Zamora","capital":"Puerto Cumarebo","parroquias":["Puerto Cumarebo","La Ciénaga","La Soledad","Pueblo Cumarebo","Zazárida"]}]},
    {"iso_31662":"VE-J","estado":"Guárico","capital":"San Juan de Los Morros","id_estado":11,"municipios":[{"municipio":"Miranda","capital":"Calabozo","parroquias":["El Calvario","El Rastro","Guardatinajas","Capital Urbana Calabozo"]},{"municipio":"Roscio","capital":"San Juan de Los Morros","parroquias":["Cantagallo","San Juan de los Morros","Parapara"]},{"municipio":"Zaraza","capital":"Zaraza","parroquias":["Unare","Zaraza"]}]},
    {"iso_31662":"VE-K","estado":"Lara","capital":"Barquisimeto","id_estado":12,"municipios":[{"municipio":"Iribarren","capital":"Barquisimeto","parroquias":["Catedral","Concepción","El Cují","Juan de Villegas","Santa Rosa","Tamaca","Unión","Aguedo Felipe Alvarado","Buena Vista","Juárez"]},{"municipio":"Torres","capital":"Carora","parroquias":["Altagracia","Antonio Díaz","Camacaro","Castañeda","Torres","Trinidad Samuel"]}]},
    {"iso_31662":"VE-L","estado":"Mérida","capital":"Mérida","id_estado":13,"municipios":[{"municipio":"Libertador","capital":"Mérida","parroquias":["Antonio Spinetti Dini","Arias","Caracciolo Parra Pérez","Domingo Peña","El Llano","Gonzalo Picón Febres","Jacinto Plaza","Juan Rodríguez Suárez","Milla","Sagrario","El Morro","Los Nevados"]},{"municipio":"Alberto Adriani","capital":"El Vigía","parroquias":["Presidente Betancourt","Presidente Páez","Gabriel Picón González","Héctor Amable Mora","José Nucete Sardi","Pulido Méndez"]}]},
    {"iso_31662":"VE-M","estado":"Miranda","capital":"Los Teques","id_estado":14,"municipios":[{"municipio":"Guaicaipuro","capital":"Los Teques","parroquias":["Altagracia de la Montaña","Cecilio Acosta","Los Teques","El Jarillo","San Pedro.","Tácata","Paracotos"]},{"municipio":"Sucre","capital":"Petare","parroquias":["Leoncio Martínez","Petare","Caucagüita","Filas de Mariche","La Dolorita"]},{"municipio":"Zamora","capital":"Guatire","parroquias":["Guatire","Bolívar"]},{"municipio":"Páez","capital":"Río Chico","parroquias":["Río Chico","El Guapo","Tacarigua de la Laguna","Paparo","San Fernando del Guapo"]}]},
    {"iso_31662":"VE-N","estado":"Monagas","capital":"Maturín","id_estado":15,"municipios":[{"municipio":"Maturín","capital":"Maturín","parroquias":["Alto de los Godos","Boquerón","Las Cocuizas","La Cruz","San Simón","El Corozo","El Furrial","Jusepín","La Pica","San Vicente"]},{"municipio":"Piar","capital":"Aragua de Maturín","parroquias":["Aparicio","Aragua de Maturín","Chaguamal","El Pinto","Guanaguana","La Toscana","Taguaya"]}]},
    {"iso_31662":"VE-O","estado":"Nueva Esparta","capital":"La Asunción","id_estado":16,"municipios":[{"municipio":"Mariño","capital":"Porlamar","parroquias":["Porlamar"]},{"municipio":"Arismendi","capital":"La Asunción","parroquias":["Arismendi"]},{"municipio":"Maneiro","capital":"Pampatar","parroquias":["Aguirre","Maneiro"]},{"municipio":"Gómez","capital":"Santa Ana","parroquias":["Bolívar","Guevara","Cerro de Matasiete","Santa Ana","Sucre"]}]},
    {"iso_31662":"VE-P","estado":"Portuguesa","capital":"Guanare","id_estado":17,"municipios":[{"municipio":"Guanare","capital":"Guanare","parroquias":["Cordova","Guanare","San José de la Montaña","San Juan de Guanaguanare","Virgen de Coromoto"]},{"municipio":"Páez","capital":"Acarigua","parroquias":["Acarigua","Payara","Pimpinela","Ramón Peraza"]},{"municipio":"Turén","capital":"Villa Bruzual","parroquias":["Canelones","Santa Cruz","San Isidro Labrador"]}]},
    {"iso_31662":"VE-R","estado":"Sucre","capital":"Cumaná","id_estado":18,"municipios":[{"municipio":"Sucre","capital":"Cumaná","parroquias":["Altagracia Cumaná","Santa Inés Cumaná","Valentín Valiente Cumaná","Ayacucho Cumaná","San Juan","Raúl Leoni","Gran Mariscal"]},{"municipio":"Bermúdez","capital":"Carúpano","parroquias":["Santa Catalina","Santa Rosa","Santa Teresa","Bolívar","Maracapana"]},{"municipio":"Valdez","capital":"Güiria","parroquias":["Cristóbal Colón","Bideau","Punta de Piedras","Güiria"]}]},
    {"iso_31662":"VE-S","estado":"Táchira","capital":"San Cristóbal","id_estado":19,"municipios":[{"municipio":"San Cristóbal","capital":"San Cristóbal","parroquias":["La Concordia","San Juan Bautista","Pedro María Morantes","San Sebastián","Dr. Francisco Romero Lobo"]},{"municipio":"Bolívar","capital":"San Antonio del Táchira","parroquias":["Bolívar","Palotal","General Juan Vicente Gómez","Isaías Medina Angarita"]},{"municipio":"Junín","capital":"Rubio","parroquias":["Junín","La Petrólea","Quinimarí","Bramón"]},{"municipio":"García de Hevia","capital":"La Fría","parroquias":["García de Hevia","Boca de Grita","José Antonio Páez"]}]},
    {"iso_31662":"VE-T","estado":"Trujillo","capital":"Trujillo","id_estado":20,"municipios":[{"municipio":"Trujillo","capital":"Trujillo","parroquias":["Andrés Linares","Chiquinquirá","Cristóbal Mendoza","Cruz Carrillo","Matriz","Monseñor Carrillo","Tres Esquinas"]},{"municipio":"Valera","capital":"Valera","parroquias":["Juan Ignacio Montilla","La Beatriz","La Puerta","Mendoza del Valle de Momboy","Mercedes Díaz","San Luis"]},{"municipio":"Boconó","capital":"Boconó","parroquias":["Boconó","El Carmen","Mosquey","Ayacucho","Burbusay","General Ribas","Guaramacal"]}]},
    {"iso_31662":"VE-W","estado":"Vargas","capital":"La Guaira","id_estado":21,"municipios":[{"municipio":"Vargas","capital":"Vargas","parroquias":["Caraballeda","Carayaca","Carlos Soublette","Caruao Chuspa","Catia La Mar","El Junko","La Guaira","Macuto","Maiquetía","Naiguatá","Urimare"]}]},
    {"iso_31662":"VE-U","estado":"Yaracuy","capital":"San Felipe","id_estado":22,"municipios":[{"municipio":"San Felipe","capital":"San Felipe","parroquias":["San Javier","Albarico","San Felipe"]},{"municipio":"Bruzual","capital":"Chivacoa","parroquias":["Chivacoa","Campo Elías"]},{"municipio":"Nirgua","capital":"Nirgua","parroquias":["Salóm","Temerla","Nirgua"]}]},
    {"iso_31662":"VE-V","estado":"Zulia","capital":"Maracaibo","id_estado":23,"municipios":[{"municipio":"Maracaibo","capital":"Maracaibo","parroquias":["Antonio Borjas Romero","Bolívar","Cacique Mara","Carracciolo Parra Pérez","Cecilio Acosta","Cristo de Aranza","Coquivacoa","Chiquinquirá","Francisco Eugenio Bustamante","Idelfonzo Vásquez","Juana de Ávila","Luis Hurtado Higuera","Manuel Dagnino","Olegario Villalobos.","Raúl Leoni","Santa Lucía","Venancio Pulgar","San Isidro"]},{"municipio":"Cabimas","capital":"Cabimas","parroquias":["Ambrosio","Carmen Herrera","La Rosa","Germán Ríos Linares","San Benito","Rómulo Betancourt","Jorge Hernández","Punta Gorda","Arístides Calvani"]},{"municipio":"San Francisco","capital":"San Francisco","parroquias":["San Francisco","El Bajo","Domitila Flores","Francisco Ochoa","Los Cortijos","Marcial Hernández"]},{"municipio":"Lagunillas","capital":"Ciudad Ojeda","parroquias":["Libertad","Alonso de Ojeda","Venezuela","Eleazar López Contreras","Campo Lara"]}]},
    {"iso_31662":"VE-A","estado":"Distrito Capital","capital":"Caracas","id_estado":24,"municipios":[{"municipio":"Libertador","capital":"Caracas","parroquias":["23 de enero","Altagracia","Antímano","Caricuao","Catedral","Coche","El Junquito","El Paraíso","El Recreo","El Valle","Candelaria","La Pastora","La Vega","Macarao","San Agustín","San Bernardino","San José","San Juan","San Pedro","Santa Rosalía","Santa Teresa","Sucre (Catia)"]}]},
]


def run():
    # 1. País Venezuela
    pais, p_created = Paises.objects.get_or_create(nombre='Venezuela')
    print(f"{'✅ Creado' if p_created else '🔄 Existe'} país: Venezuela (id={pais.pk})")

    total_estados = total_municipios = total_parroquias = 0

    for data in VENEZUELA:
        # 2. Estado
        estado, e_created = Estados.objects.get_or_create(
            nombre=data['estado'],
            pais=pais
        )
        if e_created:
            total_estados += 1
            print(f"  📍 Estado: {data['estado']}")

        # 3. Municipios
        for mun_data in data.get('municipios', []):
            municipio, m_created = Municipios.objects.get_or_create(
                nombre=mun_data['municipio'],
                estado=estado,
                defaults={'capital': mun_data.get('capital', '')}
            )
            if m_created:
                total_municipios += 1

            # 4. Parroquias
            for par_nombre in mun_data.get('parroquias', []):
                _, pr_created = Parroquias.objects.get_or_create(
                    nombre=par_nombre,
                    municipio=municipio
                )
                if pr_created:
                    total_parroquias += 1

    print(f"\n{'='*50}")
    print(f"✅ Importación completada:")
    print(f"   Estados   : {total_estados}")
    print(f"   Municipios: {total_municipios}")
    print(f"   Parroquias: {total_parroquias}")
    print(f"{'='*50}")


if __name__ == '__main__':
    run()
