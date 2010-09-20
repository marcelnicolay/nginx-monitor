(function($){

	$.fn.serversNode = function(){

		var change_graph = function($elem){

			$node = $elem.parent().parent().parent().parent()

			$("ol li img", $node).each(function(){
				$this = $(this);
				
				var src = $this.attr("src").match(/(.*)(request|connection)\-(\w+)/);
				var path = src[1];
				var type = src[2];
				var period = src[3];
				
				$this.attr("src",path+type+"-"+$elem.attr("graph")+".png");
			});
		}
		
		return this.each(function(){
			$node = $(this);
			$navegacao = $(".submenu a",$node);
		
			$navegacao.unbind().bind("click", function(){
				change_graph($(this));
			});
		});

	};
	
})(jQuery);