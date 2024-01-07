$(document).ready(function() {
    $('.next').click(function(){
        currentImage = $('.slider__img.active');
        nextImage = currentImage.next();
        if(nextImage.length){
            currentImage.removeClass('active');
            nextImage.addClass('active');
        };
    });
    $('.prev').click(function(){
        currentImage = $('.slider__img.active');
        prevImage = currentImage.prev();
        if(prevImage.length){
            currentImage.removeClass('active');
            prevImage.addClass('active');
        };
    });
});