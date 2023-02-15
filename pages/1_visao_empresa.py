from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static


st.set_page_config( page_title='Visão Empresa', page_icon="", layout='wide')

#-----------------------------------
# Funções
# --------------------------------
def country_maps(df1):
   
    #import folium

    df_aux = df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']].groupby(['City', 'Road_traffic_density']).median().reset_index()

    df_aux = df_aux.loc[df_aux['City'] != 'NaN', :]
    df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]
    
    import folium

#df_aux = df_aux.head()
    map = folium.Map()

    #map


    for index, location_info in df_aux.iterrows():
        folium.Marker( [ location_info['Delivery_location_latitude' ], location_info['Delivery_location_longitude']] ).add_to( map )

    folium_static(map, width=1024, height=600)
       
   
    return None

def order_share_by_week(df1):
       
    df_aux01 = df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    df_aux02 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby('week_of_year').nunique().reset_index()
    df_aux = pd.merge( df_aux01, df_aux02, how='inner', on='week_of_year')
    df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    fig = px.line(df_aux, x='week_of_year', y='order_by_deliver')

    return fig

 
def order_by_week(df1):

    #df1['week_of_year'] = df1['Order_Date'].dt.strftime( '%U' )

    df_aux = df1.loc[:, ['ID' , 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()

    fig = px.line(df_aux, x = 'week_of_year', y = 'ID' )

    st.plotly_chart( fig, use_container_width=True )
    
#--  algo neste código está duplicando o gráfico de order_by_week

    return fig


def traffic_order_city(df1):
        df_aux = df1.loc[:, ['ID', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index()
        df_aux = df_aux.loc[df_aux['City'] != 'NaN', :]
        df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]

        fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City' )

        return fig

def traffic_order_share(df1):
               
        #st.markdown('# Coluna 01')
        df_aux = df1.loc[: , ['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()

        df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]

        df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum()

        fig = px.pie(df_aux, values='entregas_perc', names ='Road_traffic_density' )


        return fig

def order_metric(df1):
   
        df_aux = df1.loc[:, ['ID' , 'Order_Date']].groupby( 'Order_Date' ).count().reset_index()

        fig = px.bar(df_aux, x = 'Order_Date', y = 'ID' )
       
       
        return fig
    
def clean_code(df1):

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


    df1['week_of_year'] = df1['Order_Date'].dt.strftime( '%U' )

    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split( '(min)' )[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    return df1

#inicio da estrutura logica do cod -----
#--------------
#----- importando ----
#--------------

df = pd.read_csv('dataset/train.csv')

# ------------------------
#--- Limpando os dados  -----
#-------------------------

df1 = clean_code(df)


#--------------------------------------------------------------------------------------------


df_aux = df1.loc[:, ['ID' , 'Order_Date']].groupby( 'Order_Date' ).count().reset_index()

px.bar(df_aux, x = 'Order_Date', y = 'ID' )

#----------------------
#Barra Lateral
#--------------------------
st.header( 'Marketplace - Visão Empresa' )
#image_path = 'logo1.png'
image = Image.open('logo1.png')
st.sidebar.image( image, width=120 )


st.sidebar.markdown( '## Fastest Delivery in Town' )
st.sidebar.markdown( """___""" )

st.sidebar.markdown( '## Selecione uma data limite')
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

st.dataframe( df1 )
#-------------------------


#print('estou aqui')
#print( df1.head() )

#-----------------------------------
#streamlit layout
#---------------


tab1, tab2, tab3 = st.tabs (['Visão Gerencial', 'Visão Tática', 'Visão Geográfica' ])


with tab1:
    with st.container():
       
        fig = order_metric(df1)
        st.markdown('# Pedidos por dia')
        st.plotly_chart( fig, use_container_width=True )

       
       
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            fig = traffic_order_share(df1)
            st.header('Tempo de entrega por tipo de tráfego')
            st.plotly_chart( fig, use_container_width=True )
           
        with col2:
            st.header('Volume de tráfego por tipo de cidade')
            fig = traffic_order_city(df1)
            st.plotly_chart(fig, use_container_width=True)
           
                 
with tab2:
    with st.container():      
        st.markdown("# Pedidos por semana")
        fig = order_by_week(df1)
        st.plotly_chart( fig, use_container_width=True )


    with st.container():
        st.markdown("# Pedidos por semana do ano")
        fig = order_share_by_week(df1)
        st.plotly_chart( fig, use_container_width=True )


with tab3:
    st.title('Região das primeiras entregas deste dia')
    country_maps(df1)
