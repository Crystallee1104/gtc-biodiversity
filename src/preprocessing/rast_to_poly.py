"""
Adding examples of raster to polygon functions (probably not working that well).
"""


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


def gdal_poly()
    """
    pip install GDAL
    sudo easy_install GDAL
    https://gdal.org/download.html
    https://trac.osgeo.org/osgeo4w/
    """
    from osgeo import gdal
    gdal.UseExceptions()
    band = dataset.GetRasterBand(1)
