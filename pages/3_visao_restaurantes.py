from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static


st.set_page_config( page_title='Visão Restaurante', page_icon="", layout='wide')

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

#----------------------
#Barra Lateral
#--------------------------
st.header( 'Marketplace - Visão Restaurantes' )
#image_path = 'logo1.png'
image = Image.open('logo1.png')
st.sidebar.image( image, width=120 )


st.sidebar.title( ' Fastest Delivery in Town' )
#st.sidebar.markdown( ' Fastest Delivery in Town' )

st.sidebar.markdown( """___""" )

st.sidebar.markdown( ' Selecione uma data limite')
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

#------------------ Layout streamlit ------

tab1, tab2, tab3 = st.tabs (['Visão Gerencial', '_', '_' ])


with tab1:
    with st.container():
        st.title("Métricas Gerais")

        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            delivery_unique = len(df1.loc[:,'Delivery_person_ID'].unique())
            col1.metric('Entregadores Únicos',  delivery_unique)
                       
        with col2:

            cols = ['Delivery_location_latitude', 'Delivery_location_longitude',  'Restaurant_latitude',  'Restaurant_longitude']

            df1['distance'] = (df1.loc[:, cols].apply(lambda x:
                       haversine((x['Restaurant_latitude'], x['Restaurant_longitude']),( x['Delivery_location_latitude'], x['Delivery_location_longitude']  )), axis=1))

            avg_distance = np.round(df1['distance'].mean(), 2)
            col2.metric( 'A distancia média das entregas é', avg_distance )

        with col3:
                   
            cols = ['Time_taken(min)', 'Festival']
            df_aux = df1.loc[:, cols].groupby( 'Festival' ).agg( {'Time_taken(min)': ['mean', 'std']} )
   
            df_aux.columns = ['avg_time','std_time']
            df_aux = df_aux.reset_index()
            df_aux = np.round( df_aux.loc[df_aux['Festival'] == 'Yes', 'avg_time'], 2 )
            col3.metric( 'Tempo Médio de Entrega c/ Festival', df_aux)
           # df_aux
        with col4:
            cols = ['Time_taken(min)', 'Festival']
            df_aux = df1.loc[:, cols].groupby( 'Festival' ).agg( {'Time_taken(min)': ['mean', 'std']} )
   
            df_aux.columns = ['avg_time','std_time']
            df_aux = df_aux.reset_index()
            df_aux = np.round( df_aux.loc[df_aux['Festival'] == 'Yes', 'std_time'], 2 )
            col4.metric( 'Desvio padrão Médio de Entrega c/ Festival', df_aux)
            
        with col5:
                   
            cols = ['Time_taken(min)', 'Festival']
            df_aux = df1.loc[:, cols].groupby( 'Festival' ).agg( {'Time_taken(min)': ['mean', 'std']} )
   
            df_aux.columns = ['avg_time','std_time']
            df_aux = df_aux.reset_index()
            df_aux = np.round( df_aux.loc[df_aux['Festival'] == 'No', 'avg_time'], 2 )
            col5.metric( 'Tempo Médio de Entrega c/ Festival', df_aux)

           # df_aux
            
        with col6:
            
            cols = ['Time_taken(min)', 'Festival']
            df_aux = df1.loc[:, cols].groupby( 'Festival' ).agg( {'Time_taken(min)': ['mean', 'std']} )
   
            df_aux.columns = ['avg_time','std_time']
            df_aux = df_aux.reset_index()
            df_aux = np.round( df_aux.loc[df_aux['Festival'] == 'No', 'std_time'], 2 )
            col6.metric( 'Desvio padrão Médio de Entrega c/ Festival', df_aux)
            

    with st.container():
      #------------------ gráfico pizza 3 cores
        st.markdown("""___""")
        st.title('Tempo Medio de entrega por cidade')
        cols = ['City', 'Time_taken(min)']
        df_aux = df1.loc[:, cols].groupby( 'City').agg( {'Time_taken(min)': ['mean', 'std']} )
            
        df_aux.columns = ['avg_time','std_time']
            
        df_aux = df_aux.reset_index()
            
        fig = go.Figure()
        fig.add_trace( go.Bar( name='Control', x=df_aux['City'], y=df_aux['avg_time'], error_y=dict( type='data', array=df_aux['std_time'] )))
            
        fig.update_layout(barmode='group')
        st.plotly_chart( fig )
            #fig.show()
        
       
    with st.container():
        st.markdown("""___""")
        st.title("Distribuição do tempo de entrega por região")
       
 #       col1,col2 = st.columns( 2)
        # gráfico 3 palito
        #with col1:
            
        cols=['Delivery_location_latitude','Delivery_location_longitude','Restaurant_latitude', 'Restaurant_longitude']
        df1['distance'] = df1.loc[:, cols].apply(lambda x: haversine( (x['Restaurant_latitude'], x['Restaurant_longitude']),(x['Delivery_location_latitude'], x['Delivery_location_longitude'])),axis=1)

        avg_distance = df1.loc[:, ['City', 'distance']].groupby('City').mean().reset_index()
        fig = go.Figure(data=[go.Pie( labels=avg_distance['City'], values=avg_distance['distance'], pull=[0,0,0])])
        st.plotly_chart( fig )

            
    with st.container():
        st.markdown("""___""")
        st.title("Desvio padrão de tempo de entrega por tipo de região e tráfego")


        cols = ['City', 'Time_taken(min)', 'Road_traffic_density']
        df_aux = df1.loc[:, cols].groupby( ['City', 'Road_traffic_density']).agg({'Time_taken(min)' : ['mean','std']} )

        df_aux.columns = ['avg_time', 'std_time']

        df_aux = df_aux.reset_index()

        fig = px.sunburst(df_aux, path=['City','Road_traffic_density'], values='avg_time',
                  color='std_time', color_continuous_scale='BuPu',
                  color_continuous_midpoint=np.average(df_aux['std_time'] ) )  
        st.plotly_chart(fig)
                  
                  
                  
#fig.show()
        #with col3:df
            #st.markdown('##### col3')
     
           
    with st.container():
        st.markdown("""___""")
        st.title("Média e Desvio Padrão de tempo de entrega por tipo de cidade e qualidade do trânsito ")
        
        cols = ['City', 'Time_taken(min)', 'Road_traffic_density']
        df_aux = df1.loc[:, cols].groupby( ['City','Road_traffic_density']).agg({'Time_taken(min)':['mean', 'std']})

        df_aux.columns = ['avg_time', 'std_time']

        df_aux = df_aux.reset_index()
        
        st.dataframe(df_aux)
       
# ------------