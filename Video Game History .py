#!/usr/bin/env python
# coding: utf-8

# ## Video Game History

# Project is identifying patterns to determine if a video game was successful.  This enables early projection for games being released and to market the games correctly.  Data is from 2016.  The open source file conatins information relating to the name of the game, platform releasing the game, year of release, genre, North American sales in USD million, European sales in USD million, sales in Japan in USD million, sales in other countries in USD million, critic score (maximum of 100, user score (maximum of 10), and rating from the Entertainment Software Rating Board.  The rating evaluates a game's content and assigns an age rating such as Teen or Mature.
# 
# The open source file will be loaded into the jupyter notebook.  The data will be prepared by unifying column name print type, converting to appropriate data types, handle missing values, and calculating the total sales for each game. Data will then be analyzed.  Is the data for every time frame of games released significant? which platforms with the greatest total sales per year? Have previously successful platforms become unsuccessful? How long does it generally take for new platforms to appear and old ones to fade?  These questions will enable us to narrow a working time frame to create projections for 2017.  
# 
# Porjections for 2017 will be based on pleatforms with leading sales globally.  An evaluation will be made on how user and professional reviews affect sales for one popular platform (Wii). Analysis will be done using box and scatter plots. Comparisions will be made between the sale of one game on other platforms. Discovery will be made on what is the most 
# profitable genre.  
# 
# A user profile for each region will be made to determine:
# The top five platforms. Describe variations in their market shares from region to region.
# The top five genres. Explain the difference.
# Do ESRB ratings affect sales in individual regions?
# 
# Competency of hypotheses testing will be demonstrated by creating hypotheses in the following area:
# 
# —Average user ratings of the Xbox One and PC platforms are the same. 
# —Average user ratings for the Action and Sports genres are different.
# 
# Exciting conclusions and projections will follow.  

# In[1]:


#import libraries 
import pandas as pd 
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats as st
import plotly.graph_objects as go




# In[2]:


#import csv file 
games = pd.read_csv('/datasets/games.csv')
games.head()


# In[3]:


#make all the column names lowercase
games.columns=games.columns.str.lower()
games.head()


# In[4]:


games.info()


# In[5]:


#convert to approrpiate data type
#year_of_release needs to be date/time
games['year_of_release']=games['year_of_release'].fillna(0).astype('int')

#confirm change 
games.info()
games.head()


# Initially there was 269 rows missing release year.  I chose to fill them in with a year 0.  Then in the future only perform analysis on games where the release score is known.  

# In[6]:


#look for duplicates
games.duplicated().sum()
#there are no duplicates


# In[7]:


#look for empty rows 
games.isna().sum()


# There critic_score and the user_score should not have any value subsituted in.  Each rating would be unique to the game and the platform so there is no way to impune the results. I chose to fill the values in with 0 for each and when performing analysis will filter out rows with the values 0 in these columns.  
# 
# A user review may be empty because the game is new and reviews are not available.  The critic score can be empty because perhaps it was not reviewed or released in an area where there are no critics.  The year of release could be missing as an oversight during data entry. 
# 

# In[8]:


#fill in column for critic_score and user_Score with 0 
games['critic_score']=games['critic_score'].fillna('0')
games['user_score']=games['user_score'].fillna('0')

games.head(20)


# In[9]:


empty_rows = games[games['name'].isna()]
print(empty_rows)


# In[10]:


#the two row missing names is also missing genre information and critic score.  
#this data will be needed later and 2 rows is only 0.000119653% of the data. Decision to drop 
games=games.dropna(subset=['name'])
games.isna().sum()


# In[11]:


#fill in rating empty slots changed to be NA for not available. 
games['rating']=games['rating'].fillna('NA')
games.isna().sum()


# The abbreviation TBD (to be determined) is found in some "user_score" ratings. "User_score" is currently as an object data type.  Plan to convert to integer with coerce to replace NAN into the rows. 

# In[12]:


#convert column data type 
games['user_score'] = pd.to_numeric(games['user_score'], errors='coerce') 
#convert user_score from 1-10 rating to 1-100 to match critic_score
games['user_score'] = games['user_score']*10 
games.head()


# In[13]:


