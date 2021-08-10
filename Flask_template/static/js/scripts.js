/*!
* Start Bootstrap - Agency v7.0.4 (https://startbootstrap.com/theme/agency)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-agency/blob/master/LICENSE)
*/
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            offset: 74,
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

});

  
// hiding graph content and displaying other graph

$(document).ready(function(){
    $("#Arms").click(function(){
      $("#content_legs").hide();
    });
    $("#Arms").click(function(){
      $("#content_body").hide();
    });
    $("#Arms").click(function(){
      $("#content_arms").show();
    });
    $("#Legs").click(function(){
        $("#content_arms").hide();
      });
      $("#Legs").click(function(){
        $("#content_body").hide();
      });
      $("#Legs").click(function(){
        $("#content_legs").show();
      });
      $("#Body").click(function(){
        $("#content_arms").hide();
      });
      $("#Body").click(function(){
        $("#content_legs").hide();
      });
      $("#Body").click(function(){
        $("#content_body").show();
      });
  });


  // hiding graph content and displaying other graph
$(document).ready(function(){
  $("#Arms_user").click(function(){
    $("#content_legs_user").hide();
  });
  $("#Arms_user").click(function(){
    $("#content_body_user").hide();
  });
  $("#Arms_user").click(function(){
    $("#content_arms_user").show();
  });
  $("#Legs_user").click(function(){
      $("#content_arms_user").hide();
    });
    $("#Legs_user").click(function(){
      $("#content_body_user").hide();
    });
    $("#Legs_user").click(function(){
      $("#content_legs_user").show();
    });
    $("#Body_user").click(function(){
      $("#content_arms_user").hide();
    });
    $("#Body_user").click(function(){
      $("#content_legs_user").hide();
    });
    $("#Body_user").click(function(){
      $("#content_body_user").show();
    });
});

// hiding stroke content and displaying loading bar
    
var file = document.getElementById("stroke_submit");
var content = document.getElementById("content_main");
var process = document.getElementById("process");
var loading = document.getElementById("loading");


file.onclick = function(){
  if( document.getElementById("file_upload").files.length == 0 ){
    console.log("no files selected");
}
else {
  content.style.display = 'none';
  process.style.display = 'block';
  loading.style.display = 'block';
}
}




  



    






