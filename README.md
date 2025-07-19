import streamlit as st
import datetime

# -------------------- ข้อมูลเมนู --------------------
menu = {
    "กาแฟ": {
        "ร้อน": {
            "เอสเพรสโซ่": 30,
            "อเมริกาโน่": 30,
            "คาปูชิโน่": 35,
            "ลาเต้": 35,
            "มอคค่า": 40,
            "คาราเมล": 40,
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
        },
        "ปั่น": {
            "อเมริกาโน่": 40,
            "คาปูชิโน่": 45,
            "ลาเต้": 45,
            "มอคค่า": 50,
            "คาราเมล": 50,
        },
    },
    "ชา": {
        "มัทฉะ ร้อน": 30,
        "มัทฉะลาเต้": 40,
        "มัทฉะลาเต้ ปั่น": 45,
        "ชามะนาว": 35,
    },
    "นม": {
        "นมสตอเบอรี่": 40,
        "นมกล้วย": 40,
        "นมคาราเมล": 40,
        "นมเผือก": 40,
        "ชานม": 40,
        "นมบลูเบอรี่": 40,
    },
    "โซดา": {
        "บลูโซดา": 40,
        "มะนาวโซดา": 35,
        "น้ำผึ้งมะนาวโซดา": 40,
        "อิตาเลียนโซดา": 35,
        "ลิ้นจี่โซดา": 35,
        "เบอรี่มินต์": 35,
        "ชาสตอเบอรี่": 35,
    },
    "ช็อกโกแลต": {
        "ช็อกโกแลต ร้อน": 30,
        "ช็อกโกแลต เย็น": 40,
        "ช็อกโกแลต ปั่น": 45,
    },
    "สมูทตี้": {
        "Orange Smoothie": 45,
        "Lychee Smoothie": 45,
        "Mango Smoothie": 45,
        "Kiwi Smoothie": 45,
        "Strawberry Smoothie": 45,
        "Blueberry Smoothie": 45,
        "Passion Fruit Smoothie": 45,
    }
}

# -------------------- ตัวแปรสถานะ --------------------
if "orders" not in st.session_state:
    st.session_state.orders = []
if "sales" not in st.session_state:
    st.session_state.sales = []

# -------------------- UI --------------------
st.title("☕ PWS'S LIFE CAFE")
tabs = st.tabs(["📋 เมนู", "📦 ออเดอร์ย้อนหลัง", "📈 ยอดขายรวม"])

# -------------------- Tab: เมนู --------------------
with tabs[0]:
    customer_name = st.text_input("👤 ชื่อลูกค้า")
    search = st.text_input("🔎 ค้นหาเมนู")
    order = []
    
    for category, items in menu.items():
        with st.expander(category):
            if category == "กาแฟ":
                for subcat, drinks in items.items():
                    st.markdown(f"**{subcat}**")
                    for drink, price in drinks.items():
                        if search.lower() in drink.lower():
                            qty = st.number_input(f"{drink} ({price}฿)", 0, 10, key=f"{drink}_{subcat}")
                            if qty > 0:
                                order.append((f"{drink} ({subcat})", qty, price))
            else:
                for drink, price in items.items():
                    if search.lower() in drink.lower():
                        qty = st.number_input(f"{drink} ({price}฿)", 0, 10, key=drink)
                        if qty > 0:
                            order.append((drink, qty, price))

    if order:
        st.subheader("🧾 รายการที่สั่ง")
        total = 0
        for drink, qty, price in order:
            st.write(f"{drink} x {qty} = {qty*price} ฿")
            total += qty * price
        st.success(f"💰 รวมทั้งหมด: {total} บาท")

        paid = st.number_input("💵 จำนวนเงินที่ลูกค้าจ่าย", min_value=0, step=1)
        if st.button("✅ ชำระเงิน"):
            change = paid - total
            now = datetime.datetime.now()
            st.session_state.orders.append({
                "name": customer_name,
                "items": order,
                "total": total,
                "time": now.strftime("%H:%M:%S"),
                "done": False,
            })
            st.session_state.sales.append(order)
            if change >= 0:
                st.success(f"เงินทอน: {change} บาท")
            else:
                st.error("จ่ายไม่ครบ!")

# -------------------- Tab: ออเดอร์ย้อนหลัง --------------------
with tabs[1]:
    st.subheader("📦 ออเดอร์ย้อนหลัง")
    for i, od in enumerate(st.session_state.orders):
        with st.expander(f"🧾 {od['name']} เวลา {od['time']}"):
            for drink, qty, price in od['items']:
                st.write(f"{drink} x {qty} = {qty*price} ฿")
            st.write(f"💰 รวม: {od['total']} บาท")
            if od['done']:
                st.success("สถานะ: เสร็จแล้ว")
            else:
                if st.button("✅ เสร็จแล้ว", key=f"done_{i}"):
                    st.session_state.orders[i]['done'] = True
                    st.experimental_rerun()
                else:
                    st.warning("สถานะ: ไม่เสร็จ")

# -------------------- Tab: ยอดขายรวม --------------------
with tabs[2]:
    st.subheader("📈 ยอดขายรวม")
    total_sale = 0
    cup_count = 0
    summary = {}
    for order in st.session_state.sales:
        for drink, qty, price in order:
            total_sale += qty * price
            cup_count += qty
            summary[drink] = summary.get(drink, 0) + qty

    st.metric("💵 รายได้รวม", f"{total_sale} บาท")
    st.metric("🥤 จำนวนแก้วทั้งหมด", f"{cup_count} แก้ว")

    st.subheader("📊 รายการที่ขาย")
    for drink, qty in summary.items():
        st.write(f"{drink}: {qty} แก้ว")
