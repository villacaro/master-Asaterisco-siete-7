var table;
$(document).on("ready",ready);
function ready(e)
{

	/*
	Ocultar link no validos
	PAGE_404_URL: variable impresa en la base de los 
	templates
	*/
	// Reloj
	var monthNames = [ "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre" ]; 
	var dayNames= ["Domingo","Lunes","Martes","Miércoles","Jueves","Viernes","Sábado"]

	// Create a newDate() object
	var res = date_server.split("-");
	var format = formatDate(res);
	// Extract the current date from Date object
	//newDate.setDate(newDate.getDate());
	// Output the day, date, month and year   
	$('#Date').html(monthNames[format.date.getMonth()] + " " + format.date.getDate() + ', ' + format.date.getFullYear());
	// console.log(format);
	var seconds = format.sec + 1;
	var minutes = format.min;
	var hours = format.hour;
	var d = format.d;

	setInterval( function() {
		// Create a newDate() object and extract the seconds of the current time on the visitor's
		if(seconds >= 60){
			seconds = 0;
			minutes++;
			if(minutes >= 60){
				minutes = 0;
				hours++;
				if (hours === 12 && d === "PM") {
				    d = "AM";
				}else if(hours === 13 && d === "AM"){
					hours = 1;
				}else if(hours === 12 && d === "AM"){
					d = "PM";
				}else if(hours === 13 && d === "PM"){
					hours = 1;
				}
			}
		}
		// Add a leading zero to seconds value
		//$("#sec").html(( seconds < 10 ? "0" : "" ) + seconds);
		$("#min").html(( minutes < 10 ? "0" : "" ) + minutes);
		$("#hours").html(( hours < 10 ? "0" : "" ) + hours);
		$("#d").html(d);
		seconds++;
		},1000);
		
	/*setInterval( function() {
		// Create a newDate() object and extract the minutes of the current time on the visitor's
		var minutes = new Date().getMinutes();
		// Add a leading zero to the minutes value
		$("#min").html(( minutes < 10 ? "0" : "" ) + minutes);
	    },1000);
		
	setInterval( function() {
		// Create a newDate() object and extract the hours of the current time on the visitor's
		var hours = new Date().getHours();
		// Add a leading zero to the hours value
		$("#hours").html(( hours < 10 ? "0" : "" ) + hours);
	    }, 1000);*/

	$( "a" ).each( function( index, element ){

    	if( element.hash == PAGE_404_URL ){
    		$(this).addClass("invisible");
    		//console.log( $(this) )
    	}

	});

	Activo();

	verboseIcons()
	
	/**CHOSEN**/
	$(".select-chosen").chosen({no_results_text: "Oops, no hay resultados que coincidad! para: "});
	/********/
	/*Table data*/
	
	table = $('.table-data-reportes').dataTable({
        "sPaginationType": "full_numbers",
        "iDisplayLength": 50,
        "bLengthChange": false,
        "bFilter": false,
    });

	table = $('.table-data').dataTable({
        "sPaginationType": "full_numbers",
        "iDisplayLength": 50,
        "aaSorting": [],
    });
    table2 = $('.table-data2').dataTable({
        "sPaginationType": "full_numbers",
        "bSort": false,
        "bPaginate": false,
        "iDisplayLength": 50
    });
    /* Dropdown */
    $(".header-item").click(function(e){
  		e.stopPropagation();
  		$(".header-dropdown").toggle();
	});
	$(".header-dropdown").click(function(e){
  		e.stopPropagation();
  	});
    $(document).click( function(){
        $(".header-dropdown").hide();
    });
    /* Modals */
    var top_modal_h = (($(".modal .modal-container").height()/2)+40)*(-1);
    $(".modal .modal-container").css({"margin-top":top_modal_h});
    $(".exe-modal").click(function(){
    	$(".header-dropdown").hide();
    	$(".modal").css({"display":"block"});
    	$(".modal").stop().animate({"opacity":1});

    	window[this.attributes.exe_modal_funct.nodeValue](
    		this.attributes.exe_modal_param.nodeValue
    	);

    });
    $(".modal-close").click(function(){
    	$(".modal").stop().animate({"opacity":0}, function(){
    		$(this).css({"display":"none"});
    	});
    });
    /**/
	$(".sidebar").vplugin("sidebar_init");
	/**/
	init();
	/**/
	b = 0;
	$("#nav-menu .nav-option").on("click", function(){
    	$("#nav-menu ul ul").slideUp();
    	if(!$(this).next().is(":visible"))
		{
			//alert("holaa");
			$(this).next().slideDown();
		}
		return false;
    });
    $("#nav-menu .nav_dropdown").find(".active").parent().parent().css({"display":"block"});
	$(".sidebar .menu .dropdown li").mouseover(function(){
		$(this).find(".dropdown-side").css({"display":"block"});
		$(this).find(".dropdown-side").stop().animate({"opacity":1},300);
		$(this).find(".menu_item").addClass("menu_item_small_activate");
	}).mouseout(function(){
		$(this).find(".dropdown-side").stop().animate({"opacity":0},300,function(){
			$(this).css({"display":"none"});
		});
		$(this).find(".menu_item").removeClass("menu_item_small_activate");
	});

	window.onresize = function(){
		init();
		$(".sidebar").vplugin("sidebar_init");
	}
	$(window).scroll(function () {
		
	});

}
expandir_encuentros_automaticos_var = 0;
function ExpandirOpcionesAgencia(){
	if(expandir_encuentros_automaticos_var==0){
		$(".invisible2").css({"display":"block"});
		expandir_encuentros_automaticos_var = 1;
	}
	else{
		$(".invisible2").css({"display":"none"});
		expandir_encuentros_automaticos_var = 0;
	}
}

