import pandas as pd
import streamlit as st

# ضبط إعدادات الصفحة
st.set_page_config(
    page_title="مشاهير دبي - فاحص الأسعار والمخزون",
    layout="centered"
)
# عرض الشعار (تأكدي من مطابقة اسم الملف في مجلد stock_app)
try:
    st.image("logo.png.png", width=140)
except Exception:
    try:
        st.image("logo.png", width=140)
    except Exception:
        pass

# عنوان التطبيق
st.title(" نظام التحقق السريع من الأسعار والمخزون📦")
st.subheader("شركة مشاهير دبي التجارية - فرع مكة الراشدية")
st.markdown("---")

# تحميل بيانات المنتجات
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("products.xlsx", dtype={"barcode": str})
        return df
    except FileNotFoundError:
        st.error("لم يتم العثور على ملف products.xlsx.")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    search_type = st.radio(
        "اختر طريقة البحث:",
        ("الباركود", "اسم المنتج"),
        horizontal=True
    )

    query = st.text_input("أدخل نص البحث أو امسح الباركود:")

    if query:
        if search_type == "الباركود":
            results = df[df['barcode'].astype(str).str.contains(query, na=False)]
        else:
            results = df[df['product_name'].astype(str).str.contains(query, case=False, na=False)]
        
        if not results.empty:
            st.success(f"تم العثور على {len(results)} منتج")
            for index, row in results.iterrows():
                st.markdown(f"### : {row['product_name']}")
                st.markdown(f"**السعر:** {row['price']} ر.س")
                st.markdown(f"**الكمية المتاحة في المخازن:** {row['stock']} قطعة")
                st.markdown(f"**الموقع:** {row['location']}")
                st.markdown("---")
        else:
            st.warning("لم يتم العثور على أي منتج حسب البحث.")