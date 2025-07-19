
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

if "orders" not in st.session_state:
    st.session_state.orders = []
if "current_order" not in st.session_state:
    st.session_state.current_order = []
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None

menu_data = {
    "กาแฟ": {
        "ร้อน": {
            "เอสเพรสโซ่": 30, "อเมริกาโน่": 30, "คาปูชิโน่": 35, "ลาเต้": 35,
            "มอคค่า": 40, "คาราเมล": 40
        },
        "เย็น": {
            "อเมริกาโน่": 35, "คาปูชิโน่": 40, "ลาเต้": 40, "มอคค่า": 45,
            "คาราเมล": 45, "อเมริกาโน่ส้ม": 50, "อเมริกาโน่น้ำผึ้ง": 50,
            "Blue Sky Coffee": 40, "กาแฟมะพร้าว": 50
        },
        "ปั่น": {
            "คาปูชิโน่": 45, "ลาเต้": 45, "มอคค่า": 50, "คาราเมล": 50
        }
    },
    "ชา": {
        "ร้อน": {"มัทฉะ": 30, "ชามะลิ": 35},
        "เย็น": {"มัทฉะลาเต้": 40},
        "ปั่น": {"มัทฉะลาเต้": 45}
    },
    "นม": {
        "เมนู": {
            "นมสดสตอเบอรี่": 40, "นมกล้วย": 40, "นมคาราเมล": 40,
            "นมเผือก": 40, "ชานม": 40, "นมบลูเบอร์รี่": 40
        }
    },
    "โซดา": {
        "เมนู": {
            "บลูโซดา": 40, "มะนาวโซดา": 35, "น้ำผึ้งมะนาวโซดา": 40,
            "อิตาเลียนโซดา": 35, "ลิ้นจี่โซดา": 35, "เบอร์รี่มิ้นต์": 35,
            "ชาสตอเบอรี่": 35
        }
    },
    "สมูตตี้": {
        "เมนู": {
            "ส้ม": 45, "ลิ้นจี่": 45, "มะม่วง": 45, "กีวี่": 45,
            "สตรอเบอร์รี่": 45, "บลูเบอร์รี่": 45, "เสาวรส": 45
        }
    }
}

# Sidebar หมวดหลัก
st.sidebar.header("เลือกหมวดหมู่เมนู")
main_categories = ["กาแฟ", "ชา", "นม", "โซดา", "สมูตตี้"]
selected_main = st.sidebar.radio("เลือกหมวดหมู่", main_categories)

st.session_state.selected_category = selected_main

sub_categories = list(menu_data[selected_main].keys())
selected_sub = None
if len(sub_categories) > 1:
    selected_sub = st.sidebar.radio("เลือกประเภท", sub_categories)
else:
    selected_sub = sub_categories[0]

# แสดงเมนู
if selected_main and selected_sub:
    st.header(f"{selected_main} - {selected_sub}")
    for item, price in menu_data[selected_main][selected_sub].items():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{item}** - {price}฿")
        with col2:
            qty = st.number_input(f"จำนวน {item}", min_value=0, step=1, key=item)
            if qty > 0:
                st.session_state.current_order.append({
                    "ชื่อเมนู": item,
                    "ราคา": price,
                    "จำนวน": qty
                })

st.divider()

# แสดงออเดอร์ที่เลือก
if st.session_state.current_order:
    st.subheader("ออเดอร์ที่เลือก")
    total_price = sum(i["ราคา"] * i["จำนวน"] for i in st.session_state.current_order)
    total_cups = sum(i["จำนวน"] for i in st.session_state.current_order)
    df_order = pd.DataFrame(st.session_state.current_order)
    st.table(df_order)
    st.markdown(f"**รวมราคา:** {total_price} ฿")
    st.markdown(f"**จำนวนแก้ว:** {total_cups}")

    pay_method = st.radio("ช่องทางชำระเงิน", ["สด", "โอน"])
    amount_paid = st.number_input("เงินที่รับมา", min_value=0.0, step=1.0)
    change = amount_paid - total_price if amount_paid >= total_price else 0
    st.markdown(f"**เงินทอน:** {change:.2f} ฿")

    customer_name = st.text_input("ชื่อลูกค้า")
    if st.button("ยืนยันออเดอร์"):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.orders.append({
            "ลูกค้า": customer_name,
            "เมนู": st.session_state.current_order,
            "ยอดรวม": total_price,
            "จำนวนแก้ว": total_cups,
            "ช่องทาง": pay_method,
            "เงินที่รับ": amount_paid,
            "เงินทอน": change,
            "เวลา": now,
            "สถานะ": "ยังไม่เสร็จ"
        })
        st.success("บันทึกออเดอร์เรียบร้อยแล้ว")
        st.session_state.current_order = []

st.divider()
st.subheader("รายการออเดอร์ทั้งหมด")
for i, order in enumerate(st.session_state.orders):
    with st.expander(f"{order['ลูกค้า']} | {order['ยอดรวม']}฿ | {order['เวลา']}"):
        st.write("เมนูที่สั่ง:")
        for item in order["เมนู"]:
            st.write(f"- {item['ชื่อเมนู']} x {item['จำนวน']} = {item['จำนวน'] * item['ราคา']} ฿")
        st.write(f"**ช่องทางชำระ:** {order['ช่องทาง']}")
        st.write(f"**เงินที่รับ:** {order['เงินที่รับ']} ฿")
        st.write(f"**เงินทอน:** {order['เงินทอน']} ฿")
        st.write(f"**จำนวนแก้ว:** {order['จำนวนแก้ว']}")
        status = st.radio("สถานะ", ["ยังไม่เสร็จ", "เสร็จแล้ว"], index=0 if order["สถานะ"] == "ยังไม่เสร็จ" else 1, key=f"status_{i}")
        order["สถานะ"] = status
