#Import Libraries
import pandas as pd
from pathlib import Path

#Create DataFrame
url = 'https://raw.githubusercontent.com/asaslam1541/project_dashboard/main/artisan_data.csv'
artisan_df = pd.read_csv(url)

#Display DataFrame
artisan_df.head()

#Modify & Adjust Data
# Strip any whitespace and convert to string
artisan_df['Annual Income Range'] = artisan_df['Annual Income Range'].astype(str).str.strip()

# Replace the incorrect value 500000 with 100000
artisan_df['Annual Income Range'] = artisan_df['Annual Income Range'].replace('500000', '100000')

# Remove commas and convert to numeric
artisan_df['Annual Income Range'] = artisan_df['Annual Income Range'].str.replace(',', '').astype(float)

# Replace the incorrect value 500000 with 100000

# Strip any whitespace and convert to string
artisan_df['What type of handicraft your business is focused on?'] = artisan_df['What type of handicraft your business is focused on?'].astype(str).str.strip()
artisan_df['What type of handicraft your business is focused on?'] = artisan_df['What type of handicraft your business is focused on?'].replace('Carteps and Rugs', 'Carpets & Rugs')
artisan_df['What type of handicraft your business is focused on?'] = artisan_df['What type of handicraft your business is focused on?'].replace('Carpets and Rugs', 'Carpets & Rugs')
artisan_df['What type of handicraft your business is focused on?'] = artisan_df['What type of handicraft your business is focused on?'].replace('Leather work', 'Leatherwork')
artisan_df['What type of handicraft your business is focused on?'] = artisan_df['What type of handicraft your business is focused on?'].replace('Jewlery', 'Jewelry')
artisan_df['What type of handicraft your business is focused on?'] = artisan_df['What type of handicraft your business is focused on?'].replace('Textile', 'Textiles')

#Import Dashboard Libraries
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output


# Try to load the dataset
try:
    artisan_df = pd.read_csv(url)
except Exception as e:
    print(f"Error loading data: {e}")
    artisan_df = pd.DataFrame()  # Create an empty dataframe as a fallback

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Define the layout of the app
app.layout = html.Div([
    html.H1("Interactive Dashboard"),
    dcc.Dropdown(
        id='city-dropdown',
        options=[{'label': city, 'value': city} for city in artisan_df['City'].unique()] + [{'label': 'All Cities', 'value': 'All Cities'}],
        value='All Cities',
        clearable=False
    ),
    dcc.Dropdown(
        id='handicraft-dropdown',
        options=[{'label': 'All Categories', 'value': 'All Categories'}] +
                [{'label': category, 'value': category} for category in artisan_df['What type of handicraft your business is focused on?'].unique()],
        value='All Categories',
        clearable=False
    ),
    dcc.Graph(id='age-income-scatter'),
    html.Div([
        dcc.Graph(id='category-bar-chart', style={'display': 'inline-block', 'width': '50%'}),
        dcc.Graph(id='market-bar-chart', style={'display': 'inline-block', 'width': '50%'})
    ])
])

# Callback to update the graphs based on dropdown selections
@app.callback(
    [Output('age-income-scatter', 'figure'),
     Output('category-bar-chart', 'figure'),
     Output('market-bar-chart', 'figure')],
    [Input('city-dropdown', 'value'),
     Input('handicraft-dropdown', 'value')]
)
def update_graphs(selected_city, selected_category):
    if artisan_df.empty:
        return {}, {}, {}  # Return empty figures if data is not loaded

    if selected_city == 'All Cities':
        filtered_df = artisan_df
    else:
        filtered_df = artisan_df[artisan_df['City'] == selected_city]

    if selected_category != 'All Categories':
        filtered_df = filtered_df[filtered_df['What type of handicraft your business is focused on?'] == selected_category]

    # Create scatter plot
    fig_scatter = px.scatter(filtered_df, x='Age', y='Annual Income Range', color='City', title=f'Age vs Income in {selected_city}')
    
    # Create bar chart for categories
    category_counts = filtered_df['What type of handicraft your business is focused on?'].value_counts()
    fig_category_bar = px.bar(category_counts, x=category_counts.index, y=category_counts.values, title='Handicraft Categories')

    # Create bar chart for market distribution
    market_columns = ['Local Market', 'Village Level', 'Foreign Market', 'National Market']
    market_counts = filtered_df[market_columns].apply(pd.Series.value_counts).fillna(0).loc['Yes']
    fig_market_bar = px.bar(market_counts, x=market_counts.index, y=market_counts.values, title='Market Distribution')

    return fig_scatter, fig_category_bar, fig_market_bar

# Run the app on a different port
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
