// JS For All Pages

function checkCookie() {
    const token = document.cookie;
    // console.log(token);
    if (token !== "") {
        document.getElementById('loginbutton').style.display = "none";
        const split = token.split(".");
        let parsedToken = JSON.parse(atob(split[1]));
        // console.log(parsedToken)
        let username = parsedToken["username"]
        let password = parsedToken["password"]
        // console.log(username)
        let userLabel = document.getElementById('userprofile').lastElementChild;
        userLabel.innerHTML = username;

        let requestOptions = {
            method: 'POST',
            headers: {
                'Authorization' : "Basic " + btoa(username + ":" + password)
            },
            // redirect: 'follow',
            credential: 'include'
        };
      
        fetch("http://127.0.0.1:5000/order/get_cart_order", requestOptions)
        .then(response => response.json())
        .then(result => {
        //   console.log(result)
          document.getElementById('cart-count').innerHTML = result.length
        })
        .catch(error => console.log('error', error));

    } else {
        document.getElementById('userprofile').style.display = "none";
    }
}

function movePage() {
    location.href = 'login.html'
  }

// function notifCart() {
   
//     const token = document.cookie;
//     if (token !== "") {
//         const split = token.split(".");
//         let parsedToken = JSON.parse(atob(split[1]));
//         // console.log(parsedToken)
//         let username = parsedToken["username"]
//         let password = parsedToken["password"]
//         // console.log(username)
        
//         let requestOptions = {
//           method: 'POST',
//           headers: {
//               'Authorization' : "Basic " + btoa(username + ":" + password)
//           },
//           // redirect: 'follow',
//           credential: 'include'
//       };
    
//       fetch("http://127.0.0.1:5000/order/get_cart_order", requestOptions)
//       .then(response => response.json())
//       .then(result => {
//         console.log(result)
//         document.getElementById('cart-count').innerHTML = result.length
//       })
//       .catch(error => console.log('error', error));
//     }
// }

function logout() {
    document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    location.reload()
}

// function cancelOrder(id) {
//     const token = document.cookie;
//     if (token !== "") {

//         const split = token.split(".");
//         let parsedToken = JSON.parse(atob(split[1]));
//         console.log(parsedToken)
//         let username = parsedToken["username"]
//         let password = parsedToken["password"]
//         let userId = parsedToken["id"]
//         // console.log(username)

//         let order_id = id
//         console.log(order_id)
    
//         const myHeaders = new Headers();
//         myHeaders.append("Authorization", "Basic " + btoa(username+":"+password));
//         myHeaders.append("Content-Type", "application/json");

        
//         const raw = JSON.stringify({
//         "order_id": order_id
//         });

//         var requestOptions = {
//         method: 'DELETE',
//         // headers: myHeaders,
//         body: raw,
//         redirect: 'follow'
//         };

//         fetch("http://127.0.0.1:5000/order/cancel_order", requestOptions)
//         .then(response => response.json())
//         .then((result) => {
//             console.log(result)
//             alert("Order Berhasil di cancel")
//             location.reload()
//         })
//         .catch(error => console.log('error', error));
//     }
// }

function getOrderDetail(id) {
        // alert(id)

        let idValue = id
        // console.log(idValue)
        const requestOptions = {
          method: 'GET'
          // redirect: 'follow'
        };
      
      fetch(`http://127.0.0.1:5000/order/get_orderdetail/${idValue}`, requestOptions)
        .then(response => response.json())
        .then((result) => {
            // console.log(result)
            let modalOrderDetail = "";
            let i = 1
            result.forEach(myFunction);
            document.getElementById("modal-order-detail").innerHTML = modalOrderDetail;

            
            function myFunction(order) {
                modalOrderDetail += 
                    `<tr>
                        <th scope="row">Item ${i}</th>
                        <td>${order.nama_item}</td>
                        <td>${order.jumlah_subbarang} Barang</td>
                        <td>IDR ${order.subtotal_harga}</td>
                    </tr>`
                    i++
              
        }})
        .catch(error => console.log('error fetching', error));
}