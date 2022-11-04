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

function getKategori() {
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