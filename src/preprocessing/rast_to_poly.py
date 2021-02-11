"""
Adding examples of raster to polygon functions (probably not working that well).
"""
import os
import numpy as np
import src.constants as cst
import rasterio
import matplotlib.pyplot as plt
from rasterio import features
import geopandas as gpd
from rasterio.features import shapes
from rasterio import plot as rplot
from rasterio.plot import show as rshow
from rasterio.mask import mask as rmask


def arcpy_nonsimplified(workspace, outPolygons, inRaster="zone", field="VALUE"):
    """
    https://desktop.arcgis.com/en/arcmap/10.3/tools/conversion-toolbox/raster-to-polygon.htm
    # conda install -c esri arcgis
    # pip install arcgis 
    :param workspace: path e.g. "C:/data"
    :param workspace: file path e.g. "c:/output/zones.shp"
    :param inRaster:
    :param field:
    """
    import arcpy
    from arcpy import env
    # Set environment settings
    env.workspace = workspace
    # Execute RasterToPolygon
    arcpy.RasterToPolygon_conversion(inRaster, outPolygons, "NO_SIMPLIFY", field)


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


def raster_to_poly(input_tiff_path, output_geojson_path):
    """
    Using rasterio to go from raster to polygon
    but needs a tiff with an input.
    usage: 

    """
    mask = None
    with rasterio.Env():
        with rasterio.open(input_tiff_path) as image:
            image_band_1 = image.read(1) # first band
            results = (
            {'properties': {'raster_val': v}, 'geometry': s}
            for i, (s, v) 
            in enumerate(
                shapes(image_band_1, mask=mask, transform=image.transform)))
    geoms = list(results)
    gpd_polygonized_raster = gpd.GeoDataFrame.from_features(geoms)
    print(gpd_polygonized_raster)
    gpd_polygonized_raster.to_file(output_geojson_path, driver='GeoJSON')


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


def esa_cci_to_geojson(output_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)), "out")):
    for year in range(1992, 2016):
        path = "/gws/nopw/j04/ai4er/guided-team-challenge/2021/biodiversity/esa_cci_rois/esa_cci_" + str(year) + "_chernobyl.tif"
        raster_to_poly(path, os.path.join(output_dir, "esa_cci_" + str(year) + "_chernobyl.geojson"))


def comp_goejsons():
    if True:
        year = 1995
        old_path = "/gws/nopw/j04/ai4er/guided-team-challenge/2021/biodiversity/esa_cci_rois/esa_cci_" + str(year) + "_chernobyl.geojson"
        df_places_old = gpd.read_file(old_path, encoding="utf-8")
        new_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "out", "esa_cci_" + str(year) + "_chernobyl.geojson")
        df_places_new = gpd.read_file(new_path, encoding="utf-8")
        print(df_places_new)
        print(df_places_old)


"""
(/home/users/sithom/gtc-biodiversity/env) [sithom@sci2 gtc-biodiversity]$ python3 main.py 
Traceback (most recent call last):
  File "fiona/_shim.pyx", line 83, in fiona._shim.gdal_open_vector
  File "fiona/_err.pyx", line 291, in fiona._err.exc_wrap_pointer
fiona._err.CPLE_OpenFailedError: '/gws/nopw/j04/ai4er/guided-team-challenge/2021/biodiversity/esa_cci_rois/esa_cci_1995_chernobyl.geojson' not recognized as a supported file format.

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "main.py", line 12, in <module>
    rtp.comp_goejsons()
  File "/home/users/sithom/gtc-biodiversity/src/preprocessing/rast_to_poly.py", line 121, in comp_goejsons
    df_places_old = gpd.read_file(old_path, encoding="utf-8")
  File "/home/users/sithom/gtc-biodiversity/env/lib/python3.8/site-packages/geopandas/io/file.py", line 96, in _read_file
    with reader(path_or_bytes, **kwargs) as features:
  File "/home/users/sithom/gtc-biodiversity/env/lib/python3.8/site-packages/fiona/env.py", line 400, in wrapper
    return f(*args, **kwargs)
  File "/home/users/sithom/gtc-biodiversity/env/lib/python3.8/site-packages/fiona/__init__.py", line 256, in open
    c = Collection(path, mode, driver=driver, encoding=encoding,
  File "/home/users/sithom/gtc-biodiversity/env/lib/python3.8/site-packages/fiona/collection.py", line 162, in __init__
    self.session.start(self, **kwargs)
  File "fiona/ogrext.pyx", line 540, in fiona.ogrext.Session.start
  File "fiona/_shim.pyx", line 90, in fiona._shim.gdal_open_vector
fiona.errors.DriverError: '/gws/nopw/j04/ai4er/guided-team-challenge/2021/biodiversity/esa_cci_rois/esa_cci_1995_chernobyl.geojson' not recognized as a supported file format.
"""
