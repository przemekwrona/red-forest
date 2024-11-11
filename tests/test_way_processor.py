import geopandas as gdf
import geopandas.testing
import osmium

from unittest import TestCase

from shapely import LineString, Point

from red_forest.geometry.way_processor import WayProcessor


class TestWayProcessor(TestCase):

    def test_export_bus_stops(self):
        # given
        osm_file = "tests/resources/zalesie.pbf"
        highway_secondary_processor = osmium.FileProcessor(osm_file).with_filter(osmium.filter.TagFilter(("highway", "secondary"))).with_locations()

        # when
        highway_secondary = WayProcessor(highway_secondary_processor).to_geo_dataframe()

        # then
        assert highway_secondary is not None
        assert len(highway_secondary) == 16
        geopandas.testing.assert_geodataframe_equal(highway_secondary, gdf.GeoDataFrame({"tag_name": [
            "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
        ]}, geometry=gdf.GeoSeries([
            LineString([Point(21.0545134, 52.0282614), Point(21.0541566, 52.0282734)]),
            LineString([Point(21.0541566, 52.0282734), Point(21.0536947, 52.0282442), Point(21.0530545, 52.0281184)]),
            LineString([Point(21.0587718, 52.0280653), Point(21.0580452, 52.0280679), Point(21.057356, 52.0280958), Point(21.0545134, 52.0282614)]),
            LineString([Point(21.0410711, 52.0276339), Point(21.0408221, 52.0275785), Point(21.040646, 52.0275365), Point(21.0405181, 52.0275178)]),
            LineString([Point(21.0672804, 52.0293303), Point(21.0667918, 52.0291829), Point(21.0597498, 52.0281614), Point(21.0592585, 52.028102),
                        Point(21.0587718, 52.0280653)]),
            LineString([Point(21.0463999, 52.0277911), Point(21.043923, 52.027749), Point(21.0433499, 52.0276515)]),
            LineString([Point(21.0405181, 52.0275178), Point(21.0395329, 52.0274695)]),
            LineString([Point(21.0433499, 52.0276515), Point(21.0427958, 52.0275429), Point(21.0426806, 52.0275252), Point(21.0425385, 52.0275156),
                        Point(21.0424007, 52.0275171), Point(21.0422597, 52.0275256), Point(21.0421232, 52.0275398), Point(21.041951, 52.0275656),
                        Point(21.0417508, 52.0276201)]),
            LineString([Point(21.0530545, 52.0281184), Point(21.0525214, 52.0279627), Point(21.0520706, 52.027831), Point(21.0516699, 52.0277334),
                        Point(21.0515227, 52.0277204), Point(21.0512081, 52.0276926), Point(21.0490948, 52.0277683)]),
            LineString([Point(21.0413893, 52.0276728), Point(21.0413236, 52.0276719), Point(21.0412495, 52.0276668), Point(21.0411991, 52.0276604),
                        Point(21.041125, 52.0276461), Point(21.0410711, 52.0276339)]),
            LineString([Point(21.0367355, 52.0273632), Point(21.0364974, 52.0273566), Point(21.0362424, 52.0273496), Point(21.0357605, 52.0273478),
                        Point(21.035401, 52.0273501), Point(21.0350742, 52.0273603), Point(21.0347776, 52.0273851), Point(21.0344325, 52.0274268),
                        Point(21.0329514, 52.0276396), Point(21.0321489, 52.0277575), Point(21.0298604, 52.0281017), Point(21.0296422, 52.0281365)]),
            LineString([Point(21.0395329, 52.0274695), Point(21.0393756, 52.0274619), Point(21.0377636, 52.0274016)]),
            LineString([Point(21.0296422, 52.0281365), Point(21.0295089, 52.0281697), Point(21.0291199, 52.0282762), Point(21.02894, 52.0283266),
                        Point(21.0289027, 52.0283367), Point(21.0257, 52.0292486), Point(21.0255617, 52.0292928), Point(21.0254066, 52.0293469),
                        Point(21.0252025, 52.029433), Point(21.0250083, 52.0295233), Point(21.0243764, 52.0298286), Point(21.023983, 52.0300186),
                        Point(21.0234006, 52.030277), Point(21.0221409, 52.0308073), Point(21.0220054, 52.0308631), Point(21.0219026, 52.0309102),
                        Point(21.0217287, 52.0309962), Point(21.0204936, 52.0316195), Point(21.02014, 52.031798), Point(21.0194319, 52.0321559)]),
            LineString([Point(21.0377636, 52.0274016), Point(21.0370016, 52.027375), Point(21.0367355, 52.0273632)]),
            LineString([Point(21.0417508, 52.0276201), Point(21.0415853, 52.0276537), Point(21.0414816, 52.0276688), Point(21.0413893, 52.0276728)]),
            LineString([Point(21.0490948, 52.0277683), Point(21.0479173, 52.0278017), Point(21.0473416, 52.0278181), Point(21.0463999, 52.0277911)])
        ]), crs="EPSG:4326"))
