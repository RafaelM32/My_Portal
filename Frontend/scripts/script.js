//Use to load the data from api with videos contents
//when the calls succeeds, it calls the fuction that places the iframes inside the div content

function load_iframes(){    
    const url = 'http://127.0.0.1:5000/iframes'
    $.ajax({
        type: 'POST',
        url: url,
        data: JSON.stringify({videos_quantity_peer_channel: 2}),
        contentType: "application/json",
        success: function(data){load_iframes_in_site(data['videos_list'])},
        dataType:'json'
    })
}

//Use to save new channels to search for videos
function add_channel(ch){
    const url = 'http://127.0.0.1:5000/channel_list'
    $.ajax({
        type: 'POST',
        url: url,
        data: JSON.stringify({channel: ch}),
        contentType: "application/json",
        success: function(data){console.log(data)},
        dataType:'json'
    })
}


//Use to delete channels in Database
function delete_channel(ch){
    const url = 'http://127.0.0.1:5000/channel_list'
    $.ajax({
        type: 'DELETE',
        url: url,
        data: JSON.stringify({channel: ch}),
        contentType: "application/json",
        success: function(data){console.log(data)},
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


load_iframes()