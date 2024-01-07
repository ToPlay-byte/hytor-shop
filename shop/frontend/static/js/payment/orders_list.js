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

$('.orders-list__btn').click(function(e){
    console.log('hello')
    e.preventDefault()
    console.log(this)
    btn = $(this)
    pk = btn.data('order-id')
    $.ajax({
        url: '/orders/ajax/delete-order',
        method: 'POST',
        headers: { "X-CSRFToken": getCookie("csrftoken")},
        data: { pk: pk },
        success: function() {
            console.log(this)
            btn.parent().remove()
            location.reload()
        }
    })
})