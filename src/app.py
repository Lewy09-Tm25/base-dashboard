'''
 # @ Create Time: 2025-01-21 18:33:13.385085
'''

import pandas as pd
import numpy as np
from faker import Faker
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import datetime

# Set random seed for reproducibility
np.random.seed(42)
fake = Faker()

# Generate fake data for Time to Grid Connection (Primary Metric)
def generate_deployment_data():
    start_date = datetime.date(2023, 1, 1)
    dates = [start_date + datetime.timedelta(days=x) for x in range(365)]
    
    # Create baseline trend that improves over time (from ~180 days to ~100 days)
    baseline = np.linspace(180, 100, len(dates))
    
    # Add seasonal variation and random noise
    seasonal = 15 * np.sin(np.linspace(0, 4*np.pi, len(dates)))  # Seasonal pattern
    noise = np.random.normal(0, 5, len(dates))  # Random variation
    
    times = baseline + seasonal + noise
    
    return pd.DataFrame({
        'date': dates,
        'days_to_connection': times.clip(min=90)  # Ensure no values below 90 days
    })

# Generate fake data for Battery Capacity Utilization
def generate_utilization_data():
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    
    # Create baseline trend that improves over time (from ~70% to ~90%)
    baseline = np.linspace(70, 90, len(dates))
    
    # Add seasonal variation and random noise
    seasonal = 5 * np.sin(np.linspace(0, 8*np.pi, len(dates)))  # Seasonal pattern
    noise = np.random.normal(0, 2, len(dates))  # Random variation
    
    utilization = baseline + seasonal + noise
    
    return pd.DataFrame({
        'date': dates,
        'utilization': utilization.clip(min=65, max=98)  # Keep within realistic bounds
    })

# Generate fake data for Market Penetration by Region and Time
def generate_market_penetration_data():
    regions = ['West Coast', 'Southwest', 'Northeast', 'Southeast', 'Midwest', 
               'Mountain', 'Pacific Northwest', 'Central', 'Mid-Atlantic']
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='M')
    
    data = []
    for region in regions:
        # Base rate different for each region
        base_rate = np.random.uniform(5, 15)
        
        # Growth rate different for each region
        growth_rate = np.random.uniform(0.2, 0.5)
        
        for date in dates:
            # Calculate penetration rate with some randomness
            months_passed = (date - pd.Timestamp('2023-01-01')).days / 30
            penetration = base_rate + (growth_rate * months_passed) + np.random.normal(0, 0.5)
            
            data.append({
                'date': date,
                'region': region,
                'penetration_rate': max(0, min(penetration, 30))  # Cap at 30%
            })
    
    return pd.DataFrame(data)

# Create the data
deployment_df = generate_deployment_data()
utilization_df = generate_utilization_data()
penetration_df = generate_market_penetration_data()
# print(penetration_df.columns)

# Custom CSS for enhanced styling
external_stylesheets = [
    'https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap'
]

app = Dash(__name__, title="BaseDashboard")

# Declare server for deployment. Needed for Procfile.
server = app.server
# Custom color palette
colors = {
    'primary': '#1a365d',
    'secondary': '#7c3aed',
    'accent': '#059669',
    'background': '#f8fafc',
    'text': '#1e293b'
}

