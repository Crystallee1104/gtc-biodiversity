"""
Adding examples of raster to polygon functions (probably not working that well).
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import src.constants as cst
import rasterio
import geopandas as gpd
from rasterio import features
from rasterio.features import shapes
from rasterio import plot as rplot
from rasterio.plot import show as rshow
from rasterio.mask import mask as rmask


def raster_to_poly(input_tif_path, output_geojson_path):
    """
    Using rasterio to go from raster to polygon
    using a tif file as an input.
    input_tif_path: full path and name of input tif file.
    output_geojson_path: full pathe and name of output geojson file.
    """
    mask = None
    with rasterio.Env():
        with rasterio.open(input_tif_path) as image:
            image_band_1 = image.read(1) # first band
            results = (
            {'properties': {'raster_val': v}, 'geometry': s}
            for i, (s, v) 
            in enumerate(
                shapes(image_band_1, mask=mask, transform=image.transform)))
    geoms = list(results)
    gpd_polygonized_raster = gpd.GeoDataFrame.from_features(geoms)
    gpd_polygonized_raster.to_file(output_geojson_path, driver='GeoJSON')


def esa_cci_to_geojson(output_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)), "out")):
    """
    output_dir: path to folder with no trailing slash

    """
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    for year in range(1992, 2016):
        path = "/gws/nopw/j04/ai4er/guided-team-challenge/2021/biodiversity/esa_cci_rois/esa_cci_" + str(year) + "_chernobyl.tif"
        raster_to_poly(path, os.path.join(output_dir, "esa_cci_" + str(year) + "_chernobyl.geojson"))


def test_rast():
    print("testing")
    img = rasterio.open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "in", "cea.tif"))
    print(img)
    print(dir(img))
    print(img.meta)
    array = img.read(1)
    plt.imshow(array, cmap='pink')
    plt.colorbar()
    plt.savefig(os.path.join(os.path.dirname(os.path.realpath(__file__)), "out", "cea.png"))
    plt.clf()
    # https://gis.stackexchange.com/questions/187877/how-to-polygonize-raster-to-shapely-polygons

    mask = None
    with rasterio.Env():
        with rasterio.open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "in", "cea.tif")) as img:
            imag = img.read(1) # first band
            image = (imag // 100).astype('int16')
            plt.imshow(image, cmap='pink')
            plt.colorbar()
            plt.savefig(os.path.join(os.path.dirname(os.path.realpath(__file__)), "out", "cea-blocked.png"))
            plt.clf()
            # print(image[0:100, 5:10])
            results = (
            {'properties': {'raster_val': v}, 'geometry': s}
            for i, (s, v) 
            in enumerate(
                shapes(image, mask=mask, transform=img.transform)))
    geoms = list(results)
    gpd_polygonized_raster = gpd.GeoDataFrame.from_features(geoms)
    gpd_polygonized_raster.to_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), "out", "cea.geojson"), driver='GeoJSON')
    
    # open from geojson, plot, and print.
    df_places = gpd.read_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), "out", "cea.geojson"))
    fig, (ax1) = plt.subplots(1, 1, figsize=(10, 4))
    ax1.set_title("polygonized data")
    df_places.plot(ax=ax1, alpha=0.5, cmap='pink')
    #plt.colorbar()
    plt.savefig(os.path.join(os.path.dirname(os.path.realpath(__file__)), "out", "cea-polygonized.png"))
    print(df_places)
    print(df_places.loc[0])
    print(df_places.loc[1])
    print(dir(df_places.loc[0]))
    print(df_places.loc[0].geometry)
    print(df_places.loc[1].geometry)


def trial_esa_cci():
    for year in range(1992, 2016):
        path = "/gws/nopw/j04/ai4er/guided-team-challenge/2021/biodiversity/esa_cci_rois/esa_cci_" + str(year) + "_chernobyl.tif"
        image = rasterio.open(path)
        print(image)
        rshow(image.read(), transform=image.transform, cmap='pink')
        # plt.colorbar()
        plt.savefig(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                    "out", "esa_cci_" + str(year) + "_chernobyl.png"))
        # takes roughly 1 minute to run:
        raster_to_poly(path, os.path.join(os.path.dirname(os.path.realpath(__file__)),
                       "out", "esa_cci_" + str(year) + "_chernobyl.geojson"))
