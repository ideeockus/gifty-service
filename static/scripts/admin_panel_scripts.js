/*
Комментарий сверху чтобы код не прилипал к верхней границе)))
JS сорян
 */


document.addEventListener("DOMContentLoaded", admin_panel_loaded);
let goods_categories;
let current_goods_category;
let has_popups = false;  // Чтобы кучу попытов не открывало. Наверное так это делается, хз :)
let pictures_dir = "/static/pictures/";
let add_card_img = "/static/pictures/plus4.png";


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
            goods_category_select.addEventListener('change', on_category_select);
            draw_cards();
        }
    );  // подтягивает список категорий с бека для отображения dropdown списка
}

function on_category_select(event) {
    let category_name = event.target.value;
    current_goods_category = goods_categories[category_name];
    draw_cards();
}


function draw_add_card() {
    let goods_cards_div = document.getElementById("goods_cards_div");
    let card = document.createElement("div");
    card.className = "goods_item_card";
    let img = document.createElement("img");
    img.src = add_card_img;
    card.appendChild(img);

    let name_p = document.createElement("p");
    name_p.innerHTML = "Add";
    name_p.className = "name_p";
    card.appendChild(name_p);

    goods_cards_div.appendChild(card);
    card.addEventListener("click", on_add_card_click);
}
/*
    Тут каша потомучто я не знаю как делить js код на части
 */
function on_add_card_click(event) {
    has_popups ? console.log("Попыт уже открыт") : call_add_goods_item_popup()
}

function call_card_popup(card_elem, save_btn_listener, close_btn_listener) {
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
    let btn_div = document.createElement("div");
    btn_div.className = "btn_div"
    let close_btn = document.createElement("div");
    close_btn.className = "div-button"
    close_btn.textContent = "Close";
    let save_btn = document.createElement("div");
    save_btn.className = "div-button"
    save_btn.textContent = "Save";
    close_btn.addEventListener("click", close_btn_listener);
    save_btn.addEventListener("click", save_btn_listener);
    btn_div.append(close_btn, save_btn);

    popup_div.append(input_name, input_description, input_price, input_image, btn_div)

    document.addEventListener('keydown', (event) => {
        // с горячими клавишами попизже
        let name = event.key;
        if (name === "Enter") {
            save_btn_listener()
        } else if (name === "Escape") {
            close_btn_listener()
        }
    }, false);

    let goods_cards_div = document.getElementById("goods_cards_div");
    goods_cards_div.appendChild(popup_div)
    has_popups = true;

    if (card_elem !== null) {
        let name = card_elem.dataset.name;
        let description = card_elem.dataset.description;
        let price = card_elem.dataset.price;

        input_name.value = name;
        input_description.value = description;
        input_price.value = price;

    }

    return [input_name, input_description, input_price, input_image, popup_div]
}

function call_add_goods_item_popup() {
    console.log("Adding item")
    let [input_name, input_description, input_price, input_image, popup_div] = call_card_popup(null, card_save, card_close);

    function card_save() {
        let name = input_name.value;
        let description = input_description.value;
        let price = parseFloat(input_price.value);
        let img = input_image.files[0];
        let item = new GoodsItem(0, name, description, price, current_goods_category, "")  // как это работает? хз
        console.log("Saving item: " + JSON.stringify(item));

        upload_picture(img).then(
            data => {
                console.log(data);
                item.img_path = data['img_path'];
                add_goods_item(item).then(
                    data => {
                        let item_id = data['item_id'];
                        console.log("new goods item: " + item_id);
                        draw_cards();
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
}

function draw_cards() {
    let goods_cards_div = document.getElementById("goods_cards_div");
    let saved_scroll_y = window.scrollY;  // save scroll position
    goods_cards_div.innerHTML = ""; //clean
    console.log("Request items for category "+ current_goods_category)
    get_goods_by_category(current_goods_category).then(
        goods_list => {
            console.log("Goods: " + goods_list);
            goods_list.forEach( item => {
                let goods_item = new GoodsItem(item.id,  item.name,
                    item.description,  item.price,  item.category,  item.img_path);
                draw_goods_item_card(goods_item);
            });
            draw_add_card();
            window.scroll(0, saved_scroll_y);
        }
    );

}

function draw_goods_item_card(item) {
    // item - GoodsItem
    let goods_cards_div = document.getElementById("goods_cards_div");
    let card = document.createElement("div");
    card.className = "goods_item_card";
    let img = document.createElement("img");
    img.src = pictures_dir + item.img_path;
    card.appendChild(img);

    // store item data
    card.dataset.id = item.id;
    card.dataset.name = item.name;
    card.dataset.description = item.description;
    card.dataset.price = item.price;
    card.dataset.category = item.category;
    card.dataset.img_path = item.img_path;

    let name_p = document.createElement("p");
    name_p.innerHTML = item.name; // js что ты делаеш
    name_p.className = "name_p";
    card.appendChild(name_p);
    let description_p = document.createElement("p");
    description_p.innerHTML = item.description + " | " + Math.round(item.price * 100) / 100;
    description_p.className = "description_p";
    card.appendChild(description_p);

    goods_cards_div.appendChild(card);
    card.addEventListener("click", on_goods_item_card_click);
}

function on_goods_item_card_click(event) {
    console.log("Editing item");
    let card = event.currentTarget;
    console.log(card);
    let [input_name, input_description, input_price, input_image, popup_div] = call_card_popup(card, card_save, card_close);

    function card_save() {
        let name = input_name.value;
        let description = input_description.value;
        let price = parseFloat(input_price.value);
        let img = input_image.files[0];
        let item = new GoodsItem(0, name, description, price, current_goods_category, img)  // как это работает? хз
        console.log("Editing item: " + JSON.stringify(item));

        upload_picture(img).then(
            data => {
                console.log(data);
                item.img_path = data['img_path'];
                edit_goods_item(item).then(
                    data => {
                        let item_id = data['item_id'];
                        console.log("edit goods item: " + item_id);
                        draw_cards()
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

async function edit_goods_item(item) {
    // item - GoodsItem obj
    return postData("/admin/edit_goods_item", {
        "id": item.id,
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

