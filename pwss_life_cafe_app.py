
import streamlit as st
import datetime

# --- ระบบ Login ---
def login():
    st.title("🔐 เข้าสู่ระบบ")
    password = st.text_input("รหัสผ่าน", type="password")
    if password == "pwss2021":
        st.session_state["logged_in"] = True
        st.experimental_rerun()
    elif password != "":
        st.error("รหัสผ่านไม่ถูกต้อง")

if "logged_in" not in st.session_state:
    login()
    st.stop()

st.set_page_config(page_title="ระบบแคชเชียร์ร้านกาแฟ", layout="wide")

# ข้อมูลเมนู
menu_data = {
    "กาแฟ": {
        "ร้อน": {
            "เอสเพรสโซ่": 30,
            "อเมริกาโน่": 30,
            "ลาเต้": 35,
            "คาปูชิโน่": 35,
            "มอคค่า": 35
        },
        "เย็น": {
            "เอสเพรสโซ่": 40,
            "อเมริกาโน่": 40,
            "ลาเต้": 45,
            "คาปูชิโน่": 45,
            "มอคค่า": 45
        },
        "ปั่น": {
            "เอสเพรสโซ่": 50,
            "อเมริกาโน่": 50,
            "ลาเต้": 55,
            "คาปูชิโน่": 55,
            "มอคค่า": 55
        }
    },
    "ชา": {
        "เมนู": {
            "ชาเขียว": 40,
            "ชาไทย": 40,
            "ชาเย็น": 40
        }
    },
    "นม": {
        "เมนู": {
            "นมสด": 35,
            "นมชมพู": 35,
            "ไมโล": 35,
            "โอวัลติน": 35
        }
    },
    "โซดา": {
        "เมนู": {
            "บลูฮาวาย": 40,
            "แดงมะนาวโซดา": 40,
            "กีวี่โซดา": 40
        }
    },
    "สมูทตี้": {
        "เมนู": {
            "สตรอว์เบอร์รี่": 45,
            "บลูเบอร์รี่": 45,
            "มะม่วง": 45
        }
    }
}

# ตัวแปร session state
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None
if 'selected_subcategory' not in st.session_state:
    st.session_state.selected_subcategory = None

st.title("☕ ระบบแคชเชียร์ร้านกาแฟ")

# หน้าหมวดหลัก
st.subheader("เลือกหมวดหมู่หลัก")
cols = st.columns(len(menu_data))
for i, category in enumerate(menu_data.keys()):
    if cols[i].button(category):
        st.session_state.selected_category = category
        st.session_state.selected_subcategory = None

category = st.session_state.selected_category
subcategory = st.session_state.selected_subcategory

# หมวดหมู่ย่อย
if category:
    st.divider()
    st.subheader(f"📂 หมวดย่อยในหมวด {category}")
    subcategories = menu_data[category].keys()
    cols = st.columns(len(subcategories))
    for i, subcat in enumerate(subcategories):
        if cols[i].button(subcat):
            st.session_state.selected_subcategory = subcat

# แสดงเมนูในหมวดย่อย
if category and subcategory:
    st.divider()
    st.subheader(f"🍽 เมนู: {category} > {subcategory}")
    menu_items = menu_data[category][subcategory]

    with st.form("order_form", clear_on_submit=False):
        quantities = {}
        for item, price in menu_items.items():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{item}** - {price} บาท")
            with col2:
                qty = st.number_input(f"จำนวน {item}", min_value=0, key=f"{item}-{category}", step=1)
                quantities[item] = (price, qty)

        customer_name = st.text_input("🧍‍♂️ ชื่อลูกค้า/ผู้รับ", key="customer_name")
        total = sum(price * qty for price, qty in quantities.values())
        st.info(f"💰 ยอดรวม: {total} บาท")
        paid = st.number_input("💵 เงินที่รับมา", min_value=0, value=0, step=1, key="paid_amount")
        change = paid - total if paid >= total else 0
        st.success(f"💸 เงินทอน: {change} บาท")

        submitted = st.form_submit_button("✅ ยืนยันออเดอร์")

        if submitted:
            order_items = [(item, price, qty) for item, (price, qty) in quantities.items() if qty > 0]
            if order_items:
                order = {
                    "name": customer_name,
                    "items": order_items,
                    "total": total,
                    "paid": paid,
                    "change": change,
                    "time": datetime.datetime.now().strftime("%H:%M:%S"),
                    "done": False
                }
                st.session_state.orders.append(order)
                st.success("เพิ่มออเดอร์เรียบร้อยแล้ว")
                st.session_state.selected_category = None
                st.session_state.selected_subcategory = None
                st.experimental_rerun()

# แสดงรายการออเดอร์
st.divider()
st.subheader("🧾 รายการออเดอร์ทั้งหมด")

if st.session_state.orders:
    for i, order in enumerate(st.session_state.orders):
        with st.expander(f"🕒 {order['time']} - {order['name']} | ยอด {order['total']} บาท", expanded=False):
            for item, price, qty in order["items"]:
                st.write(f"{item} - {price} x {qty} = {price * qty} บาท")
            st.write(f"รวมทั้งหมด: {order['total']} บาท")
            st.write(f"รับเงินมา: {order['paid']} บาท | ทอน: {order['change']} บาท")

            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("🗑 ลบ", key=f"del-{i}"):
                    st.session_state.orders.pop(i)
                    st.rerun()
            with col2:
                if st.button("✅ เสร็จแล้ว" if not order["done"] else "✔️ เสร็จแล้ว", key=f"done-{i}"):
                    st.session_state.orders[i]["done"] = True
                    st.rerun()
else:
    st.info("ยังไม่มีออเดอร์")

# รายงานยอดขาย
st.divider()
if st.button("📊 ดูรายงานยอดขาย"):
    total_cash = 0
    total_cups = 0
    for order in st.session_state.orders:
        total_cash += order['total']
        total_cups += sum(qty for _, _, qty in order['items'])
    st.success(f"ยอดขายรวม: {total_cash} บาท | จำนวนแก้ว: {total_cups} แก้ว")
