import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from pytrends.request import TrendReq

def g_trends(word1, word2):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(kw_list=[word1, word2], timeframe='today 3-m') # see below for options

    # get interest by region
    data = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True)
    data['difference'] = data[word1] - data[word2]

    return data['difference']

word1 = input("Please enter first word: ")
word2 = input("Please enter second word: ")

difference = g_trends(word1, word2)

# world map
world_map = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# dictionary mapping google trends country names to geopandas country names
country_name_mapping = {
    'United States of America': 'United States',
    'Turkey': 'Türkiye',
    'Congo - Brazzaville': 'Congo',
    'Congo - Kinshasa': 'Dem. Rep. Congo',
    'South Sudan': 'S. Sudan',
    'Central African Republic': 'Central African Rep.',
    'Côte d’Ivoire ': 'Côte d\'Ivoire',
    'Eswatini': 'eSwatini',
    'Western Sahara': 'W. Sahara'
}
difference.rename(index=country_name_mapping, inplace=True)
merged = world_map.set_index('name').join(difference)
world_map['name'] = world_map['name'].replace(country_name_mapping)

# merge trends data with the world map
world_map.set_index('name', inplace=True)
world_map = world_map.join(difference)

fig, ax = plt.subplots(1, 1, figsize=(8, 6))
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)

world_map.plot(column='difference', cmap='bwr', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True, cax=cax)

ax.axis('off')

sm = plt.cm.ScalarMappable(cmap='bwr', norm=plt.Normalize(vmin=-100, vmax=100))
sm._A = []
cbar = fig.colorbar(sm, cax=cax, orientation='vertical')

cbar.set_ticks([-100, 0, 100])
cbar.ax.set_yticklabels(['more '+word2, 'equal', 'more '+word1])

box = cbar.ax.get_position()
cbar.ax.set_position([box.x0 - 0.05, box.y0 + box.height * 0.1,
                      box.width, box.height * 0.8])

plt.tight_layout()
plt.show()


# options for time period in line 8
#'now 1-H': past hour
#'now 4-H': past 4 hours
#'now 1-d': past day
#'now 7-d': past 7 days
#'today 1-m': past month
#'today 3-m': past 3 months
#'today 12-m': past year
#'today 5-y': past 5 years
#'all': all available data