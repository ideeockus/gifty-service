/*
Комментарий сверху чтобы код не прилипал к верхней границе)))
JS сорян
 */

document.addEventListener("DOMContentLoaded", admin_panel_loaded);

function admin_panel_loaded() {
    console.log("Admin Panel page loaded");

    // load category list to select dropdown
    let goods_category_select = document.getElementById("goods_category_select");
    get_categories().then(
        categories => {
            console.log("Got categories: "+categories)
            categories.forEach(
                category => {
                    let opt = document.createElement('option');
                    opt.value = category;
                    opt.innerHTML = category;
                    goods_category_select.appendChild(opt);
                }
            )
        }

    );
}

async function postData(url = '', data = {}) {
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    redirect: 'follow', // manual, *follow, error
    body: JSON.stringify(data) // body data type must match "Content-Type" header
  });
  // console.log(response)
  // console.log(await response.text())
  return response.json(); // parses JSON response into native JavaScript objects
}

async function get_categories() {
    let categories = postData("/api/get_categories");
    // console.log(categories);
    return categories;
}


async function get_goods_by_category() {
    let goods = postData("/api/get_goods_by_category");
    console.log(goods);
    return goods;
}

