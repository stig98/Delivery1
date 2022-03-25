import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

# Div.
import pandas as pd
import numpy as np
import calendar

# Plotly
import plotly.express as px
import plotly.graph_objects as go


# Get data

import Delivery1_chri65gz
order = Delivery1_chri65gz.get_data()
df_year = Delivery1_chri65gz.get_year()
df_month = Delivery1_chri65gz.get_month()

# Diagram - Employee by Sales
fig_employee = px.bar(order, 
    x='employee_name', y='total', 
    color='type', text='total', title='Sales by Employee',
    hover_data=[],
    labels={'total':'Total sales', 'emp_name':'Employee', 'type':'Product Type'})
fig_employee.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig_employee.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis_tickangle=45)

# Diagram - Products by sale
fig_products = px.bar(order, 
    x='products_name', y='total'
    color='type'), text='total', title='Sales by products',
    hover_data=[],
    labels={'total':'Total Products sold', 'productname':'Productname', 'type':'Product type'})
fig_products.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig_products.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis_tickangle=45)




# Activate the app

#app = dash.Dash(__name__)

dash_app = dash.Dash(__name__)
app = dash_app.server

# ***************************************
# Layout
# ***************************************
dash_app.layout = html.Div(
    children=[
        html.Div(className='row',
                children=[
                    html.Div(className='four columns div-user-controls',
                            children=[
                                html.H2('Sales dashboard'),
                                html.P('Select filters from dropdown'),

                    html.Div(children="Month", className="menu-title"),
                            dcc.Dropdown(
                                id='drop_month',
                                options=[{'label':selectmonth, 'value':selectmonth} for selectmonth in df_month['monthnames']],
                            ),
                    html.Div(children="Year", className="menu-title"),
                            dcc.Dropdown(
                                id='drop_year',
                                options=[{'label':selectyear, 'value':selectyear} for selectyear in df_year]
                            ),
                            ]
                    ),
                    html.Div(className='eight columns div-for-charts bg-grey',
                            children=[
                                dcc.Graph(id="sales_employee", figure=fig_employee),
                                dcc.Graph(id="Sales by products", figure=fig_products)
                            ]
                    ),
                ]
            )
        ]
)

# ***************************************
# Callbacks
# ***************************************
# Output er diagrammet
# Input er DropDown
@dash_app.callback(Output('sales_employee', 'figure'),
              [Input('drop_month', 'value')],
              [Input('drop_year', 'value')])

def update_graph(drop_month, drop_year):
    if drop_year:
        if drop_month:
            # Data i både drop_month og drop_year
            order_fig1 = order.loc[(order['orderyear'] == drop_year) & (order['ordermonth'] == drop_month)]
        else:
            # Data i drop_year. men ikke drop_month
            order_fig1 = order.loc[order['orderyear'] == drop_year]
    else:
        if drop_month:
            # Data i drop_month, men ikke drop_year
            order_fig1 = order.loc[order['ordermonth'] == drop_month]
        else:
            # Ingen data - ikke noget valgt
            order_fig1 = order
        
    return {'data':[go.Bar(
        x = order_fig1['productname'],
        y = order_fig1['total']
            )
        ]
    }

# ***************************************
# Run the app
# ***************************************
if __name__ == '__main__':
    dash_app.run_server(debug=True)