import pandas as pd
import streamlit as st
import os

@st.cache_data(ttl=1)
def load_data():
    return pd.read_excel("products.xlsx", dtype=str)

df = load_data()

# عرض شعار الشركة (الصورة) في أعلى التطبيق إذا كانت متوفرة
if os.path.exists("logo.png"):
    st.image("logo.png", width=150)
elif os.path.exists("logo.png.png"):
    st.image("logo.png.png", width=150)

st.title("شركة مشاهير دبي التجارية - فرع مكة الراشدية")
st.subheader("فاحص الأسعار والمخزون الذكي")

# خانة البحث الشاملة
search_query = st.text_input("🔍 ابحث برقم الباركود أو اسم المنتج:")

if search_query:
    # البحث في جميع أعمدة الجدول
    mask = df.astype(str).apply(lambda col: col.str.contains(search_query, case=False, na=False)).any(axis=1)
    result = df[mask]

    if not result.empty:
        for index, row in result.iterrows():
            st.markdown("---")
            # قراءة البيانات بناءً على أسماء الأعمدة في جدولك
            code_val = row.get('rcode', row.iloc[0])
            name_val = row.get('product name', row.iloc[1])
            price_val = row.get('price', row.iloc[2])
            stock_val = row.get('stock', row.iloc[3])

            st.write(f"### 📦 اسم المنتج: {name_val}")
            st.write(f"🏷️ **الباركود:** {code_val}")
            st.write(f"💰 **السعر:** {price_val}")
            st.write(f"📊 **المخزون الحالي:** {stock_val}")

            try:
                current_stock = int(float(stock_val))
                sold_qty = st.number_input(
                    "الكمية المباعة:", 
                    min_value=1, 
                    max_value=max(1, current_stock), 
                    value=1, 
                    key=f"qty_{index}"
                )

                if st.button("🛒 تأكيد البيع وخصم الكمية", key=f"btn_{index}"):
                    # تحديث المخزون في عمود stock
                    df.at[index, 'stock'] = str(current_stock - int(sold_qty))
                    df.to_excel("products.xlsx", index=False)
                    st.success(f"تمت العملية بنجاح! المخزون المتبقي: {df.at[index, 'stock']}")
                    st.rerun()
            except:
                pass
    else:
        st.warning("عذراً، المنتج غير موجود في النظام.")
