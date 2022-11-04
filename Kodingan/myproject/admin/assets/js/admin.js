function getTop5User() {
    
    const requestOptions = {
        method: 'GET'
        // redirect: 'follow'
      };
      console.log("A")
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
      console.log("A")
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