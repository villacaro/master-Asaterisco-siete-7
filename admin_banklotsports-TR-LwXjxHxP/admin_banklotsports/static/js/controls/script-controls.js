$(document).on("ready",page);
function page(e)
{
	
	IniReset()

}

function IniReset(){
	ModalidadesDiseabled();
	CondicionesDiseabled();

	if($("#id_bloque option:selected").val()==null && $("#id_banca option:selected").val()==null && $("#id_distribuidor option:selected").val()!=null){
		$("#id_agencia").empty();
		$("#id_agencia").attr('disabled','disabled');
	}
	else{
		if($("#id_bloque option:selected").val()!=null){
			$("#id_banca").empty();
			$("#id_banca").attr('disabled','disabled');
			$("#id_distribuidor").empty();
			$("#id_distribuidor").attr('disabled','disabled');
			$("#id_agencia").empty();
			$("#id_agencia").attr('disabled','disabled');
		}
	}

	$("#id_id_deporte").on("change",consultar_modalidades);
	$("#id_id_modalidades").on("change",consultar_condiciones);
	$("#cls_modalidad").on("click",cls_modalidad);
	$("#add_modalidad").on("click",add_modalidad);
	$("#cls_condicion").on("click",cls_condicion);
	$("#id_id_condiciones_obj").on("dblclick",cls_condicion);
	$("#add_condicion").on("click",add_condicion);
	$("#id_id_condiciones").on("dblclick",add_condicion);
	$("#guardar_modalidades").on("click",guardar_modalidades);
	$("#guardar_condiciones").on("click",guardar_condiciones);

	$("#id_id_evento").empty();
	$("#id_id_temporadas").empty();
	$("#id_id_temporadas_2").empty();
	$("#id_id_jornada").empty();
	$("#id_id_jornada_2").empty();
	$("#id_id_jornada_3").empty();

	$("#id_id_deportes").on("change",consultar_eventos);
	$("#id_id_evento").on("change",consultar_temporadas);
	$("#id_id_temporadas").on("change",consultar_jornadas);
	$("#id_id_temporadas_2").on("change",consultar_jornadas);
	$("#id_id_jornada").on("change",consultar_encuentros_asignar_logros);
	$("#id_id_jornada_2").on("change",consultar_encuentros_editar_logros);
	$("#id_id_jornada_3").on("change",consultar_encuentros_premiar_logros);

	$("#add_equipo").on("click",add_equipo);
	$("#cls_equipo").on("click",cls_equipo);
	
	$("#add_equipo_2").on("click",add_equipo_2);
	$("#cls_equipo_2").on("click",cls_equipo_2);

	$("#id_id_equipos").on("dblclick",add_equipo);
	$("#id_id_equipos_obj").on("dblclick",cls_equipo);

	$("#id_id_modalidad").on("dblclick",add_modalidad);
	$("#id_id_modalidad_obj").on("dblclick",cls_modalidad);

	$("#id_id_equipos_2").on("dblclick",add_equipo_2);
	$("#id_id_equipos_obj_2").on("dblclick",cls_equipo_2);

	$("#temporada_equipo_guardar").on("click",TemporadaEquipoGuardar);
	
	EquiposDiseabled();

	$("#id_crear_encuentro").on("click",Crear_Encuentro);
	$("#ConsultarDetalleEncuentro").on("click",ConsultarDetalleEncuentro_AsignarLogros);

	$("#id_bloque").on("change",consultar_bancas);
	$("#id_banca").on("change",consultar_distribuidor);
	$("#id_distribuidor").on("change",consultar_agencias);

	$("#espandirLogro_button").on("click",espandirLogro);
	espandirLogro_var = 0

	$("#logro_id_modalidad").on("click",ConsultarCondicionesEncuentroFilter);

	$("#logro_id_condicion").on("click",SeleccionarCondicion);
	
	$("#id_agregar_logro").on("click",AgregarLogro);
}

