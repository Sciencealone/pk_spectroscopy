import streamlit as st
from pk_spectrum import pKSpectrum

st.title('pK spectroscopy app')

# Provide template for the data
st.sidebar.write('Please use this template to enter sample data')
with open('data/sample.xltx', 'rb') as file:
    btn = st.sidebar.download_button(
        label='Excel 2007+ template',
        data=file,
        file_name='sample.xltx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.template'
    )

st.sidebar.markdown("""---""")

# Load source data
uploaded_file = st.sidebar.file_uploader('Load sample data in XLSX format', type='xlsx')
if uploaded_file is None:
    exit()

pks = pKSpectrum(uploaded_file)

st.sidebar.markdown("""---""")

st.sidebar.subheader('Sample information')
st.sidebar.write(f'Sample name: {pks.sample_name}')
st.sidebar.write(f'Comment: {pks.comment}')
st.sidebar.write(f'Date: {pks.date}')
st.sidebar.write(f'Time: {pks.time}')
st.sidebar.write(f'Sample volume: {pks.sample_volume}')
st.sidebar.write(f'Alkaline concentration: {pks.alkaline_concentration}')
