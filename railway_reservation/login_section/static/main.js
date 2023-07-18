console.log("Hello World")

const ItineraryForm = document.getElementById('itinerary-form')

// cars-json
const cityDataBox = document.getElementById('city-data-box')
const cityInput = document.getElementById('city')

const arrivalInput = document.getElementById('arrival')

const itineraryDataBox = document.getElementById('itinerary-data-box')
const itineraryInput = document.getElementById('itinerary')

const btnBox = document.getElementById('btn-box')
// const alertBox = document.getElementById('alert-box')

const itineraryText = document.getElementById('itinerary-text')
const cityText = document.getElementById('city-text')

const adultFee = document.getElementById('adult-fee')

const csrf = document.getElementsByName('csrfmiddlewaretoken')

$.ajax({
    type: 'GET',
    url: '/city-json/',
    success: function(response){
        console.log(response.data)
        const citiesData = response.data
        citiesData.map(item =>{
            const option = document.createElement('option')
            option.textContent = item.city_name
            option.setAttribute('class', 'item')
            // option.setAttribute('id', 'car-text')
            option.setAttribute('data-value', item.city_name)
            cityDataBox.appendChild(option)
        })
    },
    error: function (error){ 
        console.log("From city section")
        console.log(error)
    }
})

cityInput.addEventListener('change', e => {
    // console.log('City:')
    console.log(e.target.value)
    const selected_city = e.target.value

    // alertBox.innerHTML=""
    itineraryDataBox.innerHTML= ""
    itineraryText.textContent = "Choisissez une destination"
    itineraryText.classList.add("default")

    $.ajax({
        type: 'GET',
        url: `itinerary-json/${selected_city}/`,
        success: function(response){
            console.log(response.data)
            const itinerariesData = response.data
            itinerariesData.map(item =>{
                const option = document.createElement('option')
                option.textContent = item.arrival_city__city_name
                option.setAttribute('class', 'item')
                // option.setAttribute('id', 'model-text')
                option.setAttribute('data-value', item.arrival_city__city_name)
                // adultFee.innerHTML= item.adult_fee
                itineraryDataBox.appendChild(option)
            })

            itineraryInput.addEventListener('change', e => {
                console.log("Inside itinerary section")
            })
        },
        error: function(error){
            console.log(error)
        }
    })

    
})

