import geopandas as gpd


class FileProcessorInterface:

    def to_geodata_frame(self) -> gpd.GeoDataFrame:
        """Load osm file and convert to geodata frame"""
        pass
