import osmium
import geopandas as gpd
import folium
import h3
from geojson import Feature, FeatureCollection
import json
import matplotlib
import os
from red_forest.io import node_processor, area_processor, way_processor
from red_forest.io.file_processor_interface import FileProcessorInterface


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

        if 'fillColor' not in self._config:
            if 'color' in self._config:
                self._config['fillColor'] = self._config['color']

        return self

    def get_processor(self):
        if self._is_with_areas:
            return area_processor.AreaProcessor(self._file_processor)
        elif self._is_with_locations:
            return way_processor.WayProcessor(self._file_processor)
        else:
            return node_processor.NodeProcessor(self._file_processor)

    def to_geodata_frame(self) -> gpd.GeoDataFrame:
        return self.get_processor().to_geo_dataframe()

    def plot(self, folium_map):
        data = self.to_geodata_frame()["geometry"].to_json()
        folium_geojson = folium.GeoJson(data=data, style_function=lambda x: self._config)
        folium_geojson.add_to(folium_map)

    def hexagons_dataframe_to_geojson(self, df_hex, column_name="value"):
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
        nodes_by_hex_id["value"] = nodes_by_hex_id["geometry"]
        geojson_data = self.hexagons_dataframe_to_geojson(nodes_by_hex_id)

        min_value = 0
        max_value = nodes_by_hex_id.geometry.max()
        print(max_value)
        max_value = 150
        column_name = 'value'
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
        with open(path, "w") as file:
            for query in node_processor.NodeProcessor(self._file_processor).to_sql():
                file.write(query)
