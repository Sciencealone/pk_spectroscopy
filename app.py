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
if uploaded_file is not None:

    pks = pKSpectrum(uploaded_file)

    st.sidebar.markdown("""---""")

    st.sidebar.subheader('Sample information')
    for label, item in [
        ('Sample name', pks.sample_name),
        ('Comment', pks.comment),
        ('Date', pks.date),
        ('Time', pks.time),
        ('Sample volume', pks.sample_volume),
        ('Alkaline concentration', pks.alkaline_concentration)
    ]:
        st.sidebar.write(f'{label}: {item}')
