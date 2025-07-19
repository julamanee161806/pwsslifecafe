import streamlit as st
from datetime import datetime
import uuid

# -------------------- ข้อมูลเมนู --------------------
menu = {
    "กาแฟร้อน": {
        "เอสเพรสโซ่": 30,
        "อเมริกาโน่": 30,
        "คาปูชิโน่": 35,
        "ลาเต้": 35,
        "มอคค่า": 40,
        "คาราเมล": 40,
        "Blue Sky Coffee": 40,
    },
    "กาแฟเย็น": {
        "อเมริกาโน่": 35,
        "คาปูชิโน่": 40,
        "ลาเต้": 40,
        "มอคค่า": 45,
        "คาราเมล": 45,
        "อเมริกาโน่ส้ม": 50,
        "อเมริกาโน่น้ำผึ้ง": 50,
        "Blue Sky Coffee": 50,
        "กาแฟพะยอ": 50,
    },
    "กาแฟปั่น": {
        "คาปูชิโน่": 45,
        "ลาเต้": 45,
        "มอคค่า": 50,
        "คาราเมล": 50,
    },
    "ชา": {
        "มัทฉะ": 30,
        "มัทฉะลาเต้": 40,
        "ชามะนาว": 35,
        "ชานม": 40,
        "ช็อกโกแลตลาเต้": 40,
    },
    "นม": {
        "นมสตรอเบอรี่": 40,
        "นมกล้วย": 40,
        "นมคาราเมล": 40,
    },
    "โซดา": {
        "บลูโซดา": 40,
        "น้ำผึ้งมะนาวโซดา": 40,
        "อิตาเลี่ยนโซดา": 35,
    },
    "สมูทตี้": {
        "Strawberry Smoothie": 45,
        "Mango Smoothie": 45,
        "Blueberry Smoothie": 45,
    },
}

# -------------------- State --------------------
if "order_items" not in st.session_state:
    st.session_state.order_items = []
    st.session_state.orders = []
    st.session_state.sales = {"สด": 0, "โอน": 0}
    st.session_state.cups = 0

# -------------------- UI --------------------
st.set_page_config(page_title="PWS's Life Cafe", layout="wide")
st.title("☕ ระบบแคชเชียร์ - PWS's LIFE CAFE")

menu_tab, order_tab, sales_tab = st.tabs(["📋 เลือกเมนู", "📦 ออเดอร์ย้อนหลัง", "📈 ยอดขายรวม"])

# -------------------- Tab: เมนู --------------------
with menu_tab:
    st.subheader("เลือกเมนู")
    customer = st.text_input("ชื่อผู้รับ")
    pay_method = st.radio("วิธีชำระเงิน", ["สด", "โอน"], horizontal=True)

    selected_category = st.selectbox("เลือกหมวดหมู่เมนู", list(menu.keys()))
    search = st.text_input("ค้นหาเมนู")

    for name, price in menu[selected_category].items():
        if search.lower() in name.lower():
            cols = st.columns([5, 2, 2])
            with cols[0]:
                st.markdown(f"**{name}** {price}฿")
            with cols[1]:
                qty = st.number_input(f"จำนวน: {name}", min_value=0, step=1, key=name)
            with cols[2]:
                if st.button("เพิ่ม", key=f"add_{name}"):
                    st.session_state.order_items.append({"name": name, "price": price, "qty": qty})

    if st.session_state.order_items:
        st.divider()
        st.subheader("🧾 สรุปรายการ")
        total = sum(i['price'] * i['qty'] for i in st.session_state.order_items)
        for item in st.session_state.order_items:
            st.write(f"{item['name']} x {item['qty']} = {item['price'] * item['qty']} บาท")
        st.success(f"รวมทั้งหมด: {total} บาท")

        paid = st.number_input("จำนวนเงินที่ลูกค้าจ่าย", min_value=0)
        if paid >= total:
            change = paid - total
            st.info(f"เงินทอน: {change} บาท")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ ชำระเงิน"):
                order = {
                    "id": str(uuid.uuid4())[:8],
                    "name": customer,
                    "items": st.session_state.order_items.copy(),
                    "total": total,
                    "method": pay_method,
                    "time": datetime.now().strftime('%H:%M:%S'),
                    "status": "ยังไม่เสร็จ"
                }
                st.session_state.orders.append(order)
                st.session_state.sales[pay_method] += total
                st.session_state.cups += sum(i