#create new column with sum of sales in all regions 
games['total_sales']=games['na_sales']+games['eu_sales']+games['jp_sales']+games['other_sales']
games.head()


# Analyze the data. 

# In[14]:


#Look at how many games were released in different years. Is the data for every period significant?
#find info about "year_of_release"
print(games['year_of_release'].max())
print(games[games['year_of_release'] != 0]['year_of_release'].min())
print(games['year_of_release'].median())
print(games.info())


# In[15]:


games_per_year=games['year_of_release'].value_counts()
games_per_year.head(20)


# In[16]:


#add visualization for number of games produced per year. 
games_per_year.plot(
kind='bar',
title='Games Produced Per Year',
color='red', 
xlabel='Year', 
ylabel='Number of Games')



# The top ten years for the most games to be released were from 2002-2010. The earliest year for production was 1980 with only 9 games prodcued.  The highest number of games (1427) were released in 2008. The data from 2002-2010 would have more significant data because more user and critic reviews are available due to the popularity of games. 

# In[17]:


#Look at how sales varied from platform to platform. 
top_sales_platforms=games.groupby('platform')['total_sales'].sum().reset_index
top_sales_platforms


# The most popular platform is the PS2 with sales of $1255.77 in USD millions. 

# In[18]:


#Choose the platforms with the greatest total sales and build a distribution based on data for each year. 
# Filter rows where platform is 'PS2'
ps2_sales = games[games['platform'] == 'PS2']

# Group by 'year_of_release' and sum 'total_sales'
ps2_sales_per_year = ps2_sales.groupby('year_of_release')['total_sales'].sum().reset_index()

# Display the result
print(ps2_sales_per_year)


# In[19]:


ps2_sales_per_year.plot(x='year_of_release',y='total_sales',kind='bar',title= 'PS2 Historical Sales Data',xlabel='Release Year',ylabel='Sales (USD millions)')
plt.show()


# In[20]:


#Find platforms that used to be popular but now have zero sales. 
# Group by platform and year, and sum sales
platform_sales_per_year = games.groupby(['platform', 'year_of_release']).agg({'total_sales': 'sum'}).reset_index()
platform_sales_per_year


# In[21]:


# Printed above that the max year in dataset is 2016
recent_years = platform_sales_per_year[platform_sales_per_year['year_of_release'] >= 2015]
#create dataframe to list if there have been no sales in 2016
zero_sales_recently = recent_years[recent_years['total_sales'] == 0]['platform'].unique()


# In[22]:


# Group by platform and find the first and last year with sales
platform_lifespan = platform_sales_per_year.groupby('platform')['year_of_release'].agg(['min', 'max']).reset_index()
platform_lifespan.columns = ['platform', 'First_year', 'Last_year']
#drop all the years where first_year is 0 because unknown 
platform_lifespan = platform_lifespan[platform_lifespan['First_year'] != 0]

print(platform_lifespan)


# In[23]:


# Calculate the lifespan as Last Year minus First Year
platform_lifespan['Lifespan'] = platform_lifespan['Last_year'] - platform_lifespan['First_year']

# Sort platforms by the lifespan
platform_lifespan_sorted = platform_lifespan.sort_values(by='Lifespan', ascending=False)
print(platform_lifespan_sorted)
print(platform_lifespan_sorted.info())
total_lifespan=platform_lifespan_sorted['Lifespan'].mean()
print(total_lifespan)


# In[24]:


#add visualization for platform lifespan. 
platform_lifespan_sorted.plot(
kind='bar',
x='platform',
y='Lifespan',
title='Existance of a Platform',
color='green', 
xlabel='Platform', 
ylabel='Number of Years Existed')


# Lifespan in the video game business fluctuates.  There are 3 companies confirmed for existing for less than a year (GG, PCFX, TG16). On the other side of the spectrum NES had a lifespan of 11 years as a company.  On average the lifespan of a company is under 4 yeaers (3.7 years to be exact). In order to project information for 2017 only information from 2011-2016 will be considered.  This will take into account any newly emerging and dissapearing platforms.  The ones who are dissapearing inform the decision on how to market and build platforms for success. 

# In[25]:


