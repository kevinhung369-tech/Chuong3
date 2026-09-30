from flask import Flask, render_template, request, jsonify, abort
from markupsafe import escape

app = Flask(__name__)

# Khởi tạo dữ liệu mẫu
BOOKS = [
    {
        "id": 1,
        "title": "Cấu trúc dữ liệu",
        "author": "Nguyễn Văn A",
        "year": 2020,
        "category": "Lập trình",
        "available": True,
    },
    {
        "id": 2,
        "title": "Cơ sở dữ liệu",
        "author": "Trần Thị B",
        "year": 2021,
        "category": "Dữ liệu",
        "available": False,
    },
    {
        "id": 3,
        "title": "Flask căn bản",
        "author": "Lê Văn C",
        "year": 2022,
        "category": "Lập trình",
        "available": True,
    },
    {
        "id": 4,
        "title": "Trí tuệ nhân tạo",
        "author": "Phạm Thị D",
        "year": 2023,
        "category": "AI",
        "available": True,
    },
]
CATEGORIES = list(set(book["category"] for book in BOOKS))


# Route 1: Trang chủ
@app.route("/")
def index():
    total_books = len(BOOKS)
    available_books = sum(1 for book in BOOKS if book["available"])
    return render_template("index.html", total=total_books, available=available_books)


# Route 2: Danh sách sách và lọc
@app.route("/books")
def list_books():
    category_filter = request.args.get("category")
    filtered_books = (
        [b for b in BOOKS if b["category"] == category_filter]
        if category_filter
        else BOOKS
    )
    return render_template("books.html", books=filtered_books, categories=CATEGORIES)


# Route 3: Chi tiết sách HTML
@app.route("/books/<int:book_id>")
def book_detail(book_id):
    book = next((b for b in BOOKS if b["id"] == book_id), None)
    if not book:
        abort(404, description=f"Không có sách với ID = {book_id}")
    return render_template("detail.html", book=book)


# Route 4: API toàn bộ sách JSON
@app.route("/api/books")
def api_list_books():
    return jsonify(BOOKS)


# Route 5: API chi tiết sách JSON
@app.route("/api/books/<int:book_id>")
def api_book_detail(book_id):
    book = next((b for b in BOOKS if b["id"] == book_id), None)
    if not book:
        return jsonify({"error": f"Không có sách với ID = {book_id}"}), 404
    return jsonify(book)


# Xử lý lỗi 404 chung
@app.errorhandler(404)
def page_not_found(e):
    if request.path.startswith("/api/"):
        return jsonify({"error": str(e.description)}), 404
    return render_template("404.html", error_msg=e.description), 404


if __name__ == "__main__":
    app.run(debug=True)
