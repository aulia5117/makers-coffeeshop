function userCheckCookie() {
    const token = document.cookie;
    // console.log(token);
    if (token !== "") {
        // document.getElementById('loginbutton').style.display = "none";
        const split = token.split(".");
        let parsedToken = JSON.parse(atob(split[1]));
        // console.log(parsedToken)
        let username = parsedToken["username"]
        // console.log(username)
        let userLabel = document.getElementById('userprofile').lastElementChild;
        userLabel.innerHTML = username;

    } else {
        document.getElementById('userprofile').style.display = "none";
    }
}

function userGetUserData() {
    const token = document.cookie;
    // console.log(token);
    if (token !== "") {

        const split = token.split(".");
        let parsedToken = JSON.parse(atob(split[1]));
        // console.log(parsedToken)
        let id = parsedToken["id"]
        // let password = parsedToken["password"]
        console.log(id)

        const requestOptions = {
            method: 'GET'
            // redirect: 'follow'
          };
          
          fetch(`http://127.0.0.1:5000/user/get_update_data/${id}`, requestOptions)
            .then(response => response.json())
            .then((result) => {
                user = result[0]
                document.getElementById('input-nama-user').value = user.nama_user
                document.getElementById('input-email-user').value = user.email_user
                document.getElementById('input-username').value = user.username
            })
            .catch(error => console.log('error', error));
    }
}

function userUpdateUser() {

    const token = document.cookie;
    console.log(token);
    if (token !== "") {

        const split = token.split(".");
        let parsedToken = JSON.parse(atob(split[1]));
        // console.log(parsedToken)
        let username = parsedToken["username"]
        let password = parsedToken["password"]
        // console.log(username)

        const myHeaders = new Headers();
        myHeaders.append("Authorization", "Basic " + btoa(username+":"+password));
        myHeaders.append("Content-Type", "application/json");

        let nama_user = document.getElementById('input-nama-user').value
        let email_user = document.getElementById('input-email-user').value
        let username_user = document.getElementById('input-username').value

        const raw = JSON.stringify({
        "nama_user": nama_user,
        "email_user": email_user,
        "username" : username_user
        });

        const requestOptions = {
        method: 'PUT',
        headers: myHeaders,
        body: raw,
        credential : "include"
        // redirect: 'follow'
        };

        fetch("http://127.0.0.1:5000/user/update", requestOptions)
        .then(response => response.json())
        .then((result) => {
            alert("Update Sukses")
            console.log(result)
        })
        .catch(error => console.log('error', error));
    }
}