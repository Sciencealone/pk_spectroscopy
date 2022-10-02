import os
import pandas as pd
import streamlit as st
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Segment, Range1d
from pk_spectrum import pKSpectrum, TitrationModes


# Change app page parameters
st.set_page_config(page_title='pK Spectrum')


st.title('pK spectroscopy app')
st.markdown('[Get more detail in Github repository ➡](https://github.com/Sciencealone/pkspec-streamlit)')

# Select titration mode
titration_mode_label = st.sidebar.radio('Select titration mode', ('Volumetric', 'Coulometric'))
if titration_mode_label == 'Volumetric':
    titration_mode = TitrationModes.VOLUMETRIC
else:
    titration_mode = TitrationModes.COULOMETRIC

# Load source data
uploaded_file = st.sidebar.file_uploader('Load sample data in XLSX format', type='xlsx')
if uploaded_file is not None:

    pks = pKSpectrum(uploaded_file, titration_mode)

    st.sidebar.markdown("""---""")

    st.sidebar.subheader('Sample information')
    if titration_mode == TitrationModes.VOLUMETRIC:
        parameters = [
            ('Sample name', pks.sample_name),
            ('Comment', pks.comment),
            ('Timestamp', pks.timestamp),
            ('Sample volume', pks.sample_volume),
            ('Alkaline concentration', pks.alkaline_concentration),
            ('Data points', len(pks.alkaline_volumes))
        ]
    else:
        parameters = [
            ('Sample name', pks.sample_name),
            ('Comment', pks.comment),
            ('Timestamp', pks.timestamp),
            ('Sample volume', pks.sample_volume),
            ('Current', pks.current),
            ('Data points', len(pks.alkaline_volumes))
        ]
    for label, item in parameters:
        st.sidebar.write(f'{label}: {item}')

    # Display titration curve expander
    with st.expander('Source data'):

        # Check we have any data
        if len(pks.alkaline_volumes) or len(pks.times) > 0:
            title = 'Titration curve'
            if pks.sample_name:
                title = f'{title} ({pks.sample_name})'

            if titration_mode == TitrationModes.VOLUMETRIC:
                x_axis_label = 'Titrant volume, ml'
                x_values = pks.alkaline_volumes
            else:
                x_axis_label = 'Titration time, s'
                x_values = pks.times

            p = figure(
                title=title,
                x_axis_label=x_axis_label,
                y_axis_label='pH')
            p.line(x_values, pks.ph_values, line_width=2, legend_label='All data')
            valid_x = x_values[:pks.valid_points]
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

    # Get results
    peaks, error = pks.make_calculation(pk_start, pk_end, d_pk, integration_constant)

    # Check results for validity
    if peaks is None:
        st.error('Error in calculations! Please check the titration mode, source data, and parameters.')
    else:

        # Display the results
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
    st.write('You may use some [samples](https://github.com/Sciencealone/pkspec_streamlit/tree/main/data) '
             'from the repository.')

    # Provide template for the data
    st.write('Please apply this template to enter the sample data:')
    with open('data/sample.xltx', 'rb') as file:
        btn = st.download_button(
            label='Excel 2007+ template',
            data=file,
            file_name='sample.xltx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.template'
        )
