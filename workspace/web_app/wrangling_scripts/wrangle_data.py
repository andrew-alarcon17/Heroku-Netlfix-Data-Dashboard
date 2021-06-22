import pandas as pd
import plotly.graph_objs as go

# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`

def clean_data(dataset):
    """Cleans the netflix data frame.

    Replaces null values in the raitngs column with the mean. 
    Removes 2 rows of the genres column where null values were present.

    Args:
        dataset (str): name of the csv data file

    Returns:
        None

    """
    
    df = pd.read_csv(dataset)
    df['rating'].fillna(int(df['rating'].mean()), inplace=True)
    df = df.dropna( how='any', subset=['genres'])
    
    return df

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    # first chart plots arable land from 1990 to 2015 in top 10 economies 
    # as a line chart
    
    df = pd.read_csv('data/netflix_list.csv')
    
    graph_one = []
    #df.columns = ['genre', 'scores']
    df.sort_values('rating', ascending=False, inplace=True)

    graph_one.append(
        go.Scatter(
            x = df.title.tolist(),
            y = df.rating.tolist(),
            mode = 'lines'
        )
    )

    layout_one = dict(title = 'Shows/Movies by Score',
                      xaxis = dict(title = 'Title',autotick=True,),
                      yaxis = dict(title = 'Rating'),
                     )
    
    graph_two = []
    data2 = df.groupby(df.orign_country)["rating"].mean().head(11).sort_values(ascending=False)
    top_countries = pd.DataFrame(data2)
    top_countries = top_countries.reset_index()
    top_countries.drop(top_countries.loc[top_countries['orign_country']=='-'].index, inplace=True)
    
    
    #df.columns = ['genre', 'scores']
    top_countries.sort_values(by='rating')

    graph_two.append(
        go.Bar(
            x = top_countries.orign_country.tolist(),
            y = top_countries.rating.tolist(),
        )
    )

    layout_two = dict(title = 'Countries by Their Average Ratings',
                      xaxis = dict(title = 'Origin Country',autotick=True,),
                      yaxis = dict(title = 'Rating'),
                     )
    
    graph_three = []
    data3 = df.startYear.value_counts()
    shows_year = pd.DataFrame(data3)
    shows_year = shows_year.reset_index()
    shows_year.rename(columns = {'index':'Year', 'startYear':'Count',}, inplace = True)
    shows_year = shows_year.head(10)
    
    #df.columns = ['genre', 'scores']
    shows_year.sort_values(by='Year')
    
    graph_three.append(
        go.Bar(
            x = shows_year.Year.tolist(),
            y = shows_year.Count.tolist(),
        )
    )

    layout_three = dict(title = 'Number of Shows Released Each Year since 2011',
                      xaxis = dict(title = 'Year',),
                      yaxis = dict(title = 'Count'),
                     )
    
    graph_four = []
    top_episodes = df.nlargest(10, columns=['episodes'])
    
    graph_four.append(
        go.Bar(
            x = top_episodes.title.tolist(),
            y = top_episodes.episodes.tolist(),
        )
    )

    layout_four = dict(title = 'Shows With The Most Episodes',
                      xaxis = dict(title = 'Title',),
                      yaxis = dict(title = 'Episode Count'),
                     )
    
    
    # append all charts to the figures list
    figures = []
    #figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))

    return figures