#Which platforms are leading in sales? Which ones are growing or shrinking? Select several potentially profitable platforms.
recent_games = games[(games['year_of_release'] >= 2011) & (games['year_of_release'] <= 2016)]
print(recent_games.head())
#group by platform 
recent_games_sales = recent_games.groupby(['platform', 'year_of_release']).agg({'total_sales': 'sum'}).reset_index()
print(recent_games_sales)


# In[26]:


for platform in recent_games_sales['platform'].unique():
    subset = recent_games_sales[recent_games_sales['platform'] == platform]
    plt.plot(subset['year_of_release'], subset['total_sales'], label=platform, alpha=0.7)

# Adding labels and title
plt.xlabel('Release Year')
plt.ylabel('Total Sales (in USD millions)')
plt.title('Most Recent Platform Sales Performance')
plt.legend(title='Platform')
plt.tight_layout()


# Overall sales seem to be down.  The PS4 and DS platforms were increasing from 2013 to 2015.  However in 2016 they seemed to decrease from their 2015 high.  The PS3, 3DS, and X360 were on a rapid decline.  This most likely is incluenced by the release of the newer systm models (PS4 and DS).  The PSP system was decreasing from 2011 to 2015 and has dissapeared from the list at 2016.  The Wii took a hit when the newer game platform WiiU was released in 2012.  It does appear that the PSV has maintained from 2012 to 2016 a modicum of continues success being above 0 and below 20$ million in sales. 

# In[27]:


#Build a box plot for the global sales of all games, broken down by platform. 
plt.figure(figsize=(14, 8))
sns.boxplot(x='platform', y='total_sales', data=recent_games_sales)

plt.xlabel('Platform', fontsize=12)
plt.ylabel('Global Sales (in USD millions)', fontsize=12)
plt.title('Distribution of Global Sales by Platform', fontsize=16)
plt.xticks(rotation=45)
plt.show()


# Boxplot above shows there is significant differences in sales of each platform.  The PS3 and PS4 have close medians.  The PS3 has a larger range of sales.  The X360 also has a larger range than the PS4 but its median sales are lower. The lower performing platforms under 20 million dollars are DS, PC, PS2, PSP, PSV, Wii, and WiiU. The 3DS and the XOne also has a similiar performance range of sales from ~20-60 million dollars.   

# In[28]:


#Take a look at how user and professional reviews affect sales for X360.  Interested because the range of sales is quite high. 
#use dataframe for filtered within past 5 years to create a dataframe of just X360 information
X360_sales = recent_games[recent_games['platform'] == 'X360']
X360_sales.head()



# In[29]:


#simplify x360 dataframe by grouping according to the name and critic score 
X360_sales_critic = X360_sales.groupby(['name', 'critic_score']).agg({'total_sales': 'sum'}).reset_index()
X360_sales_critic = X360_sales_critic[X360_sales_critic['critic_score'] != 0]
X360_sales_critic.head()


# In[30]:


#create a dataframe grouped by x360 name and user_score
X360_sales_user = X360_sales.groupby(['name', 'user_score']).agg({'total_sales': 'sum'}).reset_index()
#drop any row that has a user_score of 0
X360_sales_user = X360_sales_user[X360_sales_user['user_score'] != 0]
X360_sales_user.head()


# In[31]:


#merge the dataframes on the common name 
x360_reviews=X360_sales_critic.merge(X360_sales_user, on='name')
#check datatypes
x360_reviews.info()
#adjust datatypes to be able to perform calculations
x360_reviews['critic_score']=x360_reviews['critic_score'].astype('int')
x360_reviews['review_difference']=x360_reviews['critic_score']-x360_reviews['user_score']
x360_reviews = x360_reviews[x360_reviews['critic_score'] != 0]

x360_reviews


# In[32]:


x360_reviews['category'] = x360_reviews['review_difference'].apply(lambda x: 'Positive' if x > 0 else 'Negative')
print(x360_reviews.head())
# Count the occurrences of each category
category_counts = x360_reviews['category'].value_counts()

# Create a pie chart
plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#ff9999'])
plt.title('Distribution of Positive vs Negative Differences')
plt.axis('equal')  # Equal aspect ratio ensures that the pie is drawn as a circle.
plt.show()


# Overall it seems that the critics seem to give a higher score to games than users do in their review. 

# In[33]:


