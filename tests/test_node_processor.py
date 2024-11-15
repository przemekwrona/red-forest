import geopandas as gdf
import geopandas.testing
import osmium

from unittest import TestCase
from shapely import Point
from red_forest.io.node_processor import NodeProcessor


class TestNodeProcessor(TestCase):

    def test_export_bus_stops(self):
        # given
        osm_file = "tests/resources/zalesie.pbf"
        bus_stops_processor = osmium.FileProcessor(osm_file).with_filter(osmium.filter.TagFilter(("highway", "bus_stop")))

        # when
        bus_stops = NodeProcessor(bus_stops_processor).to_geo_dataframe()

        # then
        assert bus_stops is not None
        assert len(bus_stops) == 9
        geopandas.testing.assert_geodataframe_equal(bus_stops, gdf.GeoDataFrame({"tag_name": [
            "Nowinek 01",
            "Nowinek 02",
            "Leśnych Boginek 01",
            "Leśnych Boginek 02",
            "Wiekowej Sosny 02",
            "Wiekowej Sosny 01",
            "Koralowych Dębów 02",
            "Koralowych Dębów 01",
            "PKP Zalesie Górne 01"
        ]}, geometry=gdf.GeoSeries([
            Point(21.0404921, 52.0159269),
            Point(21.0407004, 52.0167134),
            Point(21.0409347, 52.0218449),
            Point(21.0410585, 52.0219221),
            Point(21.0357502, 52.0274355),
            Point(21.036252, 52.027281),
            Point(21.0289503, 52.0283983),
            Point(21.0290855, 52.0282223),
            Point(21.040026, 52.027063)
        ]), crs="EPSG:4326"))

    def test_export_shelters(self):
        # given
        osm_file = "tests/resources/zalesie.pbf"
        shelter_processor = osmium.FileProcessor(osm_file).with_filter(osmium.filter.TagFilter(("amenity", "shelter")))

        # when
        shelters = NodeProcessor(shelter_processor).to_geo_dataframe()

        # then
        assert shelters is not None
        assert len(shelters) == 5
        geopandas.testing.assert_geodataframe_equal(shelters, gdf.GeoDataFrame({"tag_name": [
            "", "", "", "", ""]}, geometry=gdf.GeoSeries([
            Point(21.0545755, 52.0300074),
            Point(21.0544548, 52.0299827),
            Point(21.054807, 52.0299017),
            Point(21.0547602, 52.0298594),
            Point(21.0549604, 52.0302007)
        ]), crs="EPSG:4326"))

    def test_export_bus_stops(self):
        # given
        osm_file = "tests/resources/zalesie.pbf"
        bus_stops_processor = osmium.FileProcessor(osm_file).with_filter(osmium.filter.TagFilter(("highway", "bus_stop")))

        # when
        bus_stops_sql = NodeProcessor(bus_stops_processor).to_sql()

        # then
        assert bus_stops_sql is not None
        assert len(bus_stops_sql) == 9
        assert bus_stops_sql == ["INSERT INTO table_name (osm_id, name, ref, lon, lat) VALUES (4898111189, 'Nowinek 01', '375701', 21.0404921, 52.0159269);\n",
                                 "INSERT INTO table_name (osm_id, name, ref, lon, lat) VALUES (4898111190, 'Nowinek 02', '375702', 21.0407004, 52.0167134);\n",
                                 "INSERT INTO table_name (osm_id, name, ref, lon, lat) VALUES (11034252516, 'Leśnych Boginek 01', '388301', 21.0409347, 52.0218449);\n",
                                 "INSERT INTO table_name (osm_id, name, ref, lon, lat) VALUES (11034252517, 'Leśnych Boginek 02', '388302', 21.0410585, 52.0219221);\n",
                                 "INSERT INTO table_name (osm_id, name, ref, lon, lat) VALUES (11034252518, 'Wiekowej Sosny 02', '381602', 21.0357502, 52.0274355);\n",
                                 "INSERT INTO table_name (osm_id, name, ref, lon, lat) VALUES (11034252519, 'Wiekowej Sosny 01', '381601', 21.036252, 52.027281);\n",
                                 "INSERT INTO table_name (osm_id, name, ref, lon, lat) VALUES (11034252521, 'Koralowych Dębów 02', '381502', 21.0289503, 52.0283983);\n",
                                 "INSERT INTO table_name (osm_id, name, ref, lon, lat) VALUES (11034252522, 'Koralowych Dębów 01', '381501', 21.0290855, 52.0282223);\n",
                                 "INSERT INTO table_name (osm_id, name, ref, lon, lat) VALUES (12124170351, 'PKP Zalesie Górne 01', '384201', 21.040026, 52.027063);\n"]
