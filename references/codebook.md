# Raw files/directories covered in this codebook
  - [link](link): details


## `raw/Crop Yield`

Summary | 
 --- | ---
type | Excel files
time | Daily 2010-2015; Monthly 2015
geography | Nbi, Msa, ksm, Nku, Thika, Kisii C

This isn't really crop yield data, it's market prices for various commodities (e.g., Maize, Wheat, Cabbages, etc.). Prices have a geographic region in Kenya associated with them. There may be a way to estimate yield based on price (depending on relationship of supply/demand).

Data appears to come from the Kenyan [National Farmers Information Service](http://www.nafis.go.ke/category/market-info/). Potentially, we could scrape additional date ranges from this site. However, it appears that the Excel files are not available for download--only JPG screenshots of them. Googling for additional xlsx files turns up some links that might be relevant, but as of right now requests are timing out. For example, [www.nafis.go.ke/wp-content/uploads/2012/07/1272012.xls](www.nafis.go.ke/wp-content/uploads/2012/07/1272012.xls) and [http://www.kilimo.go.ke/kilimo_docs/market_prices/](http://www.kilimo.go.ke/kilimo_docs/market_prices/). Potentially could email contact address: MINISTRY OF AGRICULTURE, Market Research and Information, E-mail: marketinfo@kilimo.go.ke or info_amdi@yahoo.com


## `raw/Elevation Data`

 Summary | 
 --- | ---
type | TIF (raster)
time | N/A
geography | All of Kenya covered by the tiles (not masked to just Kenya).

This folder was empty except for a link to [SRTM Data](http://srtm.csi.cgiar.org/SELECTION/inputCoord.asp). Downloaded the tiles that cover Kenya:

   | 43 | 44 | 45
 --- | --- | --- | ---
 12 | X | X | X
 13 | X | X | X

Files are of the form `srtm_X_Y/srtm_X_Y.tif`. Values appear to be meters.


## `raw/FAO-AGROECOLOGICAL DATA`

Shapefiles for Agro-ecological zones in Kenya and Africa.


### `raw/FAO-AGROECOLOGICAL DATA/AEZ16_CLAS--SSA.tif`

 Summary | 
 --- | ---
type | TIF
time | N/A
geography | All of Africa

Raster of 16 levels of agro-ecological zones in Africa.

### `raw/FAO-AGROECOLOGICAL DATA/aez8_clas--ssa.tif_5`

 Summary | 
 --- | ---
type | TIF
time | N/A
geography | All of Africa

Raster of 8 levels of agro-ecological zones in Africa.

### `raw/FAO-AGROECOLOGICAL DATA/Kenya_aezones`

 Summary | 
 --- | ---
type | Shapefile
time | N/A
geography | Does not include "non-cultivated" areas.

From Kenya_Aez.doc:
> Coverage showing the agro-ecological zones of Kenya based on temperature belts (maximum temperature limits within which the main crops of Kenya can flourish) and the main zones (probability of meeting the temperature and water requirements of the leading crops i.e. the climatic yield potential). Its aim is to provide the framework for ecological land-use potential.
> This coverage does not include information on the non-cultivated (pastoralist) areas. There is, however a grid layer Kenya_LGP_Aez, based on length of growing period done by FAO which has information on the whole country and is available in the database.
> Additional attribute information
> Main zones
> (0) Per humid  (1) Humid  (2) Sub-humid  (3) Semi-humid  (4) Transitional  (5) Semi-arid  (6) Arid  (7) Per arid
> Temperature belts
> (TA) Tropical alpine  (Annual mean temperature, 2-10 degrees)                                                 
> (UH) Upper Highland (Annual mean temperature, 10-15degrees occasional night frost)        
> (LH) Lower Highland (Annual mean temperature, 15-18,M.min 8-11, normal, no frost)
> (UM) Upper midland  (Annual mean temperature, 18-21degrees,M.min 11-14)
> (LM) Lower Midland (Annual mean temperature, 21-24 degrees, M.mean >14degs)
> (IL) Inner Lowland (Annual mean temperature >24 degrees, M.maximum>31 degrees)
> (CL) Coastal Lowland (Annual mean temperature >24, M.maximum <31 degrees)


## `raw/Rainfall Data`

 Summary | 
 --- | ---
type | TIF
time | 2012-2015, yearly
geography | Worldwide

Global rainfall accumulation (Notes say average monthly accumulation) for years 2012-2015. Data is from the NASA TRMM mission. This missions ended and future rainfall collection will [be from TMPA, TMPA-RT, and IMERG](https://pmm.nasa.gov/sites/default/files/document_files/TMPA-to-IMERG_transition.pdf).

Additional data is [available for download](https://pps.gsfc.nasa.gov/register.html#), and getting a higher temporal resolution may be worth exploring.

Files are named `trmm_acc_YYYY.tif`

## `raw/Soil Data/SOTWIS_Kenya_ver1.0`

 Summary | 
 --- | ---
type | Shapefiles
time | N/A
geography | Kenya

Soil properties from the [ISRIC Kenya SOTER database](http://www.isric.org/projects/soter-kenya-kensoter). Version 2.0 [is now available for download](http://www.isric.org/data/soil-and-terrain-database-kenya-ver-20-kensoter) so we may consider updating.


## `raw/User Data`

Data from FarmDrive about their farmers.


### `raw/User Data/tbl_farmer.csv`


### `raw/User Data/user_data.csv`

Same basic data as [`tbl_farmer.csv`](), but with some manual updates to location.


### `raw/User Data/ward_leve_data.rds`

R object file with dataframe that looks like it contains counts of "registrations" for geographies in Kenya.

It's possible that these are voter registrations in Kenya (so can approximate population). Other voter data [seems to be available here](http://www.iebc.or.ke/index.php/2015-01-15-11-10-24/downloads/category/statistics-of-voters). For example, sum of `BARINGO NORTH` rows is ~= to the [voter registrations per Constituency](http://www.iebc.or.ke/index.php/2015-01-15-11-10-24/downloads/item/voters-register-statistics-per-constituency?category_id=56).

**Questions for Elvis:**
 - What is this tracking?

Head of the file:
```
     OBJECTID                         NAME          CONSTITUEN       COUNTY_NAM REGISTERED
0        2853                     BARTABWA       BARINGO NORTH          BARINGO       3855
1        2750                     BARWESSA       BARINGO NORTH          BARINGO       8019
2        2690                   KABARTONJO       BARINGO NORTH          BARINGO       7384
3        2786             SAIMO/KIPSARAMAN       BARINGO NORTH          BARINGO       7911
4        2669                    SAIMO/SOI       BARINGO NORTH          BARINGO       5647
5        2668              EWALEL/CHAPCHAP     BARINGO CENTRAL          BARINGO       6382
```


## `raw/Ward Shapefiles`

Geographic boundaries for political units in Kenya.


Contains shapefiles for `ward.results` and `ward.results.formatted`. It looks like `ward.results` is properly projected with WGS84 (4326), so we should favor that one.