function verboseIcons(){
	$( ".icon-info2" ).each( function( index, element ){
		element.title = "Ver detalle"
	});

	$( ".icon-edit2" ).each( function( index, element ){
		element.title = "Editar"
	});

	$( ".icon-delete" ).each( function( index, element ){
		element.title = "Eliminar"
	});

	$( ".icon-switch" ).each( function( index, element ){
		element.title = "Cambiar contraseña"
	});

	$( ".icon-tag" ).each( function( index, element ){
		element.title = "Editar etiqueta"
	});
}

function init(){
	max_tam = 0;
	$(".login-side").each(function(){
		if($(this).height()>max_tam){
			max_tam = $(this).height();
		}
	});
	/*if(w_screen() > 800){
		$(".form").css({"margin-top":(max_tam/2)-($(".form").height()/2)});
		$(".login").css({"margin-top":(h_screen()/2)-($(".login").height()/2)});
	}else{
		$(".login").css({"margin-top":20});
		$(".form").css({"margin-top":0});
	}*/
	/**/
	$(".margin-navside").css({"padding-left":$(".navside").width()});
	$(".navbar-nav .head").css({"width":$(".navside").width()});
	/**/
	/*w_input = $(".login-side").width();
	w_ico_input = $(".form .input-icon").width();
	$(".form input").css({"width":w_input-w_ico_input-70});*/
}
function filter(value,i){
    table.fnFilter(value,i);
}
function h_screen(){
	if(typeof(window.innerHeight) == "number"){ //Non-IE
		return window.innerHeight;
	}else if(document.documentElement && document.documentElement.clientHeight){ //IE 6+ in 'standards compliant mode'
		return document.documentElement.clientHeight;
	}else if(document.body && document.body.clientHeight){ //IE 4 compatible
		return document.body.clientHeight;
	}
	return 0;
}
function w_screen(){
	if(typeof(window.innerWidth) == "number"){ //Non-IE
		return window.innerWidth;
	}else if(document.documentElement && document.documentElement.clientWidth){ //IE 6+ in 'standards compliant mode'
		return document.documentElement.clientWidth;
	}else if(document.body && document.body.clientWidth){ //IE 4 compatible
		return document.body.clientWidth;
	}
	return 0;
}
(function( $ ) {
	var methods = {
		init : function( config ) {
	    	config = jQuery.extend({
	    		container : ''
	    	}, config);
	    	return $(this).each(function ( ){
	    		config.container = $(this);
	    		config.container.css({"min-height":h_screen()});
	    	});
	    },
	    sidebar_init : function( config ) {
	    	config = jQuery.extend({
	    		container : ''
	    	}, config);
	    	return $(this).each(function ( ){
	    		config.container = $(this);
	    		config.container.css({"min-height":$(document).height()-44});
	    	});
	    }
	};
	$.fn.vplugin = function( method ) {
  		if ( methods[method] ) {
	    	return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
	    } else if ( typeof method === 'object' || ! method ) {
	    	return methods.init.apply( this, arguments );
	    } else {
	    	$.error( 'Method ' +  method + ' does not exist on jQuery.tooltip' );
	    }
  	};
})( jQuery );

function formatDate(date) {
	"use strict";
	var month = parseInt(date[1]) - 1;
    var d = new Date(date[0], month, date[2], date[3], date[4], date[5]);
    var hh = d.getHours();
    var m = d.getMinutes();
    var s = d.getSeconds();
    var dd = "AM";
    var h = hh;
    if (h >= 12) {
        h = hh-12;
        dd = "PM";
    }
    if (h == 0) {
        h = 12;
    }

    /* if you want 2 digit hours:
    h = h<10?"0"+h:h; */

    var pattern = new RegExp("0?"+hh+":"+m+":"+s);
    var pattern = {
    	hour:h,
    	min:m,
    	sec:s,
    	d:dd,
    	date:d
    }  

    return pattern;
}

function dajax(url,json_array,type){
	$.ajax({
			url : url,
			type : "GET",
			dataType: "json",
			data : {
			datain : json_array,
			csrfmiddlewaretoken: $("#token").val()
			},
			success : function(json) {
				execute(json,type);
			},
			error : function(xhr,errmsg,err) {
				
				console.log("#================ERROR=====================")
				console.log( url )
				console.log( xhr )
				console.log( errmsg )
				console.log( err )
				console.log("#==========================================")
						
			}
		});
}

function dajax_actividad(url){
	$.ajax({
			url : url,
			type : "GET",
			dataType:'html',
			data : {
			},
			success : function(resp) {

				if( resp == 1 ){
					//redirec a login
					window.location.href = ACCESO_URL;
				}
				else{
					//no redirec
				}

				//execute(json,type);
			},
			error : function(xhr,errmsg,err) {
				
				console.log("#================ERROR=====================")
				console.log( url )
				console.log( xhr )
				console.log( errmsg )
				console.log( err )
				console.log("#==========================================")
						
			}
		});
}

var session_inactiva;
var session_activa;

function Inacivo(){
	//alert("inactivo")
	session_inactiva = setInterval("tiempo_inactivo()", 60000 * 30  );//60000 = 1 minuto
	clearInterval(session_activa);
}

function tiempo_inactivo(){
	dajax_actividad( LOGOUT_URL );
}

function Activo(){

	session_activa = setInterval("tiempo_activo()", 60000 * 25 );//60000 = 1 minuto
	clearInterval(session_inactiva);

}

function tiempo_activo(){

	dajax_actividad( INDEX_URL );

}

String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}