function VerificarNumValido (id) {

	numero = parseInt($("#"+String(id)).val())

	if( numero  == 0 ){
			$("#"+String(id)).val("")
	}

}

function EliminarJugadaFuntion(pk){
	
	dajax("/juego/dajax/jugadas/","{\"id\":\""+String(pk)+"\",\"obj\":\"jugada_eliminar\"}","jugada_eliminar")

}

function AgregarLogro(){
	if ( $("#logro_id_modalidad option:selected").val()!=0 ){
		//alert($("#logro_id_modalidad option:selected").html())

		if ( $("#logro_id_condicion option:selected").val()!=0 ){

			pk = $("#logro_id_condicion option:selected").val().split("-")[0]
			tipo = $("#logro_id_condicion option:selected").val().split("-")[1]
			
			if (tipo=="True") {
				if ( $("#logro_id_condicion_equipo option:selected").html()!="---" ){

					equipo = $("#logro_id_condicion_equipo option:selected").val()
					logro = $("#logro_nuevo").val();
					if (logro!=0){
						AgregarLogroProceso(pk,equipo,logro);
					}
					else{
						alert("El logro debe ser diferente de 0")
					}
				}
				else{
					alert("debe seleccionar un equipo");
				}
			}
			else{

				equipo = $("#logro_id_condicion_equipo option:selected").val()
				logro = $("#logro_nuevo").val();
				if (logro!=0){
					AgregarLogroProceso(pk,equipo,logro);
				}
				else{
					alert("El logro debe ser diferente de 0")
				}

			}

		}
		else{
			alert("debe seleccionar una condicion");
		}

	}
	else{
		alert("debe seleccionar una modalidad");
	}
}

function AgregarLogroProceso(condicion,equipo,logro){

	var data = String(condicion) + "-" + String(equipo)  + "-" + String(logro);

	dajax("/juego/dajax/jugadas/","{\"id\":\""+data+"\",\"obj\":\"jugada_agregar\"}","jugada_agregar")
	

}

function SeleccionarCondicion() {
	
	$("#logro_id_condicion_equipo").attr('disabled', true);

	//$("#logro_id_condicion_equipo option[value="+ 0 +"]").attr("selected",true);
	$("#logro_id_condicion_equipo").prop('selectedIndex', 0);
	if( $(this).val() != 0){
		
		if( $(this).val().split("-")[1]=="True"){
			$("#logro_id_condicion_equipo").attr('disabled', false);
		}

	}
}

function ConsultarCondicionesEncuentroFilter(){
	$("#logro_id_condicion").empty();
	if( $(this).val() != 0){
		dajax("/juego/dajax_consultar/","{\"id\":\""+$(this).val()+"\",\"obj\":\"condiciones_encuentro_filter\"}","logro_id_condicion")
	}
}

function espandirLogro() {

	if(espandirLogro_var==0){
		$(".logros-agregar").css({"display":"inline-block"});
		espandirLogro_var = 1
	}
	else{
		$(".logros-agregar").css({"display":"none"});
		espandirLogro_var=0
	}
}

function consultar_bancas(){
	$("#id_banca").empty();
	$("#id_banca").removeAttr('disabled');
	if( $(this).val() != 0){
		dajax("/users/cadena/","{\"id\":\""+$(this).val()+"\",\"obj\":\"banca\"}","id_banca");
	}
	else{
		$("#id_banca").attr('disabled','disabled');
		$("#id_distribuidor").empty();
		$("#id_distribuidor").attr('disabled','disabled');
		$("#id_agencia").empty();
		$("#id_agencia").attr('disabled','disabled');
	}
}

function consultar_distribuidor(){
	$("#id_distribuidor").empty();
	$("#id_distribuidor").removeAttr('disabled');
	if( $(this).val() != 0){
		dajax("/users/cadena/","{\"id\":\""+$(this).val()+"\",\"obj\":\"distribuidor\"}","id_distribuidor");
	}
	else{
		$("#id_distribuidor").attr('disabled','disabled');
		$("#id_agencia").empty();
		$("#id_agencia").attr('disabled','disabled');
	}
}

