import geopandas as gpd
from shapely import LineString


class WayProcessor:

    def __init__(self, way_processor):
        self._way_processor = way_processor

    def to_geo_dataframe(self):
        ways = []
        tag_name = []

        for way in self._way_processor:
            if way.is_way():
                lat_point_list = []
                lon_point_list = []

                for point in way.nodes:
                    if point.location.valid():
                        lat_point_list.append(point.lat)
                        lon_point_list.append(point.lon)

                line_way = LineString(zip(lon_point_list, lat_point_list))

                if not line_way.is_empty:
                    ways.append(line_way)

                    tag_name.append('')

        data = {
            "tag_name": tag_name
        }

        return gpd.GeoDataFrame(data, geometry=gpd.GeoSeries(ways), crs="EPSG:4326")
