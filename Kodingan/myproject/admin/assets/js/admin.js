function getTop5User() {
    
    const requestOptions = {
        method: 'GET'
        // redirect: 'follow'
      };

      fetch("http://127.0.0.1:5000/reporting/top5_user", requestOptions)
        .then(response => response.json())
        .then((result) => {
        console.log(result)
        let text = "";
        let i = 1
        result.forEach(myFunction);
        document.getElementById("top-5-user").innerHTML = text;
         
        function myFunction(user) {
          text += 
           `<tr>
                <th scope="row">${i}</th>
                <td>${user.nama_user}</td>
                <td>${user.email_user}</td>
                <td>${user.total_pembelian} Barang</td>
            </tr>` 
            i++
        }
        })
        .catch(error => console.log('error', error));
}

function getTop5Item() {
    
    const requestOptions = {
        method: 'GET'
        // redirect: 'follow'
      };

      fetch("http://127.0.0.1:5000/reporting/top5_item", requestOptions)
        .then(response => response.json())
        .then((result) => {
        console.log(result)
        let text = "";
        let i = 1
        result.forEach(myFunction);
        document.getElementById("top-5-item").innerHTML = text;
         
        function myFunction(item) {
          text += 
           `<tr>
                <th scope="row">${i}</th>
                <td>${item.nama_item}</td>
                <td>IDR ${item.harga_item}</td>
                <td>${item.jumlah_terbeli} Barang</td>
            </tr>` 
            i++
        }
        })
        .catch(error => console.log('error', error));
}

function adminGetKategori() {
    const requestOptions = {
    method: 'GET',
    redirect: 'follow'
  };
  
  fetch("http://127.0.0.1:5000/get_kategori", requestOptions)
    .then(response => response.json())
    .then((result) => {
      // console.log(result)
      let text = "";
      let i = 1
      result.forEach(myFunction);
      document.getElementById("input-kategori").innerHTML = text;
       
      function myFunction(kategori) {
        text += 
         `<option value="${kategori.kategori_id}">${kategori.nama_kategori}</option>` 
          i++
      }
    })
    .catch(error => console.log('error', error));
}

function postMenu() {
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    let nama_item = document.getElementById('input-nama-item').value
    let deskripsi = document.getElementById('input-deskripsi').value
    let harga_item = document.getElementById('input-harga-item').value
    let jumlah_item = document.getElementById('input-jumlah-item').value
    let kategori_id = document.getElementById('input-kategori').value
    console.log(nama_item)
    console.log(deskripsi)
    // console.log(harga_item)
    // console.log(jumlah_item)
    // console.log(kategori_id)

    let raw = JSON.stringify({
      "nama_item": nama_item,
      "deskripsi": deskripsi,
      "harga_item": harga_item,
      "jumlah_item": jumlah_item,
      "kategori_id": kategori_id
    });

    const requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: raw,
      // redirect: 'follow'
    };

    fetch("http://127.0.0.1:5000/item/add_item", requestOptions)
      .then(response => response.json())
      .then((result) => {
        console.log(result)
        alert("Menu baru telah dimasukkan")
      })
      .catch(error => console.log('error', error));
}

function adminGetAllItem() {

  const requestOptions = {
    method: 'GET',
    redirect: 'follow'
  };
  
  fetch("http://127.0.0.1:5000/get_all_item", requestOptions)
    .then(response => response.json())
    .then(result => {
        // console.log(result)
        let text = "";
        let i = 1
        result.forEach(myFunction);
        document.getElementById("item-table").innerHTML = text;
         
        function myFunction(item) {
          text += 
           `<tr>
                <th scope="row">${i}</th>
                <span id="${item.item_id}" hidden>${item.item_id}</span>
                <td>${item.nama_item}</td>
                <td>IDR ${item.harga_item}</td>
                <td>${item.kategori}</td>
                <td>${item.jumlah_terbeli} Barang</td>
                <td><button type="button" id="${item.item_id}" onclick="adminGetItemModal(this.id)" class="btn btn-info btn-sm me-1" data-bs-toggle="modal"
                data-bs-target="#modalUpdate">
                Update
                <span id="item-id" hidden>${item.item_id}</span>
              </button></td>
            </tr>` 
            i++
        }
    })
    .catch(error => console.log('error fetching', error));
}

function adminGetItemModal(id) {
    // alert(id)

    let idValue = id
    // console.log(idValue)

    const requestOptions = {
      method: 'GET'
      // redirect: 'follow'
    };
  
  fetch(`http://127.0.0.1:5000/get_item/${idValue}`, requestOptions)
    .then(response => response.json())
    .then((result) => {
        console.log(result)
        item = result[0]
        document.getElementById('input-nama-item').value = item.nama_item
        document.getElementById('input-deskripsi').value = item.deskripsi
        document.getElementById('input-harga-item').value = item.harga_item
        document.getElementById('input-jumlah-item').value = item.jumlah_item
        // console.log(item.nama_item)
        document.getElementById("modal-nama-item").innerHTML = "Update Item - " + item.nama_item 
        // document.getElementById("input-nama-item").setAttribute("value",item.nama_item)
        // document.getElementById("input-deskripsi").value = item.deskripsi
        // document.getElementById("input-harga-item").setAttribute("value",item.harga_item)
        // document.getElementById("input-jumlah-item").setAttribute("value",item.jumlah_item)     
          
    })
    .catch(error => console.log('error fetching', error));
}

function adminUpdateMenu() {

  let nama_item = document.getElementById('input-nama-item').value
  let deskripsi = document.getElementById('input-deskripsi').value
  let harga_item = document.getElementById('input-harga-item').value
  // parseInt(harga_item)
  let jumlah_item = document.getElementById('input-jumlah-item').value
  // parseInt(jumlah_item)
  console.log(harga_item,jumlah_item)
  let id = document.getElementById('item-id').innerHTML
  console.log(id)
  
  let myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");
  
  const raw = JSON.stringify({
    "nama_item": nama_item,
    "deskripsi" : deskripsi,
    "harga_item" : harga_item,
    "jumlah_item" : jumlah_item
  });
  
  const requestOptions = {
    method: 'PUT',
    headers: myHeaders,
    body: raw,
    redirect: 'follow'
  };
  
  fetch(`http://127.0.0.1:5000/item/update_item/${id}`, requestOptions)
    .then(response => response.json())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));
}

function adminGetAllOrder() {
  const requestOptions = {
    method: 'GET',
    redirect: 'follow'
  };
  
  fetch("http://127.0.0.1:5000/order/get_all_order", requestOptions)
    .then(response => response.json())
    .then((result) => {
        console.log(result)
        let text = "";
        let i = 1
        result.forEach(myFunction);
        document.getElementById("item-table").innerHTML = text;
         
        function myFunction(item) {
          text += 
           `<tr>
                <th scope="row">${i}</th>
                <td>${item.nama_user}
                  <span hidden>User ID</span>
                </td>
                <td>Order Status
                  <span hidden>Order ID</span>
                </td>
                <td>Waktu Order</td>
                <td>Jumlah Barang</td>
                <td>Total Harga</td>
                <td>Action</td>
            </tr>` 
            i++
        }
    }
    // console.log("a")
    )
    .catch(error => console.log('error', error));
}