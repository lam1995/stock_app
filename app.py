import pandas as pd
import streamlit as st

# تحميل البيانات مع تحديث مباشر
@st.cache_data(ttl=1)
def load_data():
    return pd.read_excel("products.xlsx", dtype={"barcode": str})

df = load_data()

st.title("شركة مشاهير دبي التجارية - فرع مكة الراشدية")
st.subheader("فاحص الأسعار والمخزون الذكي")

# خانة البحث بالباركود أو اسم المنتج
search_query = st.text_input("🔍 ابحث برقم الباركود أو اسم المنتج:")

if search_query:
    # البحث في الجدول
    result = df[
        df["barcode"].astype(str).str.contains(search_query, na=False) |
        df["name"].astype(str).str.contains(search_query, na=False)
    ]

    if not result.empty:
        for index, row in result.iterrows():
            st.markdown("---")
            st.write(f"### 📦 اسم المنتج: {row['name']}")
            st.write(f"💰 **السعر:** {row['price']}")
            st.write(f"📊 **المخزون الحالي:** {row['stock']}")

            # تحديد الكمية المراد خصمها (مبيعات)
            sold_qty = st.number_input(
                "الكمية المباعة:", 
                min_value=1, 
                max_value=int(row['stock']), 
                value=1, 
                key=f"qty_{index}"
            )

            # زر تأكيد البيع والخصم
            if st.button(f"🛒 تأكيد البيع وخصم الكمية", key=f"btn_{index}"):
                # خصم الكمية من الجدول
                df.at[index, 'stock'] = int(row['stock']) - int(sold_qty)
                # حفظ التحديث في ملف الإكسيل
                df.to_excel("products.xlsx", index=False)
                st.success(f"تمت العملية بنجاح! المخزون المتبقي الآن: {df.at[index, 'stock']}")
                st.rerun()
    else:
        st.warning("عذراً، المنتج غير موجود في النظام.")
