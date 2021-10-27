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
    get_categories().then(  // подтягивает список категорий с бека для отображения dropdown списка
        categories => {
            goods_categories = categories
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
    );
}

function on_category_select(event) {
    let category_name = event.target.value;
    current_goods_category = goods_categories[category_name];
    draw_cards();
}


function draw_add_card() {
    /* Нарисовать карточку добавления */
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

function call_card_popup(card_elem) {
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

    popup_div.append(input_name, input_description, input_price, input_image);

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
    /* Попыт добавления нового товара */
    console.log("Adding item")
    let [input_name, input_description, input_price, input_image, popup_div] = call_card_popup(null);

    // кнопки попыта (круче чем симпл димпл)
    let btn_div = document.createElement("div");
    btn_div.className = "btn_div"
    // копка закрытия (эх почему я не знаю реак)
    let close_btn = document.createElement("div");
    close_btn.className = "div-button";
    close_btn.textContent = "Close";
    close_btn.addEventListener("click", card_close);
    // кнопка сохранения
    let save_btn = document.createElement("div");
    save_btn.className = "div-button";
    save_btn.textContent = "Save";
    save_btn.addEventListener("click", card_save);
    // кнопка импорта товаров с экселя
    let xlx_import_btn = document.createElement("div");
    xlx_import_btn.className = "div-button";
    xlx_import_btn.textContent = "Import xlx";
    xlx_import_btn.addEventListener("click", import_goods_xlx);
    btn_div.append(xlx_import_btn, close_btn, save_btn);
    popup_div.appendChild(btn_div);

    popup_div.addEventListener('keydown', (event) => {
        // с горячими клавишами попизже
        let name = event.key;
        if (name === "Enter") {
            card_save()
        } else if (name === "Escape") {
            card_close()
        }
    }, false);

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

    function import_goods_xlx() {
        card_close();
        let xlx_input_field = document.createElement('input');
        xlx_input_field.type = 'file';

        xlx_input_field.addEventListener("change", (event) => {
           let xlx_file = event.target.files[0];
           if (xlx_file === undefined) {
               return;
           }
           import_xlx_goods(xlx_file).then(
               response => {
                   let status = response['status'];
                   console.log("Import goods xlx. Status: " + status);
                   draw_cards();
               }
           );
        });

        xlx_input_field.click();
    }
}

function draw_cards() {
    /* Отрисовать карточки товара */
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
    /* нарисовать карточку товара (1шт) */
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
    /* Обработчик нажатия на карточку товара */
    console.log("Editing item");
    let card = event.currentTarget;
    // console.log(card);
    let [input_name, input_description, input_price, input_image, popup_div] = call_card_popup(card);
    console.log(popup_div);

    let btn_div = document.createElement("div");
    btn_div.className = "btn_div"
    // копка закрытия (эх почему я не знаю реак)
    let close_btn = document.createElement("div");
    close_btn.className = "div-button";
    close_btn.textContent = "Close";
    close_btn.addEventListener("click", card_close);
    // кнопка сохранения
    let save_btn = document.createElement("div");
    save_btn.className = "div-button";
    save_btn.textContent = "Save";
    save_btn.addEventListener("click", card_save);
    // кнопка удаления товара
    let remove_goods_item_btn = document.createElement("div");
    remove_goods_item_btn.className = "div-button";
    remove_goods_item_btn.textContent = "Delete";
    remove_goods_item_btn.addEventListener("click", on_remove_goods_item_click);
    btn_div.append(remove_goods_item_btn, close_btn, save_btn);
    popup_div.appendChild(btn_div);

    popup_div.addEventListener('keydown', (event) => {
        // с горячими клавишами попизже
        let name = event.key;
        if (name === "Enter") {
            card_save()
        } else if (name === "Escape") {
            card_close()
        }
    }, false);


    function card_save() {
        let id = parseInt(card.dataset.id);
        let name = input_name.value;
        let description = input_description.value;
        let price = parseFloat(input_price.value);
        let img = input_image.files[0];
        let img_path = (img === undefined) ? card.dataset.img_path : "";
        console.log(id, name, description, price, img);
        let item = new GoodsItem(id, name, description, price, current_goods_category, img_path);
        console.log("Editing item: " + JSON.stringify(item));

        // лучше не смотрите на эту штуку
        if (img !== undefined) {
            upload_picture(img).then(
                data => {
                    console.log(data);
                    item.img_path = data['img_path'];
                    edit_goods_item(item).then(
                        data => {
                            let status = data['status'];
                            console.log("edit goods item. success: " + status);
                            draw_cards()
                        }
                    );
                }
            );
        } else {
            edit_goods_item(item).then(
                    data => {
                        let status = data['status'];
                        console.log("edit goods item. success: " + status);
                        draw_cards()
                    }
                );
        }
        has_popups = false;
        popup_div.remove();
    }

    function card_close() {
        has_popups = false;
        popup_div.remove();
    }

    function on_remove_goods_item_click() {
        card_close();
         let item_id = parseInt(card.dataset.id);
        remove_goods_item(item_id).then(response => {
            let status = response['status'];
            console.log("Remove goods item. Status: " + status);
            draw_cards();
        });
    }
}


// ------------------ api methods -----------------
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

async function remove_goods_item(item_id) {
    return postData("/admin/remove_goods_item", {
        "id": item_id,
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

async function import_xlx_goods(file) {
    console.log("importing goods from xlx")
    let formData = new FormData();

    formData.append("goods_xlx", file);
    let response = await fetch('/admin/import_xlx_goods', {method: "POST", body: formData});
    return response.json()
}

