
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

st.set_page_config(page_title="PWS'S LIFE CAFE", layout="wide")

# ------------------------ Data Setup ------------------------ #
menu_data = {
    "กาแฟ": {
        "ร้อน": {
            "เอสเพรสโซ่": 30,
            "อเมริกาโน่": 30,
            "คาปูชิโน่": 35,
            "ลาเต้": 35,
            "มอคค่า": 40,
            "คาราเมล": 40,
            "ช็อกโกโก้": 30,
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
        "ร้อน": {
            "มัทฉะ": 30
        },
        "เย็น": {
            "มัทฉะลาเต้": 40,
            "ชามะนาว": 35
        },
        "ปั่น": {
            "มัทฉะลาเต้": 45
        }
    },
    "นม": {
        "เย็น": {
            "นมสดสตอเบอรี่": 40,
            "นมกล้วย": 40,
            "นมคาราเมล": 40,
            "นมเผือก": 40,
            "ชานม": 40,
            "นมบลูเบอร์รี่": 40
        }
    },
    "โซดา": {
        "เย็น": {
            "บลูโซดา": 40,
            "มะนาวโซดา": 35,
            "น้ำผึ้งมะนาวโซดา": 40,
            "อิตาเลี่ยนโซดา": 35,
            "ลิ้นจี่โซดา": 35,
            "เบอรี่มิ้นต์": 35,
            "ชาสตอเบอรี่": 35
        }
    },
    "สมูตตี้": {
        "ปั่น": {
            "Orange Smoothie": 45,
            "Lychee Smoothie": 45,
            "Mango Smoothie": 45,
            "Kiwi Smoothie": 45,
            "Strawberry Smoothie": 45,
            "Blueberry Smoothie": 45,
            "Passion Fruit Smoothie": 45
        }
    }
}

# ------------------------ Session Setup ------------------------ #
if "order" not in st.session_state:
    st.session_state.order = []
if "cash_received" not in st.session_state:
    st.session_state.cash_received = 0

# ------------------------ Layout ------------------------ #
st.title("☕ ระบบแคชเชียร์ - PWS'S LIFE CAFE")

main_categories = list(menu_data.keys())
selected_main = st.radio("เลือกหมวดหมู่เมนู", main_categories, key="main_radio")

if selected_main:
    sub_categories = list(menu_data[selected_main].keys())
    selected_sub = st.radio(f"เลือกประเภท ({selected_main})", sub_categories, key="sub_radio")

    if selected_sub:
        st.subheader(f"เมนู {selected_main} ({selected_sub})")
        for item, price in menu_data[selected_main][selected_sub].items():
            col1, col2 = st.columns([3, 1])
            with col1:
                qty = st.number_input(f"{item} ({price}฿)", min_value=0, step=1, key=f"{item}_{selected_main}_{selected_sub}")
            with col2:
                if st.button("เพิ่ม", key=f"add_{item}_{selected_main}_{selected_sub}"):
                    if qty > 0:
                        st.session_state.order.append({
                            "name": item,
                            "qty": qty,
                            "price": price,
                            "total": qty * price
                        })
                        st.success(f"เพิ่ม {item} x {qty} แล้ว")

# ------------------------ Order Summary ------------------------ #
st.markdown("---")
st.subheader("🧾 รายการที่สั่ง")

if st.session_state.order:
    total_price = sum(item["total"] for item in st.session_state.order)
    for i, item in enumerate(st.session_state.order):
        st.write(f"{i+1}. {item['name']} x {item['qty']} = {item['total']}฿")
    st.info(f"💰 ยอดรวม: {total_price} ฿")

    st.number_input("💵 เงินที่รับมา", min_value=0, step=1, key="cash_received_input")
    st.session_state.cash_received = st.session_state.cash_received_input

    if st.session_state.cash_received >= total_price:
        change = st.session_state.cash_received - total_price
        st.success(f"เงินทอน: {change} ฿")
    else:
        st.warning("⚠️ เงินไม่พอ")

    customer_name = st.text_input("ชื่อลูกค้า (ไม่บังคับ)")
    if st.button("✅ ยืนยันออเดอร์"):
        if st.session_state.cash_received >= total_price:
            st.success(f"ยืนยันออเดอร์เรียบร้อย ขอบคุณค่ะ")
            st.session_state.order.clear()
            st.session_state.cash_received = 0
        else:
            st.warning("กรุณาใส่เงินให้พอก่อนยืนยัน")
else:
    st.write("ยังไม่มีการสั่งสินค้า")
