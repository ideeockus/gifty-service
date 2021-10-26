export const name = "models";

export function GoodsItem(id, name, description, price, category, img_path) {
    this.id = id;
    this.name = name;
    this.description = description;
    this.price = price;
    this.category = category;
    this.img_path = img_path;
}  // а может стоит typescript изучить? Я конечно не фронтендер, но все же с js связываться не хочется

export { GoodsItem }