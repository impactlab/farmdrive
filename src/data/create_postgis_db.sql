CREATE EXTENSION postgis;
CREATE EXTENSION postgis_topology;
CREATE EXTENSION fuzzystrmatch;
CREATE EXTENSION postgis_tiger_geocoder;
ALTER DATABASE farmdrive SET postgis.gdal_enabled_drivers TO 'GTiff PNG JPEG';