function consultar_agencias(){
	$("#id_agencia").empty();
	$("#id_agencia").removeAttr('disabled');
	if( $(this).val() != 0){
		dajax("/users/cadena/","{\"id\":\""+$(this).val()+"\",\"obj\":\"agencia\"}","id_agencia");
	}
	else{
		$("#id_agencia").attr('disabled','disabled');
	}
}

function consultar_modalidades(){
	$("#id_id_modalidad").empty()
	$("#id_id_modalidad_obj").empty()
	$("#id_id_modalidades").empty()
	$("#id_id_condiciones").empty()
	$("#id_id_condiciones_obj").empty()
	ModalidadesEnabled();
	CondicionesDiseabled();
	if( $(this).val() != 0){
		dajax("/juego/dajax_consultar_1/","{\"id\":\""+$(this).val()+"\",\"obj\":\"modalidad_filter\"}","id_id_modalidad");
		dajax("/juego/dajax_consultar_1/","{\"id\":\""+$(this).val()+"\",\"obj\":\"modalidades\"}","id_id_modalidades");
	}
	else{
		ModalidadesDiseabled();
	}
}

function consultar_condiciones(){
	CondicionesEnabled();
	$("#id_id_condiciones").empty()
	$("#id_id_condiciones_obj").empty()
	if( $(this).val() != 0){
		dajax("/juego/dajax_consultar_1/","{\"modalidad\":\""+$(this).val()+"\",\"deporte\":\""+$("#id_id_deporte option:selected").val()+"\",\"obj\":\"condicion\"}","id_id_condiciones");
	}
	else
		CondicionesDiseabled();
}

function CondicionesDiseabled(){
	$("#id_id_condiciones").attr('disabled','disabled');
	$("#id_id_condiciones_obj").attr('disabled','disabled');
	$("#add_condicion").attr('disabled','disabled');
	$("#cls_condicion").attr('disabled','disabled');
	$("#guardar_condiciones").attr('disabled','disabled');
}

function CondicionesEnabled(){
	$("#id_id_condiciones").removeAttr('disabled');
	$("#id_id_condiciones_obj").removeAttr('disabled');
	$("#add_condicion").removeAttr('disabled');
	$("#cls_condicion").removeAttr('disabled');
	$("#guardar_condiciones").removeAttr('disabled');
}


function ModalidadesDiseabled(){
	$("#id_id_modalidades").attr('disabled','disabled');
	$("#id_id_modalidad").attr('disabled','disabled');
	$("#id_id_modalidad_obj").attr('disabled','disabled');
	$("#add_modalidad").attr('disabled','disabled');
	$("#cls_modalidad").attr('disabled','disabled');
	$("#guardar_modalidades").attr('disabled','disabled');
}
function ModalidadesEnabled(){
	$("#id_id_modalidades").removeAttr('disabled');
	$("#id_id_modalidad").removeAttr('disabled');
	$("#id_id_modalidad_obj").removeAttr('disabled');
	$("#add_modalidad").removeAttr('disabled');
	$("#cls_modalidad").removeAttr('disabled');
	$("#guardar_modalidades").removeAttr('disabled','disabled');
}

function add_modalidad(){
	if($("#id_id_modalidad option:selected").val()!=null){
		$("#id_id_modalidad_obj").append('<option value="'+$("#id_id_modalidad option:selected").val()+'" >'+$("#id_id_modalidad option:selected").html()+'</option>');
		$("#id_id_modalidad option:selected").remove();
	}
}

function add_condicion(){
	if($("#id_id_condiciones option:selected").val()!=null){
		$("#id_id_condiciones_obj").append('<option value="'+$("#id_id_condiciones option:selected").val()+'" >'+$("#id_id_condiciones option:selected").html()+'</option>');
		$("#id_id_condiciones option:selected").remove();
	}
}

