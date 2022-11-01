function getItem() {
    const requestOptions = {
        method: 'GET',
        redirect: 'follow'
      };
      
      fetch("http://127.0.0.1:5000/get_all_item", requestOptions)
        .then(response => response.json())
        .then(result => {
            // console.log(result)
            let text = "";
            result.forEach(myFunction);
            document.getElementById("menu-parent").innerHTML = text;
             
            function myFunction(item) {
              text += 
               `<div class="col-md-4">
                        <div class="card mb-4 product-wap rounded-0">
                            <a href="#" onclick="pageItem(${item.item_id})" class="text-decoration-none">
                            <span id="itemId${item.item_id}" hidden>${item.item_id}</span>
                            <div class="card rounded-0">
                                <img class="card-img rounded-0 img-fluid" src="assets/img/coffee-sample.jpg">
                                <div class="card-img-overlay rounded-0 product-overlay d-flex align-items-center justify-content-center"></div>
                            </div>
                            <div class="card-body text-center">
                                <p class="h3 text-decoration-none">${item.nama_item}</p>
                                <p class="text-center mb-0">IDR ${item.harga_item}</p>
                            </div>
                        </div>
                        </a>
                    </div>` 
            }
        })
        .catch(error => console.log('error fetching', error));
}

function pageItem(param) {
    let a = document.getElementById('itemId'+param).textContent
    location.href = "menu-single.html?id="+param+""
    console.log(a)
}