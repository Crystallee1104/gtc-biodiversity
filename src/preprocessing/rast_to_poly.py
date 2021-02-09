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


def rasterio_poly(input_raster_file, band):
    """
    https://rasterio.readthedocs.io/en/latest/topics/features.html
    :param intput_raster_file: e.g. geotiff.
    :param band: int
    :return: polygon
    """
    import rasterio
    from rasterio import features
    with rasterio.open(input_raster_file) as img:
        blue = img.read(band)
        mask = blue != 255
        shapes = features.shapes(blue, mask=mask, transform=img.transform)
    return shapes


def gdal_poly():
    """
    pip install GDAL
    sudo easy_install GDAL
    https://gdal.org/download.html
    https://trac.osgeo.org/osgeo4w/
    """
    from osgeo import gdal
    gdal.UseExceptions()
    band = dataset.GetRasterBand(1)


def test_all():
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