function cls_modalidad(){
	if($("#id_id_modalidad_obj option:selected").val()!=null){

		var data_json = new Array();
		var pk1 = $("#id_id_deporte option:selected").val();
		var pk2 = $("#id_id_modalidad_obj option:selected").val();
    	data_json.push({deporte: pk1, modalidad: pk2, accion:"delete"});
		dajax("/modalidades/asignar-modalidad-deporte/",JSON.stringify( data_json ),"Asociar_Deporte_Modalidad")
		
		$("#id_id_modalidad").append('<option value="'+$("#id_id_modalidad_obj option:selected").val()+'" >'+$("#id_id_modalidad_obj option:selected").html()+'</option>');
		$("#id_id_modalidad_obj option:selected").remove();
	}
}

function cls_condicion(){
	if($("#id_id_condiciones_obj option:selected").val()!=null){

		var data_json = new Array();
		var pk1 = $("#id_id_deporte option:selected").val();
		var pk2 = $("#id_id_modalidades option:selected").val();
		var pk3 = $("#id_id_condiciones_obj option:selected").val();
    	data_json.push({deporte: pk1, modalidad: pk2,condicion: pk3, accion:"delete"});
		dajax("/condiciones/asignar-condicion-modalidad/",JSON.stringify( data_json ),"Asociar_Condicion_Modalidad")
		

		$("#id_id_condiciones").append('<option value="'+$("#id_id_condiciones_obj option:selected").val()+'" >'+$("#id_id_condiciones_obj option:selected").html()+'</option>');
		$("#id_id_condiciones_obj option:selected").remove();
	}
}

function guardar_condiciones(){
	var data_json = new Array();
	var entro = false;

	$("#id_id_condiciones_obj option").each(function(){
		var pk1 = $("#id_id_deporte option:selected").val();
		var pk2 = $("#id_id_modalidades option:selected").val();
		var pk3 = $(this).val();
    	data_json.push({deporte: pk1, modalidad: pk2, condicion: pk3 ,accion:"create"});
    	entro = true;
    });
    if( entro == true){
    	dajax("/condiciones/asignar-condicion-modalidad/", JSON.stringify( data_json ),"Asociar_Condicion_Modalidad");
    }
    else{
    	alert("No hay ninguna condicion seleccionada");
    }
}

function guardar_modalidades(){
	var data_json = new Array();
	var entro = false;

	$("#id_id_modalidad_obj option").each(function(){
		var pk1 =  $("#id_id_deporte option:selected").val();
		var pk2 = $(this).val();
    	data_json.push({deporte: pk1, modalidad: pk2, accion:"create"});
    	entro = true;
    });
    if( entro == true){
    	dajax("/modalidades/asignar-modalidad-deporte/", JSON.stringify( data_json ),"Asociar_Deporte_Modalidad");
    }
    else{
    	alert("No hay ninguna modalidad seleccionada");
    }
}




function ConsultarDetalleEncuentro_AsignarLogros(){
	//if($("#id_submit").val()=="")
		//return false;
	
	if($("#id_id_encuentro option:selected").val()!=0){
		$("#id_submit").val($("#id_id_encuentro option:selected").val());
		return true;
		//alert($("#id_id_encuentro option:selected").val());		
		//dajax("/juego/dajax_consultar/","{\"id\":\""+$("#id_id_encuentro option:selected").val()+"\",\"obj\":\"detalle_encuentro\"}","MostrarTablaEncuentro");
	}
	else
		return false;
	
}

var MaxEquipos = 0;
function Crear_Encuentro(){
	if($("#id_id_equipos_obj_2 option").length<2){
		alert("como minimo se deben enfrentar 2 equipos");
		return false;
	}
	else{
		$("#id_id_equipos_obj_2 option").each(function(){
			$("#id_equipos_hidden").val( $("#id_equipos_hidden").val() +","+$(this).val())
		});
	}
}

