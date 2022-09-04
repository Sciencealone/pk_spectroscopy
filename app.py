import streamlit as st
from bokeh.plotting import figure
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
        ('Timestamp', pks.timestamp),
        ('Sample volume', pks.sample_volume),
        ('Alkaline concentration', pks.alkaline_concentration),
        ('Data points', len(pks.alkaline_volumes))
    ]:
        st.sidebar.write(f'{label}: {item}')

    # Display titration curve
    with st.expander('Titration curve'):

        # Check we have any data
        if len(pks.alkaline_volumes) > 0:
            title = 'Titration curve'
            if pks.sample_name:
                title = f'{title} ({pks.sample_name})'

            p = figure(
                title=title,
                x_axis_label='Titrant volume',
                y_axis_label='pH')
            p.line(pks.alkaline_volumes, pks.ph_values, line_width=2)
            st.bokeh_chart(p, use_container_width=True)
        else:
            st.write('Not enough data!')


else:
    st.write('⬅ Waiting for a data file in the sidebar.')
