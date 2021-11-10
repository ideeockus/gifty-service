document.addEventListener("DOMContentLoaded", orders_page_loaded);
let has_popups = false;

function GoodsItem(id, name, description, price, category, img_path) {
    this.id = id;
    this.name = name;
    this.description = description;
    this.price = price;
    this.category = category;
    this.img_path = img_path;
}

function Order(id, box_type, customer_name, customer_email, customer_phone, customer_address, creation_date,
               comment, goods) {
    this.id = id;
    this.box_type = box_type;
    this.customer_name = customer_name;
    this.customer_email = customer_email;
    this.customer_phone = customer_phone;
    this.customer_address = customer_address;
    this.creation_date = creation_date;
    this.comment = comment;
    this.goods = goods;
}

function orders_page_loaded() {
    console.log("Orders Page loaded");

    // load category list to select dropdown
    let orders_table = document.getElementById("orders_table");
    get_orders().then(  // подтягивает список категорий с бека для отображения dropdown списка
        response => {
            console.log(response)
            let orders = response['orders']
            orders.forEach(
                order => {
                    add_order_record(order);
                }
            )
        }
    );
}

function add_order_record(order) {
    let orders_table = document.getElementById("orders_table");
    let orders_table_body = orders_table.getElementsByTagName('tbody')[0]
    let order_row = orders_table_body.insertRow()

    let status = order_row.insertCell(0)
    status.innerHTML = order['status']

    let name = order_row.insertCell()
    name.innerHTML = order['customer_name']

    let email = order_row.insertCell()
    email.innerHTML = order['customer_email']

    let phone = order_row.insertCell()
    phone.innerHTML = order['customer_phone']
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

async function get_orders() {
    return postData("/admin/get_orders");
}