function TemporadaEquipoGuardar(){
	var data_json = new Array();
	var entro = false;

	$("#id_id_equipos_obj option").each(function(){
		//alert( $(this).html() );
		var pk1 =  $("#id_id_temporadas option:selected").val();
		var pk2 = $(this).val();
    	data_json.push({temporada: pk1, equipo: pk2, accion:"create"});
    	entro = true;

    });
    if( entro == true){
    	dajax("/temporadas/asignar-equipos/", JSON.stringify( data_json ),"Asociar_Temporada_Equipo");
    }
    else{
    	alert("No hay ningun equipo seleccionado");
    }
}

function EquiposDiseabled(){
	$("#id_id_equipos").attr('disabled','disabled');
	$("#id_id_equipos_obj").attr('disabled','disabled');
	$("#add_equipo").attr('disabled','disabled');
	$("#cls_equipo").attr('disabled','disabled');
	$("#temporada_equipo_guardar").attr('disabled','disabled');
	$("#id_id_equipos_obj").empty()
}
function EquiposEnabled(){
	$("#id_id_equipos").removeAttr('disabled');
	$("#id_id_equipos_obj").removeAttr('disabled');
	$("#add_equipo").removeAttr('disabled');
	$("#cls_equipo").removeAttr('disabled');
	$("#temporada_equipo_guardar").removeAttr('disabled');
}

function add_equipo(){
	if($("#id_id_equipos option:selected").val()!=null){
		$("#id_id_equipos_obj").append('<option value="'+$("#id_id_equipos option:selected").val()+'" >'+$("#id_id_equipos option:selected").html()+'</option>');
		$("#id_id_equipos option:selected").remove();
	}

}
function cls_equipo(){
	if($("#id_id_equipos_obj option:selected").val()!=null){

		var data_json = new Array();
		var pk1 = $("#id_id_temporadas option:selected").val();
		var pk2 = $("#id_id_equipos_obj option:selected").val();
    	data_json.push({temporada: pk1, equipo: pk2, accion:"delete"});

		dajax("/temporadas/asignar-equipos/",JSON.stringify( data_json ),"Asociar_Temporada_Equipo")
		
		$("#id_id_equipos").append('<option value="'+$("#id_id_equipos_obj option:selected").val()+'" >'+$("#id_id_equipos_obj option:selected").html()+'</option>');
		$("#id_id_equipos_obj option:selected").remove();
	}
}

function add_equipo_2(){
	if($("#id_id_equipos_2 option:selected").val()!=null){

		if( $("#id_id_equipos_obj_2 option").length  >= MaxEquipos )
		{
			alert("Para un encuentro de " + $("#id_id_deportes option:selected").html() + " solo pueden enfrentarse un maximo de "+MaxEquipos+" equipos");
		}
		else{
			$("#id_id_equipos_obj_2").append('<option value="'+$("#id_id_equipos_2 option:selected").val()+'" >'+$("#id_id_equipos_2 option:selected").html()+'</option>');
			$("#id_id_equipos_2 option:selected").remove();
		}
	}

}
function cls_equipo_2(){
	if($("#id_id_equipos_obj_2 option:selected").val()!=null){

		$("#id_id_equipos_2").append('<option value="'+$("#id_id_equipos_obj_2 option:selected").val()+'" >'+$("#id_id_equipos_obj_2 option:selected").html()+'</option>');
		$("#id_id_equipos_obj_2 option:selected").remove();
	}
}

function consultar_eventos(){
	$("#id_id_evento").empty();
	$("#id_id_temporadas").empty();	
	$("#id_id_temporadas_2").empty();	
	$("#id_id_jornada").empty();
	$("#id_id_jornada_2").empty();
	$("#id_id_jornada_3").empty();

	$("#id_id_equipos").empty();
	$("#id_id_encuentro").empty()
	EquiposDiseabled();
	if( $(this).val() != 0){
		dajax("/juego/dajax_consultar/","{\"id\":\""+$(this).val()+"\",\"obj\":\"evento\"}","id_id_evento")
		//dajax("/juego/dajax_consultar/","{\"id\":\""+$(this).val()+"\",\"obj\":\"equipo_all\"}","id_id_equipos")
		//alert("equipo all");
		dajax("/juego/dajax_consultar/","{\"id\":\""+$(this).val()+"\",\"obj\":\"MaxEquipos\"}","MaxEquipos")
		
	}
}

