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

function userGetExistingOrder() {
    const token = document.cookie;
    // console.log(token);
    if (token !== "") {

        const split = token.split(".");
        let parsedToken = JSON.parse(atob(split[1]));
        console.log(parsedToken)
        let username = parsedToken["username"]
        let password = parsedToken["password"]
        let userId = parsedToken["id"]
        // console.log(username)

        const requestOptions = {
            method: 'GET',
            redirect: 'follow'
        };
      
      fetch(`http://127.0.0.1:5000/order/get_order/${userId}`, requestOptions)
        .then(response => response.json())
        .then((result) => {
            console.log(result)
            let order_pending = "";
            let order_aktif = "";
            let i = 1
            let j = 1
            result.forEach(myFunction);
            document.getElementById("order-pending").innerHTML = order_pending;
            document.getElementById("order-aktif").innerHTML = order_aktif;
            
            function myFunction(user) {
            if (user.order_status === 'pending') {
                order_pending += 
                    `<tr>
                            <th scope="row">${i}</th>
                            <td>${user.order_status}
                            <span hidden>${user.user_id}</span>
                            <span hidden>${user.order_id}</span>
                            </td>
                            <td>${user.order_date}</td>
                            <td>${user.jumlah_barang} Barang</td>
                            <td>IDR ${user.total_harga}</td>
                            <td>
                                <button type="button" id="${user.order_id}" onclick="function(this.id)" class="btn btn-info btn-sm me-1" data-bs-toggle="modal"
                                data-bs-target="#modalUpdate">
                                Detail
                                <span id="item-id" hidden>${user.order_id}</span>
                                </button>
                                <button type="button" id="${user.order_id}" onclick="function(this.id)" class="btn btn-danger btn-sm me-1" data-bs-toggle="modal"
                                data-bs-target="#modalUpdate">
                                Cancel
                                <span id="item-id" hidden>${user.order_id}</span>
                                </button>
                            </td>
                    </tr>`
                    i++
            } else if (user.order_status === 'activate') {
                order_aktif += 
                    `<tr>
                            <th scope="row">${j}</th>
                            <td>${user.order_status}
                            <span hidden>${user.user_id}</span>
                            <span hidden>${user.order_id}</span>
                            </td>
                            <td>${user.order_date}</td>
                            <td>${user.jumlah_barang} Barang</td>
                            <td>IDR ${user.total_harga}</td>
                            <td>
                                <button type="button" id="${user.order_id}" onclick="function(this.id)" class="btn btn-info btn-sm me-1" data-bs-toggle="modal"
                                data-bs-target="#modalUpdate">
                                Detail
                                <span id="item-id" hidden>${user.order_id}</span>
                                </button>
                            </td>
                    </tr>`
                    j++
            }
             
            
        }
        })
        .catch(error => console.log('error', error));

    }
}

function userGetOrderHistory() {
    const token = document.cookie;
    // console.log(token);
    if (token !== "") {

        const split = token.split(".");
        let parsedToken = JSON.parse(atob(split[1]));
        console.log(parsedToken)
        // let username = parsedToken["username"]
        // let password = parsedToken["password"]
        let userId = parsedToken["id"]
        // console.log(username)

        const requestOptions = {
            method: 'GET',
            redirect: 'follow'
        };
      
      fetch(`http://127.0.0.1:5000/order/get_order/${userId}`, requestOptions)
        .then(response => response.json())
        .then((result) => {
            console.log(result)
            let order_history = "";
            let i = 1
            result.forEach(myFunction);
            document.getElementById("order-history").innerHTML = order_history;

            
            function myFunction(user) {
            if (user.order_status === 'completed') {
                order_history += 
                    `<tr>
                            <th scope="row">${i}</th>
                            <td>${user.order_date}
                                <span hidden>${user.user_id}</span>
                                <span hidden>${user.order_id}</span>
                            </td>
                            <td>${user.jumlah_barang} Barang</td>
                            <td>IDR ${user.total_harga}</td>
                            <td><button type="button" id="${user.order_id}" onclick="function(this.id)" class="btn btn-info btn-sm me-1" data-bs-toggle="modal"
                            data-bs-target="#modalUpdate">
                            Detail
                            <span id="item-id" hidden>${user.order_id}</span>
                          </button></td>
                    </tr>`
                    i++
            }              
            
        }
        })
        .catch(error => console.log('error', error));

    }
}
