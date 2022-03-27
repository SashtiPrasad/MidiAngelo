// Hover move listing
$(document).ready(function() {

	
	// pretty photo
	$("a[rel^='prettyPhoto']").prettyPhoto({
		theme: 'light_square'
	});	

	// tooltip
	$.tools.tooltip.addEffect("fade",
		// opening animation
		function(done) {
			this.getTip().fadeIn();
			done.call();
		},
		// closing animation
		function(done) {
			this.getTip().fadeOut();
			done.call();
		}
	);
	$(".tool").tooltip({
		effect: 'fade',
		offset: [50, 0]
	});
	$(".tool-right").tooltip({
		effect: 'fade',
		position: 'center right',
		offset: [0, -50],
		tipClass: 'tooltip-right'
	});
	$(".tool-bottom").tooltip({
		effect: 'fade',
		position: 'bottom center',
		offset: [-50, 0],
		tipClass: 'tooltip-bottom'
	});
	$(".tool-left").tooltip({
		effect: 'fade',
		position: 'center left',
		offset: [0, 50],
		tipClass: 'tooltip-left'
	});
	
	//superfish
	$("ul.sf-menu").superfish({
		autoArrows:  false, // disable generation of arrow mark-up
		  animation: {height:'show'},
		  speed: 'fast'
	}); 
	
	// rollovers
	$("#sidebar li.sidemenu ul li.cat-item a").hover(function() { 
		// on rollover	
		$(this).stop().animate({ 
			marginLeft: "7" 
		}, "fast");
	} , function() { 
		// on out
		$(this).stop().animate({
			marginLeft: "0" 
		}, "fast");
	});	
		
	// slideshow
  	$('#slides')
  	.before('<div id="slideshow-nav-holder"><div id="slideshow-nav">')
  	.cycle({ 
		fx:     'scrollHorz', 
		speed:  500, 
		timeout: 6000, 
		pause: 1,
		pager:  '#slideshow-nav'
	});

	// add right cornoer to slide control
	$('#slideshow-nav-holder').prepend('<div class="nav-left"></div>');
	$('#slideshow-nav-holder').append('<div class="nav-right"></div>');
		
	//  slide fade
	$('.slide-fade').cycle({ 
		fx:     'fade', 
		speed:  500, 
		timeout: 3000, 
		pause: 1
	});
	
	//  slide scroll
	$('.slide-scroll').cycle({ 
		fx:     'scrollHorz', 
		speed:  500, 
		timeout: 3000, 
		pause: 1
	});
	
	// toggle
	$(".toggle-container").hide(); 
	$(".toggle-trigger").click(function(){
		$(this).toggleClass("active").next().slideToggle("slow");
		return false;
	});
	
	// accordion
	$('.accordion-container').hide(); 
	$('.accordion-trigger:first').addClass('active').next().show();
	$('.accordion-trigger').click(function(){
		if( $(this).next().is(':hidden') ) { 
			$('.accordion-trigger').removeClass('active').next().slideUp();
			$(this).toggleClass('active').next().slideDown();		}
		return false;
	});
	
	
	// tabs
	$('.tabbed').tabs({
		fxFade: true
	});
	
	// cufon
	Cufon.replace('.custom, #nav>li>a, .follow-us li, .fancy, #footer ul.footer-cols li.col h6, .page-title, .page-subtitle, .block-title, .link-button, .sub-header, h1, h2, h3 ,h4, h5, h6, #portfolio-filter li, .gallery li em, .meta .day, .meta .month-year, .meta .comments, #posts .post-title, ul.blog-pager a, .comments-header, .portfolio-title, .client-title', { 
				fontFamily: 'bebas-neue',
				hover: true	
	});
	
	// twitter 
   /* getTwitters('twitter-holder', {
        id: 'ansimuz', 
        prefix: '',
        clearContents: false,
        count: 1, 
        withFriends: true,
        ignoreReplies: false,
        newwindow: true,
        template: '<div class="twitter-entry">"%text%" <span class="twitter-time">%time%</span> </div>'

    });*/
	
	
		
//close			
});
	


// search clearance	
function defaultInput(target){
	if((target).value == 'Search...'){(target).value=''}
}

function clearInput(target){
	if((target).value == ''){(target).value='Search...'}
}
