from flask import Flask, render_template, request

app = Flask(__name__)


def parse_number(val):
    if not val or val.strip() == "":
        return None, "Vui lòng nhập một số."
    try:
        val = val.replace(",", ".")
        return float(val), None
    except ValueError:
        return None, "Vui lòng nhập một số."


def format_number(num):
    if num.is_integer():
        return int(num)
    return num


@app.route("/", methods=["GET", "POST"])
def calculator():
    a_val = ""
    b_val = ""
    op_val = "+"
    error_a = None
    error_b = None
    error_general = None
    result = None

    if request.method == "POST":
        a_val = request.form.get("a", "")
        b_val = request.form.get("b", "")
        op_val = request.form.get("op", "+")

        a_num, error_a = parse_number(a_val)
        b_num, error_b = parse_number(b_val)

        if not error_a and not error_b:
            if op_val not in ["+", "-", "*", "/"]:
                error_general = "Phép toán không hợp lệ."
            elif op_val == "/" and b_num == 0:
                error_b = "Không thể chia cho 0."
            else:
                res = 0
                if op_val == "+":
                    res = a_num + b_num
                elif op_val == "-":
                    res = a_num - b_num
                elif op_val == "*":
                    res = a_num * b_num
                elif op_val == "/":
                    res = a_num / b_num

                str_a = format_number(a_num)
                str_b = format_number(b_num)
                str_res = format_number(res)
                result = f"{str_a} {op_val} {str_b} = {str_res}"

    # Gọi đến file calculator.html trong thư mục templates
    return render_template(
        "calculator.html",
        a=a_val,
        b=b_val,
        op=op_val,
        error_a=error_a,
        error_b=error_b,
        error_general=error_general,
        result=result,
    )


if __name__ == "__main__":
    app.run(debug=True)
