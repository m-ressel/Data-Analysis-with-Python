import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column

# Add an overweight column to the data. To determine if a person is overweight,
# first calculate their BMI by dividing their weight in kilograms by the square of their height in meters.
# If that value is > 25 then the person is overweight. Use the value 0 for NOT overweight and the value 1 for overweight.

# I'll use function np.where() that works in the following way:
# np.where(condition, value if condition is true, value if condition is false)

df['overweight'] = np.where(df['weight']/((df['height']/100)**2) > 25, 1, 0)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1,
# make the value 0. If the value is more than 1, make the value 1.

df['cholesterol'] = np.where(df['cholesterol'] == 1, 0, 1)
df['gluc'] = np.where(df['gluc'] == 1, 0, 1)


# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values
    # from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars=['cardio'],
                     value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature.
    # You will have to rename one of the columns for the catplot to work correctly.
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().to_frame(name='total').reset_index()

    # Draw the catplot with 'sns.catplot()'

    graph = sns.catplot(data=df_cat, kind="bar", x="variable", y="total", hue="value", col="cardio")

    # Get the figure for the output
  
    fig = graph.fig
  
    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
# below functions come from here: https://seaborn.pydata.org/examples/many_pairwise_correlations.html

def draw_heat_map():
    # Clean the data
    df_heat = df.loc[(df['ap_lo'] <= df['ap_hi']) &
                     (df['height'] >= df['height'].quantile(0.025)) &
                     (df['height'] <= df['height'].quantile(0.975)) &
                     (df['weight'] >= df['weight'].quantile(0.025)) &
                     (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    # tril would generate a mask for the lower triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(16, 9))

    # Draw the heatmap with 'sns.heatmap()'
    # center - https://www.python-graph-gallery.com/92-control-color-in-seaborn-heatmaps

    sns.heatmap(corr, mask=mask, square=True, linewidths=0.5, fmt='.1f', annot=True, center=0).grid(False)

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
