
import fitz
import streamlit as st



st.set_page_config(
    page_title="PDF XML Embedder",
    page_icon="📎",
    layout="wide"
)

st.markdown("""
<style>
.block-container { padding-top: 1.5rem; max-width: 1100px; }

.company-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
}
.company-name {
    font-size: 16px;
    font-weight: 600;
    color: #2C3E50;
}
.top-divider {
    height: 1px;
    background-color: #E5E7EB;
    margin-bottom: 1.5rem;
}

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

st.markdown("""
<div style='
    text-align: center;
    padding-top: 10px;
    padding-bottom: 5px;
'>
    <h1 style='
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0px;
        color: #1F2937;
        letter-spacing: 0.5px;
    '>
        Shahad's Invoicing
    </h1>
    <p style='
        font-size: 15px;
        color: #6B7280;
        margin-top: 4px;
    '>
        Professional Invoicing Service
    </p>
</div>
<hr style='margin-top:20px; margin-bottom:30px; border:1px solid #E5E7EB;'>
""", unsafe_allow_html=True)

st.markdown("# Embed XML into PDF")
st.caption("Attach an XML file to a PDF invoice and download the updated PDF.")
st.divider()

col1, col2 = st.columns(2)
with col1:
    pdf_file = st.file_uploader("1) Upload PDF", type=["pdf"])
with col2:
    xml_file = st.file_uploader("2) Upload XML", type=["xml"])

output_name = st.text_input("Output file name", "output.pdf")

def embed_xml_bytes_in_pdf(pdf_bytes: bytes, xml_name: str, xml_bytes: bytes) -> bytes:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    doc.embfile_add(xml_name, xml_bytes)
    out = doc.tobytes()
    doc.close()
    return out

if st.button("Embed XML into PDF", use_container_width=True):
    if not pdf_file or not xml_file:
        st.error("Please upload both a PDF and an XML file.")
    else:
        name = output_name.strip() or "output.pdf"
        if not name.lower().endswith(".pdf"):
            name += ".pdf"

        with st.spinner("Embedding XML..."):
            new_pdf = embed_xml_bytes_in_pdf(pdf_file.read(), xml_file.name, xml_file.read())

        st.success("✅ Done! The XML was embedded as an attachment.")
        st.download_button(
            "⬇ Download embedded PDF",
            data=new_pdf,
            file_name=name,
            mime="application/pdf",
            use_container_width=True
        )

st.markdown("""
<div class="footer">
  © 2026 Shahad's Invoicing Company Ltd.<br>
  For inquiries, please contact sh_6895@hotmail.com
</div>
""", unsafe_allow_html=True)
