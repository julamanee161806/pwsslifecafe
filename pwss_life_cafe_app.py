
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
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="PWS's Life Cafe", layout="wide")
st.title("PWS's Life Cafe")

# เมนูหลัก
menu_categories = {
    "กาแฟ": {
        "ร้อน": {
            "เอสเพรสโซ่": 30,
            "อเมริกาโน่": 30,
            "คาปูชิโน่": 35,
            "ลาเต้": 35,
            "มอคค่า": 40,
            "คาราเมล": 40,
            "Blue Sky Coffee": 40,
            "กาแฟมะพร้าว": 50
        },
        "เย็น": {
            "อเมริกาโน่": 35,
            "คาปูชิโน่": 40,
            "ลาเต้": 40,
            "มอคค่า": 45,
            "คาราเมล": 45,
            "อเมริกาโน่ส้ม": 50,
            "อเมริกาโน่น้ำผึ้ง": 50,
            "Blue Sky Coffee": 40,
            "กาแฟมะพร้าว": 50
        },
        "ปั่น": {
            "อเมริกาโน่": 40,
            "คาปูชิโน่": 45,
            "ลาเต้": 45,
            "มอคค่า": 50,
            "คาราเมล": 50
        }
    },
    "ชา": {
        "มัทฉะ ร้อน": 30,
        "มัทฉะลาเต้": 40,
        "มัทฉะลาเต้ ปั่น": 45,
        "ชามะนาว": 35
    },
    "นม": {
        "นมสดสตอเบอรี่": 40,
        "นมกล้วย": 40,
        "นมคาราเมล": 40,
        "นมเผือก": 40,
        "ชานม": 40,
        "นมบลูเบอรี่": 40
    },
    "โซดา": {
        "บลูโซดา": 40,
        "มะนาวโซดา": 35,
        "น้ำผึ้งมะนาวโซดา": 40,
        "อิตาเลี่ยนโซดา": 35,
        "ลิ้นจี่โซดา": 35,
        "เบอรี่มิ้นต์": 35,
        "ชาสตอเบอรี่": 35
    },
    "สมูทตี้": {
        "Orange Smoothie": 45,
        "Lychee Smoothie": 45,
        "Mango Smoothie": 45,
        "Kiwi Smoothie": 45,
        "Strawberry Smoothie": 45,
        "Blueberry Smoothie": 45,
        "Passion Fruit Smoothie": 45
    }
}

# Session state
if "orders" not in st.session_state:
    st.session_state.orders = []
if "current_order" not in st.session_state:
    st.session_state.current_order = []

# เลือกหมวดหลัก
selected_category = st.sidebar.radio("เลือกหมวดหมู่เมนู", list(menu_categories.keys()))

# เมนูย่อย
submenu = menu_categories[selected_category]
if isinstance(submenu, dict) and all(isinstance(v, dict) for v in submenu.values()):
    sublevel = st.selectbox("เลือกประเภท (ร้อน/เย็น/ปั่น)", list(submenu.keys()))
    subitems = submenu[sublevel]
else:
    subitems = submenu

st.subheader(f"{selected_category} {'('+sublevel+')' if 'sublevel' in locals() else ''}")

selected_items = {}
for item, price in subitems.items():
    qty = st.number_input(f"{item} ({price}฿)", min_value=0, max_value=10, step=1, key=f"{item}_{selected_category}")
    if qty > 0:
        selected_items[item] = {"qty": qty, "price": price}

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    customer = st.text_input("ชื่อลูกค้า")
with col2:
    receive = st.number_input("รับเงินมา (บาท)", min_value=0, step=1)

if st.button("ยืนยันออเดอร์"):
    if selected_items and customer:
        total = sum(i['qty'] * i['price'] for i in selected_items.values())
        change = receive - total
        order = {
            "customer": customer,
            "time": datetime.now().strftime("%H:%M:%S"),
            "items": selected_items,
            "total": total,
            "receive": receive,
            "change": change,
            "status": "ไม่เสร็จ"
        }
        st.session_state.orders.append(order)
        st.success(f"รับออเดอร์ของ {customer} แล้ว รวม {total} บาท ทอน {change} บาท")
        # ล้างค่า
        for item in selected_items:
            st.session_state[f"{item}_{selected_category}"] = 0
        st.session_state.current_order = []
    else:
        st.warning("กรุณาระบุชื่อลูกค้าและเลือกเมนูอย่างน้อย 1 รายการ")

# แสดงออเดอร์ทั้งหมด
st.header("รายการออเดอร์")
for i, order in enumerate(st.session_state.orders):
    with st.expander(f"{order['customer']} เวลา {order['time']} [{order['status']}]"):
        for item, detail in order['items'].items():
            st.write(f"- {item} x {detail['qty']} = {detail['qty'] * detail['price']}฿")
        st.write(f"**รวม:** {order['total']}฿ | รับมา: {order['receive']}฿ | ทอน: {order['change']}฿")
        if order['status'] == "ไม่เสร็จ":
            if st.button("เสร็จแล้ว", key=f"done_{i}"):
                st.session_state.orders[i]['status'] = "เสร็จแล้ว"

# สรุปรายได้
st.header("สรุปยอดขาย")
all_items = []
total_income = 0
total_cups = 0
for order in st.session_state.orders:
    total_income += order['total']
    for item, detail in order['items'].items():
        total_cups += detail['qty']

st.metric("รายได้รวม", f"{total_income} บาท")
st.metric("จำนวนแก้วที่ขาย", f"{total_cups} แก้ว")
