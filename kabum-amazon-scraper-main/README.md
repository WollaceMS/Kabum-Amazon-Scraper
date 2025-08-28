# 🛒 Comparador de Preços KaBuM x Amazon

Projeto desenvolvido por  
- [**Jonatha Pravatta**](https://www.linkedin.com/in/jonathapravatta/)  
- [**Wollace Macedo**](https://www.linkedin.com/in/wollacemacedo/)  

---

Aplicação em **Python + Streamlit** para praticar **Web Scraping** e consumo de **API**.  
Você digita o nome de um produto e o app mostra, lado a lado, resultados da KaBuM e da Amazon com preço, imagem e link.

> ⚠️ Este é um **MVP acadêmico**, feito em pouco tempo, então ainda pode conter bugs, principalmente no scraping da Amazon.
> (Os dados da Amazon são obtidos por meio de scraping e podem não estar sempre disponíveis devido a políticas da empresa.)

---

<img width="1365" height="564" alt="screenshot" src="https://github.com/user-attachments/assets/a327e2de-de86-4f81-8ceb-ff3f3adb8045" />


## ✨ Funcionalidades
- Busca na **KaBuM** via API pública.
- Busca na **Amazon** via scraping com BeautifulSoup.
- Exibição lado a lado com nome, preço, imagem e link direto.
- Interface simples em **Streamlit**.

---

## 🧩 Tecnologias utilizadas
- Python 3
- Streamlit
- Requests
- BeautifulSoup4
- Unidecode

---

## 🚀 Como rodar localmente

```bash
# Clone este repositório
git clone https://github.com/seu-usuario/comparador-kabum-amazon.git
cd comparador-kabum-amazon

# (Opcional) Crie e ative um ambiente virtual
python -m venv .venv
# Linux/Mac
source .venv/bin/activate
# Windows
.venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Rode o app
streamlit run app.py
