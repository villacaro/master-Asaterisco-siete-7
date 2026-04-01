(function() {
    var __bind = function(fn, me){
        return function(){ 
            return fn.apply(me, arguments); 
        }; 
    };

    (function ($, window) {
        "use strict";

        var $win = $(window),
            _css = $.fn.css;

        var Theme;
        Theme = (function(){
        	Theme.prototype.defaults = {
        		speed: 1
        	};

        	function Theme(el, options){
        		this.options = $.extend({}, options);
        		this.$el = $(el);
                this.$btn = this.$el.find(".btn");
                this.$sidebar = this.$el.find(".sidebar");
                this._initColors();
        		this._changeColors(this.options.colors);
        	};

            Theme.prototype._initColors = function() {
                var color;
                var css;
                for(color in this.options.colors){
                    css = {
                        'bordercolor':this._colorLuminance(this.options.colors[color].color, -0.1),
                        'textcolor':this._colorLuminance(this.options.colors[color].color, 0.6),
                        'darkercolor':this._colorLuminance(this.options.colors[color].color, -0.2)};
                    this.options.colors[color] = $.extend(css, this.options.colors[color]);
                }
            };

        	Theme.prototype._changeColors = function(colors) {
    	        this.$btn.each(function(){
                    var self = $(this);
                    var color;
                    if(self.hasClass("btn-primary")){
                        for(color in colors){
                            if(colors[color].color_type == 0){
                                self.css({
                                    'background-color':colors[color].color,
                                    'border-color':colors[color].bordercolor});
                                break;
                            }
                        }
                    }
                });
                var color;
                for(color in colors){
                    if(colors[color].color_type == 0){
                        var title = $(".sidebar .nav_p");
                        var subtitle = $(".sidebar .nav .nav-option");
                        var subtitle_css = {
                            'background-color':colors[color].bordercolor,
                            'border-color':colors[color].darkercolor
                        };
                        this.$sidebar.css({
                            'background-color':colors[color].color,
                            'border-color':colors[color].darkercolor});
                        title.css({'color':colors[color].textcolor});
                        subtitle.css(subtitle_css);
                        //inicio.css(subtitle_css);
                    }
                }
    	    };

            Theme.prototype._colorLuminance = function(hex, lum) {
                // validate hex string
                hex = String(hex).replace(/[^0-9a-f]/gi, '');
                if (hex.length < 6) {
                    hex = hex[0]+hex[0]+hex[1]+hex[1]+hex[2]+hex[2];
                }
                lum = lum || 0;
                // convert to decimal and change luminosity
                var rgb = "#", c, i;
                for (i = 0; i < 3; i++) {
                    c = parseInt(hex.substr(i*2,2), 16);
                    c = Math.round(Math.min(Math.max(0, c + (c * lum)), 255)).toString(16);
                    rgb += ("00"+c).substr(c.length);
                }
                return rgb;
            };

        	return Theme;
        })();

        return $.fn.extend({
        	themesChanger: function(colors){
        		this.each(function(){
        			var $this, data, self = this,
        			$this = $(this);
        			data = $this.data('themesChanger');
        			if(!data){
                        var options = {"colors":colors};
        				$this.data('themesChanger', (data = new Theme(this, options)));
        			}
        		});
        	}
        });

    })(jQuery, window);
}).call(this);