# -*- coding: utf-8 -*-
"""
Created on Thu May 27 10:46:59 2021

@author: ldouglas
"""

###########IMPORT STATEMENTS###############################
import dash 
from dash_table import DataTable, FormatTemplate
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from datetime import datetime
from dash_extensions.enrich import Input, Output, ServersideOutput, Dash, FileSystemStore, State
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame, send_bytes
from dash.exceptions import PreventUpdate
from dash.dependencies import ALL
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import webbrowser
import dash_table
import plotly.express as px
import datetime as dt
import getpass
import flask
import base64
import plotly.express as px

pd.options.mode.chained_assignment = None  # default='warn'

###########READ DATA FILES###################################

kidscount = pd.read_excel('C:/Users/ldouglas/Documents/L Douglas/DS4A/KidsCount.xlsx')
warddata = pd.read_excel('C:/Users/ldouglas/Documents/L Douglas/DS4A/DatabyWard.xlsx')


#################IMAGES########################################
ward1map = 'ward1map.png'
ward2map = 'ward2map.png'
wardmapall = 'wardmapall.jpeg'
#encoded_image = base64.b64encode(open(ward1map, 'rb').read())

tsunami_logo = 'TSUNAMI_LOGO_CROP.jpg'
encoded_image = base64.b64encode(open(wardmapall, 'rb').read())
############COLORS############################################
blue = '#2c3e50'
indigo = '#6610f2'
purple = '#6f42c1'
pink = '#e83e8c'
red = '#e74c3c'
orange = '#fd7e14'
yellow = '#f39c12'
green = '#18bc9c'
teal = '#20c997'
cyan = '#3498db'
white = '#fff'
gray = '#95a5a6'
gray_dark = '#343a40'
primary = '#2c3e50'
secondary = '#95a5a6'
success = '#18bc9c'
info = '#3498db'
warning = '#f39c12'
danger = '#e74c3c'
dark = '#7b8a8b'

##bootstrap colors
tsunamiblue = '#1261D8' #tsunami blue
primary = '#129dd8' #pratt&whitney blue
secondary = '#6c757d'
light = '#ecf0f1'
red = '#900d09'
font_family = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"'

##############IMPORTING BOOTSTRAP THEME#######################
output_defaults = dict(backend=FileSystemStore(cache_dir = 'cache_dir'),
                       session_check=True)

app = Dash(__name__, output_defaults=output_defaults, external_stylesheets=[dbc.themes.BOOTSTRAP])



################FUNCTIONS################################
def create_medianincomecard(title, number, description):
    card = dbc.Card(
     dbc.CardBody([
         #html.H2(title, id='Scrap_title'), 
         html.H5(number, id='MedianIncome_value'),
         html.P(description, id='MIDescription')
         ]), id='MedianIncomeCard', style={'textAlign':'center'}, color= tsunamiblue, inverse=True)
    return card

def create_povertycard(title, number, description):
    card = dbc.Card(
     dbc.CardBody([
         #html.H2(title, id='Scrap_title'), 
         html.H5(number, id='Poverty_value'),
         html.P(description, id='PvDescription')
         ]), id='PovertyCard', style={'textAlign':'center'}, color= tsunamiblue, inverse=True)
    return card

def create_communitygardencard(title, number, description):
    card = dbc.Card(
     dbc.CardBody([
         #html.H2(title, id='Scrap_title'), 
         html.H5(number, id='CommunityGarden_value'),
         html.P(description, id='CGDescription')
         ]), id='CommunityGardenCard', style={'textAlign':'center'}, color= tsunamiblue, inverse=True)
    return card

def create_populationcard(title, number, description):
    card = dbc.Card(
     dbc.CardBody([
         #html.H2(title, id='Scrap_title'), 
         html.H5(number, id='Population_value'),
         html.P(description, id='PDescription')
         ]), id='PopulationCard', style={'textAlign':'center'}, color= tsunamiblue, inverse=True)
    return card

