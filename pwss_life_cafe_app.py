
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

st.set_page_config(page_title="PWS's Life Cafe", layout="wide")

# --- ข้อมูลเมนู ---
menu = {
    "กาแฟ": {
        "ร้อน": {
            "เอสเพรสโซ่": 30,
            "อเมริกาโน่": 30,
            "คาปูชิโน่": 35,
            "ลาเต้": 35,
            "มอคค่า": 40,
            "คาราเมล": 40,
            "ช็อกโกโก้ลาเต้": 30
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
            "กาแฟมะพร้าว": 50,
            "ช็อกโกโก้ลาเต้": 40
        },
        "ปั่น": {
            "อเมริกาโน่": 40,
            "คาปูชิโน่": 45,
            "ลาเต้": 45,
            "มอคค่า": 50,
            "คาราเมล": 50,
            "กาแฟมะพร้าว": 50,
            "ช็อกโก": 45
        }
    },
    "ชา": {
        "มัทฉะ ร้อน": 30,
        "มัทฉะลาเต้": 40,
        "มัทฉะลาเต้ ปั่น": 45,
        "ชามะนาว": 35,
        "ชานม": 40
    },
    "นม": {
        "นมสดสตอเบอรี่": 40,
        "นมกล้วย": 40,
        "นมคาราเมล": 40,
        "นมเผือก": 40,
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
        "Orange Smoothie ส้ม ปั่น": 45,
        "Lychee Smoothie ลิ้นจี่ ปั่น": 45,
        "Mango Smoothie มะม่วง ปั่น": 45,
        "Kiwi Smoothie กีวี่ ปั่น": 45,
        "Strawberry Smoothie สตอเบอรี่ ปั่น": 45,
        "Blueberry Smoothie บลูเบอรี่ ปั่น": 45,
        "Passion Fruit Smoothie เสาวรส ปั่น": 45
    }
}

if "orders" not in st.session_state:
    st.session_state.orders = []

if "sales" not in st.session_state:
    st.session_state.sales = []

st.title("☕ ระบบแคชเชียร์ - PWS's LIFE CAFE")

# --- สั่งออเดอร์ ---
st.header("🧾 สั่งออเดอร์")
with st.form("order_form"):
    col1, col2 = st.columns([2, 1])
    selections = []
    with col1:
        for cat, items in menu.items():
            st.subheader(cat)
            if isinstance(items, dict):
                for subcat, subitems in items.items():
                    st.markdown(f"**{subcat}**")
                    for item, price in subitems.items():
                        qty = st.number_input(f"{item} ({price}฿)", min_value=0, step=1, key=f"{cat}_{subcat}_{item}")
                        if qty > 0:
                            selections.append((item, price, qty))
            else:
                for item, price in items.items():
                    qty = st.number_input(f"{item} ({price}฿)", min_value=0, step=1, key=f"{cat}_{item}")
                    if qty > 0:
                        selections.append((item, price, qty))

    with col2:
        customer_name = st.text_input("ชื่อผู้รับ")
        total = sum(price * qty for _, price, qty in selections)
        st.markdown(f"### ยอดรวม: {total} ฿")
        paid = st.number_input("ลูกค้าจ่ายมา (บาท)", min_value=0, step=1)
        change = paid - total if paid >= total else 0
        st.markdown(f"เงินทอน: {change} ฿")

        submitted = st.form_submit_button("✅ ยืนยันออเดอร์")
        if submitted and selections and customer_name:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            order = {
                "ชื่อผู้รับ": customer_name,
                "เวลา": now,
                "ยอดรวม": total,
                "จ่าย": paid,
                "ทอน": change,
                "สถานะ": "ไม่เสร็จ",
                "รายการ": selections
            }
            st.session_state.orders.append(order)
            st.session_state.sales.append(order)
            st.success("บันทึกออเดอร์เรียบร้อยแล้ว!")
            st.rerun()

# --- ติดตามออเดอร์ ---
st.header("📋 ติดตามสถานะออเดอร์")
for i, order in enumerate(st.session_state.orders):
    with st.expander(f"{order['ชื่อผู้รับ']} | {order['เวลา']} | {order['สถานะ']}"):
        for item, price, qty in order['รายการ']:
            st.write(f"{item} x{qty} = {price * qty} ฿")
        st.write(f"ยอดรวม: {order['ยอดรวม']} ฿")
        if st.button("✅ เสร็จแล้ว", key=f"done_{i}"):
            st.session_state.orders[i]['สถานะ'] = "เสร็จแล้ว"
            st.rerun()

# --- สรุปยอดขาย ---
st.header("📈 รายงานยอดขาย")
if st.button("ดูยอดขายย้อนหลัง"):
    df = pd.DataFrame(st.session_state.sales)
    total_income = sum(order['ยอดรวม'] for order in st.session_state.sales)
    total_cups = sum(qty for order in st.session_state.sales for _, _, qty in order['รายการ'])
    st.metric("รายได้รวม", f"{total_income} ฿")
    st.metric("จำนวนแก้วที่ขาย", f"{total_cups} แก้ว")

    for i, order in enumerate(st.session_state.sales):
        with st.expander(f"{order['ชื่อผู้รับ']} | {order['เวลา']}"):
            for item, price, qty in order['รายการ']:
                st.write(f"{item} x{qty} = {price * qty} ฿")
            st.write(f"ยอดรวม: {order['ยอดรวม']} ฿ | จ่าย: {order['จ่าย']} ฿ | ทอน: {order['ทอน']} ฿")
