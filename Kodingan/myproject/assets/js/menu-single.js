function getItemById() {
    const requestOptions = {
        method: 'GET'
        // redirect: 'follow'
      }
     
    let linkURL = String(location.search)
    sliceUjung = linkURL.split("=")
    valueUjung = sliceUjung[1]

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