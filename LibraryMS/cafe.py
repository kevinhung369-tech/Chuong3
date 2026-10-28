import math
from datetime import datetime
from flask import Flask, abort, render_template, request

app = Flask(__name__)

SHOP = {
    "name": "Cà phê Sông Hương",
    "address": "12 Lê Lợi, Huế",
    "phone": "0886025408",
    "open": 7,
    "close": 22,
}

PROMOTIONS = [
    "Giảm 10% cho sinh viên",
    "Mua 2 tặng 1 vào thứ Hai",
]

# 7 món theo đề bài
MENU = [
    {
        "id": 1,
        "name": "cà phê đen",
        "price": 20000,
        "image": "ca-phe-den.jpg",
        "available": True,
    },
    {
        "id": 2,
        "name": "cà phê sữa",
        "price": 22000,
        "image": "ca-phe-sua.jpg",
        "available": True,
    },
    {
        "id": 3,
        "name": "bạc xỉu",
        "price": 30000,
        "image": "bac-xiu.jpg",
        "available": False,
    },
    {
        "id": 4,
        "name": "trà đào",
        "price": 25000,
        "image": "tra-dao.jpg",
        "available": True,
    },
    {
        "id": 5,
        "name": "trà sữa",
        "price": 28000,
        "image": "tra-sua.jpg",
        "available": True,
    },
    {
        "id": 6,
        "name": "nước ép cam",
        "price": 35000,
        "image": "nuoc-ep-cam.jpg",
        "available": True,
    },
    {
        "id": 7,
        "name": "sinh tố bơ",
        "price": 40000,
        "image": "sinh-to-bo.jpg",
        "available": True,
    },
]


@app.template_filter("vnd")
def format_vnd(value):
    return f"{value:,}".replace(",", ".") + " đ"


# 1. Trang chủ
@app.route("/")
def index():
    gio_param = request.args.get("gio")
    if gio_param is not None:
        try:
            current_hour = int(gio_param)
        except ValueError:
            current_hour = datetime.now().hour
    else:
        current_hour = datetime.now().hour

    is_open = SHOP["open"] <= current_hour < SHOP["close"]

    return render_template(
        "index.html",
        shop=SHOP,
        promotions=PROMOTIONS,
        current_hour=current_hour,
        is_open=is_open,
    )


# 2. Trang Thực đơn với Phân trang
@app.route("/menu")
def show_menu():
    page_param = request.args.get("page", 1)

    # Xử lý nếu page_param không phải là số (VD: /menu?page=abc -> coi như trang 1)
    try:
        page = int(page_param)
    except ValueError:
        page = 1

    per_page = 3  # Mỗi trang 3 món
    total_items = len(MENU)
    pages = math.ceil(total_items / per_page) if total_items > 0 else 1

    # Kiểm tra trang hợp lệ: nếu page < 1 hoặc page > pages thì trả về lỗi 404
    if page < 1 or (pages > 0 and page > pages):
        abort(404)

    # Cắt danh sách món theo trang
    start = (page - 1) * per_page
    end = start + per_page
    items_on_page = MENU[start:end]

    return render_template("menu.html", items=items_on_page, page=page, pages=pages)


# 3. Trang Liên hệ
@app.route("/contact")
def contact():
    return render_template("contact.html", shop=SHOP)


# 4. Xử lý Lỗi 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
