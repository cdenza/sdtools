import pandas as pd
import plotly.express as px
import streamlit as st

#Import data from vehicles_us
df = pd.read_csv('vehicles_us.csv')

#Establish other used variables
color_map = {'black':'black',
             'blue':'blue',
             'white':'lightgrey',
             'red':'red',
             'silver':'silver',
             'grey':'grey',
             'other':'yellow'
}
bin_count = 12
# hist_width = 800
# hist_height = 600
replacement_colors = ['yellow', 'orange', 'purple', 'green', 'brown', 'custom']

#Craft Dataframe we will use
colors_df = df.dropna(subset=['paint_color', 'model_year'])
colors_df['model_year'] = colors_df['model_year'].astype(int)
#Translate to correct format
colors_df['days_listed'] = pd.to_timedelta(colors_df['days_listed'], unit='D')
colors_df['date_posted'] = pd.to_datetime(colors_df['date_posted'], format='%Y-%m-%d')
#Add column for date sold
colors_df['date_sold'] = colors_df['date_posted'] + colors_df['days_listed']
#Reduce data
colors_df = colors_df[['model_year', 'paint_color', 'date_posted', 'date_sold']]
#Bundle less popular colors to 'other' category
colors_df['paint_color'] = colors_df['paint_color'].replace(replacement_colors, 'other')

#Histogram to compare colors
st.header('Car Popularity by Color')
# get a list of car colors
colors_list = sorted(colors_df['paint_color'].unique())
# get user's inputs from a dropdown menu
color_1 = st.selectbox(
                              label='Select Color 1', # title of the select box
                              options=colors_list, # options listed in the select box
                              index=colors_list.index('red') # default pre-selected option
                              )
# repeat for the second dropdown menu
color_2 = st.selectbox(
                              label='Select Color 2',
                              options=colors_list, 
                              index=colors_list.index('black')
                              )
# filter the dataframe 
mask_filter = (colors_df['paint_color'] == color_1) | (colors_df['paint_color'] == color_2)
color_df_filtered = colors_df[mask_filter]

# add a checkbox if a user wants to normalize the histogram
normalize = st.checkbox('Normalize histogram', value=True)
if normalize:
    histnorm = 'percent'
else:
    histnorm = None

# create a plotly histogram figure
fig = px.histogram(color_df_filtered,
                      x='date_posted',
                      nbins=bin_count,
                      color='paint_color',
                      histnorm=histnorm,
                      barmode='overlay')
# display the figure with streamlit
st.write(fig)



# Scatter plot
st.header('Car Paint Colors Over The Years')
# Select color to highlight
highlight_color = st.selectbox(
    'Highlight paint color in scatter plot:',
    options=colors_list,
    index=colors_list.index('red')
)

# Adjust opacity based on selected color
#colors_df['opacity'] = colors_df['paint_color'].apply(
#    lambda x: 1.0 if x == highlight_color else 0.1)

# Create scatter plot
fig_scatter = px.scatter(
    colors_df,
    x='date_posted',
    y='model_year',
    color='paint_color',
    # opacity=colors_df['opacity'],
    color_discrete_map=color_map,
    hover_data=['date_sold']
)

st.write(fig_scatter)