def create_grocerystorecard(title, number, description):
    card = dbc.Card(
     dbc.CardBody([
         #html.H2(title, id='Scrap_title'), 
         html.H5(number, id='GroceryStore_value'),
         html.P(description, id='GSDescription')
         ]), id='GroceryStoreCard', style={'textAlign':'center'}, color= tsunamiblue, inverse=True)
    return card

def create_wardsizecard(title, number, description):
    card = dbc.Card(
     dbc.CardBody([
         #html.H2(title, id='Scrap_title'), 
         html.H5(number, id='WardSize_value'),
         html.P(description, id='WSDescription')
         ]), id='WardSizeCard', style={'textAlign':'center'}, color= tsunamiblue, inverse=True)
    return card



#############DASHBOARD LAYOUT##################################
header = dbc.Container([
        dbc.Col([
            html.H3(
                children='WASHINGTON, DC WARD STATISTICS & COMMUNITY FRIDGE ANALYTICS', 
                style={'color':'white', 'padding-top':'0.25rem'}
                )])
        ],style={'background-color':tsunamiblue,
              'padding':'3rem 3rem 3rem 3rem',
              'list-style-type':'None',
              'textAlign':'center',
              'height':'10vh'
              }, 
    fluid=True)
'''
sidebar = html.Div([
        dbc.Row([
            dbc.Col([
                html.Br(),
                html.H6('Ward'),
                dcc.Dropdown(id='ward_dropdown', 
                             options = [{'label': mod, 'value':mod} for mod in kidscount['Ward'].unique()],
                             value = None,
                             placeholder = 'Select an ward')
                ])
            ])
        ])
'''

    
tab_ward_statistics=dbc.Tab([    
    dbc.Row([
    dbc.Col([
        html.Hr(),
        dbc.Row([
            html.Div([dbc.Label("Select a Ward --> ")], style={'display':'inline-block', 'backgroundColor': tsunamiblue}),
            html.Div([dbc.RadioItems(
                  options=[{'label': mod, 'value':mod} for mod in warddata['Ward'].unique()],    
                  value='All Wards',
                 inline=True, id='RadioButtonAttribute')], style={'display': 'inline-block'})  ],style={'color':'white', 'background-color':tsunamiblue, 'padding':'1rem 1rem 1rem 1rem'} ),
    html.Hr(),
    dbc.CardGroup([ # Score Cards
                   dbc.Card([
                       dbc.CardHeader([
                           html.H6('Median Income'),
                           dbc.CardBody([
                               dbc.Spinner([create_medianincomecard('Median Income', '0', '(By Ward)')]) ])
                           ], id='medianincome_card')],),
                   dbc.Card([
                       dbc.CardHeader([
                           html.H6('Poverty %'),
                           dbc.CardBody([
                               dbc.Spinner([create_povertycard('% in Poverty', '49 %', '(% of Population)')]) ])
                           ], id='poverty_card')]),
                   dbc.Card([
                       dbc.CardHeader([
                           html.H6('Community Gardens'),
                           dbc.CardBody([
                               dbc.Spinner([create_communitygardencard('# of Community Gardens', '8', '(Counts By Ward)')])])
                           ], id='communitygarden_card')]),
                   dbc.Card([
                       dbc.CardHeader([
                           html.H6('Population'),
                           dbc.CardBody([
                               dbc.Spinner([create_populationcard('Population', '100k', '(Population by Ward)')])])
                           ], id='population_card')]),
                   dbc.Card([
                       dbc.CardHeader([
                           html.H6('Size of Ward'),
                           dbc.CardBody([
                               dbc.Spinner([create_wardsizecard('WardSize', '650sqft', '(Sq Footage of Ward)')]) ])
                           ], id='wardsize_card')]),
                   dbc.Card([
                       dbc.CardHeader([
                           html.H6('Grocery Stores'),
                           dbc.CardBody([
                               dbc.Spinner([create_grocerystorecard('# of Grocery Stores', '8', '(Counts By Ward)')]) ])
                           ], id='grocerystore_card')])
                   ]),
    ], width=8, align='center', style={'textAlign':'center'}),
    dbc.Col([
        dbc.Row([
        dbc.Col([html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={'padding':'4rem 1rem','width':'80%', 'height':'80%', 'textAlign': 'center', 'align': 'center'})], ),
  #      dbc.Col([html.H1('Personal Development Plan (PDP)')], align='center', style={'textAlign':'center'}),
  #      dbc.Col([html.H6('Version 0.2; 8/2/2021')], align='center', style={'textAlign':'center'}),
        ]),
        ]),
    ],no_gutters=True),
    
    html.Br(), 
    dbc.Row([#Smoothing Graph 
                dbc.Col([
                    dbc.CardGroup([
                        dbc.Card([
                            dbc.CardHeader([
                                html.H5('MEDIAN INCOME OVER TIME'), ]),
                                dbc.CardBody([dbc.Spinner(dcc.Graph(id='graph_scatter')) ]) ], id='smoothing-card', color= tsunamiblue, inverse=True),  
                dbc.Card([
                            dbc.CardHeader([
                                html.H5('COMMUNITY GARDENS'), ]),
                                dbc.CardBody([dbc.Spinner()]) ]), 
                dbc.Card([
                            dbc.CardHeader([
                                html.H5('GROCERY STORES'), ]),
                                dbc.CardBody([dbc.Spinner()]) ]), 
                dbc.Card([
                            dbc.CardHeader([
                                html.H5('AGE STATISTICS'), ]),
                                dbc.CardBody([dbc.Spinner()]) ]) ]) ]) 
                ], align='center', justify='center', style={'textAlign':'center'}),
    dcc.Store(id='warddata'),
    ], label='Ward Statistics', tab_id='tab_ward_statistics')

