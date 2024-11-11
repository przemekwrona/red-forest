import geopandas as gpd
from shapely import Polygon


class AreaProcessor:

    def __init__(self, area_processor):
        self._area_processor = area_processor

    def to_geo_json(self):
        polygons = []
        tag_name = []

        for area in self._area_processor:
            if area.is_area():
                for outer in area.outer_rings():
                    lat_point_list = []
                    lon_point_list = []

                    for n in outer:
                        if n.location.valid():
                            lat_point_list.append(n.lat)
                            lon_point_list.append(n.lon)

                    holes = []

                    for inner in area.inner_rings(outer):
                        lat_point_holes = []
                        lon_point_holes = []

                        for n in inner:
                            if n.location.valid():
                                lat_point_holes.append(n.lat)
                                lon_point_holes.append(n.lon)

                        inner_hole = zip(lon_point_holes, lat_point_holes)
                        holes.append(inner_hole)

                    polygon_geom = Polygon(zip(lon_point_list, lat_point_list), holes)
                    polygons.append(polygon_geom)

                try:
                    tag_name.append(area.tags['name'])
                except KeyError:
                    tag_name.append('')
        data = {
            "tag_name": tag_name
        }

        geometry_series = gpd.GeoSeries(polygons)

        return gpd.GeoDataFrame(data, geometry=geometry_series, crs="EPSG:4326")
