const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});

function signIn() {
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    // console.log(username, password);

    // var myHeaders = new Headers();
    // myHeaders.append("Authorization", "Basic " + btoa(username + ":" + password));
    // console.log(myHeaders);

    let requestOptions = {
        method: 'POST',
        headers: {
            'Authorization' : "Basic " + btoa(username + ":" + password)
        },
        redirect: 'follow',
        credential: 'include'
    };

    // var requestOptions2 = {
    //     method: 'POST',
    //     headers : myHeaders,
    //     redirect: 'follow',
    //     credential: 'include'
    // };

    function setCookie(cName, cValue, expDays) {
        let date = new Date();
        date.setTime(date.getTime() + (expDays * 24 * 60 * 60 * 1000));
        const expires = "expires=" + date.toUTCString();
        document.cookie = cName + "=" + cValue + "; " + expires + "; path=/";
        };

    fetch("http://127.0.0.1:5000/login", requestOptions)
    .then(response => response.json())
    .then((data) => {
            console.log(data.message)
            if (data.message === "success") {
                setCookie('token', data.token, 1)
                location.href = 'index.html'
            } else {
                alert("error fetching return")
            }
        })
    .catch(error => console.log('error fetching', error));
}

function register() {
    let name = document.getElementById("registerName").value;
    let email = document.getElementById("registerEmail").value;
    let username = document.getElementById("registerUsername").value;
    let password = document.getElementById("registerPassword").value;
    console.log(name,email,username,password);

    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var raw = JSON.stringify({
    "nama_user": name,
    "email_user": email,
    "username": username,
    "password": password
    });

    var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: raw,
    redirect: 'follow'
    };

    fetch("http://127.0.0.1:5000/register", requestOptions)
    .then(response => response.text())
    .then(result => {
        console.log(result)
        alert("Register berhasil, silahkan login")
    })
    .catch(error => console.log('error fetching', error));

}