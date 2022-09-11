import os
import pandas as pd
import streamlit as st
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Segment, Range1d
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

    # Display titration curve expander
    with st.expander('Source data'):

        # Check we have any data
        if len(pks.alkaline_volumes) > 0:
            title = 'Titration curve'
            if pks.sample_name:
                title = f'{title} ({pks.sample_name})'

            p = figure(
                title=title,
                x_axis_label='Titrant volume',
                y_axis_label='pH')
            p.line(pks.alkaline_volumes, pks.ph_values, line_width=2, legend_label='All data')
            valid_x = pks.alkaline_volumes[:pks.valid_points]
            valid_y = pks.ph_values[:pks.valid_points]
            p.scatter(valid_x, valid_y, color='red', legend_label='Valid points')
            p.legend.location = 'top_left'
            st.bokeh_chart(p, use_container_width=True)
        else:
            st.write('Not enough data!')

    # Gather main control variables expander
    with st.expander('Parameters', expanded=True):
        pk_start = st.number_input('Start pK (0 recommended):', value=0., min_value=0., max_value=10.)
        pk_end = st.number_input('End pK (10 recommended):', value=10., min_value=0., max_value=10.)
        d_pk = st.number_input('pK step (0.05-0.1 recommended):', value=.05, min_value=0., max_value=1.)
        integration_constant = st.checkbox('Use integration constant (recommended).', value=True)

    # Check values
    if pk_start > pk_end:
        pk_start, pk_end = pk_end, pk_start
    if d_pk > pk_end - pk_start:
        d_pk = 0.05

    # Get and display results
    peaks, error = pks.make_calculation(pk_start, pk_end, d_pk, integration_constant)
    result_df = pd.DataFrame(peaks)
    result_df = result_df[['concentration', 'mean', 'interval']].copy()
    if not result_df.empty:
        with st.expander('Results', expanded=True):
            st.write('Peaks:')
            st.write(result_df)

            # Provide download data
            prefix, ext = os.path.splitext(uploaded_file.name)
            csv = result_df.to_csv().encode('utf-8')
            st.download_button(
                'Download table (CSV)',
                csv,
                prefix + '.csv',
                'text/csv',
                key='download-csv'
            )
            st.write(f'Error: {error:.5}')

            # Plot chart
            p = figure(
                title=f'pK plot ({pks.sample_name})',
                x_axis_label='pK',
                y_axis_label='Concentration')
            p.x_range = Range1d(pk_start, pk_end)
            source = ColumnDataSource(result_df)
            glyph = Segment(x0='mean', y0=0, x1='mean', y1='concentration', line_width=3)
            p.add_glyph(source, glyph)
            st.bokeh_chart(p, use_container_width=True)

else:
    st.write('⬅ Waiting for a data file in the sidebar.')
