// JS For All Pages

function checkCookie() {
    const token = document.cookie;
    console.log(token);
    if (token !== "") {
        document.getElementById('loginbutton').style.display = "none";
        const split = token.split(".");
        let parsedToken = JSON.parse(atob(split[1]));
        console.log(parsedToken)
        let username = parsedToken["username"]
        console.log(username)
        let userLabel = document.getElementById('userprofile').lastElementChild;
        userLabel.innerHTML = username;
    } else {
        document.getElementById('userprofile').style.display = "none";
    }
}

function movePage() {
    location.href = 'login.html'
  }

function notifCart() {
   
    const token = document.cookie;
    if (token !== "") {
        const split = token.split(".");
        let parsedToken = JSON.parse(atob(split[1]));
        // console.log(parsedToken)
        let username = parsedToken["username"]
        let password = parsedToken["password"]
        // console.log(username)

         document.getElementById('cart-count')
        
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
        console.log(result)
        document.getElementById('cart-count').innerHTML = result.length
      })
      .catch(error => console.log('error', error));
    }
}

function logout() {
    document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    location.reload()
}