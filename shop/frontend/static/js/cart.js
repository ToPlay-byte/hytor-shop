function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$('.cart').on('click', function(e){
    $('.orders').fadeToggle()
})

$('.orders__exit').on('click', function(){
    $('.orders').fadeOut()
})

$(document).on('click','.orders__btn-delete', function(e) {
    parent = $(this).closest('.orders__list-item')
    CartIdItem = parent.data('product-id')
    buttonId = $('.toy__top-btn').data('product-id')
    cartBadge = $('.cart__badge')
    $.ajax({
        method: 'DELETE',
        headers: { "X-CSRFToken": getCookie("csrftoken")},
        url: '/catalog/orders/',
        data: { pk: CartIdItem},
        success: function (response){
            parent.remove()
            if (response.cart_counter){
                 cartBadge.text(response.cart_counter)
            } else {
                cartBadge.remove()
            }
            console.log(CartIdItem, buttonId)
            if (CartIdItem == buttonId) {
                $("#buy-button").removeClass('toy__top-btn--disabled').text('Add to the cart')
            }
        }
    })
})

let updateQuantity = (value, parent) => {
    pk = parent.data('product-id')
    $.ajax({
        method: 'PUT',
        headers: { "X-CSRFToken": getCookie("csrftoken")},
        url: '/catalog/orders/',
        data: { quantity: value, pk: pk },
        success: function (response){
            parent.find('.orders__price').text(response.totalPrice + '$')
        }
    })
}

$(document).on('input', '.quantity__input', function(e){
    input = $(this)
    value = input.val().match(/[1-9]+0*/)
    if (!value) {
        input.val('1')
    }
    parent = $(this).closest('.orders__list-item')
    updateQuantity($(this).val(), parent)
})

$(document).on('click', '#plus', function(e){
     number = $(this).prev().val(function(index, value) {
        return Number(value) + 1
    })
    parent = $(this).closest('.orders__list-item')
    updateQuantity(number.val(), parent)

})

$(document).on('click', '#minus', function(e){
     number = $(this).next().val(function(index, value) {
        if (value == 1) {
            return 1
        }
        return Number(value) - 1
    })
    parent = $(this).closest('.orders__list-item')
    updateQuantity(number.val(), parent)
})


