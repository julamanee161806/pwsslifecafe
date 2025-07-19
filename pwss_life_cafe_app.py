
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

import tkinter as tk
from tkinter import messagebox
import datetime

# เมนูจากร้าน PWS'S LIFE CAFE
menus = {
    "Coffee (ร้อน)": [
        ("เอสเพรสโซ่", 30), ("อเมริกาโน่", 30), ("คาปูชิโน่", 35),
        ("ลาเต้", 35), ("มอคค่า", 40), ("คาราเมล", 40)
    ],
    "Coffee (เย็น)": [
        ("อเมริกาโน่", 35), ("คาปูชิโน่", 40), ("ลาเต้", 40),
        ("มอคค่า", 45), ("คาราเมล", 45), ("Blue Sky Coffee", 40)
    ],
    "Coffee (ปั่น)": [
        ("อเมริกาโน่", 40), ("คาปูชิโน่", 45), ("ลาเต้", 45),
        ("มอคค่า", 50), ("คาราเมล", 50)
    ],
    "เมนูพิเศษ": [
        ("อเมริกาโน่ส้ม", 50), ("อเมริกาโน่น้ำผึ้ง", 50), ("กาแฟมะพร้าว", 50)
    ],
    "Tea": [
        ("มัทฉะร้อน", 30), ("มัทฉะลาเต้", 40), ("มัทฉะลาเต้ปั่น", 45), ("ชามะนาว", 35)
    ],
    "Soda": [
        ("บลูโซดา", 40), ("มะนาวโซดา", 35), ("น้ำผึ้งมะนาวโซดา", 40),
        ("อิตาเลียนโซดา", 35), ("ลิ้นจี่โซดา", 35), ("เบอรี่มิ้นต์", 35), ("ชาสตอเบอรี่", 35)
    ],
    "Chocolate": [
        ("ช็อกโกแลตร้อน", 30), ("ช็อกโกแลตเย็น", 40), ("ช็อกโกปั่น", 45)
    ],
    "Milk": [
        ("นมสตอเบอรี่", 40), ("นมกล้วย", 40), ("นมคาราเมล", 40),
        ("นมเผือก", 40), ("ชานม", 40), ("นมบลูเบอรี่", 40)
    ],
    "Smoothie": [
        ("Orange Smoothie", 45), ("Lychee Smoothie", 45), ("Mango Smoothie", 45),
        ("Kiwi Smoothie", 45), ("Strawberry Smoothie", 45),
        ("Blueberry Smoothie", 45), ("Passion Fruit Smoothie", 45)
    ]
}

sales_data = []
orders_in_progress = []
orders_completed = []

root = tk.Tk()
root.title("PWS'S LIFE CAFE - ระบบแคชเชียร์")
root.geometry("850x700")

selected_items = []
total_price = 0
cup_count = 0
payment_method = tk.StringVar(value="เงินสด")

frame_name = tk.Frame(root)
frame_name.pack(pady=5)

search_frame = tk.Frame(root)
search_frame.pack(pady=5)

frame_items = tk.Frame(root)
frame_items.pack(pady=5)

frame_order = tk.Frame(root)
frame_order.pack(pady=5)

frame_bottom = tk.Frame(root)
frame_bottom.pack(pady=10)

# ===== ชื่อผู้รับ =====
tk.Label(frame_name, text="ชื่อผู้รับ:").pack(side=tk.LEFT)
entry_name = tk.Entry(frame_name, width=30)
entry_name.pack(side=tk.LEFT)

# ===== ช่องค้นหาเมนู =====
search_var = tk.StringVar()

def search_menu():
    keyword = search_var.get().strip().lower()
    show_all_menus(filter_keyword=keyword)

tk.Label(search_frame, text="ค้นหาเมนู: ").pack(side=tk.LEFT)
tk.Entry(search_frame, textvariable=search_var, width=30).pack(side=tk.LEFT)
tk.Button(search_frame, text="ค้นหา", command=search_menu).pack(side=tk.LEFT)

# ===== รายการสั่งซื้อ =====
order_listbox = tk.Listbox(frame_order, width=70, height=10)
order_listbox.pack()

label_total = tk.Label(frame_bottom, text="รวม: 0 บาท", font=("Tahoma", 12))
label_total.pack()

label_change = tk.Label(frame_bottom, text="เงินทอน: 0 บาท", font=("Tahoma", 12))
label_change.pack()

frame_payment = tk.Frame(frame_bottom)
frame_payment.pack()

entry_cash = tk.Entry(frame_payment)
entry_cash.pack(side=tk.LEFT)
tk.Radiobutton(frame_payment, text="เงินสด", variable=payment_method, value="เงินสด").pack(side=tk.LEFT)
tk.Radiobutton(frame_payment, text="โอน", variable=payment_method, value="โอน").pack(side=tk.LEFT)

def add_item(name, price, qty=1):
    global total_price, cup_count
    selected_items.append((name, price, qty))
    order_listbox.insert(tk.END, f"{name} x{qty} - {price * qty} บาท")
    total_price += price * qty
    cup_count += qty
    label_total.config(text=f"รวม: {total_price} บาท")

