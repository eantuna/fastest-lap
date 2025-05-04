from osgeo import ogr
import xml.etree.ElementTree as ET
import math

input_xml = "/mnt/c/Users/antun/Develop/Apex/fastest-lap/database/simulations/optimal-lap-ferrari-las-vegas.xml"
output_kml = "/mnt/c/Users/antun/Develop/Apex/fastest-lap/database/simulations/optimal-lap-ferrari-las-vegas.kml"

root = ET.parse(input_xml)

x_str = root.find('x').text
y_str = root.find('y').text

x_pos = [float(item) for item in x_str.split(',')]
y_pos = [float(item) for item in y_str.split(',')]

R_earth = 6378388
DEG = math.pi / 180

# To-Do: Get this from XML
roll_ref = 36.108264955698097 * DEG
yaw0 = -115.16289039649 * DEG
roll0 = 36.108264955698097 * DEG

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