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
var first_attempt = true
var url_ = "https://my-portal-git-login-rafaelm32s-projects.vercel.app"
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
        xhrFields: {
            withCredentials: true
       },
        contentType: "application/json",
        success: function(data){load_videos_status(data); load_tumbs_in_site(videos_tumbs_dic);console.log()},
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
        xhrFields: {
            withCredentials: true
       },
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
        xhrFields: {
            withCredentials: true
       },
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
    tittle_element.innerHTML = decode_text(tex)
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

function decode_text(texto){
    const codigos = [['\\\\"', '"'],['\\xc3\\x83','Ã'],['\\xc3\\x82','Â'],['\\xc3\\x87', 'Ç'],
               ['\\xf0\\x9f\\x8c\\x88','&#127752;'],['\\xc3\\x8a','Ê'],['\\xc3\\x8d', 'Í'],
               ['\\xf0\\x9f\\x9a\\xa8','&#128680;'],['\\xc3\\x81','Á'],['\\xc3\\x89','É'],
               ['\\xc3\\x93','Ó'],['\\xe2\\x80\\x99','’'],['\\xe2\\x80\\x98','‘'],['\\xc3\\xa1','á'],
               ['\\xc3\\xa9','é'],['\\xc3\\xa2','â'],['\\xf0\\x9f\\x92\\xa3','&#128163;'],
               ['\\xc3\\xa3','ã'],['\\xc3\\xaa','ê'],['\\xc3\\xb3','ó'],['\\xf0\\x9f\\xa4\\x94','&#129300;'],
               ['\\xf0\\x9f\\x90\\x8d','&#128013;'],['\\xf0\\x9f\\x98\\xa2','&#128546;'],
               ['\\xf0\\x9f\\xa4\\x9d','&#129309;'],['\\xf0\\x9f\\x92\\xa5','&#128165;'],['\\xf0\\x9f\\x93\\x96','&#128214;'],
               ['\\xf0\\x9f\\x98\\xb1','&#128561;'],['\\xc3\\xad','í'],['\\xc3\\x95','Õ'],['\\xc3\\xa7','ç'],
               ['\\xf0\\x9f\\x92\\x8a','&#128138;'],['\\xf0\\x9f\\x98\\xa1','&#128545;'],['\\xc3\\xb5','õ'],
               ['\\xe2\\x9a\\xa0\\xef\\xb8\\x8f','&#9888;'],['\\xf0\\x9f\\x91\\x80','&#128064;'],['\\xc3\\x9a','Ú'],
               ['\\xe2\\x80\\x9c','“'],['\\xe2\\x80\\x9d','”'],['\\xef\\xbf\\xbc','￼'],['\\xe2\\x80\\xa6','...'],['\\xc4\\x81','ã'],
               ['\\xc2\\xa0','&nbsp;'],['\\xc3\\x80','À'],['\\xc3\\x94','Ô'],['\\xc3\\xa0','à'],["\\'", "'"],
               ['\\xc2\\xba','º'],['\\xf0\\x9f\\xa4\\xa3','&#129315;'],['\\xf0\\x9f\\x98\\x82','&#128514;'],
               ['\\xf0\\x9f\\x98\\x8e','&#128526;'],['\\xf0\\x9f\\x91\\x8a\\xf0\\x9f\\x8f\\xbc','&#128074;&#127996;'],
               ['\\xf0\\x9f\\x8f\\x8d\\xef\\xb8\\x8','&#127949;&#65039;'],['\\xf0\\x9f\\x91\\xb6','&#128118;'],
               ['\\xf0\\x9f\\xa7\\x91','&#129489;'],['\\xe2\\x80\\x8d','&zwj;'],['\\xe2\\x9a\\x96\\xef\\xb8\\x8f','&#9878;&#65039;'],
               ['\\xe2\\x9c\\x88\\xef\\xb8\\x8f','&#9992;&#x2708;'],['\\xf0\\x9f\\xa4\\x96','&#129302;'],['\\xf0\\x9f\\x90\\xb6','&#128054;&#x1F436;'],
               ['\\xf0\\x9f\\x95\\xb9\\xef\\xb8\\x8','&#128377;'],['\\xf0\\x9f\\xa4\\xa2','&#129314;'],['\\xf0\\x9f\\x98\\xad','&#128557;'],
               ['\\xe2\\x80\\xbc\\xef\\xb8\\x8f','!!'],['\\xc3\\xba','ú']]
    for (i in codigos){
        texto = texto.replace(codigos[i][0],codigos[i][1])
    }
    return texto
}


function load_channels(){
    const url = `${url_}/channel_list`
    $.ajax({
        type:'GET',
        url: `${url_}/channel_list`,
        success: function(data){load_videos_pear_channel(data['chanels_list'].reverse()); update_qtd(data['qtd'])}

    })
    
    
}

function load_videos_in_channel(channel){
    const url = `${url_}/videos`
    $.ajax({
        type:'POST',
        url: url,
        data: JSON.stringify({channel: channel}),
        xhrFields: {
            withCredentials: true
       },
        contentType: "application/json",
        success: function(data){append_in_videos_dic(data)},
        dataType: "json"
    })
}

function append_in_videos_dic(d){
    for(i in d['videos_list']){
        videos_tumbs_dic['videos'].push(d['videos_list'][i])
        videos_tumbs_dic['tumbs'].push(d['tumb_list'][i])
        videos_tumbs_dic['tittles'].push(d['tittle_list'][i])
        add_div_tumb_to_div_content(build_tittle_to_page(d['tumb_list'][i],d['tittle_list'][i]))
    }

    
}

function load_videos_pear_channel(channel_list){
    for(i in channel_list){
        load_videos_in_channel(channel_list[i])
    }
}

function update_qtd(num){
    h1_video_qtd.innerHTML = num
}

function update_site(){
    const url_post = `${url_}/qtd`
    $.ajax({
        type:"POST",
        url: url_post,
        data: JSON.stringify({"new_qtd": get_video_qtd()}),
        xhrFields: {
            withCredentials: true
       },
        contentType:"application/json",
        success: function(){clear_div(); load_channels()},
        dataType:"json"

    })
}

//At the end of the code i just run the buttons event to triger the functions
remove_button.addEventListener('click', delete_channel)
add_button.addEventListener('click', add_channel)
refresh_button.addEventListener('click', function(){update_site()})
less_than_button.addEventListener('click', lower_video_qtd)
gr_than_button.addEventListener('click',grower_video_qtd )


//Here is just to call the function when i load the page
//load_content(rfr=false,quantidade=get_video_qtd())
load_channels()


