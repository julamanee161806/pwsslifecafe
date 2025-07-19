
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

# --- ข้อมูลเมนู ---
menus = {
    "Coffee (ร้อน)": [("เอสเพรสโซ่", 30), ("อเมริกาโน่", 30), ("คาปูชิโน่", 35), ("ลาเต้", 35), ("มอคค่า", 40), ("คาราเมล", 40)],
    "Coffee (เย็น)": [("อเมริกาโน่", 35), ("คาปูชิโน่", 40), ("ลาเต้", 40), ("มอคค่า", 45), ("คาราเมล", 45), ("Blue Sky Coffee", 40)],
    "Coffee (ปั่น)": [("อเมริกาโน่", 40), ("คาปูชิโน่", 45), ("ลาเต้", 45), ("มอคค่า", 50), ("คาราเมล", 50)],
    "เมนูพิเศษ": [("อเมริกาโน่ส้ม", 50), ("อเมริกาโน่น้ำผึ้ง", 50), ("กาแฟมะพร้าว", 50)],
    "Tea": [("มัทฉะร้อน", 30), ("มัทฉะลาเต้", 40), ("มัทฉะลาเต้ปั่น", 45), ("ชามะนาว", 35)],
    "Soda": [("บลูโซดา", 40), ("มะนาวโซดา", 35), ("น้ำผึ้งมะนาวโซดา", 40), ("อิตาเลียนโซดา", 35), ("ลิ้นจี่โซดา", 35), ("เบอรี่มิ้นต์", 35), ("ชาสตอเบอรี่", 35)],
    "Chocolate": [("ช็อกโกแลตร้อน", 30), ("ช็อกโกแลตเย็น", 40), ("ช็อกโกปั่น", 45)],
    "Milk": [("นมสตอเบอรี่", 40), ("นมกล้วย", 40), ("นมคาราเมล", 40), ("นมเผือก", 40), ("ชานม", 40), ("นมบลูเบอรี่", 40)],
    "Smoothie": [("Orange Smoothie", 45), ("Lychee Smoothie", 45), ("Mango Smoothie", 45), ("Kiwi Smoothie", 45), ("Strawberry Smoothie", 45), ("Blueberry Smoothie", 45), ("Passion Fruit Smoothie", 45)]
}

if 'orders_in_progress' not in st.session_state:
    st.session_state.orders_in_progress = []
    st.session_state.orders_completed = []

st.title("☕ ระบบแคชเชียร์ - PWS'S LIFE CAFE")

st.sidebar.header("เลือกหมวดเมนู")
category = st.sidebar.selectbox("หมวดหมู่", list(menus.keys()))

selected_items = []
total_price = 0
cup_count = 0

with st.form("order_form"):
    st.subheader(f"📋 เมนู: {category}")
    cols = st.columns(2)
    for i, (name, price) in enumerate(menus[category]):
        if cols[i % 2].checkbox(f"{name} ({price}฿)", key=f"menu_{category}_{i}"):
            selected_items.append((name, price))
            total_price += price
            if any(x in name for x in ["กาแฟ", "ชา", "นม", "โซดา", "Smoothie"]):
                cup_count += 1

    st.markdown("---")
    name = st.text_input("ชื่อผู้รับ")
    payment = st.radio("วิธีชำระเงิน", ["เงินสด", "โอน"])
    cash_input = 0
    if payment == "เงินสด":
        cash_input = st.number_input("จำนวนเงินที่รับมา", min_value=0.0, value=0.0, step=1.0)

    submitted = st.form_submit_button("✅ ชำระเงิน")
    if submitted:
        if not selected_items:
            st.warning("กรุณาเลือกเมนูก่อน")
        elif not name:
            st.warning("กรุณาใส่ชื่อผู้รับ")
        else:
            change = cash_input - total_price if payment == "เงินสด" else 0
            if payment == "เงินสด" and change < 0:
                st.error("เงินไม่พอ")
            else:
                order = {
                    "ชื่อ": name,
                    "รายการ": selected_items.copy(),
                    "รวม": total_price,
                    "จำนวนแก้ว": cup_count,
                    "ชำระ": payment,
                    "เวลา": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "สถานะ": "ยังไม่เสร็จ"
                }
                st.session_state.orders_in_progress.append(order)
                st.success(f"บันทึกออเดอร์ของ {name} แล้ว")
                if payment == "เงินสด":
                    st.info(f"เงินทอน: {change:.2f} บาท")

st.markdown("---")
st.header("🧾 รายการออเดอร์")

st.subheader("🕓 ยังไม่เสร็จ")
for i, order in enumerate(st.session_state.orders_in_progress):
    with st.expander(f"{order['ชื่อ']} | {order['รวม']} บาท | {order['เวลา']}"):
        st.write(", ".join([item[0] for item in order['รายการ']]))
        if st.button("✅ เสร็จแล้ว", key=f"done_{i}"):
            st.session_state.orders_completed.append(order)
            st.session_state.orders_in_progress.pop(i)
            st.experimental_rerun()

st.subheader("✅ เสร็จแล้ว")
for order in st.session_state.orders_completed:
    with st.expander(f"{order['ชื่อ']} | {order['รวม']} บาท | {order['เวลา']}"):
        st.write(", ".join([item[0] for item in order['รายการ']]))
