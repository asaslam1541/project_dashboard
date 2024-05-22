#Import Libraries
import pandas as pd
from pathlib import Path

#Create DataFrame
url = 'https://raw.githubusercontent.com/asaslam1541/project_dashboard/main/artisan_data.csv'
artisan_df = pd.read_csv(url)

#Display DataFrame
artisan_df.head()

# Try to load the dataset
try:
    artisan_df = pd.read_csv(url)
except Exception as e:
    print(f"Error loading data: {e}")
    artisan_df = pd.DataFrame()  # Create an empty dataframe as a fallback

#Import Dashboard Libraries
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output


# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server


# Define the layout of the app
app.layout = html.Div([
    
    html.Div([
        dcc.Dropdown(
            id='city-dropdown',
            options=[{'label': city, 'value': city} for city in artisan_df['City'].unique()] + [{'label': 'All Cities', 'value': 'All Cities'}],
            value='All Cities',
            clearable=False,
            className='dropdown'
        ),
        dcc.Dropdown(
            id='handicraft-dropdown',
            options=[
                {'label': 'All Categories', 'value': 'All Categories'},
                {'label': 'Textiles', 'value': 'Textiles'},
                {'label': 'Carpets & Rugs', 'value': 'Carpets & Rugs'},
                {'label': 'Ceramics', 'value': 'Ceramics'},
                {'label': 'Jewelry', 'value': 'Jewelry'},
                {'label': 'Leatherwork', 'value': 'Leatherwork'}
            ],
            value='All Categories',
            clearable=False,
            className='dropdown'
        )
    ], className='dropdown-container'),
    html.Div([
        dcc.Graph(id='experience-income-scatter', className='graph'),
        dcc.Graph(id='category-bar-chart', className='graph'),
        dcc.Graph(id='market-bar-chart', className='graph'),
        dcc.Graph(id='marital-status-chart', className='graph')
    ], className='graph-container')
])

# Callback to update the scatter plot based on dropdown selection
@app.callback(
    Output('experience-income-scatter', 'figure'),
    [Input('city-dropdown', 'value'),
     Input('handicraft-dropdown', 'value')]
)
def update_scatter_plot(selected_city, selected_handicraft):
    filtered_df = artisan_df

    if selected_city != 'All Cities':
        filtered_df = filtered_df[filtered_df['City'] == selected_city]

    if selected_handicraft != 'All Categories':
        filtered_df = filtered_df[filtered_df['What type of handicraft your business is focused on?'] == selected_handicraft]

    # Count the number of "Yes" and "No" for work permits in the filtered data
    work_permit_counts = filtered_df['Do you have a work permit?'].value_counts().to_dict()

    # Ensure that the filtered data is updated correctly with the counts
    filtered_df['Work Permit Status'] = filtered_df['Do you have a work permit?'].map(
        lambda x: f'{x} ({work_permit_counts.get(x, 0)})'
    )

    # Create scatter plot with work permit status
    fig = px.scatter(filtered_df, x='Professional Experience', y='Annual Income Range', color='Work Permit Status', 
                     title=f'Experience vs Income in {selected_city} - {selected_handicraft}',
                     labels={'Work Permit Status': 'Work Permit Status'})

    # Add overall average line
    overall_avg_income = artisan_df['Annual Income Range'].mean()
    fig.add_shape(
        type="line",
        x0=filtered_df['Professional Experience'].min(),
        x1=filtered_df['Professional Experience'].max(),
        y0=overall_avg_income,
        y1=overall_avg_income,
        line=dict(color="Red", width=2, dash="dash"),
        name="Overall Average"
    )

    # Add city-specific average line if not 'All Cities'
    if selected_city != 'All Cities':
        city_avg_income = filtered_df['Annual Income Range'].mean()
        fig.add_shape(
            type="line",
            x0=filtered_df['Professional Experience'].min(),
            x1=filtered_df['Professional Experience'].max(),
            y0=city_avg_income,
            y1=city_avg_income,
            line=dict(color="Blue", width=2, dash="dot"),
            name=f"{selected_city} Average"
        )

    return fig

# Callback to update the category bar chart based on dropdown selection
@app.callback(
    Output('category-bar-chart', 'figure'),
    [Input('city-dropdown', 'value'),
     Input('handicraft-dropdown', 'value')]
)
def update_bar_chart(selected_city, selected_handicraft):
    filtered_df = artisan_df

    if selected_city != 'All Cities':
        filtered_df = filtered_df[filtered_df['City'] == selected_city]

    if selected_handicraft != 'All Categories':
        filtered_df = filtered_df[filtered_df['What type of handicraft your business is focused on?'] == selected_handicraft]

    # Group by handicraft category and count occurrences
    category_counts = filtered_df['What type of handicraft your business is focused on?'].value_counts().reset_index()
    category_counts.columns = ['Handicraft Category', 'Count']

    # Create bar chart for the number of values in each category by province
    bar_fig = px.bar(category_counts, x='Handicraft Category', y='Count', color='Handicraft Category',
                     title=f'Artisan Category by {selected_city}',
                     labels={'Count': ''})  # Remove 'Count' label from y-axis

    return bar_fig

# Callback to update the market bar chart based on dropdown selection
@app.callback(
    Output('market-bar-chart', 'figure'),
    [Input('city-dropdown', 'value'),
     Input('handicraft-dropdown', 'value')]
)
def update_market_bar_chart(selected_city, selected_handicraft):
    filtered_df = artisan_df

    if selected_city != 'All Cities':
        filtered_df = filtered_df[filtered_df['City'] == selected_city]

    if selected_handicraft != 'All Categories':
        filtered_df = filtered_df[filtered_df['What type of handicraft your business is focused on?'] == selected_handicraft]

    # Count occurrences of "Yes" for each market type
    market_counts = {
        'Local Market': filtered_df['Local Market'].value_counts().get('Yes', 0),
        'Foreign Market': filtered_df['Foreign Market'].value_counts().get('Yes', 0),
        'National': filtered_df['National'].value_counts().get('Yes', 0),
        'Village Level': filtered_df['Village Level'].value_counts().get('Yes', 0)
    }

    market_counts_df = pd.DataFrame(list(market_counts.items()), columns=['Market Type', 'Count'])

    # Create bar chart for the number of values in each market type
    market_bar_fig = px.bar(market_counts_df, x='Market Type', y='Count', color='Market Type',
                            title=f'Market Exposure for {selected_city}',
                            labels={'Count': ''})  # Remove 'Count' label from y-axis

    return market_bar_fig

# Callback to update the marital status chart based on dropdown selection
@app.callback(
    Output('marital-status-chart', 'figure'),
    [Input('city-dropdown', 'value'),
     Input('handicraft-dropdown', 'value')]
)
def update_marital_status_chart(selected_city, selected_handicraft):
    filtered_df = artisan_df

    if selected_city != 'All Cities':
        filtered_df = filtered_df[filtered_df['City'] == selected_city]

    if selected_handicraft != 'All Categories':
        filtered_df = filtered_df[filtered_df['What type of handicraft your business is focused on?'] == selected_handicraft]

    # Count occurrences of each marital status
    marital_status_counts = filtered_df['Martial State'].value_counts().reset_index()
    marital_status_counts.columns = ['Marital Status', 'Count']

    # Create bar chart for marital status distribution
    marital_status_fig = px.bar(marital_status_counts, x='Marital Status', y='Count', color='Marital Status',
                                title=f'Marital Status - {selected_city} - {selected_handicraft}',
                                labels={'Count': ''})  # Remove 'Count' label from y-axis

    return marital_status_fig

# Run the app on a different port
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
