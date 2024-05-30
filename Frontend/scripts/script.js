const url = 'http://127.0.0.1:5000/iframes'
const lista_de_urls = ["https://www.youtube.com/@rbiana/videos","https://www.youtube.com/@Mamaefalei/videos"]

$.ajax({
    type: 'POST',
    url: url,
    data: JSON.stringify({channels: lista_de_urls, videos_quantity_peer_channel: 2}),
    contentType: "application/json",
    success: function(data){console.log(data)},
    dataType:'json'
})