#show relationship between sales and positive/negative 
# Group by 'category' and sum the 'total_sales_x'
sales_by_category = x360_reviews.groupby('category')['total_sales_x'].sum().reset_index()
print(sales_by_category.head())
# Create a bar chart
plt.bar(sales_by_category['category'], sales_by_category['total_sales_x'], color=['#66b3ff', '#ff9999'])

# Add labels and title
plt.xlabel('Category')
plt.ylabel('Total Sales')
plt.title('Total Sales by Category')

# Display the chart
plt.show()


# Above bar chart shows that when critics rated a game higher the sales were influenced.  The sales were five times higher when a critic gave a game a good rating.  

# In[34]:


#Build a scatter plot and calculate the correlation between reviews and sales. Draw conclusions.
# Create a scatter plot with critic_score and user_score on x-axis, and total_sales_x on y-axis
plt.figure(figsize=(10, 6))

# Plot for critic_score vs total_sales_x
plt.scatter(x360_reviews['critic_score'], x360_reviews['total_sales_x'], color='blue', label='Critic Score', s=100)

# Plot for user_score vs total_sales_x
plt.scatter(x360_reviews['user_score'], x360_reviews['total_sales_x'], color='red', label='User Score', s=100)

# Add labels and title
plt.xlabel('Score')
plt.ylabel('Total Sales (in USD Millions X)')
plt.title('Review Score Effect on X360 Games Sales')

# Show legend
plt.legend()

# Display the plot
plt.show()


# In general the scatter plot shows that X360 games received higher reviews from critics. Also there were higher financially performing games from positive critic reviews than from user reviews. 

# In[35]:


#Compare the sales of the same games on other platforms.
# Group by title and platform to get total sales for each game-platform combination
games_platform_sales = games.groupby(['name', 'platform'])['total_sales'].sum().reset_index()
# Pivot to compare sales across platforms for the same game
games_sales_pivot = games_platform_sales.pivot(index='name', columns='platform', values='total_sales').fillna(0)

specific_game = "Call of Duty: Black Ops"  
specific_game_sales = games_sales_pivot.loc[specific_game]

# Plot sales across platforms for this specific game
specific_game_sales.plot(kind='bar', figsize=(10, 6))
plt.title(f'Sales of {specific_game} Across Platforms')
plt.xlabel('Platform')
plt.ylabel('Total Sales (in millions)')
plt.show()


# Call of Duty:Black Ops sold best in X360. Perhaps some game features were prioritized for that platform.  The same game barely charted being played on the DS platform. 

# In[36]:


#Take a look at the general distribution of games by genre. 
#What can we say about the most profitable genres? Can you generalize about genres with high and low sales?
genre_sales = games.groupby('genre')['total_sales'].sum().reset_index()
genre_sales.head()


# In[37]:


#Build a box plot for the sales per genre. 
plt.figure(figsize=(14, 8))
sns.boxplot(x='genre', y='total_sales', data=games)
plt.ylim(0,5)
plt.xlabel('Genre', fontsize=12)
plt.ylabel('Total Sales (in USD millions)', fontsize=12)
plt.title('Total Sales per Genre', fontsize=16)
plt.xticks(rotation=45)
plt.show()
#due to outliers limited the y range to 5 million to show distribution for  majority of sales 


# Overall the most successful video game genre is action.  Action games are financially seven times more successful than the least successful type of video game, strategy.  Sports is another highly popular video game genre.  

# Create a user profile for each region (NA, EU, JP) to determine:
# The top five platforms. Describe variations in their market shares from region to region.
# The top five genres. Explain the difference.

# In[38]:


#caclulate total sale per region 
na_sale_total=games['na_sales'].sum()
print(na_sale_total)

eu_sale_total=games['eu_sales'].sum()
print(eu_sale_total)

jp_sale_total=games['jp_sales'].sum()
print(jp_sale_total)


# In[39]:


# Calculate total sales for each platform in each region
na_platform_sales = games.groupby('platform')['na_sales'].sum().sort_values(ascending=False).head(5)
eu_platform_sales = games.groupby('platform')['eu_sales'].sum().sort_values(ascending=False).head(5)
jp_platform_sales = games.groupby('platform')['jp_sales'].sum().sort_values(ascending=False).head(5)
print(na_platform_sales)
# Print top five platforms for each region
print("Top 5 Platforms in North America:")
print(na_platform_sales)

