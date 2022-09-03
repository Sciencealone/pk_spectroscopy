import streamlit as st

st.title('pK spectroscopy app')

# Provide template for the data
with open('data/sample.xltx', 'rb') as file:
    btn = st.download_button(
        label='Download Excel 2007+ template',
        data=file,
        file_name='sample.xltx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.template'
    )
