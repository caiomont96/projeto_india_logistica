import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon= "",
    layout='wide'
)

#image_path = r'C:\Users\User\repos\ftc_programacao_python\logo1.png'

image = Image.open('logo1.png')

st.sidebar.image( image, width=120)


st.sidebar.markdown( '# ___')

st.sidebar.markdown('## ___')

st.sidebar.markdown("""___""")

st.write("# Dashboard Marketplace de entregas")

st.markdown(
    """
    Este Growth Dashboard foi construído para acompanhar as métricas de um aplicativo de entrega de comida na índia
    
    ## Visualização
    - Para uma melhor experiência visualização é recomendado clicar no menu do canto superior direito  >  settings  >  theme: alterar para dark
    
    ## Como utilizar esse Growth Dashboard?
    - Visão Empresa:
        - Visão Gerencial
        - Visão Tática
        - Visão Geográfica
    - Visão Entregadores:
        - Ranking de avaliações e tempo de entrega
    - Visão Restaurante:
        - Indicadores semanais de crescimento dos restaurantes
        
      
    """)