# Define the layout with enhanced styling
app.layout = html.Div([
    # Executive Summary
    html.Div([
        html.H1("Base Power Company Dashboard", 
                style={
                    'textAlign': 'center',
                    'fontFamily': 'Poppins',
                    'color': colors['primary'],
                    'fontSize': '2.5rem',
                    'padding': '20px',
                    # 'textTransform': 'uppercase',
                    'letterSpacing': '0.1em'
                }),
        html.Div([
            html.H3("Executive Note:", 
                    style={
                        'color': colors['secondary'],
                        'fontFamily': 'Poppins',
                        'fontWeight': '600'
                    }),
            html.P("""
                Time to Grid Connection is our primary metric as it directly demonstrates our core competitive advantage: 
                our ability to deploy battery storage systems significantly faster than the industry standard of 3-5 years. 
                We've achieved a 44% improvement in deployment time over the past year, reducing from 180 to approximately 100 days.
                
                Supporting metrics of Capacity Utilization and Regional Market Penetration provide crucial context about 
                operational efficiency and market expansion, validating our rapid deployment strategy's effectiveness.
            """, style={
                'fontSize': '16px',
                'lineHeight': '1.8',
                'fontFamily': 'Poppins',
                'color': colors['text']
            })
        ], style={
            'backgroundColor': colors['background'],
            'padding': '30px',
            'borderRadius': '15px',
            'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
            'margin': '20px 0'
        })
    ]),
    
    # Primary Metric - Keeping as line chart but with enhanced styling
    html.Div([
        html.H2("Primary Metric: Time to Grid Connection", 
                style={
                    'textAlign': 'center',
                    'fontFamily': 'Poppins',
                    'color': colors['primary']
                }),
        dcc.Graph(
            figure=px.line(
                deployment_df, 
                x='date', 
                y='days_to_connection',
                title='Average Days to Grid Connection (2023)',
                labels={'days_to_connection': 'Days to Connection', 'date': 'Date'},
            ).update_layout(
                height=600,
                title_x=0.5,
                title_font_size=24,
                paper_bgcolor=colors['background'],
                plot_bgcolor=colors['background'],
                font_family='Poppins',
                title_font_family='Poppins',
            ).update_traces(line_color=colors['primary'], line_width=3)
        )
    ], style={
        'marginBottom': '40px',
        'padding': '20px',
        'backgroundColor': 'white',
        'borderRadius': '15px',
        'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
    }),
    
    # Secondary Metrics with Creative Visualizations
    html.Div([
        # Battery Utilization - Gauge Chart with interpretation
        html.Div([
            html.H3("Supporting Metric: Battery Capacity Utilization",
                    style={'fontFamily': 'Poppins', 'color': colors['secondary']}),
            dcc.Graph(
                figure=go.Figure(go.Indicator(
                    mode="gauge+number",  # Removed delta for clarity
                    value=utilization_df['utilization'].iloc[-1],
                    title={
                        'text': "Current Utilization",
                        'font': {'size': 24, 'color': colors['secondary']}
                    },
                    number={
                        'suffix': "%",
                        'font': {'size': 36, 'color': colors['primary']}
                    },
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={
                        'axis': {
                            'range': [0, 100],
                            'tickwidth': 1,
                            'tickcolor': colors['text'],
                            'ticktext': ['0%', '25%', '50%', '75%', '100%'],
                            'tickvals': [0, 25, 50, 75, 100]
                        },
                        'bar': {'color': colors['secondary']},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': colors['text'],
                        'steps': [
                            {'range': [0, 50], 'color': '#fee2e2'},
                            {'range': [50, 75], 'color': '#fef3c7'},
                            {'range': [75, 100], 'color': '#dcfce7'}
                        ],
                        'threshold': {
                            'line': {'color': colors['primary'], 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                )).update_layout(
                    paper_bgcolor=colors['background'],
                )
            ),
            html.Div([
                html.P("""
                    This gauge shows our current battery capacity utilization as a percentage. The colored zones indicate performance levels: 
                    red (0-50%) needs attention, yellow (50-75%) is acceptable, and green (75-100%) is optimal. The black marker line at 90% 
                    represents our target utilization rate.
                """, 
                style={
                    'fontFamily': 'Poppins',
                    'fontSize': '14px',
                    'lineHeight': '1.5',
                    'color': colors['text'],
                    'backgroundColor': '#f8fafc',
                    'padding': '15px',
                    'borderRadius': '8px',
                    'marginTop': '15px'
                })
            ])
        ], style={'width': '45%', 'display': 'inline-block', 'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '15px', 'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'}),
        
        # Market Penetration - Sunburst Chart with interpretation
        html.Div([
            html.H3("Supporting Metric: Regional Market Penetration",
                    style={'fontFamily': 'Poppins', 'color': colors['accent']}),
            dcc.Graph(
                figure=px.sunburst(
                    penetration_df[penetration_df['date'] == penetration_df['date'].max()],
                    path=['region'],
                    values='penetration_rate',
                    title='Current Market Penetration by Region',
                    custom_data=['penetration_rate']  # Only include penetration_rate for hover
                ).update_layout(
                    height=400,
                    title_x=0.5,
                    font_family='Poppins',
                    paper_bgcolor=colors['background'],
                    hoverlabel=dict(
                        bgcolor="white",
                        font_size=16,
                        font_family="Poppins"
                    )
                ).update_traces(
                    marker=dict(colors=px.colors.sequential.Viridis),
                    hovertemplate="%{customdata[0]:.1f}%<extra></extra>",  # Only show penetration rate
                    textinfo="label",
                    textfont=dict(size=14)
                )
            ),
            html.Div([
                html.P("""
                    This sunburst chart displays market penetration across different regions. The size and color intensity of each segment 
                    represent the penetration percentage. Darker/larger segments indicate higher market penetration. Hover over any segment 
                    to see the exact penetration rate.
                """,
                style={
                    'fontFamily': 'Poppins',
                    'fontSize': '14px',
                    'lineHeight': '1.5',
                    'color': colors['text'],
                    'backgroundColor': '#f8fafc',
                    'padding': '15px',
                    'borderRadius': '8px',
                    'marginTop': '15px'
                })
            ])
        ], style={'width': '45%', 'display': 'inline-block', 'float': 'right', 'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '15px', 'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'})

# [Rest of the code remains the same]
    ])
], style={'padding': '20px', 'backgroundColor': '#f1f5f9'})

if __name__ == '__main__':
    app.run_server(debug=True)