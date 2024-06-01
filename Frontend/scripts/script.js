//Here i just load the buttons in the code
var add_button = document.getElementById("ADD")
var remove_button = document.getElementById("REMOVE")
var refresh_button = document.getElementById("REFRESH")
var text_element = document.getElementById("message")
var input_element = document.getElementById('channel')
var h1_video_qtd = document.getElementById('qtd')
var less_than_button = document.getElementById('less_video')
var gr_than_button = document.getElementById('more_video')




//Use to load the data from api with videos contents
//when the calls succeeds, it calls the fuction that places the iframes inside the div content
function load_iframes(rfr=false, quantidade = 2){    
    if (rfr){
        clear_div()
    }
    const url = 'http://127.0.0.1:5000/iframes'
    $.ajax({
        type: 'POST',
        url: url,
        data: JSON.stringify({refresh:rfr,videos_quantity_peer_channel: quantidade}),
        contentType: "application/json",
        success: function(data){load_iframes_in_site(data['videos_list'])},
        dataType:'json'
    })
}

//Use to save new channels to search for videos
function add_channel(){
    const url = 'http://127.0.0.1:5000/channel_list'
    const channel = input_element.value
    $.ajax({
        type: 'POST',
        url: url,
        data: JSON.stringify({channel: channel}),
        contentType: "application/json",
        success: function(data){show_response(data['status'])},
        dataType:'json'
    })
}


//Use to delete channels in Database
function delete_channel(){
    const url = 'http://127.0.0.1:5000/channel_list'
    const channel = input_element.value
    $.ajax({
        type: 'DELETE',
        url: url,
        data: JSON.stringify({channel: channel}),
        contentType: "application/json",
        success: function(data){show_response(data['status'])},
        dataType:'json'
    })
}


//Use to get all chennels in Database
function get_channels_list(){
    const url = 'http://127.0.0.1:5000/channel_list'
    $.get(url, function(data){console.log(data)})
}


//This function creats a iframe object that can be set inside the div
function make_iframe_object(video){
    const iframe = document.createElement('iframe')
    iframe.src = video
    iframe.title = "YouTube video player"
    iframe.frameBorder = "0"
    iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    iframe.referrerPolicy = "strict-origin-when-cross-origin"
    iframe.allowFullscreen = true
    return iframe
}


//This function is to add a iframe inside the content div
function add_iframe_to_div(ifr){
    const div = document.getElementById('content')
    div.appendChild(make_iframe_object(ifr))
}


//This function adds all the videos inside the div content
function load_iframes_in_site(iframe_lista){
    for (i in iframe_lista){
        add_iframe_to_div(iframe_lista[i])
    }
}

//This function is to clear the div when before refresh the content
function clear_div(){
    const div = document.getElementById('content')
    div.innerHTML = ''
}

//This function is use to show the message from the backend
function show_response(response){
    text_element.innerText = response
}

function get_video_qtd(){
    return parseInt(h1_video_qtd.innerText)
}

function grower_video_qtd(){
    let actual = get_video_qtd()
    if(actual < 30){
        h1_video_qtd.innerText = actual + 1
    }
}

function lower_video_qtd(){
    let actual = get_video_qtd()
    if(actual > 0){
        h1_video_qtd.innerText = actual - 1

    }
}

//At the end of the code i just run the buttons event to triger the functions
remove_button.addEventListener('click', delete_channel)
add_button.addEventListener('click', add_channel)
refresh_button.addEventListener('click', function(){load_iframes(rfr=true,get_video_qtd())})
less_than_button.addEventListener('click', lower_video_qtd)
gr_than_button.addEventListener('click',grower_video_qtd )


//Here is just to call the function when i load the page
load_iframes(quantidade=get_video_qtd())