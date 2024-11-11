import osmium
import geopandas as gpd
import folium
import h3
from geojson import Feature, FeatureCollection
import json
import matplotlib
from red_forest.geometry import node_processor, area_processor, way_processor
from red_forest.geometry.file_processor_interface import FileProcessorInterface


def get_color(custom_cm, val, vmin, vmax):
    return matplotlib.colors.to_hex(custom_cm((val - vmin) / (vmax - vmin)))


class FileProcessor(FileProcessorInterface):

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

    def to_geodata_frame(self) -> gpd.GeoDataFrame:
        if self._is_with_areas:
            return area_processor.AreaProcessor(self._file_processor).to_geo_dataframe()
        elif self._is_with_locations:
            return way_processor.WayProcessor(self._file_processor).to_geo_dataframe()
        else:
            return node_processor.NodeProcessor(self._file_processor).to_geo_dataframe()

    def plot(self, folium_map):
        if self._is_with_areas:
            df = area_processor.AreaProcessor(self._file_processor).to_geo_dataframe()
        elif self._is_with_locations:
            df = way_processor.WayProcessor(self._file_processor).to_geo_dataframe()
        else:
            df = node_processor.NodeProcessor(self._file_processor).to_geo_dataframe()

        folium_geojson = folium.GeoJson(data=df["geometry"].to_json(), style_function=lambda x: self._config)
        folium_geojson.add_to(folium_map)

    def hexagons_dataframe_to_geojson(self, df_hex, file_output=None, column_name="value"):
        """
        Produce the GeoJSON for a dataframe, constructing the geometry from the "hex_id" column
        and with a property matching the one in column_name
        """
        list_features = []

        for i, row in df_hex.iterrows():
            # try:
            geometry_for_row = {"type": "Polygon", "coordinates": [h3.cell_to_boundary(h=row["hex_id"])]}
            feature = Feature(geometry=geometry_for_row,
                              id=row["hex_id"],
                              properties={column_name: row[column_name]})
            list_features.append(feature)
            # except:
            #     print("An exception occurred for hex " + row["hex_id"])

        feat_collection = FeatureCollection(list_features)
        geojson_result = json.dumps(feat_collection)
        return geojson_result

    def hex(self, folium_map, resolution=8):
        gdf = self.to_geodata_frame()
        hex_ids = gdf.apply(lambda row: h3.latlng_to_cell(row.geometry.x, row.geometry.y, resolution), axis=1)
        gdf = gdf.assign(hex_id=hex_ids.values)

        nodes_by_hex_id = gdf.groupby("hex_id", as_index=False).agg({"geometry": "count"})

        geojson_data = self.hexagons_dataframe_to_geojson(nodes_by_hex_id, column_name='geometry')

        min_value = 0
        max_value = nodes_by_hex_id.geometry.max()
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

                    query = ("INSERT INTO table_name (osm_id, name, ref, lon, lat)"
                             "VALUES ({osm_id:n}, \'{name}\', \'{ref}\', {lon}, {lat});\n").format(
                        osm_id=node.id, name=name, ref=ref, lon=node.lon, lat=node.lat)
                    queries.append(query)

        with open(path, "w") as file:
            for query in queries:
                file.write(query)