print("Top 5 Platforms in Europe:")
print(eu_platform_sales)

print("Top 5 Platforms in Japan:")
print(jp_platform_sales)


# In[40]:


# Data for each region
platforms_na = ['X360', 'PS2', 'Wii', 'PS3', 'DS']
sales_na = [602.47, 583.84, 496.90, 393.49, 382.40]

platforms_eu = ['PS2', 'PS3', 'X360', 'Wii', 'PS']
sales_eu = [339.29, 330.29, 270.76, 262.21, 213.61]

platforms_jp = ['DS', 'PS', 'PS2', 'SNES', '3DS']
sales_jp = [175.57, 139.82, 139.20, 116.55, 100.67]

# Create a grouped bar chart
fig = go.Figure()

# Add North America sales bars
fig.add_trace(go.Bar(
    x=platforms_na,
    y=sales_na,
    name='North America',
    marker_color='blue'
))

# Add Europe sales bars
fig.add_trace(go.Bar(
    x=platforms_eu,
    y=sales_eu,
    name='Europe',
    marker_color='green'
))

# Add Japan sales bars
fig.add_trace(go.Bar(
    x=platforms_jp,
    y=sales_jp,
    name='Japan',
    marker_color='red'
))

# Update the layout
fig.update_layout(
    title="Top 5 Platform Sales in North America, Europe, and Japan",
    xaxis_title="Platform",
    yaxis_title="Total Sales (in millions)",
    barmode='group',  # Group bars side by side
    legend_title="Region",
    height=500,
    width=800
)

# Show the figure
fig.show()


# In[41]:


# Calculate total sales for each genre in each region
na_genre_sales = games.groupby('genre')['na_sales'].sum().sort_values(ascending=False).head(5)
eu_genre_sales = games.groupby('genre')['eu_sales'].sum().sort_values(ascending=False).head(5)
jp_genre_sales = games.groupby('genre')['jp_sales'].sum().sort_values(ascending=False).head(5)

# Print top five genres for each region
print("Top 5 Genres in North America:")
print(na_genre_sales)

print("Top 5 Genres in Europe:")
print(eu_genre_sales)

print("Top 5 Genres in Japan:")
print(jp_genre_sales)


# Create top genre visualization 

# Regional Profiles:
# North America 
# Top 5 Platformsa:X360,PS2,Wii,PS3,DS. 
# Top 5 Genres: Action, Sports, Shooter, Platform, Misc 
# Total Sale: 4400.570000000001
# 
# 
# Europe 
# Top 5 Platforms:PS2,PS3,X360,Wii,PS. 
# Top 5 Genres: Action, Sports, Shooter, Racing, Misc 
# Total Sale: 2424.1400000000003
# 
# 
# Japan
# Top 5 Platforms:DS, PS, PS2, SNES, 3DS. 
# Top 5 Genres:Role-Playing, Action, Sports, Platform, Misc 
# Total Sale:1297.34
# 
# Overall trend that the North American market for video games is four times as large as Japan.  An interesting note that North America and Europe have the same top 3 genres (Action, Sports, Shooter) while Japan is different.  Role-Playing genre is more popular than Japan than other regions.  Perhaps culturally the value of community is stressed. 

# In[42]:


#Do ESRB ratings affect sales in individual regions?
#look at the top 10 games in each region with their ESRB rating 
na_games = games.groupby('name') ['na_sales'].sum().sort_values(ascending=False).head()
eu_games = games.groupby('name')['eu_sales'].sum().sort_values(ascending=False).head()
jp_games = games.groupby('name')['jp_sales'].sum().sort_values(ascending=False).head()

# Convert from Series to DataFrame to allow for merging
eu_games = eu_games.reset_index()
na_games = na_games.reset_index()
jp_games = jp_games.reset_index()


# Merge 'eu_games' with the 'rating' column from the original 'games' DataFrame
eu_results = pd.merge(eu_games, games[['name', 'rating']], on='name', how='left').drop_duplicates()
na_results = pd.merge(na_games, games[['name', 'rating']], on='name', how='left').drop_duplicates()
jp_results = pd.merge(jp_games, games[['name', 'rating']], on='name', how='left').drop_duplicates()

