import spacy
import requests
from bs4 import BeautifulSoup
import streamlit as st

st.set_page_config(
    page_title="Quran Similarity Finder (مكتشف تشابه القرآن)",
    page_icon="🕋",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 190px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 100px;
        margin-left: -500px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h1 style='text-align: centre; color: #00CDCD;'>QURAN SIMILARITY FINDER (مكتشف تشابه القرآن)</h1>",
                unsafe_allow_html=True)
# Surah Scraping

m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: snow; color : blue
}
</style>""", unsafe_allow_html=True)
with open('C:\Python3.10.1\Lib\site-packages\QtDesigner\VsCode Py\surah.txt', 'r') as file:
    kp = file.read()

kp = kp.split('  ')

col1, col2, col3 = st.columns(3)
with col2:
    surah_select = st.selectbox("SELECT SURAH (CHAPTER) [اختر سوراه]", kp)

st.text('')
st.text('')
ultimate_outcome = st.button('Find The Most Common Ayat (البحث عن الآيات الأكثر شيوعًا)')

if ultimate_outcome:
    with st.spinner('Collecting Surah Information Plz Wait... (... جمع معلومات السورة تحلى بالصبر)'):
        nlp = spacy.load('en_core_web_lg')
        url = 'https://quran411.com/{}'.format(surah_select)

        mulk = requests.get(url)
        html = mulk.content

        soup = BeautifulSoup(html, 'html.parser')

        surah = soup.find('div', id='translator')
        surah_dict = {}

        j = 1
        ayats = surah.find('ol')
        for i in ayats.find_all('li'):
            surah_dict[j] = i.text
            j += 1

    # Surah Scraping

    # for (i, j) in surah_dict.items():
    #     print(i, ":", j, '\n')

    # print('-----------------------------------------------------------------------------------------------------------------------------------')
        p = 1
        stop_words = nlp.Defaults.stop_words

    with st.spinner(f'Analyzing on {surah_select}. It Will Give You The Most Common Ayat in This Surah(Chapter) '):
        def lemma_and_stops(dicty):
            global p
            surah_dict_lemma = {}
            for i in dicty.values():
                i = i.lower()
                temp = nlp(i)
                lst = []
                for j in temp:
                    if j.lemma_ not in stop_words and not j.is_punct:
                        lst.append(j.lemma_)
                surah_dict_lemma[p] = ' '.join(lst)
                p += 1

            return surah_dict_lemma


        update1 = lemma_and_stops(surah_dict)

        # for (i, j) in update1.items():
        #     print(i, ":", j, '\n')

        print("calculating Similarity...", '\n')
        def calculate_similarity(dicty):
            similarity = {}
            kp = 1
            for (i, k) in dicty.items():
                temp = nlp(k)
                lst = []
                for (j, p) in dicty.items():
                    temp2 = nlp(p)
                    if temp.similarity(temp2) == 1.0:
                        continue
                    else:
                        lst.append(temp.similarity(temp2))
                highest = max(lst)
                similarity[i] = highest

            return similarity


        update2 = calculate_similarity(update1)
        templ = []
        print("Similarity Done...", '\n')
        for i in update2.values():
            templ.append(i)

        top = max(templ)

        def get_verse(dicty):
            for (i, j) in dicty.items():
                if j == top:
                    verse = i
                    break
            return verse

        final_verse = get_verse(update2)

        for (i, j) in surah_dict.items():
            if i == final_verse:
                st.text('')
                st.text('')
                col11, col22 = st.columns(2)
                with col11:
                    # st.write(f"EXPECTED ULTIMATE OUTCOME ALLAH KNOW'S THE BEST")
                    st.markdown(
                        "<h3 style='text-align: centre; color: #EEEE00;'>EXPECTED ULTIMATE TEACHING BUT ALLAH KNOW'S THE BEST</h3>",
                        unsafe_allow_html=True)
                with col22:
                    st.write(j)
                col111, col222 = st.columns(2)
                with col111:
                    st.markdown(
                        "<h3 style='text-align: centre; color: #EEEE00;'>VERSE NO</h3>",
                        unsafe_allow_html=True)
                with col222:
                    st.write(i)
                break