def clear_order():
    global selected_items, total_price, cup_count
    selected_items.clear()
    order_listbox.delete(0, tk.END)
    total_price = 0
    cup_count = 0
    label_total.config(text="รวม: 0 บาท")
    label_change.config(text="เงินทอน: 0 บาท")
    entry_cash.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    search_var.set("")
    show_all_menus()

def pay():
    global selected_items, total_price, cup_count
    name = entry_name.get().strip()
    if not name:
        messagebox.showwarning("คำเตือน", "กรุณากรอกชื่อผู้รับ")
        return
    try:
        cash = float(entry_cash.get()) if payment_method.get() == "เงินสด" else total_price
        change = cash - total_price
        if change < 0:
            messagebox.showerror("ผิดพลาด", "จำนวนเงินไม่เพียงพอ")
            return
        label_change.config(text=f"เงินทอน: {change:.2f} บาท")

        now = datetime.datetime.now()
        order = {
            "ชื่อ": name,
            "รายการ": selected_items.copy(),
            "รวม": total_price,
            "จำนวนแก้ว": cup_count,
            "ชำระ": payment_method.get(),
            "เวลา": now.strftime("%H:%M:%S")
        }
        sales_data.append(order)
        orders_in_progress.append(order)

        messagebox.showinfo("สำเร็จ", f"รับออเดอร์จาก {name} แล้ว\nเวลา: {order['เวลา']}")
        clear_order()

    except ValueError:
        messagebox.showerror("ผิดพลาด", "กรุณาใส่จำนวนเงินให้ถูกต้อง")

def show_summary():
    total_sales = sum(s['รวม'] for s in sales_data)
    total_cups = sum(s['จำนวนแก้ว'] for s in sales_data)
    cash = sum(s['รวม'] for s in sales_data if s['ชำระ'] == "เงินสด")
    transfer = sum(s['รวม'] for s in sales_data if s['ชำระ'] == "โอน")
    messagebox.showinfo("รายงาน", f"ยอดขายรวม: {total_sales} บาท\nจำนวนแก้ว: {total_cups}\nเงินสด: {cash} บาท\nโอน: {transfer} บาท")

def show_orders():
    window = tk.Toplevel(root)
    window.title("รายการออเดอร์ทั้งหมด")

    tk.Label(window, text="\u23F3 ยังไม่เสร็จ", font=("Tahoma", 12, "bold")).pack()
    for i, order in enumerate(orders_in_progress):
        text = f"[{order['เวลา']}] {order['ชื่อ']} | {', '.join([f'{x[0]} x{x[2]}' for x in order['รายการ']])} | {order['รวม']} บาท"
        frame = tk.Frame(window)
        frame.pack(fill='x', pady=2)
        tk.Label(frame, text=text).pack(side=tk.LEFT)
        tk.Button(frame, text="เสร็จแล้ว", command=lambda idx=i: mark_done(idx, window)).pack(side=tk.RIGHT)

    tk.Label(window, text="\n✅ เสร็จแล้ว", font=("Tahoma", 12, "bold")).pack()
    for order in orders_completed:
        text = f"[{order['เวลา']}] {order['ชื่อ']} | {', '.join([f'{x[0]} x{x[2]}' for x in order['รายการ']])} | {order['รวม']} บาท"
        tk.Label(window, text=text).pack()

def mark_done(index, window):
    order = orders_in_progress.pop(index)
    orders_completed.append(order)
    window.destroy()
    show_orders()

def show_all_menus(filter_keyword=None):
    for widget in frame_items.winfo_children():
        widget.destroy()

    for category, items in menus.items():
        filtered_items = []
        for name, price in items:
            if not filter_keyword or filter_keyword in name.lower():
                filtered_items.append((name, price))
        if not filtered_items:
            continue

        tk.Label(frame_items, text=category, font=("Tahoma", 10, "bold")).pack(anchor="w", pady=(10, 0))

        for name, price in filtered_items:
            item_frame = tk.Frame(frame_items)
            item_frame.pack(anchor="w", padx=20, pady=2)

            tk.Label(item_frame, text=f"{name} ({price}฿)", width=25, anchor="w").pack(side=tk.LEFT)

            qty_var = tk.IntVar(value=1)
            tk.Spinbox(item_frame, from_=1, to=10, width=3, textvariable=qty_var).pack(side=tk.LEFT, padx=5)

            tk.Button(item_frame, text="เพิ่ม", command=lambda n=name, p=price, q=qty_var: add_item(n, p, q.get())).pack(side=tk.LEFT)

# แสดงเมนูเมื่อเริ่มต้น
show_all_menus()

# ===== ปุ่มด้านล่าง =====
tk.Button(frame_bottom, text="✅ ชำระเงิน", bg="green", fg="white", command=pay).pack(pady=5)
tk.Button(frame_bottom, text="❌ ยกเลิกออเดอร์", bg="red", fg="white", command=clear_order).pack(pady=2)
tk.Button(frame_bottom, text="📊 รายงานยอดขาย", command=show_summary).pack()
tk.Button(frame_bottom, text="📋 ออเดอร์ทั้งหมด", command=show_orders).pack(pady=5)

root.mainloop()