# Print top games for each region
print("Top Games in North America:")
print(na_results)

print("Top Games in Europe:")
print(eu_results)

print("Top Games in Japan:")
print(jp_results)


# ESRB ratings do not look like they effect sales in Japan or North American.  The majority of their top games do not have a rating available.  Yet these games are part of the top selling games in the region.  The most we can say is that all the games in Europe's top 5 do all have a rating.  The majority of their top five are rated for everyone which we can conclude is more family friendly.  The mature game "Grand Theft Auto V" shows up in both North America and Europes top games. 

# Hypothesis Testing 

# Are average user ratings of the Xbox One and PC platforms are the same?
# Null hypothesis is that the user ratings of Xbox One and PC platforms are different. 
# Alternative hypothesis is that user ratings of the Xbox One and PC platforms are the same
# Alpha threshold value is 0.05 because this demonstrates stastical significance.  

# In[43]:


#remove any 0 present in user_score
#create dataframe to compare
xbox_user_ratings=games[games['platform']=='XOne']
px_user_ratings=games[games['platform']=='PC']
xbox_user_ratings=xbox_user_ratings.dropna()
px_user_ratings=px_user_ratings.dropna()
xbox_user_ratings.head()
px_user_ratings.head()


# In[44]:


alpha=0.05
 
results = st.ttest_ind(xbox_user_ratings['user_score'], px_user_ratings['user_score'])

# test the hypothesis that the means of the two independent populations are equal
print('p-value:', results.pvalue) # your code: print the p-value you get

if results.pvalue<alpha:# your code: compare the p-value you get with the significance level):
    print("We reject the null hypothesis")
else:
    print("We can't reject the null hypothesis")


# Based on the information we can confirm that the user ratings of Xbox One and PC platform are different. 

# Are average user ratings for the Action and Sports genres are different?
# Null hypothesis is that average user ratings for the Action and Sports genres are the same. 
# Alternative hypothesis is average user ratings for the Action and Sports genres are different. 
# Alpha threshold value is 0.05 because this demonstrates stastical significance.   
# 

# In[45]:


#set statistical limit
alpha=0.05

#create dataframes to compare
action_user_ratings=games[games['genre']=='Action']['user_score'].dropna()
sports_user_ratings=games[games['genre']=='Sports']['user_score'].dropna()

#run test hypothesis on equality of two population means 
results=st.ttest_ind(action_user_ratings, sports_user_ratings)

# test the hypothesis that the means of the two independent populations are equal
print('p-value:', results.pvalue) # your code: print the p-value you get

if results.pvalue<alpha:# your code: compare the p-value you get with the significance level):
    print("We reject the null hypothesis")
else:
    print("We can't reject the null hypothesis")
    


# Based on the information we can confirm that the user ratings for action and sports genres are different. 

# General conclusions:
# 
# Video games are a million dollar international business.  New games were released every year from 1980 to 2016 when data was collected.  Business in general seem to be on the decline.  Each company/ platform tends to cycle out after 3.7 years.  The most popular systems at the time of data collection were the PS3 and PS4.  
# 
# In general critics tended to assign games higher ratings than users would  Perhaps partially to help increase sales (which positive views achieved).  Another reason for higher critic reviews would be that the critics have more insight into modifications and improvements made since reviewing a wide variety of games.  Critics also receive games for free to review.  However there were several games that users rated as being below a 20 (in a rating scale up to 100).  
# 
# Games are not created to be played equally across all platforms.  Some are optimized for the user experience in one platform. The game “Call of Duty: Black Ops” sold highest on the PS3 and X360.  
# 
# Users preferred action video games over any other type of video game.  However different regions had their own trends.  The smallest market examined (Japan) preferred role-playing games over any other genre.  These results were achieved independent of ESRB ratings (which were not available for every game). 
# 
# In choosing to design and market a successful game for 2017 this data helps draw some conclusion. To achieve highest financial gain the video game should be action or sports based.  Marketing would be more successful in the North American regions.  Sales in North American as significantly higher than in other regions.  Unknown if this is because of access to platforms, electricity, and disposable income or another reason.  Critics should be sent a free marketing example of the game to evaluate.  If a high rating is achieved this should be mentioned in all marketing material.  Happy creating. 
# 
