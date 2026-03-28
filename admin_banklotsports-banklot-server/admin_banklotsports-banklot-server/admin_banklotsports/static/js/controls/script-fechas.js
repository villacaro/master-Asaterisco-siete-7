$(document).on("ready",page);
function page(e)
{	
	fecha = $("#fechaini").val().split("/")
	if(fecha[2]!=null){
		anho = fecha[2];
		if(fecha[1]<10)
			mes = "0"+fecha[1]
		else
			mes = fecha[1]

		if (fecha[0]<10)
			dia = "0"+fecha[0]
		else
			dia = fecha[0]   
		$("#_fechaini").val(anho+"-"+mes+"-"+dia)
		
	}
	formatFecha("fechaini")

	fecha = $("#fechafin").val().split("/")
	if(fecha[2]!=null){
		anho = fecha[2];
		if(fecha[1]<10)
			mes = "0"+fecha[1]
		else
			mes = fecha[1]

		if (fecha[0]<10)
			dia = "0"+fecha[0]
		else
			dia = fecha[0]   
		$("#_fechafin").val(anho+"-"+mes+"-"+dia)
		
	}
	formatFecha("fechafin")
}

function formatFecha( id ){

	if($("#_"+id).val() == "")
	{
		$("#"+id).val("")
	}
	else{
		//fecha = new Date($("#_"+id).val().split("-")[0], $("#_"+id).val().split("-")[1], $("#_"+id).val().split("-")[2]);

		fecha_var = $("#_"+id).val().split("-")[2]  + "/" + $("#_"+id).val().split("-")[1]  + "/" + $("#_"+id).val().split("-")[0];

		$("#"+id).val(fecha_var);
	}

}
