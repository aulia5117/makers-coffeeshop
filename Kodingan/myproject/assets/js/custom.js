// JS For All Pages

function checkCookie() {
    const token = document.cookie;
    // console.log(token);
    if (token !== "") {
        document.getElementById('loginbutton').style.display = "none";
        const split = token.split(".");
        let parsedToken = JSON.parse(atob(split[1]));
        console.log(parsedToken)
        let username = parsedToken["username"]
        // console.log(username)
        let userLabel = document.getElementById('userprofile').lastElementChild;
        userLabel.innerHTML = username;
    } else {
        document.getElementById('userprofile').style.display = "none";
    }
}

function movePage() {
    location.href = 'login.html'
  }

function logout() {
    document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    location.reload()
}