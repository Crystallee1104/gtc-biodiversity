import os
import pathlib
import matplotlib.pyplot as plt
import folium
import geopandas as gpd
# import src.constants as cst
# from src.constants import GWS_DATA_DIR

GWS_DATA_DIR = pathlib.Path("/gws/nopw/j04/ai4er/guided-team-challenge/2021/biodiversity")


def get_bio():
    # Getting biotope data
    bio_path = os.path.join(GWS_DATA_DIR, "chernobyl_habitat_data", "Biotope_EUNIS_ver1.shp")
    return gpd.read_file(bio_path)

def get_veg():
    # getting vegetation data
    veg_path = os.path.join(GWS_DATA_DIR, "chernobyl_habitat_data", "Vegetation_mape.shp")
    return gpd.read_file(veg_path)


def plot_together():
    bio_data = get_bio()
    veg_data = get_veg()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    ax1.set_title("bio_data")
    bio_data.plot(ax=ax1)
    ax2.set_title("veg_data")
    veg_data.plot(ax=ax2)
    plt.savefig(os.path.join("report", "figures", "veg_bio_cher.png"))


def get_geoj():
    gj_path = os.path.join(GWS_DATA_DIR, "esa_cci_rois", "esa_cci_2005_chernobyl.geojson")
    file = open(gj_path, 'rt')
    return gpd.read_file(file, encoding='ascii')


def get_merged():
    bio_data = get_bio()
    veg_data = get_veg()
    # This adds a number for each category for color coding
    bio_data['Eunis_name_num'] = bio_data.Eunis_name.astype('category').cat.codes.astype('int64')

    # TODO: fix coordinates to actual location
    m2 = folium.Map([51.386998452, 30.092666296],
                    zoom_start=8,
                    tiles='cartodbpositron')

    # Adding the colored polygons for both datasets
    bio_choropleth = folium.Choropleth(bio_data, data=bio_data, key_on='feature.properties.OBJECTID',
                                    columns=['OBJECTID','Eunis_name_num'], fill_color='YlOrBr', 
                                    name="bio_data")
    bio_choropleth.add_to(m2)
    # Adding the labels
    folium.features.GeoJsonPopup(fields=['Eunis_name'], labels=True ).add_to(bio_choropleth.geojson)

    veg_data['index'] = veg_data.index
    veg_choropleth = folium.Choropleth(veg_data, data=veg_data, key_on='feature.properties.index',
                                    columns=['index','Vegetation'], fill_color='YlOrBr', 
                                    name="veg_data")
    veg_choropleth.add_to(m2)

    # Adding more layers (satellite and openstreetmap)
    folium.TileLayer(tiles='OpenStreetMap').add_to(m2)
    folium.TileLayer(
            tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr = 'Esri',
            name = 'Esri Satellite',
            overlay = False,
            control = True
        ).add_to(m2)

    # Adding a layer control
    folium.LayerControl().add_to(m2)
    # Btw this is probably where EUNIS comes from:
    # https://eunis.eea.europa.eu/
    display("Bio_data", bio_data.head(3))
    display("Veg_data", veg_data.head(3))

    # Get a list of the Eunis labels
    print(bio_data.Eunis_name.unique().tolist())
    #print("Number of polygons:", len(bio_data))

    merged_data = veg_data.merge(bio_data, on='AREA') # validate="one_to_one")
    print(len(merged_data))
    merged_data.head()

    return merged_data

