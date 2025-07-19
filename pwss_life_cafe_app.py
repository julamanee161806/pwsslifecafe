
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

st.set_page_config(page_title="PWS's Life Cafe - ระบบแคชเชียร์", layout="wide")

===== ตั้งข้อมูลเมนูตามภาพ =====

menu_data = { "กาแฟ": { "ร้อน": { "เอสเพรสโซ่": 30, "อเมริกาโน่": 30, "คาปูชิโน่": 35, "ลาเต้": 35, "มอคค่า": 40, "คาราเมล": 40 }, "เย็น": { "อเมริกาโน่": 35, "คาปูชิโน่": 40, "ลาเต้": 40, "มอคค่า": 45, "คาราเมล": 45, "อเมริกาโน่ส้ม": 50, "อเมริกาโน่น้ำผึ้ง": 50, "Blue Sky Coffee": 40, "กาแฟมะพร้าว": 50 }, "ปั่น": { "อเมริกาโน่": 40, "คาปูชิโน่": 45, "ลาเต้": 45, "มอคค่า": 50, "คาราเมล": 50, "ช็อกโก": 45 } }, "ชา": { "เมนู": { "มัทฉะ ร้อน": 30, "มัทฉะลาเต้": 40, "มัทฉะลาเต้ ปั่น": 45, "ชามะนาว": 35, "ชานม": 40 } }, "นม": { "เมนู": { "นมสตอเบอรี่": 40, "นมกล้วย": 40, "นมคาราเมล": 40, "นมเผือก": 40, "นมบลูเบอรี่": 40 } }, "โซดา": { "เมนู": { "บลูโซดา": 40, "มะนาวโซดา": 35, "น้ำผึ้งมะนาวโซดา": 40, "อิตาเลี่ยนโซดา": 35, "ลิ้นจี่โซดา": 35, "เบอรี่มิ้นต์": 35, "ชาสตอเบอรี่": 35 } }, "สมูทตี้": { "เมนู": { "Orange Smoothie ส้ม ปั่น": 45, "Lychee Smoothie ลิ้นจี่ ปั่น": 45, "Mango Smoothie มะม่วง ปั่น": 45, "Kiwi Smoothie กีวี่ ปั่น": 45, "Strawberry Smoothie สตอเบอรี่ ปั่น": 45, "Blueberry Smoothie บลูเบอรี่ ปั่น": 45, "Passion Fruit Smoothie เสาวรส ปั่น": 45 } } }

if 'orders' not in st.session_state: st.session_state.orders = [] if 'selected_cat' not in st.session_state: st.session_state.selected_cat = None if 'selected_sub' not in st.session_state: st.session_state.selected_sub = None

st.title("☕ PWS's LIFE CAFE - ระบบแคชเชียร์")

===== เลือกหมวดหลัก =====

st.subheader("เลือกหมวดหลัก") cols = st.columns(len(menu_data)) for i, cat in enumerate(menu_data): if cols[i].button(cat): st.session_state.selected_cat = cat st.session_state.selected_sub = None

cat = st.session_state.selected_cat sub = st.session_state.selected_sub

===== เลือกหมวดย่อย =====

if cat: st.divider() st.subheader(f"เลือกหมวดย่อยในหมวด {cat}") subs = menu_data[cat].keys() cols = st.columns(len(subs)) for i, subcat in enumerate(subs): if cols[i].button(subcat): st.session_state.selected_sub = subcat

===== แสดงเมนูและฟอร์มสั่ง =====

if cat and sub: st.divider() st.subheader(f"เมนู: {cat} > {sub}") items = menu_data[cat][sub]

quantities = {}
total = 0
for item, price in items.items():
    col1, col2, col3 = st.columns([3,1,1])
    col1.write(f"{item} - {price} บาท")
    q = col2.number_input("", min_value=0, step=1, key=f"{cat}_{sub}_{item}")
    col3.write(f"{price * q} บาท")
    quantities[item] = (price, q)
    total += price * q

cust = st.text_input("ชื่อผู้รับ")
paid = st.number_input("รับเงินมา", min_value=0, step=1)
change = paid - total if paid >= total else 0

st.info(f"ยอดรวม: {total} บาท")
st.success(f"เงินทอน: {change} บาท")

if st.button("✅ ยืนยันออเดอร์"):
    order_items = [(i, p, q) for i, (p, q) in quantities.items() if q > 0]
    if order_items:
        st.session_state.orders.append({
            "name": cust,
            "items": order_items,
            "total": total,
            "paid": paid,
            "change": change,
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "done": False
        })
        st.success("บันทึกออเดอร์แล้ว")
        st.session_state.selected_cat = None
        st.session_state.selected_sub = None
        st.experimental_rerun()

===== แสดงออเดอร์ทั้งหมด =====

st.divider() st.subheader("รายการออเดอร์ทั้งหมด") if st.session_state.orders: for idx, o in enumerate(st.session_state.orders): with st.expander(f"{o['time']} — {o['name']} | ยอด {o['total']} บาท"): for it, pr, q in o['items']: st.write(f"{it} x{q} = {pr*q} บาท") st.write(f"รับเงิน: {o['paid']} | ทอน: {o['change']} บาท") btn = st.button("✅ เสร็จแล้ว" if not o['done'] else "✔️ เสร็จแล้ว", key=f"done_{idx}") if btn: st.session_state.orders[idx]['done'] = True st.experimental_rerun() else: st.info("ยังไม่มีออเดอร์")

===== รายงานยอดขาย =====

st.divider() if st.button("📊 ดูยอดขายรวม"): total_sum = sum(o['total'] for o in st.session_state.orders) cups = sum(q for o in st.session_state.orders for _, _, q in o['items']) st.success(f"ยอดรวม: {total_sum} บาท | จำนวนแก้ว: {cups} ")

