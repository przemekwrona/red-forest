import geopandas as gpd

from red_forest.geometry.file_processor_interface import FileProcessorInterface


class NodeProcessor(FileProcessorInterface):

    def __init__(self, node_processor):
        self._node_processor = node_processor

    def to_geo_dataframe(self):
        lat = []
        lon = []
        tag_name = []

        for node in self._node_processor:
            if node.is_node() and node.location.valid():
                lat.append(node.lat)
                lon.append(node.lon)

                try:
                    tag_name.append(node.tags['name'])
                except KeyError:
                    tag_name.append('')

        data = {
            "tag_name": tag_name
        }

        geometry_series = gpd.GeoSeries(gpd.points_from_xy(lon, lat))

        return gpd.GeoDataFrame(data, geometry=geometry_series, crs="EPSG:4326")
