import geopandas as gpd
import pandas as pd
import streamlit as st
from folium.features import GeoJsonPopup, GeoJsonTooltip
import branca
import folium
from streamlit_folium import st_folium

st.set_page_config(layout = 'wide')

st.write("# Brooklyn 202 Map")
st.write('* HUD Distressed properties outlined in green')

@st.cache_resource
def get_df() -> pd.DataFrame:
    gdf = gpd.read_file('bk-202s-final-hr.geojson')
    return gdf

df = get_df()

columns_list = ['Property Name', 'property_name_text',
                 'standardized_address',
                 'HUD Distressed?',
                 'BBL',
                 'Community Board', 'Council District',
                 'Borough', 'Neighborhood Tabulation Areas (NTA)',
                 'owner_organization_name', 'Owner-Name 1','Owner-Name 2',
                 'Owner-Mail Recipient Name','Owner-Portfolio Owner or Agent',
                 'Owner-PLUTO','Owner-Corporation Name HDP',
                 'mgmt_agent_org_name', 'mgmt_agent_main_phone_number',
                 'owner_main_phone_number_text', 
                 'property_category_name','primary_financing_type',
                 'Occupancy', 'property_total_unit_count',
                'Building Construction Year','cnstrct_yr','age',
                'num_floors',
                'Gross Floor Area (NYC DOF)', 'self_reported_gross_floor_area',
                'Lien names',
                'Excepted Building Category','Terms of Exception', 
                'List of All Property Use Types at Property',
                'Subject to Compliance Starting in 2024',
                'Energy Grade',       
                'Fuel Oil #1 Use (kBtu)', 'Fuel Oil #2 Use (kBtu)',
                'Fuel Oil #4 Use (kBtu)', 'Fuel Oil #5 & 6 Use (kBtu)',
                'Diesel #2 Use (kBtu)', 'Propane Use (kBtu)', 'Kerosene Use (kBtu)',
                'Natural Gas Use (therms)', 'Natural Gas Use (kBtu)',
                'District Steam Use (kBtu)', 'district_chilledwater_use',
                'Electricity Use - Grid Purchase (kWh)',
                'LL84 Total GHG Emissions (MTCO2e)', 'Energy Star Score',
                'Site Energy Unit Intensity (EUI) (kBtu/sqft)',
                'LL84 Direct GHG Emissions (MTCO2e)',
                'LL84 Indirect GHG Emissions (MTCO2e)',
                'LL97 Total Carbon Emission Threshold 2024_2029',
                'LL97 Total Carbon Emission Threshold 2030_2034',
                'LL97 Total Carbon Emissions (MTCO2e)',
                'LL97 Excess Emissions 2024-2029 (MTCO2e)',
                'LL97 Excess Emissions 2030-2034 (MTCO2e)',
                'LL97 Penalties 2024-2029 (USD)', 'LL97 Penalties 2030-2035 (USD)',
                'geometry']

col1, col2 = st.columns([0.6, 0.4])

