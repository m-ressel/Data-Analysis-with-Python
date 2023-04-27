import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date')

# Clean data
df = df.loc[(df['value'] >= df['value'].quantile(0.025)) &
            (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(16, 4))
    ax.plot(df.index, df['value'], color='red', linewidth='0.75')

    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    fig.show()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    # changing index into data type
    df_bar.index = pd.to_datetime(df_bar.index)

    # extracting month name
    df_bar['month'] = df_bar.index.month_name()
    # extracting year
    df_bar['year'] = df_bar.index.year

    # Draw bar plot
    # importing calendar to get months' names in order
    import calendar
    hue_order = list(calendar.month_name)[1:]

    fig, ax = plt.subplots(figsize=(6, 8))
    sns.barplot(x='year', y='value', hue='month', hue_order=hue_order, palette=sns.color_palette(), errorbar=None, data=df_bar)
    ax.set(xlabel='Years', ylabel='Average Page Views')
    plt.xticks(rotation=90)
    ax.legend(title="Months", loc='upper left')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box.date = pd.to_datetime(df_box.date)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    sns.boxplot(x='year', y='value', data=df_box, linewidth=0.5, ax=ax1)
    sns.boxplot(x='month', y='value', data=df_box, order=months, linewidth=0.5, ax=ax2)
    ax1.set(xlabel='Year', ylabel='Page Views')
    ax2.set(xlabel='Month', ylabel='Page Views')
    ax1.set_title("Year-wise Box Plot (Trend)")
    ax2.set_title("Month-wise Box Plot (Seasonality)")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