function consultar_temporadas(){
	$("#id_id_temporadas").empty();	
	$("#id_id_temporadas_2").empty();	
	$("#id_id_jornada").empty();
	$("#id_id_jornada_2").empty();
	$("#id_id_jornada_3").empty();
	$("#id_id_encuentro").empty()
	EquiposDiseabled();

	if( $(this).val() != 0){
		dajax("/juego/dajax_consultar/","{\"id\":\""+$(this).val()+"\",\"obj\":\"temporada\"}","id_id_temporadas")
		dajax("/juego/dajax_consultar/","{\"id\":\""+$(this).val()+"\",\"obj\":\"temporada\"}","id_id_temporadas_2")
	}
}
function consultar_jornadas(){
	$("#id_id_jornada").empty();
	$("#id_id_jornada_2").empty();
	$("#id_id_jornada_3").empty();
	$("#id_id_equipos").empty();
	$("#id_id_equipos_2").empty();
	$("#id_id_equipos_obj_2").empty();
	$("#id_id_encuentro").empty()
	if( $(this).val() != 0){
		$("#id_id_equipos").empty();
		$("#id_id_equipos_obj").empty();
		existe = new String( $("#id_id_jornada").val())
		//alert(existe)
		if( existe=="null" ){
			//alert("jornada");
			dajax("/juego/dajax_consultar/","{\"id\":\""+$(this).val()+"\",\"obj\":\"jornada\"}","id_id_jornada");
		}
		else{
			//alert("jornada_2");
			existe = new String( $("#id_id_jornada_2").val())
			if( existe=="null" ){
				dajax("/juego/dajax_consultar/","{\"id\":\""+$(this).val()+"\",\"obj\":\"jornada\"}","id_id_jornada_2");
			}
			else{
				dajax("/juego/dajax_consultar/","{\"id\":\""+$(this).val()+"\",\"obj\":\"jornada\"}","id_id_jornada_3");
			}
		}

		if($(this).attr("id") == "id_id_temporadas"){
			dajax("/juego/dajax_consultar/","{\"id\":\""+$("#id_id_deportes option:selected").val()+"-"+$("#id_id_temporadas option:selected").val()+"\",\"obj\":\"equipo_all\"}","id_id_equipos");
			EquiposEnabled();
		}
		else{
			dajax("/juego/dajax_consultar/","{\"id\":\""+$("#id_id_temporadas_2 option:selected").val()+"\",\"obj\":\"equipo_filter_2\"}","id_id_equipos_2");
		}
		//alert("equipo filter");
	}
	else{
		if($(this).attr("id") == "id_id_temporadas"){
			EquiposDiseabled();
		}
	}
}

function consultar_encuentros_asignar_logros(){
	$("#id_id_encuentro").empty()
	if( $(this).val() != 0){
		dajax("/juego/dajax_consultar/","{\"id\":\""+$(this).val()+"\",\"obj\":\"encuentro_asignar_logros\"}","id_id_encuentro");
	}
}

function consultar_encuentros_editar_logros(){
	$("#id_id_encuentro").empty()
	if( $(this).val() != 0){
		dajax("/juego/dajax_consultar/","{\"id\":\""+$(this).val()+"\",\"obj\":\"encuentro_editar_logros\"}","id_id_encuentro");
	}
}

function consultar_encuentros_premiar_logros(){
	$("#id_id_encuentro").empty()
	if( $(this).val() != 0){
		dajax("/juego/dajax_consultar/","{\"id\":\""+$(this).val()+"\",\"obj\":\"encuentro_premiar_logros\"}","id_id_encuentro");
	}
}

