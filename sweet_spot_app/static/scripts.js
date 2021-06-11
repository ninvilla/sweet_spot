$(document).ready(function(){

    var API_ID = 'c555bfb5'
    var API_KEY = 'fbb5e81800d79cca9f3b170a4c61e200'

    $('form').submit(function(){
        var searchInput = $('#search-bar').val()
        var foodId = `${searchInput}`
        
        var url = `https://api.edamam.com/search?q=${foodId}&app_id=${API_ID}&app_key=${API_KEY}&to=30`

        $.get(url, function(data){
            for(i=0; i<=30; i++){
                $('.recipe_results').prepend(
                    `<div class="card m-3" style="width: 18rem;">
                        <img class="card-img-top" src="${data.hits[i].recipe.image}" alt="${data.hits[i].recipe.label}">
                        <div class="card-body">
                            <h5 class="card-title">${data.hits[i].recipe.label}</h5>
                            <p class="card-text">Servings: ${data.hits[i].recipe.yield}</p>
                            <a href="${data.hits[i].recipe.url}" class="btn btn-primary">See Recipe</a>
                        </div>
                    </div>`
                )
            }
        }, 'json')
        return false;
    })

})