import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title='Insight Haven: Data Analysis Platform',
    page_icon='📲'
)

st.markdown('## :blue[InsightStream Analytics]')
st.markdown('### :grey[Analyse the data easily]')
st.markdown('---')

file = st.file_uploader('Drop any csv or excel file', type=['csv', 'xlsx'])
data = None

if file is not None:
    if file.name.endswith('csv'):
        data = pd.read_csv(file)
    else:
        data = pd.read_excel(file)

    st.dataframe(data)
    st.info('File has been uploaded successfully', icon='📁')

if data is not None:
    st.markdown('## :blue[Basic Information of the Dataset]')
    st.markdown('---')

    tab1, tab2, tab3, tab4 = st.tabs([':blue[Summary]', ':blue[Top and Bottom Rows]', ':blue[Data Types]', ':blue[Columns]'])

    with tab1:
        st.write(f'There are {data.shape[0]} rows and {data.shape[1]} columns in the uploaded dataset.')
        st.dataframe(data.describe())

    with tab2:
        st.markdown('### :grey[Top Rows]')
        toprows = st.slider('Number of rows you want', 1, data.shape[0], key='top_slider')
        st.dataframe(data.head(toprows))
        st.markdown('### :grey[Bottom Rows]')
        bottomrows = st.slider('Number of rows you want', 1, data.shape[0], key='bottom_slider')
        st.dataframe(data.tail(bottomrows))

    with tab3:
        st.markdown('### :grey[Data Types of Columns]')
        st.dataframe(data.dtypes)

    with tab4:
        st.markdown('### :grey[Column Names in Dataset]')
        st.dataframe(data.columns)

    st.markdown('## :blue[Column Value to Count]')
    st.markdown('---')

    with st.expander('Value Count'):
        col1, col2 = st.columns(2)
        with col1:
            column = st.selectbox('Choose Column Name', options=list(data.columns))
        with col2:
            toprows = st.number_input('Top Rows', min_value=1, step=1)
        count = st.button('Count the Filtered Data')
        if count:
            result = data[column].value_counts().reset_index()
            result.columns = [column, 'count']
            st.dataframe(result)
            st.markdown('### :grey[Visualisation]')
            st.markdown('---')

            # Bar plot
            figure = px.bar(result, x=column, y='count', text='count')
            st.plotly_chart(figure)

            # Line plot
            figure = px.line(result, x=column, y='count', text='count')
            st.plotly_chart(figure)

            # Pie chart
            figure = px.pie(result, names=column, values='count')
            st.plotly_chart(figure)

    st.markdown('## :blue[Group by: Simplifies the Analysis of Data]')
    st.markdown('---')
    st.write('GROUP BY is essential for extracting valuable insights from large datasets by summarizing and analyzing data efficiently.')

    with st.expander('Group by Your Columns'):
        col1, col2, col3 = st.columns(3)
        with col1:
            groupby_cols = st.multiselect('Choose Columns to Group By', options=list(data.columns))
        with col2:
            operation_column = st.selectbox("Choose Column for Operations", options=list(data.columns))
        with col3:
            operations = st.selectbox('Choose Operations to Apply', options=['sum', 'max', 'min', 'mean', 'median', 'count'])

        if groupby_cols:
            if data[operation_column].dtype in ['int64', 'float64']:
                agg_operations = {
                    'sum': 'sum',
                    'max': 'max',
                    'min': 'min',
                    'mean': 'mean',
                    'median': 'median',
                    'count': 'count'
                }
                result = data.groupby(groupby_cols).agg(
                    newcol=(operation_column, agg_operations.get(operations, 'count'))
                ).reset_index()
                st.dataframe(result)
            else:
                result = data.groupby(groupby_cols).size().reset_index(name='count')
                st.dataframe(result)

            st.markdown('### :grey[Detailed Graphical Visualisation]')
            st.markdown('---')
            graph = st.selectbox('Choose Your Graph', options=['line', 'bar', 'scatter', 'pie', 'sunburst'])

            if graph == 'line':
                x_axis = st.selectbox('Choose X Axis', options=list(result.columns))
                y_axis = st.selectbox('Choose Y Axis', options=list(result.columns))
                color = st.selectbox('Colour Information', options=[None] + list(result.columns))
                fig = px.line(result, x=x_axis, y=y_axis, color=color, markers='o')
                st.plotly_chart(fig)

            elif graph == 'bar':
                x_axis = st.selectbox('Choose X Axis', options=list(result.columns))
                y_axis = st.selectbox('Choose Y Axis', options=list(result.columns))
                color = st.selectbox('Colour Information', options=[None] + list(result.columns))
                facet_col = st.selectbox('Column Information', options=[None] + list(result.columns))
                fig = px.bar(result, x=x_axis, y=y_axis, color=color, facet_col=facet_col, barmode='group')
                st.plotly_chart(fig)

            elif graph == 'scatter':
                x_axis = st.selectbox('Choose X Axis', options=list(result.columns))
                y_axis = st.selectbox('Choose Y Axis', options=list(result.columns))
                color = st.selectbox('Colour Information', options=[None] + list(result.columns))
                size = st.selectbox('Size Column', options=[None] + list(result.columns))
                fig = px.scatter(result, x=x_axis, y=y_axis, color=color, size=size)
                st.plotly_chart(fig)

            elif graph == 'pie':
                # Ensure `values` column is numeric
                numeric_columns = [col for col in result.columns if pd.api.types.is_numeric_dtype(result[col])]
                categorical_columns = [col for col in result.columns if pd.api.types.is_string_dtype(result[col])]

                if numeric_columns and categorical_columns:
                    values_column = st.selectbox('Choose Values Column', options=numeric_columns)
                    names_column = st.selectbox('Choose Labels Column', options=categorical_columns)

                    if values_column and names_column:
                        fig = px.pie(result, values=values_column, names=names_column)
                        st.plotly_chart(fig)
                    else:
                        st.error('Please select valid columns for values and labels.')
                else:
                    st.error('Ensure there are numeric columns for values and categorical columns for labels.')


            elif graph == 'sunburst':
                path = st.multiselect('Choose Your Path', options=list(result.columns))

                # Ensure the columns used for `values` are numeric
                numeric_columns = [col for col in result.columns if pd.api.types.is_numeric_dtype(result[col])]

                if numeric_columns:
                    values_column = st.selectbox('Choose Values Column', options=numeric_columns)

                    # Ensure the chosen column for `values` is numeric
                    if values_column:
                        fig = px.sunburst(result, path=path, values=values_column)
                        st.plotly_chart(fig)
                    else:
                        st.error('Please select a valid numeric column for values.')
                else:
                    st.error(
                        'No numeric columns available for values. Please ensure that there are numeric columns in the dataset.')

