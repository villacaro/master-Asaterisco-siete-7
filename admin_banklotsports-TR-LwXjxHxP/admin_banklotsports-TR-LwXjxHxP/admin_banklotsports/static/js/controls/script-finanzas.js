$(document).on("ready",page);
function page(e)
{

	$("#id_filter_deporte").on("change",filter_buscar_temporadas);
	$("#id_filter_temporada").on("change",filter_buscar_encuentros);

	$("#id_filter_encuentro").on("change",filter_buscar_grupos_modalidad);
	
	$("#id_filter_grupo_modalidad").on("change",filter_buscar_modalidades)
	$("#id_filter_modalidad").on("change",filter_buscar_condiciones)

	$("#id_filter_bloque").on("change",filter_buscar_bancas)
	$("#id_filter_banca").on("change",filter_buscar_distribuidores)
	$("#id_filter_distribuidor").on("change",filter_buscar_agencias)
	$("#id_filter_agencia").on("change",filter_buscar_taquillas)

	$("#id_filtro_deporte").on("change",filter_buscar_torneos);


}

function filter_buscar_torneos(){
	$("#id_filtro_torneo").empty()
	$("#id_filtro_torneo").trigger("chosen:updated");
	if( $("#id_filtro_deporte").val() != 0 ){
		dajax("/finanzas/dajax/filtros/","{\"id\":\""+ $("#id_filtro_deporte").val() +"\",\"obj\":\"filtro_torneo\"}","id_filtro_torneo");
	}

}

function filter_buscar_temporadas(){

	$("#id_filter_temporada").empty()
	$("#id_filter_temporada").trigger("chosen:updated");
	$("#id_filter_encuentro").empty()
	$("#id_filter_encuentro").trigger("chosen:updated");
	
	if( $("#id_filter_deporte").val() != 0 && $("#id_filter_fecha_inicio").val() != '' ){
		dajax("/finanzas/dajax/filtros/","{\"id\":\""+ $("#id_filter_deporte").val() + ","+ $("#id_filter_fecha_inicio").val() +"\",\"obj\":\"filter_temporada\"}","id_filter_temporada");
	}

}


function filter_buscar_encuentros(){

	$("#id_filter_encuentro").empty()
	$("#id_filter_encuentro").trigger("chosen:updated");
	
	if( $("#id_filter_temporada").val() != 0 && $("#id_filter_fecha_inicio").val() != '' ){
		dajax("/finanzas/dajax/filtros/","{\"id\":\""+ $("#id_filter_temporada").val() + ","+ $("#id_filter_fecha_inicio").val() +"\",\"obj\":\"filter_encuentro\"}","id_filter_encuentro");
	}

}

function filter_buscar_grupos_modalidad(){
	$("#id_filter_grupo_modalidad").empty()
	$("#id_filter_grupo_modalidad").trigger("chosen:updated");
	
	if( $("#id_filter_encuentro").val() != 0){
		dajax("/finanzas/dajax/filtros/","{\"id\":\""+ $("#id_filter_encuentro").val() +"\",\"obj\":\"filter_grupo_modalidad\"}","id_filter_grupo_modalidad");
	}
}

function filter_buscar_modalidades(){

	$("#id_filter_modalidad").empty()
	$("#id_filter_modalidad").trigger("chosen:updated");
	$("#id_filter_condicion").empty()
	$("#id_filter_condicion").trigger("chosen:updated");

	var encuento = 0
	if( $("#id_filter_encuentro").val() != null)
		encuento = $("#id_filter_encuentro").val()

	if( $("#id_filter_grupo_modalidad").val() != 0){
		dajax("/finanzas/dajax/filtros/","{\"id\":\""+ encuento +"," + $("#id_filter_grupo_modalidad").val() +"\",\"obj\":\"filter_modalidad\"}","id_filter_modalidad");
	}

}

function filter_buscar_condiciones(){

	$("#id_filter_condicion").empty()
	$("#id_filter_condicion").trigger("chosen:updated");

	if ( $("#id_filter_encuentro").val() != null)
		if( $("#id_filter_grupo_modalidad").val()!= 0 && $("#id_filter_modalidad").val() != 0 && $("#id_filter_encuentro").val() != 0){
			dajax("/finanzas/dajax/filtros/","{\"id\":\""+ $("#id_filter_encuentro").val() +","+$("#id_filter_grupo_modalidad").val()+","+ $("#id_filter_modalidad").val() +"\",\"obj\":\"filter_condicion\"}","id_filter_condicion");
		}

}

function filter_buscar_bancas () {
	
	$("#id_filter_banca").empty()
	$("#id_filter_banca").trigger("chosen:updated");
	$("#id_filter_distribuidor").empty()
	$("#id_filter_distribuidor").trigger("chosen:updated");
	$("#id_filter_agencia").empty()
	$("#id_filter_agencia").trigger("chosen:updated");
	$("#id_filter_taquilla").empty()
	$("#id_filter_taquilla").trigger("chosen:updated");

	if( $("#id_filter_bloque").val() != 0){
		dajax("/finanzas/dajax/filtros/","{\"id\":\""+ $("#id_filter_bloque").val() +"\",\"obj\":\"filter_banca\"}","id_filter_banca");
	}
}

function filter_buscar_distribuidores () {
	
	$("#id_filter_distribuidor").empty()
	$("#id_filter_distribuidor").trigger("chosen:updated");
	$("#id_filter_agencia").empty()
	$("#id_filter_agencia").trigger("chosen:updated");
	$("#id_filter_taquilla").empty()
	$("#id_filter_taquilla").trigger("chosen:updated");

	if( $("#id_filter_banca").val() != 0){
		dajax("/finanzas/dajax/filtros/","{\"id\":\""+ $("#id_filter_banca").val() +"\",\"obj\":\"filter_distribuidor\"}","id_filter_distribuidor");
	}
}

function filter_buscar_agencias () {
	
	$("#id_filter_agencia").empty()
	$("#id_filter_agencia").trigger("chosen:updated");
	$("#id_filter_taquilla").empty()
	$("#id_filter_taquilla").trigger("chosen:updated");

	if( $("#id_filter_distribuidor").val() != 0){
		dajax("/finanzas/dajax/filtros/","{\"id\":\""+ $("#id_filter_distribuidor").val() +"\",\"obj\":\"filter_agencia\"}","id_filter_agencia");
	}
}

function filter_buscar_taquillas(){

}


function execute(data,type){

	//alert(JSON.stringify( data[0] ))
	$("#"+type).append('<option value="0" >Todo</option>');

	$.each( data[0] , function(obj){
		$("#"+type).append('<option value="'+data[0][obj]["pk"]+'" >'+data[0][obj]["nombre"]+'</option>');
	});

	$("#"+type).trigger("chosen:updated");
	
}