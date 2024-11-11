import osmium
import geopandas
import folium
import h3
from shapely import Point
from shapely.geometry import Polygon, LineString
from geojson import Feature, FeatureCollection
import json
import matplotlib
from red_forest.geometry import builder, node_processor, area_processor, way_processor


def get_color(custom_cm, val, vmin, vmax):
    return matplotlib.colors.to_hex(custom_cm((val - vmin) / (vmax - vmin)))


class FileProcessor:

    def __init__(self, indata):
        self._config = None
        self._file_processor = None
        self._is_with_areas = False
        self._is_with_locations = False

        self._file = indata
        self._file_processor = osmium.FileProcessor(indata)

    def with_key(self, key):
        self._file_processor = self._file_processor.with_filter(osmium.filter.KeyFilter(key))
        return self

    def with_tag(self, tag):
        key, value = tag
        self._file_processor = self._file_processor.with_filter(osmium.filter.TagFilter((key, value)))
        return self

    def with_locations(self):
        self._file_processor = self._file_processor.with_locations()
        self._is_with_locations = True
        return self

    def with_areas(self):
        self._file_processor = self._file_processor.with_areas()
        self._is_with_areas = True
        return self

    def with_config(self, config):
        if config is None:
            config = {}
        self._config = config
        return self

    def append(self, data, folium_map):
        polygon_json = geopandas.GeoSeries(data).to_json()
        folium_geojson = folium.GeoJson(data=polygon_json, style_function=lambda x: self._config)
        folium_geojson.add_to(folium_map)

    def plot(self, folium_map):
        for node in self._file_processor:
            if node.is_area():
                for outer in node.outer_rings():
                    lat_point_list = []
                    lon_point_list = []

                    for n in outer:
                        if n.location.valid():
                            lat_point_list.append(n.lat)
                            lon_point_list.append(n.lon)

                    holes = []

                    for inner in node.inner_rings(outer):
                        lat_point_holes = []
                        lon_point_holes = []

                        for n in inner:
                            if n.location.valid():
                                lat_point_holes.append(n.lat)
                                lon_point_holes.append(n.lon)

                        inner_hole = zip(lon_point_holes, lat_point_holes)
                        holes.append(inner_hole)

                    polygon_geom = Polygon(zip(lon_point_list, lat_point_list), holes)

                    self.append(polygon_geom, folium_map)

            if node.is_way():
                lat_point_list = []
                lon_point_list = []

                for way in node.nodes:
                    if way.location.valid():
                        lat_point_list.append(way.lat)
                        lon_point_list.append(way.lon)

                polygon_way = LineString(zip(lon_point_list, lat_point_list))

                if not polygon_way.is_empty:
                    self.append(polygon_way, folium_map)

            if node.is_node():
                if node.location.valid():
                    folium.Circle(location=[node.lat, node.lon], radius=2, fill=True, color='#3388FF', fillColor='#3388FF').add_to(folium_map)

    def hexagons_dataframe_to_geojson(self, df_hex, file_output=None, column_name="value"):
        """
        Produce the GeoJSON for a dataframe, constructing the geometry from the "hex_id" column
        and with a property matching the one in column_name
        """
        list_features = []

        for i, row in df_hex.iterrows():
            try:
                geometry_for_row = {"type": "Polygon", "coordinates": [h3.cell_to_boundary(h=row["hex_id"])]}
                feature = Feature(geometry=geometry_for_row, id=row["hex_id"], properties={column_name: row[column_name]})
                list_features.append(feature)
            except:
                print("An exception occurred for hex " + row["hex_id"])

        feat_collection = FeatureCollection(list_features)
        geojson_result = json.dumps(feat_collection)
        return geojson_result

    def hex(self, folium_map):
        names = []
        points = []
        for node in self._file_processor:
            if node.is_node():
                if node.location.valid():
                    point = Point(node.lat, node.lon)
                    points.append(point)

        resolution = 8
        gdf = geopandas.GeoDataFrame({'geometry': points}, crs="EPSG:4326")
        hex_ids = gdf.apply(lambda row: h3.latlng_to_cell(row.geometry.y, row.geometry.x, resolution), axis=1)
        gdf = gdf.assign(hex_id=hex_ids.values)

        dataset2001byhexid = gdf.groupby("hex_id", as_index=False).agg({"geometry": "count"})

        geojson_data = self.hexagons_dataframe_to_geojson(dataset2001byhexid, column_name='geometry')

        min_value = 0
        max_value = dataset2001byhexid.geometry.max()
        column_name = 'geometry'
        custom_cm = matplotlib.cm.get_cmap('Blues')

        border_color = 'black'
        fill_opacity = 0.8
        name_layer = "Choropleth "
        folium.GeoJson(
            geojson_data,
            style_function=lambda feature: {
                'fillColor': get_color(custom_cm, feature['properties'][column_name], vmin=min_value, vmax=max_value),
                'color': border_color,
                'weight': 1,
                'fillOpacity': fill_opacity
            },
            name=name_layer
        ).add_to(folium_map)

        print("")

    def hex_area(self, folium_map):
        aaa = []
        for node in self._file_processor:
            if node.is_area():
                polygons = builder.area_to_polygon(node)
                aaa = aaa + polygons
                print("")

            # if node.is_way():
            #     lat_point_list = []
            #     lon_point_list = []
            #
            #     for way in node.nodes:
            #         if way.location.valid():
            #             lat_point_list.append(way.lat)
            #             lon_point_list.append(way.lon)
            #
            #     polygon_way = LineString(zip(lon_point_list, lat_point_list))
            #
            #     if not polygon_way.is_empty:
            #         self.append(polygon_way, folium_map)

            if node.is_node():
                if node.location.valid():
                    folium.Circle(location=[node.lat, node.lon], radius=2, fill=True, color='#3388FF', fillColor='#3388FF').add_to(folium_map)

        print("")

    def to_sql(self, path):
        queries = []
        for node in self._file_processor:
            if node.is_node():
                if node.location.valid():
                    name = ''
                    ref = ''
                    try:
                        ref = node.tags['ref']
                    except KeyError as ref_not_exists:
                        pass

                    try:
                        name = node.tags['name']
                        name = name.replace("'", "''")
                    except KeyError as name_not_exists:
                        pass

                    query = "INSERT INTO table_name (osm_id, name, ref, lon, lat) VALUES ({osm_id:n}, \'{name}\', \'{ref}\', {lon}, {lat});\n".format(
                        osm_id=node.id, name=name, ref=ref, lon=node.lon, lat=node.lat)
                    queries.append(query)

        with open(path, "w") as file:
            for query in queries:
                file.write(query)

    def to_geodata_frame(self):
        if self._is_with_areas:
            return area_processor.AreaProcessor(self._file_processor).to_geo_json()
        elif self._is_with_locations:
            return way_processor.WayProcessor(self._file_processor).to_geo_json()
        else:
            return node_processor.NodeProcessor(self._file_processor).to_geo_json()
