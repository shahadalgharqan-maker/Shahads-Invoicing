import streamlit as st


# -----------------------------
# Language Dictionary (YOUR TEXT – unchanged)
# -----------------------------
translations = {
    "English": {
        "upload_pdf": "1) Upload PDF",
        "upload_xml": "2) Upload XML",
        "output_name": "Output file name",
        "button": "Embed XML into PDF",
        "success": "✅ Done! The XML was embedded as an attachment.",
        "download": "⬇ Download embedded PDF",
        "missing": "Please upload both a PDF and an XML file.",
    },
    "العربية": {
        "upload_pdf": "PDF ارفع ملف",
        "upload_xml": "XML ارفع ملف",
        "output_name": "اختر اسم الملف الجديد",
        "button": "إتمام العملية",
        "success": "✅ داخل الفاتورة بنجاح XML تم إدخال ملف",
        "download": "⬇ تحميل الملف الجديد",
        "missing": "معاً PDF وملف XML يرجى رفع ملف",
    }
}

# -----------------------------
# Sidebar Language Selector
# -----------------------------
lang = st.sidebar.selectbox("🌍 Language / اللغة", ["English", "العربية"])
T = translations[lang]


COUNTER_FILE = "embed_counter.txt"

def get_embed_count():
@@ -19,7 +50,6 @@ def increment_embed_count():
    return count

def show_admin_if_requested():
    # admin can be "1" or ["1"] depending on Streamlit version
    try:
        admin_val = st.query_params.get("admin", "")
    except Exception:
@@ -71,6 +101,9 @@ def show_admin_if_requested():
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER (UNCHANGED)
# -----------------------------
st.markdown("""
<div style='text-align: center; padding-top: 10px; padding-bottom: 5px;'>
    <h1 style='font-size: 42px; font-weight: 700; margin-bottom: 0px; color: #1F2937; letter-spacing: 0.5px;'>
@@ -86,13 +119,16 @@ def show_admin_if_requested():
st.caption("Attach an XML file to a PDF invoice and download the updated PDF.")
st.divider()

# -----------------------------
# Upload Section (TRANSLATED)
# -----------------------------
col1, col2 = st.columns(2)
with col1:
    pdf_file = st.file_uploader("1) Upload PDF", type=["pdf"], key="pdf_up")
    pdf_file = st.file_uploader(T["upload_pdf"], type=["pdf"], key="pdf_up")
with col2:
    xml_file = st.file_uploader("2) Upload XML", type=["xml"], key="xml_up")
    xml_file = st.file_uploader(T["upload_xml"], type=["xml"], key="xml_up")

output_name = st.text_input("Output file name", "output.pdf", key="out_name")
output_name = st.text_input(T["output_name"], "output.pdf", key="out_name")

def embed_xml_bytes_in_pdf(pdf_bytes: bytes, xml_name: str, xml_bytes: bytes) -> bytes:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
@@ -101,9 +137,12 @@ def embed_xml_bytes_in_pdf(pdf_bytes: bytes, xml_name: str, xml_bytes: bytes) ->
    doc.close()
    return out

if st.button("Embed XML into PDF", use_container_width=True, key="embed_btn"):
# -----------------------------
# Embed Button (TRANSLATED)
# -----------------------------
if st.button(T["button"], use_container_width=True, key="embed_btn"):
    if not pdf_file or not xml_file:
        st.error("Please upload both a PDF and an XML file.")
        st.error(T["missing"])
    else:
        name = output_name.strip() or "output.pdf"
        if not name.lower().endswith(".pdf"):
@@ -112,19 +151,21 @@ def embed_xml_bytes_in_pdf(pdf_bytes: bytes, xml_name: str, xml_bytes: bytes) ->
        with st.spinner("Embedding XML..."):
            new_pdf = embed_xml_bytes_in_pdf(pdf_file.read(), xml_file.name, xml_file.read())

        # count only after success
        increment_embed_count()

        st.success("✅ Done! The XML was embedded as an attachment.")
        st.success(T["success"])
        st.download_button(
            "⬇ Download embedded PDF",
            T["download"],
            data=new_pdf,
            file_name=name,
            mime="application/pdf",
            use_container_width=True,
            key="download_btn"
        )

# -----------------------------
# Footer (UNCHANGED)
# -----------------------------
st.markdown("""
<div class="footer">
  © 2026 Shahad's Invoicing Company Ltd.<br>
@@ -133,4 +174,3 @@ def embed_xml_bytes_in_pdf(pdf_bytes: bytes, xml_name: str, xml_bytes: bytes) ->
""", unsafe_allow_html=True)

show_admin_if_requested()
