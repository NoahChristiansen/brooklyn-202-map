import geopandas as gpd
import pandas as pd
import streamlit as st
from folium.features import GeoJsonPopup, GeoJsonTooltip
import branca
import folium
from streamlit_folium import st_folium

st.set_page_config(layout = 'wide')

st.write("# Brooklyn 202 Map")


@st.cache_resource
def get_df() -> pd.DataFrame:
    gdf = gpd.read_file('merged.geojson')
    return gdf.drop(columns = ['lstmoddate'])


df = get_df()

colormap = branca.colormap.LinearColormap(
    vmin=df["age"].quantile(0.0),
    vmax=df["age"].quantile(1),
    colors=["blue", 'mediumslateblue', "darkorchid",'mediumvioletred', "red"],
    caption="Age of Building",
)

m = folium.Map(location=[40.6602,-73.969749], zoom_start=12, tiles = "CartoDB positron")

popup = GeoJsonPopup(
    fields=['property_name_text', 'age','property_total_unit_count', 'owner_organization_name',
            'SPONSOR', 'Natural Gas Use (kBtu)', 'Electricity Use - Grid Purchase (kWh)','LL84 Total GHG Emissions (MTCO2e)', 'Energy Star Score',
            'Site Energy Unit Intensity (EUI) (kBtu/sqft)'],
    aliases=['Property Name','Building Age', 'Total Unit Count ', 'Owner Organization ',
            'Sponsor', 'Natural Gas Use (kBtu) ', 'Electricity Use - Grid Purchase (kWh) ','LL84 Total GHG Emissions (MTCO2e) ', 'Energy Star Score ',
            'Site Energy Unit Intensity (EUI) (kBtu/sqft) '],
    localize=True,
    labels=True,
    style="background-color: yellow;",
)

tooltip = GeoJsonTooltip(
    fields=['property_name_text', 'age','property_total_unit_count', 'owner_organization_name',
            'SPONSOR', 'Natural Gas Use (kBtu)', 'Electricity Use - Grid Purchase (kWh)','LL84 Total GHG Emissions (MTCO2e)', 'Energy Star Score',
            'Site Energy Unit Intensity (EUI) (kBtu/sqft)'],
    aliases=['Property Name','Building Age', 'Total Unit Count ', 'Owner Organization ',
            'Sponsor', 'Natural Gas Use (kBtu) ', 'Electricity Use - Grid Purchase (kWh) ','LL84 Total GHG Emissions (MTCO2e) ', 'Energy Star Score ',
            'Site Energy Unit Intensity (EUI) (kBtu/sqft) '],
    localize=True,
    sticky=False,
    labels=True,
    style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """,
    max_width=800,
)

folium.GeoJson(
    df,
    style_function=
    lambda x: {
        "fillColor": colormap(x["properties"]["age"])
        if x["properties"]["age"] is not None
        else "transparent",
        # "color": "black",
        'color' : colormap(x["properties"]["age"])
        if x["properties"]["age"] is not None
        else "black",
        # 'opacity':0.4,
        "fillOpacity": 0.4,
    },
    tooltip=tooltip,
    popup=popup,
).add_to(m)

colormap.add_to(m)

output = st_folium(m, width=900, height=500)

st.write('Currently Selected Property:')
if output['last_active_drawing'] is not None:
    st.dataframe(output['last_active_drawing']['properties'],
                 column_config = {'':'Column'},hide_index = True,
                 use_container_width = True)
