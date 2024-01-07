$('.header__burger').click(function(event){
    $('.header__burger, .toggle-menu, .menu__list').toggleClass('active');
});



$("#about").click(function() {
    $('html, body').animate({
        scrollTop: $(".about").offset().top
    }, 1000);
});
$("#products").click(function() {
    $('html, body').animate({
        scrollTop: $(".products").offset().top
    }, 1000);
});
$("#contacts").click(function() {
    $('html, body').animate({
        scrollTop: $(".footer").offset().top
    }, 1000);
});
