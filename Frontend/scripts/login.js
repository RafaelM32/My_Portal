const site_url = "http://127.0.0.1:5000"
const login_button = document.getElementById('login_button')

function get_username(){
    const username = document.getElementById('username').value
    return username
}

function get_password(){
    const password = document.getElementsByName('password')[0].value
    return password
}

function send_credencials(){
    $.ajax({
        type: 'POST',
        url: `${site_url}/login`,
        xhrFields: {
            withCredentials: true
       },
        credential:'include',   
        data: JSON.stringify({'username': get_username(), 'password': get_password()}),
        contentType: "application/json",
        success: function(data){if(data['valid_login']){}else{console.log(data['status'])}},
        dataType: "json"
    })
}

function change_to_site(){
    window.location.replace('../Frontend/index.html')
}


login_button.addEventListener('click', send_credencials)