tab_ward_comparisons = dbc.Tab([
    dbc.Container([
        html.Br(),
        dbc.Row([dbc.Label("Ward Comparisons", style={'color': tsunamiblue, 'font-weight': 'bold', 'font-size': '24px' })], style={'textAlign':'center', 'align': 'center'}),
        dbc.CardGroup([
            dbc.Card([
                dbc.CardBody([
                 
                        dbc.Col([
                            dcc.Dropdown(id='ward_dropdown1', 
                             options = [{'label': mod, 'value':mod} for mod in warddata['Ward'].unique()],
                             value = None,
                             placeholder = 'Select a ward'),
                            html.Br(),
                            html.H4(['Ward Score: 78']),
                            dbc.CardImg(src="DS4A/wardmap.png", bottom=True)])
                        ], style={'backgroundcolor': tsunamiblue}),
                ]),
            
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([dcc.Dropdown(id='ward_dropdown2', 
                             options = [{'label': mod, 'value':mod} for mod in kidscount['Ward'].unique()],
                             value = None,
                             placeholder = 'Select a ward'),
                            html.Br(),
                            html.H4(['Ward Score: 52']),
                            dbc.CardImg(src="DS4A/wardmap.png", bottom=True)])     
                        ], style={'backgroundcolor': tsunamiblue}) ]) ]) ]) 
                          
            ], fluid=True)
           
    ], label='Ward Comparisions', tab_id = 'tab_ward_comparisons')

tab_final_selection = dbc.Tab([ 
    dbc.Container([
        html.Br(),
        dbc.Row([dbc.Label("Final Selection - Community Fridge Location", style={'color': tsunamiblue, 'font-weight': 'bold', 'font-size': '24px' })], style={'textAlign':'center', 'align': 'center'}),
        dbc.CardGroup([
            dbc.Card([
                dbc.CardBody([
                        dbc.Col([
                            html.H4(['Where and Why']),
                            dbc.CardImg(src="DS4A/wardmap.png", bottom=True)])
                        ], style={'backgroundcolor': tsunamiblue}),
                ]),
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                            html.Br(),
                            html.H4(['Opportunity Zone']),
                            dbc.CardImg(src="DS4A/wardmap.png", bottom=True)])     
                        ], style={'backgroundcolor': tsunamiblue}) ]),
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                            html.Br(),
                            html.H4(['Selection Criteria']),
                            dbc.CardImg(src="DS4A/wardmap.png", bottom=True)])     
                        ], style={'backgroundcolor': tsunamiblue})
                ]) ]) 
                          
            ], fluid=True)
    ], label='Final Selection', tab_id='tab_final_selection')

