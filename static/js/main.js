!function(o){"use strict";setTimeout((function(){o("#spinner").length>0&&o("#spinner").removeClass("show")}),1),o(window).scroll((function(){o(this).scrollTop()>300?o(".back-to-top").fadeIn("slow"):o(".back-to-top").fadeOut("slow")})),o(".back-to-top").click((function(){return o("html, body").animate({scrollTop:0},1500,"easeInOutExpo"),!1})),o(".testimonial-carousel").owlCarousel({autoplay:!1,smartSpeed:1e3,center:!0,dots:!1,loop:!0,nav:!0,navText:['<i class="bi bi-arrow-left"></i>','<i class="bi bi-arrow-right"></i>'],responsive:{0:{items:1},768:{items:2}}})}(jQuery);