from osgeo import ogr
import xml.etree.ElementTree as ET
import math

input_xml = "/mnt/e/Develop/Apex/fastest-lap/database/simulations/optimal-lap-ferrari-mexico.xml"
input_track = "/mnt/e/Develop/Apex/fastest-lap/database/tracks/mexico/mexico.xml"
output_kml = "/mnt/e/Develop/Apex/fastest-lap/database/simulations/optimal-lap-ferrari-mexico.kml"

root = ET.parse(input_xml)

x_str = root.find('x').text
y_str = root.find('y').text

x_pos = [float(item) for item in x_str.split(',')]
y_pos = [float(item) for item in y_str.split(',')]

R_earth = 6378388
DEG = math.pi / 180

track_root = ET.parse(input_track)
origin_longitude = float(track_root.find('.//origin_longitude').text)
origin_latitude = float(track_root.find('.//origin_latitude').text)
reference_latitude = float(track_root.find('.//reference_latitude').text)
roll_ref =  reference_latitude * DEG
yaw0 = origin_longitude * DEG
roll0 = origin_latitude * DEG

new_points = []
for x, y in zip(x_pos, y_pos):
  # print(x, y)
  longitude = (x / (R_earth * math.cos(roll_ref))) + yaw0
  latitude = (-y / R_earth) + roll0
  new_points.append((longitude / DEG, latitude / DEG))

ogr.UseExceptions()
kml_driver = ogr.GetDriverByName("KML")
kml_ds = kml_driver.CreateDataSource(output_kml)
kml_layer = kml_ds.CreateLayer("optimal_lap", geom_type=ogr.wkbLineString)

new_geometry = ogr.Geometry(ogr.wkbLineString)
for point in new_points:
  new_geometry.AddPoint(point[0], point[1])

new_feature = ogr.Feature(kml_layer.GetLayerDefn())
new_feature.SetGeometry(new_geometry)
kml_layer.CreateFeature(new_feature)

new_feature = None
shapefile = None
kml_ds = None

print("Done.")