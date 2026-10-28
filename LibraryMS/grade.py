from flask import Flask, render_template, request

app = Flask(__name__)


def validate_score(val, field_name):
    """Hàm kiểm tra điểm dùng chung cho cả 3 ô"""
    if not val or val.strip() == "":
        return None, "Vui lòng nhập một số."

    # Chuẩn hóa dấu phẩy thập phân
    val_str = val.replace(",", ".")

    try:
        score = float(val_str)
        if score < 0 or score > 10:
            return None, f"Điểm phải từ 0 đến 10."
        return score, None
    except ValueError:
        return None, "Vui lòng nhập một số."


@app.route("/", methods=["GET", "POST"])
def calculate_grade():
    cc_val, gk_val, ck_val = "", "", ""
    error_cc, error_gk, error_ck = None, None, None
    result = None

    if request.method == "POST":
        cc_val = request.form.get("cc", "")
        gk_val = request.form.get("gk", "")
        ck_val = request.form.get("ck", "")

        # Kiểm tra tính hợp lệ bằng hàm dùng chung
        cc_score, error_cc = validate_score(cc_val, "CC")
        gk_score, error_gk = validate_score(gk_val, "GK")
        ck_score, error_ck = validate_score(ck_val, "CK")

        # Nếu cả 3 ô không có lỗi
        if error_cc is None and error_gk is None and error_ck is None:
            # Tính điểm trung bình môn
            final_score = round(cc_score * 0.1 + gk_score * 0.3 + ck_score * 0.6, 1)

            # Xếp loại điểm chữ & kiểm tra điểm liệt
            if ck_score < 1.0:
                letter_grade = "F (điểm thi dưới 1)"
            else:
                if final_score >= 8.5:
                    letter_grade = "A"
                elif final_score >= 7.0:
                    letter_grade = "B"
                elif final_score >= 5.5:
                    letter_grade = "C"
                elif final_score >= 4.0:
                    letter_grade = "D"
                else:
                    letter_grade = "F"

            result = f"{final_score} : {letter_grade}"

    return render_template(
        "grade.html",
        cc=cc_val,
        gk=gk_val,
        ck=ck_val,
        error_cc=error_cc,
        error_gk=error_gk,
        error_ck=error_ck,
        result=result,
    )


if __name__ == "__main__":
    app.run(debug=True)
