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
    );  // подтягивает список категорий с бека для отображения dropdown списка

    goods_category_select.addEventListener('change', on_category_select);
    addCard();
}

function on_category_select(event) {
    let category = event.target.value
    get_goods_by_category(category).then(
        goods => console.log(goods)
    )
}


function addCard() {
    let goods_cards_div = document.getElementById("goods_cards_div");
    let card = document.createElement("div")
    card.className = "goods_item_card"
    let img = document.createElement("img")
    img.src = "../../static/pictures/plus-icon-black-2.png"
    card.appendChild(img)

    let edit_btn = document.createElement("button")
    edit_btn.value = "Edit"
    card.appendChild(edit_btn)
    goods_cards_div.appendChild(card)
}


// ------------------ api methods ----------
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
    // console.log(categories);
    return postData("/api/get_categories");
}


async function get_goods_by_category(category) {
    // console.log(goods);
    return postData("/api/get_goods_by_category", {"category": category});
}

