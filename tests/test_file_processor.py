import geopandas as gdf
import geopandas.testing

from unittest import TestCase

from shapely import Point, Polygon, LineString

from red_forest.io.file_processor import FileProcessor


class TestFileProcessor(TestCase):

    def test_export_bus_stops_to_geopandas(self):
        # given
        osm_file = "tests/resources/zalesie.pbf"

        # when
        bus_stops = FileProcessor(osm_file).with_tag(("highway", "bus_stop")).to_geodata_frame()

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

    def test_export_farmlands_to_geopandas(self):
        # given
        osm_file = "tests/resources/zalesie.pbf"

        # when
        farmlands = FileProcessor(osm_file).with_tag(("landuse", "farmland")).with_areas().to_geodata_frame()

        # then
        assert farmlands is not None
        assert len(farmlands) == 5
        geopandas.testing.assert_geodataframe_equal(farmlands, gdf.GeoDataFrame({"tag_name": [
            "", "", "", "", ""]}, geometry=gdf.GeoSeries([
            Polygon([Point(21.0604584, 52.016638), Point(21.0605872, 52.0160471), Point(21.0613009, 52.0161052), Point(21.0612953, 52.0161412),
                     Point(21.0612926, 52.0161758), Point(21.0612443, 52.0164069), Point(21.061188, 52.0166314), Point(21.061173, 52.0167131),
                     Point(21.0604584, 52.016638)]),
            Polygon([Point(21.0244463, 52.0427573), Point(21.0251525, 52.041832), Point(21.0249871, 52.0417846), Point(21.0247851, 52.0417225),
                     Point(21.0251606, 52.0412335), Point(21.025201, 52.0412466), Point(21.025258, 52.0411691), Point(21.0253341, 52.0411728),
                     Point(21.0253602, 52.0411626), Point(21.0254006, 52.0411333), Point(21.0265558, 52.0396764), Point(21.0269955, 52.0391794),
                     Point(21.0271405, 52.039012), Point(21.028557, 52.0371325), Point(21.0285166, 52.0371237), Point(21.0286742, 52.0369102),
                     Point(21.02887, 52.0369637), Point(21.0289666, 52.0368366), Point(21.0291624, 52.0368911), Point(21.0289559, 52.0371732),
                     Point(21.0291517, 52.0372359), Point(21.0289508, 52.0374983), Point(21.0287172, 52.0378035), Point(21.0289197, 52.0378632),
                     Point(21.0287133, 52.0381307), Point(21.0274806, 52.039728), Point(21.0271832, 52.0401165), Point(21.0269927, 52.0400669),
                     Point(21.0247112, 52.0429282), Point(21.0244463, 52.0427573)]),
            Polygon([Point(21.0214992, 52.0408094), Point(21.0220285, 52.0401542), Point(21.0217972, 52.04009), Point(21.0220125, 52.0398116),
                     Point(21.0226306, 52.0390125), Point(21.0231448, 52.0387435), Point(21.0241683, 52.0382671), Point(21.0242432, 52.0383414),
                     Point(21.0223988, 52.0407107), Point(21.0220576, 52.041145), Point(21.0216898, 52.0409333), Point(21.0214992, 52.0408094)]),
            Polygon([Point(21.0245922, 52.0409335), Point(21.0248177, 52.0406389), Point(21.0251542, 52.0407314), Point(21.0254238, 52.0403973),
                     Point(21.0250982, 52.0402829), Point(21.0258643, 52.0392758), Point(21.0260269, 52.0393231), Point(21.0263649, 52.0388627),
                     Point(21.0262898, 52.0388413), Point(21.0262549, 52.0387819), Point(21.026271, 52.0387456), Point(21.0265355, 52.0383576),
                     Point(21.0266063, 52.0382539), Point(21.0268047, 52.0383001), Point(21.0270058, 52.037997), Point(21.0270274, 52.038004),
                     Point(21.0271896, 52.0380469), Point(21.0273251, 52.0378497), Point(21.0274954, 52.0378926), Point(21.027478, 52.0379206),
                     Point(21.0277516, 52.0378645), Point(21.0281577, 52.0373087), Point(21.0284865, 52.0368589), Point(21.0286742, 52.0369102),
                     Point(21.0285166, 52.0371237), Point(21.0271821, 52.0388446), Point(21.0267887, 52.0393351), Point(21.0262397, 52.0399696),
                     Point(21.0253923, 52.0410873), Point(21.0253484, 52.0411202), Point(21.0252866, 52.0411348), Point(21.0249355, 52.041033),
                     Point(21.0245922, 52.0409335)]),
            Polygon([Point(21.0238664, 52.0370363), Point(21.0243544, 52.0363756), Point(21.0249446, 52.0365272), Point(21.0244712, 52.0371971),
                     Point(21.0238664, 52.0370363)])
        ]), crs="EPSG:4326"))

    def test_export_bus_stops(self):
        # given
        osm_file = "tests/resources/zalesie.pbf"

        # when
        highway_secondary = FileProcessor(osm_file).with_tag(("highway", "secondary")).with_locations().to_geodata_frame()

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
