import gspread
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
from PIL import Image
import datetime

#declaring variables
sa = gspread.service_account()
sheet = sa.open('Expenses report')
worksheet = sheet.worksheet('Money Enero2')
cuentas = ['Obligaciones', 'Libertad financiera', 'imprevistos', 'Responsabilidad social', 'Educación', 'Juego']
today = datetime.datetime.today()

#Dataframe
df = pd.DataFrame(worksheet.get_all_records())
categoria = set(df['Categoria'].tolist())

print(df)
df.dropna()

#first page settings
st.set_page_config(page_title= 'Registro de finanzas personales', page_icon=':dollar:', layout='wide')
#st.header('Finanzas personales')

#Header value
total = '${:,.2f}'.format(df['Precio'].sum())

#Header
left_col, right_col = st.columns(2)

with right_col:
    #insert record
    with st.expander('Agregar registro'):
            with st.form(key='form1'):
                fisrt = st.date_input('Fecha')
                second = st.selectbox('Categoría', categoria)
                third = st.number_input('Precio', min_value=0)
                fourth = st.text_input('Descripción (Opcional)')
                submit_button = st.form_submit_button(label = 'Enviar')
            
            if submit_button:
                st.success('El registro ha sido enviado exitosamente')
                df2 = pd.DataFrame({'Fecha': str(fisrt),
                                    'Categoria': second,
                                    'Precio' : third,
                                    'Descripcion' : fourth}, index=[0])
                sheet.values_append('Money Enero2', {'valueInputOption': 'RAW'}, {'values':df2.values.tolist()})
                df = pd.DataFrame(worksheet.get_all_records())

with left_col:
    st.subheader('Total gastos mensual:')
    st.subheader(total)

st.markdown('---')

left_col, right_col = st.columns(2)

with left_col:
    #pie chart
    print(df.groupby('Categoria')['Precio'].sum())
    pie_chart = px.pie(df, title='Resumen mensual', values='Precio', names='Categoria')
    st.plotly_chart(pie_chart)

with right_col:
    #category filter
    category_selection = st.multiselect('   Categoria', categoria, default= categoria)
    mask = df['Categoria'].isin(category_selection)
    df_grouped = df[mask].groupby(by='Categoria').sum()[['Precio']]
    bar_chart = px.bar(df_grouped, title='Resumen mensual')
    st.plotly_chart(bar_chart)
    
    #worksheet.update_cell(,,)


# Connecting with `gspread` here

#ws = gc.open("SheetName").worksheet("xyz")
#existing = gd.get_as_dataframe(ws)
#updated = existing.append(your_new_data)
#gd.set_with_dataframe(ws, updated)