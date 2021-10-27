/*
Комментарий сверху чтобы код не прилипал к верхней границе)))
JS сорян
 */


document.addEventListener("DOMContentLoaded", admin_panel_loaded);
let goods_categories;
let current_goods_category;
let has_popups = false;  // Чтобы кучу попытов не открывало. Наверное так это делается, хз :)


function GoodsItem(id, name, description, price, category, img_path) {
    this.id = id;
    this.name = name;
    this.description = description;
    this.price = price;
    this.category = category;
    this.img_path = img_path;
}

function admin_panel_loaded() {
    console.log("Admin Panel page loaded");

    // load category list to select dropdown
    let goods_category_select = document.getElementById("goods_category_select");
    get_categories().then(
        categories => {
            goods_categories = categories
            // current_goods_category = Object.values(categories)[0]
            Object.keys(categories).forEach(
                category => {
                    let opt = document.createElement('option');
                    opt.value = category;
                    opt.innerHTML = category;
                    goods_category_select.appendChild(opt);
                }
            )
            current_goods_category = goods_categories[goods_category_select.value]
        }
    );  // подтягивает список категорий с бека для отображения dropdown списка

    goods_category_select.addEventListener('change', on_category_select);
    addCard();
}

function on_category_select(event) {
    let category_name = event.target.value;
    current_goods_category = goods_categories[category_name];
    get_goods_by_category(current_goods_category).then(
        goods => console.log(goods)
    )
}


function addCard() {
    let goods_cards_div = document.getElementById("goods_cards_div");
    let card = document.createElement("div");
    card.className = "goods_item_card";
    let img = document.createElement("img");
    img.src = "../../static/pictures/plus-icon-black-2.png";
    card.appendChild(img);

    let edit_btn = document.createElement("button");
    edit_btn.value = "Edit";
    card.appendChild(edit_btn);
    goods_cards_div.appendChild(card);
    card.addEventListener("click", on_add_card_click);
}
/*
    Тут каша потомучто я не знаю как делить js код на части
 */
function on_add_card_click(event) {
    has_popups ? console.log("Попыт уже открыт") : call_add_goods_item_popup()
}

function call_add_goods_item_popup() {
    console.log("Adding card")
    let popup_div = document.createElement("div");
    popup_div.className = "popup_goods_item_edit";
    let input_name = document.createElement("input");
    input_name.placeholder = "Name";
    let input_description = document.createElement("input");
    input_description.placeholder = "Description";
    let input_price = document.createElement("input");
    input_price.placeholder = "Price";
    let input_image = document.createElement("input");
    input_image.type = "file"

    // input_name.placeholder = "Category";
    let btn_div = document.createElement("div");
    btn_div.className = "btn_div"
    let close_btn = document.createElement("div");
    close_btn.className = "div-button"
    close_btn.textContent = "Close";
    let save_btn = document.createElement("div");
    save_btn.className = "div-button"
    save_btn.textContent = "Save";
    close_btn.addEventListener("click", card_close);
    save_btn.addEventListener("click", card_save);
    btn_div.append(close_btn, save_btn)

    popup_div.append(input_name, input_description, input_price, input_image, btn_div)

    function card_save() {
        let name = input_name.value;
        let description = input_description.value;
        let price = parseFloat(input_price.value);
        let img = input_image.files[0];
        console.log("Category" + current_goods_category)
        let item = new GoodsItem(0, name, description, price, current_goods_category, img)  // как это работает? хз
        console.log("Saving item: " + JSON.stringify(item));

        upload_picture(img).then(
            data => {
                console.log(data);
                item.img_path = data['img_path'];
                add_goods_item(item).then(
                    data => {
                        let item_id = data['item_id'];
                        console.log("new goods item: " + item_id);
                        // update cards later
                    }
                );
            }
        );
        has_popups = false;
        popup_div.remove();

    }

    function card_close() {
        has_popups = false;
        popup_div.remove();
    }

    document.addEventListener('keydown', (event) => {
        // с горячими клавишами попизже
        let name = event.key;
        if (name === "Enter") {
            card_save()
        } else if (name === "Escape") {
            card_close()
        }
    }, false);

    let goods_cards_div = document.getElementById("goods_cards_div");
    goods_cards_div.appendChild(popup_div)
    has_popups = true;
    // document.appendChild(popup_div)
}

function draw_cards() {
    // request item goods by category
    // clean previous cards div
    // for each draw card
}


// ------------------ api methods ----------
async function postData(url = '', data = {}) {
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    redirect: 'follow', // manual, *follow, error
    body: JSON.stringify(data)
  });
  return response.json();
}

async function get_categories() {
    // console.log(categories);
    return postData("/api/get_categories");
}


async function get_goods_by_category(category) {
    // console.log(goods);
    return postData("/api/get_goods_by_category", {"category": category});
}

async function add_goods_item(item) {
    // item - GoodsItem obj
    return postData("/admin/add_goods_item", {
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "img_path": item.img_path,
        "category": item.category,
    });
}

async function upload_picture(file) {
    // more info https://developer.mozilla.org/ru/docs/Web/API/File/Using_files_from_web_applications
    console.log("uploading file")
    if (file === undefined) {
        return ""
    }
    let formData = new FormData();

    formData.append("picture", file);
    let response = await fetch('/admin/upload_picture', {method: "POST", body: formData});
    return response.json()

}

