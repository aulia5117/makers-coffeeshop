function getItemById() {

    let linkURL = String(location.search)
    let sliceUjung = linkURL.split("=")
    let valueUjung = sliceUjung[1]

    const requestOptions = {
        method: 'GET'
        // redirect: 'follow'
      }
     
      fetch(`http://127.0.0.1:5000/get_item/${valueUjung}` , requestOptions)
        .then(response => response.json())
        .then(result => {
            // console.log(result)
            objek = result[0]
            // console.log(objek)
            document.getElementById('single-nama-item').innerHTML = objek.nama_item
            document.getElementById('single-harga-item').innerHTML = "IDR " + objek.harga_item
            document.getElementById('single-deskripsi').innerHTML = objek.deskripsi
            document.getElementById('item-quantity').setAttribute("max",objek.jumlah_item)
            document.getElementById('single-item-id').innerHTML = objek.item_id
        })
        .catch(error => console.log('error fetching', error));
}

function addToCart() {

  const token = document.cookie;
  // console.log(token);
  if (token !== "") {
      const split = token.split(".");
      let parsedToken = JSON.parse(atob(split[1]));
      // console.log(parsedToken)
      let username = parsedToken["username"]
      let password = parsedToken["password"]
      // console.log(username)

    document.getElementById('wadah-value').innerHTML = document.getElementById('item-quantity').value
    let value = document.getElementById('wadah-value').innerHTML
    // console.log(value)

    let myHeaders = new Headers();
    myHeaders.append("Authorization", "Basic " + btoa(username+":"+password));
    myHeaders.append("Content-Type", "application/json");

    let itemIdValue = document.getElementById('single-item-id').innerHTML
    let jumlahBarang = document.getElementById('wadah-value').innerHTML
    // console.log(typeof itemIdValue)
    // console.log(typeof jumlahBarang)

    let raw = JSON.stringify({
      "item_id" : itemIdValue,
      "jumlah_barang" : value
    });

    const requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: raw
      // redirect: 'follow'
    };

    fetch("http://127.0.0.1:5000/order/add_cart_order", requestOptions)
      .then(response => response.json())
      .then((result) => {
        console.log(result)
        alert("Pesanan Masuk Keranjang")
        location.reload()
      })
      .catch(error => console.log('error', error));
  } else {
    alert("Silahkan Login")
    location.href = 'login.html'
  } 
}

function buyToCart() {

  const token = document.cookie;
  // console.log(token);
  if (token !== "") {
      const split = token.split(".");
      let parsedToken = JSON.parse(atob(split[1]));
      // console.log(parsedToken)
      let username = parsedToken["username"]
      let password = parsedToken["password"]
      // console.log(username)

    document.getElementById('wadah-value').innerHTML = document.getElementById('item-quantity').value
    let value = document.getElementById('wadah-value').innerHTML
    // console.log(value)

    let myHeaders = new Headers();
    myHeaders.append("Authorization", "Basic " + btoa(username+":"+password));
    myHeaders.append("Content-Type", "application/json");

    let itemIdValue = document.getElementById('single-item-id').innerHTML
    let jumlahBarang = document.getElementById('wadah-value').innerHTML
    // console.log(typeof itemIdValue)
    // console.log(typeof jumlahBarang)

    let raw = JSON.stringify({
      "item_id" : itemIdValue,
      "jumlah_barang" : value
    });

    const requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: raw
      // redirect: 'follow'
    };

    fetch("http://127.0.0.1:5000/order/add_cart_order", requestOptions)
      .then(response => response.json())
      .then((result) => {
        console.log(result)
        alert("Pesanan Masuk Keranjang")
        location.reload()
      })
      .catch(error => console.log('error', error));
  } else {
    alert("Silahkan Login")
    location.href = 'login.html'
  } 
}