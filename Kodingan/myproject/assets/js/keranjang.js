function getKeranjang() {

    const token = document.cookie;
    // console.log(token);
    if (token !== "") {
        const split = token.split(".");
        let parsedToken = JSON.parse(atob(split[1]));
        // console.log(parsedToken)
        let username = parsedToken["username"]
        let password = parsedToken["password"]
        // console.log(username)

        // const myHeaders = new Headers();
        // myHeaders.append('Authorization', 'Basic ' + btoa(username + ":" + password));
        
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
          .then((result) => {
            console.log(result.length)
          let text = "";
          let i = 1
          result.forEach(myFunction);
          document.getElementById("get-keranjang").innerHTML = text;
           
          function myFunction(item) {
            text += 
                      `<ul>
                      <div class="card row" id="item${i}">
                          <div class="card-header">
                              <h6 class="col-lg-7">Item ${i}</h6>
                              <div  style="text-align: right;">
                              <button type="button" class="btn btn-danger ">Delete</button>
                              </div>    
                          </div>
                          <div class="card-body">
                              <div>
                                  <img src="assets/img/coffee-child-sample.jpg" class="img-thumbnail" width="200px" height="200px">
                              </div>
                              <div>
                                  <h5 id="card-nama-item${item.item_id}" class="card-title">${item.nama_item}</h5>
                                  <h6 id="card-harga-item${item.item_id}" class="card-title">${item.total_harga}  
                                  
                                  </h6>
                                  <input id="item-quantity" type="number" value="${item.jumlah_barang}" min="1"/> Barang
                              </div>
                          </div>
                        </div>
                        </ul>` 
                i++
              }
        })
          .catch(error => console.log('error fetching', error));
    }
}

// function getTotalKeranjang() {

// }