from dash import Dash, dcc, html, Input, Output
import pandas as pd
import altair as alt

df = pd.read_csv("netflix_titles.csv")
df['genre'] = df['listed_in'].apply(lambda x: x.split(', '))
df = df.explode('genre')

def plot_rating(genre):
    chart = alt.Chart(df[df.genre == genre], title=f"Rating distribution of {genre}").mark_bar().encode(
              y=alt.Y('rating', title="Rating"),
              x=alt.X('count()', title="Frequency")
              )
    return chart.to_html()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H1(children='Rating distribution of Netflix shows/movies', style={'font-size': "360%", 'color':'#bd1818'}),
    html.Br(),
        html.Iframe(
            id='bar',
            style={'border-width': '0', 'width': '600px', 'height': '500px'},
            srcDoc=plot_rating(genre='Comedies')),
            html.Div(children="Please select a genre of Netflix TV show/movie", 
            style={'color':'#bd1818'}),
            dcc.Dropdown(
            id='genre', value='Comedies',
            options=[{'label': i, 'value': i} for i in df['genre'].unique()],
            style={'height': '20px', 'width': '350px'})])

@app.callback(
    Output('bar', 'srcDoc'),
    Input('genre', 'value'))

def update_output(genre):
    return plot_rating(genre)

if __name__ == '__main__':
    app.run_server(debug=True)