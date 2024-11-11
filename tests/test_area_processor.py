import geopandas as gdf
import geopandas.testing
from unittest import TestCase
import osmium
from shapely import Point, Polygon

from red_forest.geometry.area_processor import AreaProcessor


class TestAreaProcessor(TestCase):

    def test_export_farmlands(self):
        # given
        osm_file = "resources/zalesie.pbf"
        farmland_processor = osmium.FileProcessor(osm_file).with_filter(osmium.filter.TagFilter(("landuse", "farmland"))).with_areas()

        # when
        farmlands = AreaProcessor(farmland_processor).to_geo_json()

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
                     Point(21.0238664, 52.0370363)])]), crs="EPSG:4326"))

    def test_export_railway_platforms(self):
        # given
        osm_file = "resources/zalesie.pbf"
        railway_platform_processor = osmium.FileProcessor(osm_file).with_filter(osmium.filter.TagFilter(("railway", "platform"))).with_areas()

        # when
        railway_platform = AreaProcessor(railway_platform_processor).to_geo_json()

        # then
        assert railway_platform is not None
        assert len(railway_platform) == 2
        geopandas.testing.assert_geodataframe_equal(railway_platform, gdf.GeoDataFrame({"tag_name": [
            "peron 2", "peron 1"]}, geometry=gdf.GeoSeries([
            Polygon([Point(21.0413172, 52.0273758), Point(21.0423556, 52.0256946), Point(21.0423982, 52.0257043), Point(21.0424421, 52.025714),
                     Point(21.0413963, 52.027394), Point(21.0413635, 52.0273871), Point(21.0413172, 52.0273758), Point(21.0414026, 52.0272564),
                     Point(21.0414676, 52.0272713), Point(21.0416721, 52.0269345), Point(21.0416071, 52.0269195), Point(21.0414026, 52.0272564)]),
            Polygon([Point(21.0411369, 52.0273341), Point(21.0421713, 52.0256542), Point(21.0422029, 52.0256615), Point(21.0422513, 52.0256727),
                     Point(21.041216, 52.0273517), Point(21.0411704, 52.0273419), Point(21.0411369, 52.0273341), Point(21.041222, 52.0272118),
                     Point(21.0412869, 52.0272267), Point(21.0414914, 52.0268898), Point(21.0414265, 52.0268749), Point(21.041222, 52.0272118)])]),
            crs="EPSG:4326"))
