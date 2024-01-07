function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$('.search__input').keyup(function(){
    data = $(this).val();
    if (data){
        $('.search__results').fadeIn()
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": getCookie("csrftoken")},
            url: "/catalog/search/",
            data: {'query': data},
            success: function({items}){
                $('.search__results').empty();
                console.log(items == false)
                console.log(items)
                if (items.length) {
                    items.map(function(value){
                        $('.search__results').append(`
                            <div class="search__results-item">
                                <a class="search__results-link" href="/catalog/detail/${value}">${value}</a>
                            </div>
                        `)
                    })
                }
                else {
                    console.log('hellosfd')
                    $('.search__results').append(`
                        <div class="search__results-item">
                            Nothing found
                        </div>
                    `)
                }
            }
        })
    } else {
        $('.search__results').empty();
        $('.search__results').append(`
            <div class="search__results-item">Enter something</div>
        `)
    }

})

$('.search__input').blur(function(){
    $('.search__results').fadeOut()
})