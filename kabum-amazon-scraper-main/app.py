# ---------------------------------------------------------------
# Comparador de Preços KaBuM x Amazon
# Projeto desenvolvido para aprendizado em Python e Web Scraping
# (feito por estudantes em curto período, sujeito a bugs)
# ---------------------------------------------------------------

import streamlit as st
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

# ---------------------- CONFIG STREAMLIT ----------------------
# Define título da página e layout em tela cheia
st.set_page_config(page_title="Comparador KaBuM x Amazon", layout="wide")

# Cabeçalho centralizado
st.markdown("<h1 style='text-align: center;'>🛒 Comparador de Preços</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Digite o nome do produto e veja as ofertas lado a lado.</p>", unsafe_allow_html=True)

# ---------------------- FUNÇÕES AUXILIARES ----------------------
# Função para normalizar título (usada na URL da KaBuM)
def normalize_title_to_link(title):
    return unidecode(title.lower().replace(' ', '-').replace('/', '-'))

# Converte preço (string) em número float
def limpar_preco(p):
    try:
        return float(p.replace('R$', '').replace('.', '').replace(',', '.').strip())
    except:
        return None

# ---------------------- BUSCA NA KABUM ----------------------
def buscar_kabum(termo):
    url = "https://servicespub.prod.api.aws.grupokabum.com.br/catalog/v2/products"
    params = {"query": termo, "page_number": 1, "page_size": 5}
    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        produtos = []
        for item in r.json().get("data", []):
            attr = item.get("attributes", {})
            nome = attr.get("title")
            preco = attr.get("price_with_discount")
            fotos = attr.get("photos", {}).get("g", "")
            imagem = fotos[0] if isinstance(fotos, list) and fotos else None
            id_produto = item.get("id")
            url_produto = f"https://www.kabum.com.br/produto/{id_produto}/{normalize_title_to_link(nome)}"
            if nome:
                produtos.append({
                    "nome": nome,
                    "preco": preco,
                    "imagem": imagem,
                    "url": url_produto
                })
        return produtos
    except:
        # Em caso de erro, retorna lista vazia
        return []

# ---------------------- BUSCA NA AMAZON ----------------------
def buscar_amazon(termo):
    # Cria sessão com headers para evitar bloqueio
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept-Language': 'pt-BR, pt;q=0.9'
    })

    # Monta URL de pesquisa
    base_url = f'https://www.amazon.com.br/s?k={termo}'
    res = session.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')

    # Captura os links dos produtos
    links = []
    for a in soup.find_all('a', {'class': 'a-link-normal s-no-outline'}, href=True):
        if '/dp/' in a['href']:
            links.append("https://www.amazon.com.br" + a['href'])

    # Extrai as informações de até 5 produtos
    produtos = []
    for url in list(dict.fromkeys(links))[:5]:
        produto = extrair_info_amazon(url, session)
        if produto:
            produtos.append(produto)
    return produtos

# Função auxiliar para extrair nome, preço e imagem do produto na Amazon
def extrair_info_amazon(url, session):
    res = session.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    try:
        # Nome do produto
        titulo = soup.find(id='productTitle')
        if not titulo:
            titulo = soup.find('span', {'class': 'a-size-large product-title-word-break'})
        titulo = titulo.get_text(strip=True) if titulo else None

        # Imagem principal
        imagem = soup.find('img', {'id': 'landingImage'}) or soup.find('img', {'class': 's-image'})
        imagem = imagem['src'] if imagem else None

        # Preço (pode variar de seletor)
        preco = soup.select_one('#corePriceDisplay_desktop_feature_div .a-offscreen') \
             or soup.select_one('.a-price .a-offscreen')
        preco = preco.get_text(strip=True) if preco else None

        return {
            "nome": titulo,
            "preco": limpar_preco(preco) if preco else None,
            "imagem": imagem,
            "url": url
        }
    except:
        return None

# ---------------------- APP ----------------------
# Entrada do usuário
termo = st.text_input("🔍 Digite o nome do produto")

# Só busca se o usuário digitou algo
if termo:
    col_kabum, col_amazon = st.columns(2)

    # Busca nos dois sites
    with st.spinner("Buscando na KaBuM..."):
        lista_kabum = buscar_kabum(termo)
    with st.spinner("Buscando na Amazon..."):
        lista_amazon = buscar_amazon(termo)

    # Descobre quantos itens exibir
    max_itens = max(len(lista_kabum), len(lista_amazon))

    # Exibe lado a lado
    for i in range(max_itens):
        col1, col2 = st.columns(2)

        with col1:
            if i < len(lista_kabum):
                p = lista_kabum[i]
                st.markdown("### 🟠 KaBuM")
                if p['imagem']:
                    st.image(p['imagem'], width=200)
                st.markdown(f"[**{p['nome']}**]({p['url']})", unsafe_allow_html=True)
                st.markdown(f"💰 R$ {p['preco']:.2f}" if p['preco'] else "💰 Indisponível")

        with col2:
            if i < len(lista_amazon):
                p = lista_amazon[i]
                st.markdown("### 🔵 Amazon")
                if p['imagem']:
                    st.image(p['imagem'], width=200)
                st.markdown(f"[**{p['nome']}**]({p['url']})", unsafe_allow_html=True)
                st.markdown(f"💰 R$ {p['preco']:.2f}" if p['preco'] else "💰 Indisponível")

# ---------------------------------------------------------------
# Observação: este é um projeto feito para estudo.
# Algumas buscas podem falhar (principalmente na Amazon) 
# e o código ainda pode ser melhorado! 
# ---------------------------------------------------------------
