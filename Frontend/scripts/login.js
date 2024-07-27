const site_url = "https://my-portal-git-login-rafaelm32s-projects.vercel.app"
const login_button = document.getElementById('login_button')
const msm = document.getElementById('message')
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
        success: function(data){if(data['valid_login']){change_to_site()}else{show_message(data['status'])}},
        dataType: "json"
    })
}

function change_to_site(){
    window.location.replace('../Frontend/index.html')
}

function show_message(text){
    msm.innerHTML = text
}


login_button.addEventListener('click', send_credencials)
document.addEventListener('keypress',(e)=>{if(e.key == 'Enter'){send_credencials(); console.log("A tecla foi apertada")}})
