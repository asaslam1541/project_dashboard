#Import Libraries
import pandas as pd
from pathlib import Path

#Create DataFrame
url = 'https://raw.githubusercontent.com/your-username/your-repository/main/artisan_data.csv'
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

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the Dash app
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
        options=[
            {'label': 'All Categories', 'value': 'All Categories'},
            {'label': 'Textiles', 'value': 'Textiles'},
            {'label': 'Carpets & Rugs', 'value': 'Carpets & Rugs'},
            {'label': 'Ceramics', 'value': 'Ceramics'},
            {'label': 'Jewelry', 'value': 'Jewelry'},
            {'label': 'Leatherwork', 'value': 'Leatherwork'}
        ],
        value='All Categories',
        clearable=False
    ),
    html.Div([
        dcc.Graph(id='age-income-scatter', style={'width': '100%', 'display': 'inline-block'}),
        dcc.Graph(id='category-bar-chart', style={'width': '50%', 'display': 'inline-block'}),
        dcc.Graph(id='market-bar-chart', style={'width': '50%', 'display': 'inline-block'})
    
        
    ])
])

# Callback to update the scatter plot based on dropdown selection
@app.callback(
    Output('age-income-scatter', 'figure'),
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
    fig = px.scatter(filtered_df, x='Age', y='Annual Income Range', color='Work Permit Status', 
                     title=f'Age vs Income in {selected_city} - {selected_handicraft}',
                     labels={'Work Permit Status': 'Work Permit Status'})

    # Add overall average line
    overall_avg_income = artisan_df['Annual Income Range'].mean()
    fig.add_shape(
        type="line",
        x0=filtered_df['Age'].min(),
        x1=filtered_df['Age'].max(),
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
            x0=filtered_df['Age'].min(),
            x1=filtered_df['Age'].max(),
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
                     title=f'Number of Values in Each Category by {selected_city}')

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
                            title=f'Number of Values in Each Market by {selected_city}')

    return market_bar_fig

# Run the app on a different port
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
