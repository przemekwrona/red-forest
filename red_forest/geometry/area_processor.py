import geopandas as gpd
from shapely import Polygon

from red_forest.geometry.file_processor_interface import FileProcessorInterface


class AreaProcessor(FileProcessorInterface):

    def __init__(self, area_processor):
        self._area_processor = area_processor

    def to_geo_dataframe(self) -> gpd.GeoDataFrame:
        polygons = []
        tag_name = []

        for area in self._area_processor:
            if area.is_area():
                for outer_ring in area.outer_rings():
                    lat_polygon_points = []
                    lon_polygon_points = []

                    for outer_point in outer_ring:
                        if outer_point.location.valid():
                            lat_polygon_points.append(outer_point.lat)
                            lon_polygon_points.append(outer_point.lon)

                    holes = []

                    for inner_ring in area.inner_rings(outer_ring):
                        lat_point_holes = []
                        lon_point_holes = []

                        for inner_point in inner_ring:
                            if inner_point.location.valid():
                                lat_point_holes.append(inner_point.lat)
                                lon_point_holes.append(inner_point.lon)

                        holes.append(zip(lon_point_holes, lat_point_holes))

                    polygons.append(Polygon(zip(lon_polygon_points, lat_polygon_points), holes))

                try:
                    tag_name.append(area.tags['name'])
                except KeyError:
                    tag_name.append('')
        data = {
            "tag_name": tag_name
        }

        geometry_series = gpd.GeoSeries(polygons)

        return gpd.GeoDataFrame(data, geometry=geometry_series, crs="EPSG:4326")
