//Here i just load the buttons in the code
var add_button = document.getElementById("ADD")
var remove_button = document.getElementById("REMOVE")
var refresh_button = document.getElementById("REFRESH")
var text_element = document.getElementById("message")
var input_element = document.getElementById('channel')
var h1_video_qtd = document.getElementById('qtd')
var less_than_button = document.getElementById('less_video')
var gr_than_button = document.getElementById('more_video')
var start_qtd_value = 0
var videos_tumbs_dic = {'videos':[], 'tumbs': [], 'tittles': []}
var url_ = "https://my-portal-bice.vercel.app"
//Use to load the data from api with videos contents
//when the calls succeeds, it calls the fuction that places the iframes inside the div content
function load_content(rfr=false, quantidade = parseInt(h1_video_qtd.innerText), change_qtd = false){    
    if (rfr){
        clear_div()
    }
    const url = `${url_}/iframes` 
    $.ajax({
        type: 'POST',
        url: url,
        data: JSON.stringify({refresh: rfr, videos_quantity_peer_channel: quantidade, change_videos_qtd: change_qtd}),
        contentType: "application/json",
        success: function(data){load_videos_status(data); load_tumbs_in_site(videos_tumbs_dic); console.log(data)},
        dataType:'json'
    })
}

//Use to save new channels to search for videos
function add_channel(){
    const url = `${url_}/channel_list` 
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
    const url = `${url_}/channel_list` 
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
    const url = `${url_}/channel_list` 
    $.get(url, function(data){console.log(data)})
}


//This function creats a iframe object that can be set inside the div
function make_iframe_object(video){
    const iframe = document.createElement('iframe')
    iframe.src = `https://www.youtube.com/embed/${video}`
    iframe.title = "YouTube video player"
    iframe.frameBorder = "0"
    iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    iframe.referrerPolicy = "strict-origin-when-cross-origin"
    iframe.allowFullscreen = true
    return iframe
}


//This function is to add a iframe inside the content div
function add_element_to_div(element){
    const div = document.getElementById('content')
    div.appendChild(make_iframe_object(element))
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
//This function returns the quantity of videos peer channel
function get_video_qtd(){
    return parseInt(h1_video_qtd.innerText)
}


//This function changes the quantity of videos peer channel
function grower_video_qtd(){
    let actual = get_video_qtd()
    if(actual < 30){
        h1_video_qtd.innerText = actual + 1
    }
}

//This function changes the quantity of videos peer channel
function lower_video_qtd(){
    let actual = get_video_qtd()
    if(actual > 0){
        h1_video_qtd.innerText = actual - 1

    }
}

function load_videos_status(d){
    videos_tumbs_dic['videos'] = d['videos_list']
    videos_tumbs_dic['tumbs'] = d['tumb_list']
    videos_tumbs_dic['tittles'] = d['tittle_list']
    start_qtd_value = d['videos_qtd']
    h1_video_qtd.innerText = d['videos_qtd']
}

function check_qtd_update(){
    if (parseInt(h1_video_qtd.innerText) == start_qtd_value){
        return false
    }else{
        return true
    }
}

function make_tumb(tumb_url){
    const tumb = document.createElement('img')
    tumb.title = "Youtube Tumb"
    tumb.src = tumb_url
    tumb.classList.add('tumb_img')
    tumb.addEventListener('click', function(){click_on_tumb(tumb_url)})
    return tumb
}

function make_div_tumb(){
    const div_tumb = document.createElement('div')
    div_tumb.classList.add('div_tumb')
    return div_tumb
}

function make_tittle(tex){
    const tittle_element = document.createElement('p')
    tittle_element.innerHTML = tex
    return tittle_element
}

function make_div_tittle(){
    const div_tittle = document.createElement('div')
    div_tittle.classList.add('div_tittle')
    return div_tittle
}

function build_tittle_to_page(url_tumb,tittle_text){
    const div_tumb = make_div_tumb()
    const tumb = make_tumb(url_tumb)
    const div_tittle = make_div_tittle()
    const p = make_tittle(tittle_text)

    div_tittle.appendChild(p)
    div_tumb.appendChild(tumb)
    div_tumb.appendChild(div_tittle)

    return div_tumb

}

function click_on_tumb(tumb_url){
    change_div_for_iframe(tumb_url)
}

function add_div_tumb_to_div_content(div_tumb){
    const div = document.getElementById('content')
    div.appendChild(div_tumb)
}

function load_tumbs_in_site(videos_dic){
    for(i in videos_dic['videos']){
        add_div_tumb_to_div_content(build_tittle_to_page(videos_dic['tumbs'][i],videos_dic['tittles'][i]))
    }
}

function change_div_for_iframe(url_tumb){
    const imgs = document.getElementsByClassName('tumb_img')
    for(i in imgs){
        if(imgs[i].src == url_tumb){
            const div_to_replace = imgs[i].parentElement
            const container = div_to_replace.parentElement
            container.replaceChild(make_iframe_object(select_video_by_tumb_url(url_tumb)),div_to_replace)
        }
    }
}


function select_video_by_tumb_url(tumb_url){
    for(i in videos_tumbs_dic['tumbs']){
        if (videos_tumbs_dic['tumbs'][i] == tumb_url){
            return videos_tumbs_dic['videos'][i]
        }
    }
}

//At the end of the code i just run the buttons event to triger the functions
remove_button.addEventListener('click', delete_channel)
add_button.addEventListener('click', add_channel)
refresh_button.addEventListener('click', function(){load_content(rfr=true,quantidade=get_video_qtd(), change_qtd = check_qtd_update())})
less_than_button.addEventListener('click', lower_video_qtd)
gr_than_button.addEventListener('click',grower_video_qtd )


//Here is just to call the function when i load the page
load_content(rfr=false,quantidade=get_video_qtd())
