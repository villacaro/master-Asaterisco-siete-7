$(document).on("ready",page);
function page(e)
{	
	fecha = $("#fecha").val().split("/")
	if(fecha[2]!=null){
		anho = fecha[2]
		if(fecha[1]<10)
			mes = "0"+fecha[1]
		else
			mes = fecha[1]

		if (fecha[0]<10)
			dia = "0"+fecha[0]
		else
			dia = fecha[0]   
		$("#_fecha").val(anho+"-"+mes+"-"+dia)
	}
	formatFecha("fecha")

	fecha = $("#horajuego").val().split(" ")

	if(fecha[1]!=null){
		hora = fecha[1]//saco la hora
		fecha = fecha[0].split("/")//ahora si obtengo la fecha
		
		anho = fecha[2]
		mes = fecha[1]
		dia = fecha[0]
		$("#_horajuego").val(anho+"-"+mes+"-"+dia+"T"+hora)
		//2000-01-10T23:12
		
	}
	formatFechaHora("horajuego")
	
	fecha = $("#horacierre").val().split(" ")
	if(fecha[1]!=null){
		hora = fecha[1]//saco la hora
		fecha = fecha[0].split("/")//ahora si obtengo la fecha
		
		anho = fecha[2]
		mes = fecha[1]
		dia = fecha[0] 
		$("#_horacierre").val(anho+"-"+mes+"-"+dia+"T"+hora)
		
	}
	formatFechaHora("horacierre")
}

function formatFecha( id ){


	if($("#_"+id).val() == "")
	{
		$("#"+id).val("")
	}
	else{
		//alert($("#_"+id).val());
		//fecha = new Date($("#_"+id).val());
		//alert(fecha);
		//fecha_var = (fecha.getDate()+1)  + "/" + (fecha.getMonth()+1)  + "/" + fecha.getFullYear();
		//$("#"+id).val(fecha_var);

	}

}

function formatFechaHora(id){
	
	if($("#_"+id).val() == "")
	{
		$("#"+id).val("")
	}
	else{
		fecha_hora = $("#_"+id).val().split("T")
		fecha = fecha_hora[0].split("-")
		
		$("#"+id).val(fecha[2]+"/"+fecha[1]+"/"+fecha[0]+" "+fecha_hora[1])
	}
}