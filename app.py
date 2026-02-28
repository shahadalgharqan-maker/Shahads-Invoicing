import os
import fitz
import streamlit as st

# -----------------------------
# Language Dictionary (UNCHANGED)
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
# Page Config
# -----------------------------
st.set_page_config(
    page_title="PDF XML Embedder",
    page_icon="📎",
    layout="wide"
)

# -----------------------------
# Sidebar Language Selector
# -----------------------------
lang = st.sidebar.selectbox("🌍 Language / اللغة", ["English", "العربية"])
T = translations[lang]

# -----------------------------
# Helper: Only Arabic Text Right-Aligned
# -----------------------------
def label(key):
    text = T[key]
    if lang == "العربية":
        return f"<div dir='rtl' style='text-align: right;'>{text}</div>"
    return text


def message(text):
    if lang == "العربية":
        st.markdown(
            f"<div dir='rtl' style='text-align:right;'>{text}</div>",
            unsafe_allow_html=True
        )
    else:
        st.write(text)


# -----------------------------
# Counter System
# -----------------------------
COUNTER_FILE = "embed_counter.txt"


def get_embed_count():
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "w") as f:
            f.write("0")

    with open(COUNTER_FILE, "r") as f:
        return int(f.read().strip() or "0")


def increment_embed_count():
    count = get_embed_count() + 1
    with open(COUNTER_FILE, "w") as f:
        f.write(str(count))
    return count


# -----------------------------
# Admin View
# -----------------------------
def show_admin_if_requested():
    try:
        admin_val = st.query_params.get("admin", "")
    except Exception:
        admin_val = st.experimental_get_query_params().get("admin", [""])[0]

    if isinstance(admin_val, list):
        admin_val = admin_val[0] if admin_val else ""

    if str(admin_val) != "1":
        return

    st.divider()
    st.subheader("Admin")

    pw = st.text_input("Password", type="password", key="admin_pw")

    if not pw:
        st.info("Enter password to view totals.")
        return

    if pw != st.secrets.get("ADMIN_PASSWORD", ""):
        st.error("Wrong password.")
        return

    st.success(f"📊 Total embeddings processed: {get_embed_count()}")


# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
.block-container { padding-top: 1.5rem; max-width: 1100px; }

div.stButton > button {
    padding: 0.65rem 1.1rem;
    border-radius: 10px;
    font-weight: 600;
}

.footer {
    margin-top: 4rem;
    padding-top: 1.5rem;
    border-top: 1px solid #E5E7EB;
    text-align: center;
    font-size: 13px;
    color: #6B7280;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER (UNCHANGED)
# -----------------------------
st.markdown("""
<div style='text-align: center; padding-top: 10px; padding-bottom: 5px;'>
    <h1 style='font-size: 42px; font-weight: 700; margin-bottom: 0px; color: #1F2937; letter-spacing: 0.5px;'>
        Shahad's Invoicing
    </h1>
    <p style='font-size: 15px; color: #6B7280; margin-top: 4px;'>
        Professional Invoicing Service
    </p>
</div>
<hr style='margin-top:20px; margin-bottom:30px; border:1px solid #E5E7EB;'>
""", unsafe_allow_html=True)

st.caption("Attach an XML file to a PDF invoice and download the updated PDF.")
st.divider()

# -----------------------------
# Upload Section
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    pdf_file = st.file_uploader(
        label("upload_pdf"),
        type=["pdf"],
        key="pdf_up"
    )

with col2:
    xml_file = st.file_uploader(
        label("upload_xml"),
        type=["xml"],
        key="xml_up"
    )

output_name = st.text_input(
    label("output_name"),
    "output.pdf",
    key="out_name"
)


# -----------------------------
# Embed Function
# -----------------------------
def embed_xml_bytes_in_pdf(pdf_bytes: bytes, xml_name: str, xml_bytes: bytes) -> bytes:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    doc.embfile_add(xml_name, xml_bytes)
    out = doc.tobytes()
    doc.close()
    return out


# -----------------------------
# Embed Button
# -----------------------------
if st.button(T["button"], use_container_width=True, key="embed_btn"):

    if not pdf_file or not xml_file:
        message(T["missing"])

    else:
        name = output_name.strip() or "output.pdf"

        if not name.lower().endswith(".pdf"):
            name += ".pdf"

        with st.spinner("Embedding XML..."):
            new_pdf = embed_xml_bytes_in_pdf(
                pdf_file.read(),
                xml_file.name,
                xml_file.read()
            )

        increment_embed_count()
        message(T["success"])

        st.download_button(
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
  For inquiries, please contact sh_6895@hotmail.com
</div>
""", unsafe_allow_html=True)

show_admin_if_requested()
