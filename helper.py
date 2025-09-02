import numpy as np

def fetch_medal_tally(df1,year, country):
    medal_df = df1.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x



def medal_tally(df1):

    medal_tally = df1.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally=medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values(
    'Gold',ascending=False).reset_index()
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    medal_tally['Gold']=medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['total'] = medal_tally['total'].astype('int')

    return medal_tally

def country_year_list(df1):
    years = df1['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df1['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country

def data_over_time(df1,col):

    nations_over_time = df1.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year': 'Edition', 'count':col}, inplace=True)
    return nations_over_time


# Helper Function
def most_successful(df1, sport):
    temp_df = df1.dropna(subset=['Medal'])  # Drop rows where Medal is NaN

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Create a count of medals per athlete
    athlete_medal_count = temp_df['Name'].value_counts().reset_index()
    athlete_medal_count.columns = ['Name', 'count']

    # Merge to get additional details
    merged_df = athlete_medal_count.merge(
        df1[['Name', 'Sport', 'region']].drop_duplicates('Name'),
        on='Name',
        how='left'
    )

    # Select top 15 athletes
    top_athletes = merged_df.head(15)
    return top_athletes

def yearwise_medal_tally(df1, country):
    temp_df = df1.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').size().reset_index(name='Medal')

    return final_df



def country_event_heatmap(df1, country):
    temp_df = df1.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    # Check if new_df is empty before creating the pivot table
    if new_df.empty:
        return None

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def most_successful_countrywise(df1, country):
    temp_df = df1.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]

    athlete_medal_count = temp_df['Name'].value_counts().reset_index()
    athlete_medal_count.columns = ['Name', 'Medals']

    merged_df = athlete_medal_count.merge(
        df1[['Name', 'Sport']].drop_duplicates(),
        on='Name',
        how='left'
    )
    top_10 = merged_df.head(10)
    return top_10

def weight_v_height(df1,sport):
    athlete_df = df1.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df1):
    athlete_df = df1.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final
