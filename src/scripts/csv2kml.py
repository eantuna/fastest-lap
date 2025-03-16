from osgeo import ogr
import csv

input_csv = "/Users/edgardoantuna/Develop/F1/FastestLap/fastest-lap/src/test/cli/centerline-coords-mia-GREAT.csv"
output_kml = "/Users/edgardoantuna/Develop/F1/FastestLap/fastest-lap/data/kml/mia-centerline-output-GREAT.kml"

ogr.UseExceptions()
kml_driver = ogr.GetDriverByName('KML')
kml_ds = kml_driver.CreateDataSource(output_kml)
kml_layer = kml_ds.CreateLayer("catalunya_centerline", geom_type=ogr.wkbLineString)

new_points = []
# Open the CSV file
with open(input_csv, mode='r', newline='') as file:
    # Create a CSV reader object
    csv_reader = csv.DictReader(file)
    # Loop through the remaining rows of the CSV file
    for row in csv_reader:
      print(row)
      # new_points.append((row['longitude'], row['latitude'], 0.0))
      lon = float(row['longitude'])
      lat = float(row['latitude'])
      new_points.append((lon, lat, 0))

new_geometry = ogr.Geometry(ogr.wkbLineString)
for point in new_points:
  new_geometry.AddPoint(point[0], point[1], point[2])

new_feature = ogr.Feature(kml_layer.GetLayerDefn())
# new_feature.SetFrom(feature)
new_feature.SetGeometry(new_geometry)
kml_layer.CreateFeature(new_feature)

new_feature = None
shapefile = None
kml_ds = None

print("Done.")