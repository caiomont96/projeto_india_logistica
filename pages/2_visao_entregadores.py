from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config( page_title='Visão Entregador', page_icon="", layout='wide')
df = pd.read_csv('dataset/train.csv')

#print( df.head() )


df1 = df.copy()

linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy()


linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = (df1['Weatherconditions'] != 'conditions NaN')
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = (df1['City'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = (df1['Festival'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy()



df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( int )
#df1.shape

df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float )


df1['Order_Date'] = pd.to_datetime( df1['Order_Date'], format='%d-%m-%Y' )


linhas_selecionadas = (df1['multiple_deliveries'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy()
df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )


df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()


df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split( '(min)' )[1])
df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)


df_aux = df1.loc[:, ['ID' , 'Order_Date']].groupby( 'Order_Date' ).count().reset_index()

px.bar(df_aux, x = 'Order_Date', y = 'ID' )

#----------------------
#Barra Lateral
#--------------------------
st.header( 'Marketplace - Visão Entregadores' )
#image_path = 'logo1.png'
image = Image.open('logo1.png')
st.sidebar.image( image, width=120 )


st.sidebar.title( 'Fastest Delivery in Town' )
st.sidebar.markdown( """___""" )

st.sidebar.title( 'Selecione uma data limite')
date_slider = st.sidebar.slider(
    'Até qual valor?',
    value=pd.datetime( 2022, 4, 13 ),
    min_value=pd.datetime( 2022, 2, 11),
    max_value=pd.datetime( 2022, 4, 6),
    format='DD-MM-YYYY' )

#st.header( date_slider )
st.sidebar.markdown( """___""" )

traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low','Medium','High','Jam'],
    default= ['Low','Medium','High','Jam'] )
   
st.sidebar.markdown("""___""")
st.sidebar.markdown("""___""")

#Filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]
#st.dataframe(df1.head())

#filtro de trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

#st.dataframe( df1 )
#-------------------------


#print('estou aqui kakak')
#print( df1.head() )

#-----------------------------------
#LAYOUT STREAMLIT
#---------------

tab1, tab2, tab3 = st.tabs (['Geral', '_', '_' ])

with tab1:
    with st.container():
        st.title('Métricas Gerais')
       
        col1, col2, col3, col4 = st.columns(4, gap='large')
        with col1:
           
            maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
            col1.metric('Maior de idade', maior_idade)
           
        with col2:
            menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
            col2.metric('Menor de idade', menor_idade)
           
        with col3:
            melhor_condicao = df1.loc[:, 'Vehicle_condition'].max()
            col3.metric('Melhor condição', melhor_condicao)

        with col4:
            pior_condicao = df1.loc[:, 'Vehicle_condition'].min()
            col4.metric('Pior condição', pior_condicao)
            
with st.container():
    st.markdown("""___""")
    st.title( 'Avaliacoes' )

col1, col2 = st.columns( 2 )
with col1:
    st.subheader( 'Avaliacao medias por Entregador' )
    df_avg_ratings_per_deliver = df1.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']].groupby('Delivery_person_ID').mean().reset_index()
    st.dataframe(df_avg_ratings_per_deliver)
   
   
with col2:
    st.subheader( 'Avaliacao media por transito ')
 
    df_avg_std_rating_by_traffic = ( df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']]
                                    .groupby('Road_traffic_density')
                                    .agg( {'Delivery_person_Ratings': ['mean', 'std'] }) )
                                   
   
    df_avg_std_rating_by_traffic.columns = ['delivery_mean','delivery_std']
    df_avg_std_rating_by_traffic = df_avg_std_rating_by_traffic.reset_index()
   
    st.dataframe(df_avg_std_rating_by_traffic)

   
    st.subheader( 'Avaliacao media por clima' )
       
    df_avg_std_rating_by_weather = ( df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']]
                                    .groupby('Weatherconditions')
                                    .agg( {'Delivery_person_Ratings': ['mean', 'std'] }) )
                                   
   
    df_avg_std_rating_by_weather.columns = ['delivery_mean','delivery_std']
    df_avg_std_rating_by_weather = df_avg_std_rating_by_weather.reset_index()
   
    st.dataframe(df_avg_std_rating_by_weather)
 

with st.container():
    st.markdown("""___""")
    st.title( 'Velocidade de Entrega')

col1, col2 = st.columns( 2 )
   
#----------------------
   
with col1:
    st.subheader('Top Entregadores mais rápidos')
    df2 = (df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
           .groupby( ['City', 'Delivery_person_ID'] )
           .mean()
           .sort_values(['City', 'Time_taken(min)'], ascending=True)
           .reset_index())
           
    df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
    df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)

    df3 = pd.concat( [df_aux01, df_aux02, df_aux03] ).reset_index( drop=True )
    st.dataframe(df3)

with col2:
    st.subheader('Top Entregadores mais lentos')
    df2 = (df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
           .groupby( ['City', 'Delivery_person_ID'] )
           .mean()
           .sort_values(['City', 'Time_taken(min)'], ascending=False)
           .reset_index())
           
    df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
    df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)

    df3 = pd.concat( [df_aux01, df_aux02, df_aux03] ).reset_index( drop=True )
    st.dataframe(df3)