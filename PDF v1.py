"""
Engineering & Admin PDF Toolkit — مجموعة أدوات هندسية وإدارية لملفات الـ PDF
MVP v2: Python 3.10+ / Streamlit / pypdf / Pandas / openpyxl
"""
import io
import streamlit as st
import pandas as pd
from pypdf import PdfReader, PdfWriter

st.set_page_config(page_title="مجموعة أدوات الـ PDF المهنية", page_icon="📄", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
html, body, [class*="css"], .stApp { font-family: 'Tajawal', sans-serif; direction: rtl; text-align: right; }
.stTabs [data-baseweb="tab-list"] { flex-direction: row-reverse; justify-content: flex-end; }
div[data-testid="stMetric"] { background: #ffffff; border: 1px solid #e6e8ee; border-radius: 12px; padding: 12px; }
</style>
""", unsafe_allow_html=True)

st.title("📄 مجموعة أدوات الـ PDF الهندسية والإدارية (الإصدار المطور)")
st.caption("أدوات محلية متكاملة لدمج، تقسيم، ضغط، وختم المخططات والمستندات الرسمية دون رفعها لأي سيرفر خارجي.")

with st.sidebar:
    st.header("🔒 الخصوصية والأمان")
    st.write("جميع عمليات المعالجة تتم محلياً وفي الذاكرة المؤقتة لجلستك، ولا يتم تخزين أي ملفات نهائياً.")
    st.divider()
    st.info("💡 **المكتبات المستخدمة:**\n`streamlit`, `pypdf`, `pandas`, `openpyxl`")

tab_merge, tab_split, tab_compress, tab_extract, tab_info = st.tabs([
    "🔗 دمج الملفات", 
    "✂️ تقسيم وربط", 
    "🗜️ ضغط وتحسين", 
    "📊 استخراج البيانات", 
    "ℹ️ خصائص الملف"
])

with tab_merge:
    st.subheader("دمج عدة ملفات PDF في ملف رسمي واحد")
    uploaded_files = st.file_uploader("اختر ملفات الـ PDF للدمج بترتيب صحيح", type=["pdf"], accept_multiple_files=True, key="merge_files")
    if uploaded_files:
        st.write(f"تم اختيار {len(uploaded_files)} ملفاً.")
        if st.button("بدء الدمج الشامل", type="primary"):
            writer = PdfWriter()
            for f in uploaded_files:
                reader = PdfReader(f)
                for page in reader.pages:
                    writer.add_page(page)
            output_stream = io.BytesIO()
            writer.write(output_stream)
            output_stream.seek(0)
            st.success("تم دمج الملفات بنجاح!")
            st.download_button(
                "⬇️ تحميل الملف المدمج النهائي",
                data=output_stream,
                file_name="merged_official_document.pdf",
                mime="application/pdf"
            )

with tab_split:
    st.subheader("تقسيم ملف PDF استخراج صفحات محددة")
    split_file = st.file_uploader("اختر ملف الـ PDF للتقسيم", type=["pdf"], key="split_file")
    if split_file:
        reader = PdfReader(split_file)
        total_pages = len(reader.pages)
        st.info(f"عدد الصفحات الكلي للملف: {total_pages}")
        
        col1, col2 = st.columns(2)
        start_p = col1.number_input("من الصفحة رقم", min_value=1, max_value=total_pages, value=1)
        end_p = col2.number_input("إلى الصفحة رقم", min_value=1, max_value=total_pages, value=min(5, total_pages))
        
        if st.button("استخراج النطاق المحدد", type="primary"):
            if start_p > end_p:
                st.error("رقم صفحة البداية يجب أن يكون أقل من أو مساوياً لصفحة النهاية.")
            else:
                writer = PdfWriter()
                for p_num in range(start_p - 1, end_p):
                    writer.add_page(reader.pages[p_num])
                out_stream = io.BytesIO()
                writer.write(out_stream)
                out_stream.seek(0)
                st.success(f"تم استخراج الصفحات من {start_p} إلى {end_p} بنجاح!")
                st.download_button(
                    "⬇️ تحميل الصفحات المستخرجة",
                    data=out_stream,
                    file_name=f"extracted_pages_{start_p}_to_{end_p}.pdf",
                    mime="application/pdf"
                )

with tab_compress:
    st.subheader("ضغط وتحسين حجم ملفات الـ PDF (تقليل المساحة للمخططات الكبيرة)")
    comp_file = st.file_uploader("اختر ملف الـ PDF للضغط", type=["pdf"], key="comp_file")
    if comp_file:
        reader = PdfReader(comp_file)
        st.info(f"حجم الملف الأصلي تقريباً: {comp_file.size / 1024:.1f} كيلوبايت | عدد الصفحات: {len(reader.pages)}")
        if st.button("تحسين وضغط الملف", type="primary"):
            writer = PdfWriter()
            for page in reader.pages:
                page.compress_content_streams()
                writer.add_page(page)
            writer.compress_identical_objects(remove_duplicate_objects=True)
            
            out_stream = io.BytesIO()
            writer.write(out_stream)
            out_stream.seek(0)
            
            new_size = len(out_stream.getvalue())
            st.success("تم ضغط وتحسين الملف بنجاح!")
            st.metric("الحجم الجديد", f"{new_size / 1024:.1f} كيلوبايت")
            st.download_button(
                "⬇️ تحميل الملف المضغوط",
                data=out_stream,
                file_name="compressed_document.pdf",
                mime="application/pdf"
            )

with tab_extract:
    st.subheader("استخراج النصوص والمحتوى إلى Excel لغرض المراجعة الإدارية")
    ext_file = st.file_uploader("اختر ملف الـ PDF للاستخراج", type=["pdf"], key="ext_file")
    if ext_file:
        reader = PdfReader(ext_file)
        if st.button("استخراج كافة النصوص والبيانات", type="primary"):
            data = []
            for idx, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                data.append({"الصفحة": idx + 1, "النص المستخرج": text[:800] + ("..." if len(text) > 800 else "")})
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
            
            out_excel = io.BytesIO()
            with pd.ExcelWriter(out_excel, engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name="البيانات المستخرجة", index=False)
                for ws in writer.book.worksheets:
                    ws.sheet_view.rightToLeft = True
            out_excel.seek(0)
            st.download_button(
                "⬇️ تحميل النتائج كملف Excel",
                data=out_excel,
                file_name="extracted_pdf_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

with tab_info:
    st.subheader("فحص خصائص ومستندات PDF الهندسية")
    info_file = st.file_uploader("اختر ملف PDF للفحص", type=["pdf"], key="info_file")
    if info_file:
        reader = PdfReader(info_file)
        meta = reader.metadata
        col1, col2 = st.columns(2)
        col1.metric("عدد الصفحات", len(reader.pages))
        if meta:
            col2.metric("إصدار الملف", getattr(reader, 'pdf_version', 'غير متوفر'))
            st.write(f"**العنوان:** {meta.get('/Title', 'غير متوفر')}")
            st.write(f"**المؤلف:** {meta.get('/Author', 'غير متوفر')}")
            st.write(f"**المنشئ / البرنامج:** {meta.get('/Creator', 'غير متوفر')}")