tab_ALL = html.Div([
    dbc.Tabs([tab_ward_statistics, tab_ward_comparisons, tab_final_selection], id='Tab_ALL', active_tab = 'tab_ward_statistics'),
    html.Div(id='tabcontent')
    ], style={'width': '100%'})

content = dbc.Container([
    html.Div([
        html.Br(),
        dbc.Row([tab_ALL]),
        ])
   ], fluid=True, style={'padding':'1rem 4rem', 'backgroundColor': 'light'})    

main = dbc.Container([
    header,
    html.Div([
        dbc.Row([
      #      dbc.Col([sidebar], width=3, style={'border-right':'1px solid {}'.format('secondary'),
       #                                        'height':'90vh', 'overflow-y':'scroll'}),
            dbc.Col([content], style={'height':'90vh', 'overflow-y':'scroll'})
            ], align='stretch'),
        ])], fluid=True, style={'padding':'1rem 2rem', 'backgroundColor': 'light'})



#############CALLBACKS########################################
'''@app.callback(ServersideOutput('kidsdata', 'data'),
              Input('ward_dropdown', 'value'))
def storedata(ward):
    if ward is None:
        raise PreventUpdate()
    
    kidsdata = kidscount[kidscount['Ward'] == ward]
        
    return kidsdata.to_dict('records')
'''
@app.callback(ServersideOutput('warddata', 'data'),
              Input('RadioButtonAttribute', 'value'))
def storewarddata(ward):
    if ward is None:
        raise PreventUpdate()
    
    #vendordata = mmps[(mmps['organization_name']==vendor)] 
    ward = warddata[(warddata['Ward'] == ward)]
    return ward.to_dict('records')

@app.callback(Output('graph_scatter', 'figure'),  #take stored data to create graph
              Input('RadioButtonAttribute', 'value'),
              Input('kidsdata', 'data'))
def createscattergraph(ward, kidsdata):
    #print(order)
    if kidsdata is None or len(kidsdata)==0:  #if none or has no rows
        raise PreventUpdate
    
    
    kidsdata = kidscount[kidscount['Ward'] == ward]

    fig = px.scatter(kidsdata, x='Year', y='Median Income')
    fig.update_layout(#legend=dict(orientation='h', yanchor='bottom', xanchor='right'),
                         xaxis=dict(title= 'Year'),
                          yaxis=dict(title = 'Median Income'),
                              showlegend=True)
    
    return fig

@app.callback(Output('MedianIncome_value', 'children'),
              Output('Poverty_value', 'children'),
              Output('CommunityGarden_value', 'children'),
              Output('Population_value', 'children'),
              Output('WardSize_value', 'children'),
              Output('GroceryStore_value', 'children'),
             Input('RadioButtonAttribute', 'value'),
             Input('warddata', 'data'))
def create_cardaggregations(wardselection, warddata):
    if warddata is None or len(warddata)==0:
        raise PreventUpdate()
    
    selectedwarddata = pd.DataFrame(warddata)

    #selectedwarddata = warddata[warddata['Ward']==wardselection]
    print(selectedwarddata)
    
    '''
    if ward is None:
        kidsdata = pd.DataFrame(kidscount)
    
    else:
        kidsdata = pd.DataFrame(kidsdata)
    
    print(kidsdata)
    '''
    medianincome = round(selectedwarddata['MedianIncome'].mean(),2)
    medianincome = '${:,.2f}'.format(medianincome)
    #print(medianincome)
    
    povertyvalue = round(selectedwarddata['POVERTY %'].mean(),1)
    provertyvalue = '{:,.0%}'.format(povertyvalue) 
    
    gardencount = selectedwarddata['GARDEN Counts']
    
    population = round(selectedwarddata['POPULATION'],0)
    
    size = round(selectedwarddata['SQ Miles'])
    
    grocery = round(selectedwarddata['GROCERY Counts'],0)
    return medianincome, provertyvalue, gardencount, population, size, grocery

##############RUN DASHBOARD###################################


app.layout=main
webbrowser.open('http://127.0.0.1:8050')
app.run_server()



