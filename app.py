import openai
import fitz  # PyMuPDF
import os
import streamlit as st

openai.api_key = st.secrets["openai_api_key"]  # Clé OpenAI depuis les secrets Streamlit

def extraire_texte_pdf(fichier_pdf):
    texte = ""
    with fitz.open(stream=fichier_pdf.read(), filetype="pdf") as doc:
        for page in doc:
            texte += page.get_text()
    return texte

def resumer_document(texte, niveau="standard"):
    if niveau == "court":
        prompt = "Fais un résumé très bref (5 lignes max) du texte suivant :"
    elif niveau == "détaillé":
        prompt = "Fais un résumé très détaillé avec tous les points importants du texte suivant :"
    else:
        prompt = "Fais un résumé clair et synthétique du texte suivant :"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt + "\n\n" + texte}]
    )
    return response["choices"][0]["message"]["content"]

st.set_page_config(page_title="IA Résumé Document", layout="centered")
st.title("📄 Analyse & Résumé de Documents Professionnels")
st.markdown("Optimisez votre temps avec un résumé IA instantané de vos fichiers PDF.")

uploaded_file = st.file_uploader("Choisissez un fichier PDF à analyser", type=["pdf"])
niveau = st.selectbox("Niveau de résumé souhaité :", ["court", "standard", "détaillé"])

if uploaded_file and st.button("Analyser le document"):
    with st.spinner("Analyse en cours..."):
        texte = extraire_texte_pdf(uploaded_file)
        resume = resumer_document(texte, niveau)
    st.success("Analyse terminée !")
    st.subheader("🧠 Résumé :")
    st.write(resume)

st.markdown("---")
st.caption("Projet d'IA by Freelance Innovator ✨")