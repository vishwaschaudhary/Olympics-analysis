import numpy as np

def medal_tally(df):
    medal_tally=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    medal_tally=medal_tally.groupby('region').sum()[["Gold","Silver","Bronze"]].sort_values('Gold',ascending=False).reset_index()
    medal_tally['Total']=medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']
    return medal_tally


def country_year_list(df):
    years=df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    country=np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')
    return years, country

def fetch_medal_tally(df,year,country):
    medal_df=df.drop_duplicates(subset=['Team','NOC','Year','City','Sport','Event','Medal'])
    flag=0
    if year=="Overall" and country=="Overall":
        temp_df=medal_df
    if year=="Overall" and country!="Overall":
        flag=1
        temp_df=medal_df[medal_df['region']==country]
    if year!='Overall' and country=='Overall':
        temp_df=medal_df[medal_df['Year']==int(year)]
    if year !='Overall' and country!='Overall':
        temp_df=medal_df[(medal_df['Year']==int(year)) & (medal_df['region']==country)]

    if flag==1:
        x=temp_df.groupby('Year').sum()[["Gold","Silver","Bronze"]].sort_values("Year").reset_index()
    else:
        x=temp_df.groupby('region').sum()[["Gold","Silver","Bronze"]].sort_values('Gold',ascending=False).reset_index()

    x["Total"]=x['Gold']+x["Silver"]+x["Bronze"]

    return x

def data_over_time(df,column):
    nations_over_time=df.drop_duplicates(["Year",column])["Year"].value_counts().reset_index().sort_values("Year")
    nations_over_time.rename(columns={'count':column},inplace=True)
    return nations_over_time

def most_successful(df,sport):
    temp_df=df.dropna(subset=['Medal'])
    if sport!='Overall':
        temp_df=temp_df[temp_df['Sport'] ==sport]

    x=temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='Name',right_on='Name',how='left')[['Name','count','Sport',"region"]].drop_duplicates()
    x.rename(columns={'count':'Total medals',"region":'Country'},inplace=True)
    return x

