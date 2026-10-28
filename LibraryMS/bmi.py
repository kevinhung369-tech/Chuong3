from flask import Flask, render_template, request

app = Flask(__name__)


def validate_input(val, min_val, max_val, unit_name):
    """Hàm kiểm tra dữ liệu đầu vào cho Chiều cao và Cân nặng"""
    if not val or val.strip() == "":
        return None, "Vui lòng nhập một số."

    val_str = val.replace(",", ".")

    try:
        num = float(val_str)
        if num < min_val or num > max_val:
            return None, f"Giá trị phải từ {min_val} đến {max_val}."
        return num, None
    except ValueError:
        return None, "Vui lòng nhập một số."


@app.route("/", methods=["GET", "POST"])
def calculate_bmi():
    height_val = ""
    weight_val = ""
    error_h = None
    error_w = None
    result = None

    if request.method == "POST":
        height_val = request.form.get("height", "")
        weight_val = request.form.get("weight", "")

        # Kiểm tra điều kiện: Chiều cao 50-250cm, Cân nặng 10-300kg
        height_num, error_h = validate_input(height_val, 50, 250, "Chiều cao")
        weight_num, error_w = validate_input(weight_val, 10, 300, "Cân nặng")

        if error_h is None and error_w is None:
            # Đổi cm sang m
            h_m = height_num / 100.0

            # Tính BMI và làm tròn 1 chữ số
            bmi = round(weight_num / (h_m**2), 1)

            # Phân loại theo chuẩn châu Á & xác định màu sắc
            if bmi < 18.5:
                category = "Thiếu cân"
                color_class = "warning"  # Vàng
            elif bmi < 23:
                category = "Bình thường"
                color_class = "success"  # Xanh
            elif bmi < 25:
                category = "Thừa cân"
                color_class = "warning"  # Vàng
            else:
                category = "Béo phì"
                color_class = "danger"  # Đỏ

            # Tính cân nặng nên có (BMI 18.5 - 22.9)
            min_weight = round(18.5 * (h_m**2), 1)
            max_weight = round(22.9 * (h_m**2), 1)

            # Chuẩn bị chuỗi kết quả
            result = {
                "bmi": bmi,
                "category": category,
                "color_class": color_class,
                "min_w": min_weight,
                "max_w": max_weight,
                "is_normal": (bmi >= 18.5 and bmi < 23),
            }

    return render_template(
        "bmi.html",
        height=height_val,
        weight=weight_val,
        error_h=error_h,
        error_w=error_w,
        result=result,
    )


if __name__ == "__main__":
    app.run(debug=True)