with col1:
    colormap = branca.colormap.LinearColormap(
        vmin=df["age"].quantile(0.0),
        vmax=df["age"].quantile(1),
        colors=["blue", 'mediumslateblue', "m",'mediumvioletred', "red"],
        caption="Age of Building",
    )

    m = folium.Map(location=[40.6602,-73.969749], zoom_start=12, tiles = "CartoDB positron")

    popup = GeoJsonPopup(
        fields=['standardized_address','property_name_text', 'age','property_total_unit_count', 'owner_organization_name',
                'Natural Gas Use (kBtu)', 'Electricity Use - Grid Purchase (kWh)','LL84 Total GHG Emissions (MTCO2e)', 'Energy Star Score',
                'Site Energy Unit Intensity (EUI) (kBtu/sqft)', 'HUD Distressed?'],
        aliases=['Address','Property Name','Building Age', 'Total Unit Count ', 'Owner Organization ',
                'Natural Gas Use (kBtu) ', 'Electricity Use - Grid Purchase (kWh) ','LL84 Total GHG Emissions (MTCO2e) ', 'Energy Star Score ',
                'Site Energy Unit Intensity (EUI) (kBtu/sqft) ', 'HUD Distressed?'],
        localize=True,
        labels=True,
        style="background-color: yellow;",
    )

    tooltip = GeoJsonTooltip(
        fields=['standardized_address','property_name_text', 'age','property_total_unit_count', 'owner_organization_name',
                'Natural Gas Use (kBtu)', 'Electricity Use - Grid Purchase (kWh)','LL84 Total GHG Emissions (MTCO2e)', 'Energy Star Score',
                'Site Energy Unit Intensity (EUI) (kBtu/sqft)', 'HUD Distressed?'],
        aliases=['Address','Property Name','Building Age', 'Total Unit Count ', 'Owner Organization ',
                'Natural Gas Use (kBtu) ', 'Electricity Use - Grid Purchase (kWh) ','LL84 Total GHG Emissions (MTCO2e) ', 'Energy Star Score ',
                'Site Energy Unit Intensity (EUI) (kBtu/sqft) ', 'HUD Distressed? '],
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
            'color': 'limegreen' if x["properties"]["HUD Distressed?"] == 'Yes' else (colormap(x["properties"]["age"]) if x["properties"]["age"] is not None else "black"),
            # 'color' : colormap(x["properties"]["age"]) if x["properties"]["age"] is not None else "black",
            # 'opacity':0.4,
            # 'weight': 3 if x["properties"]["HUD Distressed?"] == 'Yes' else 3,
            "opacity": 0.7 if x["properties"]["HUD Distressed?"] == 'Yes' else 1,
            "fillOpacity": 1 if x["properties"]["HUD Distressed?"] == 'Yes' else 0.7,
        },
        tooltip=tooltip,
        popup=popup,
    ).add_to(m)

    colormap.add_to(m)

    output = st_folium(m, width=900, height=600)

with col2:
    st.write('All Building Data')
    st.dataframe(df.drop(columns = ['geometry']), height = 550)
    
    # st.dataframe(df, hide_index = True, use_container_width = True)

if output['last_active_drawing'] is not None:
    st.write('Currently Selected Property:')
    output_df = pd.DataFrame(data = output['last_active_drawing']['properties'],
                                index=[0])
    st.dataframe(output_df[df.drop(columns = ['geometry']).columns],

                #  column_config = {'':'Column'},
                hide_index = True,
                use_container_width = True)

energy_columns = ['Electricity Use - Grid Purchase (kWh)',
                'Fuel Oil #1 Use (kBtu)', 'Fuel Oil #2 Use (kBtu)',
                'Fuel Oil #4 Use (kBtu)', 'Fuel Oil #5 & 6 Use (kBtu)',
                'Diesel #2 Use (kBtu)', 'Propane Use (kBtu)', 'Kerosene Use (kBtu)',
                'Natural Gas Use (therms)', 'Natural Gas Use (kBtu)',
                'District Steam Use (kBtu)', 'district_chilledwater_use',
                'LL84 Total GHG Emissions (MTCO2e)', 'Energy Star Score',
                'Site Energy Unit Intensity (EUI) (kBtu/sqft)',
                'LL84 Direct GHG Emissions (MTCO2e)',
                'LL84 Indirect GHG Emissions (MTCO2e)',
                'LL97 Total Carbon Emission Threshold 2024_2029',
                'LL97 Total Carbon Emission Threshold 2030_2034',
                'LL97 Total Carbon Emissions (MTCO2e)',
                'LL97 Excess Emissions 2024-2029 (MTCO2e)',
                'LL97 Excess Emissions 2030-2034 (MTCO2e)']


metrics = st.selectbox('Select Column to Plot: ',
                            energy_columns,
                            index = 0)
if metrics is not None:
    st.bar_chart(df, x = 'property_name_text', y = metrics )