function dajax(url,json_array,type){
	$.ajax({
			url : url,
			type : "POST",
			dataType: "json",
			data : {
			datain : json_array,
			csrfmiddlewaretoken: $("#token").val()
			},
			success : function(json) {
				execute(json,type);
			},
			error : function(xhr,errmsg,err) {
				if (xhr.status!=0)
					if (xhr.status==200)
						javascript:location.reload()
					else
						alert(xhr.status + ": " + xhr.responseText);
						
			}
		});
}
function execute(data,type){

	//alert(JSON.stringify( data ))

	if (type == "jugada_agregar"){

		if ( data[0]["error"] == 0 ){
			$("#logro_id_condicion_equipo").prop('selectedIndex', 0);
			$("#logro_id_condicion").prop('selectedIndex', 0);
			$("#logro_id_modalidad").prop('selectedIndex', 0);
			$("#logro_nuevo").val(0);
			//alert("Proceso exitoso")
			$("#formulario_jugadas_actualizar").submit();
		}
		else
		{
			alert( data[0]["error_message"] )
		}
	}
	else
	if (type=="jugada_eliminar"){
		if ( data[0]["error"] == 0 ){
			$("#formulario_jugadas_actualizar").submit();
		}
		else
		{
			alert( data[0]["error_message"] )
		}
	}
	else
	if( type == "MaxEquipos" ){
		//alert(data[0]["cantidad"]);
		MaxEquipos = data[0]["cantidad"];
	}
	else
	if(type=="Asociar_Temporada_Equipo"){
		//alert(JSON.stringify( data ));
	}
	else
	if(type=="MostrarTablaEncuentro"){
		//alert(JSON.stringify( data ));
	}
	else{
		if(type!="id_id_equipos" && type!="id_id_equipos_obj" && type!="id_id_equipos_2" && type!="id_id_modalidad" && type!="id_id_modalidad_obj" && type!="id_id_condiciones" && type!="id_id_condiciones_obj")
			$("#"+type).append('<option value="0" >------</option>');
		
		$.each(data[0], function(obj){
			//alert( data[0][obj]["nombre"] )	
			$("#"+type).append('<option value="'+data[0][obj]["pk"]+'" >'+data[0][obj]["nombre"]+'</option>');
			

			if( type == "id_id_equipos_obj")
				$("#id_id_equipos [value="+data[0][obj]["pk"]+"]").remove();

			if( type == "id_id_modalidad_obj")
				$("#id_id_modalidad [value="+data[0][obj]["pk"]+"]").remove();

			if( type == "id_id_condiciones_obj")
				$("#id_id_condiciones [value="+data[0][obj]["pk"]+"]").remove();

		});

		if(type == "id_id_equipos")
			dajax("/juego/dajax_consultar/","{\"id\":\""+$("#id_id_temporadas option:selected").val()+"\",\"obj\":\"equipo_filter\"}","id_id_equipos_obj");
		if( type == "id_id_modalidad")
			dajax("/juego/dajax_consultar_1/","{\"id\":\""+$("#id_id_deporte option:selected").val()+"\",\"obj\":\"modalidades\"}","id_id_modalidad_obj");
		if( type == "id_id_condiciones")
			dajax("/juego/dajax_consultar_1/","{\"modalidad\":\""+$("#id_id_modalidades option:selected").val()+"\",\"deporte\":\""+$("#id_id_deporte option:selected").val()+"\",\"obj\":\"condiciones\"}","id_id_condiciones_obj");

	}
	
}


/* Parte Luis */
function consultar_ciudades(){
	$("#id_ciudad_select").empty()
	$("#id_distribuidor").empty()
	if( $(this).val() != 0 ){
		dajax("/users/dajax_consultar/","{\"id\":\""+$(this).val()+"\",\"obj\":\"ciudad\"}","id_ciudad_select")
	}
}

function consultar_distribuidores(){
	$("#id_distribuidor").empty()
	$("#id_ciudad").val($(this).val());
	if( $(this).val() != 0 ){
		dajax("/users/dajax_consultar/","{\"id\":\""+$(this).val()+"\",\"obj\":\"distribuidor\"}","id_distribuidor")
	}
}
