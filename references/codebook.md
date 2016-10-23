# Raw files/directories covered in this codebook

- [`raw/Counties Shapefile`](#rawcounties-shapefile)
- [`raw/Crop Prices`](#rawcrop-prices)
- [`raw/Crop Yield/Admin Level 1 - Crops in Tons.csv`](#rawcrop-yieldadmin-level-1-crops-in-tonscsv)
- [`processed/all_crop_prices.csv`](#processedall_crop_pricescsv)
- [`raw/Elevation Data`](#rawelevation-data)
- [`raw/FAO-AGROECOLOGICAL DATA`](#rawfao-agroecological-data)
- [`raw/Rainfall Data`](#rawrainfall-data)
- [`raw/Socio Economic Data/Census2009`](#)
- [`raw/Socio Economic Data/County Government Expenditure 2013_2014.csv`](#)
- [`raw/Socio Economic Data/DHS/`](#)
- [`raw/Socio Economic Data/FinAccess2016`](#)
- [`raw/Socio Economic Data/KIHBS2005/Final Poverty Estimates All.xls`](#)
- [`raw/Socio Economic Data/KIHBS2005/Proportion_of_Households_Engaged_in_Crop_Farming_by_Region_County_Estimates_-_2005_6.csv`](#)
- [`raw/Socio Economic Data/KIHBS2005/Population_and_Household_Characteristics_County_estimates_2005_6.csv`](#)
- [`raw/Socio Economic Data/KenInfo_2012_en.csv`](#)
- [`raw/Socio Economic Data/Socio Economic data of Kenya, 2011`](#)
- [`raw/Soil Data/SOTWIS_Kenya_ver1.0`](#rawsoil-datasotwis_kenya_ver10)
- [`raw/User Data`](#rawuser-data)
- [`raw/User Data/ward_leve_data.rds`](#rawuser-dataward_leve_datards)
- [`raw/Ward Shapefiles`](#rawward-shapefiles)


## `raw/Counties Shapefile`

| Summary   | -                             |
| --------- | ----------------------------- |
| type      | Shapefile                  |
| time      | N/A |
| geography | Counties                    |
| source    | [ArcGIS user upload](http://www.arcgis.com/home/item.html?id=5f83ca29e5b849b8b05bc0b281ae27bc) |

The 47 counties in Kenya.


## `raw/Crop Prices`

| Summary   | -                             |
| --------- | ----------------------------- |
| type      | Excel files                   |
| time      | Daily 2010-2015; Monthly 2015 |
| geography | See below                     |

This is market prices for various commodities (e.g., Maize, Wheat, Cabbages, etc.). Prices have a geographic region in Kenya associated with them. There may be a way to estimate yield based on price (depending on relationship of supply/demand).

Data appears to come from the Kenyan [National Farmers Information Service](http://www.nafis.go.ke/category/market-info/). Potentially, we could scrape additional date ranges from this site. However, it appears that the Excel files are not available for download--only JPG screenshots of them. Googling for additional xlsx files turns up some links that might be relevant, but as of right now requests are timing out. For example, [www.nafis.go.ke/wp-content/uploads/2012/07/1272012.xls](www.nafis.go.ke/wp-content/uploads/2012/07/1272012.xls) and [http://www.kilimo.go.ke/kilimo_docs/market_prices/](http://www.kilimo.go.ke/kilimo_docs/market_prices/). Potentially could email contact address: MINISTRY OF AGRICULTURE, Market Research and Information, E-mail: marketinfo@kilimo.go.ke or info_amdi@yahoo.com

This raw data is cleaned and aligned into a single csv file: `data/processed/all_crop_prices.csv`

## `processed/all_crop_prices.csv`

This processed file has the following columns:

- [Bungoma](#bungoma)
- [Busia](#busia)
- [Chwele](#chwele)
- [Class](#class)
- [Code](#code)
- [Commodity](#commodity)
- [Eldoret](#eldoret)
- [Embu](#embu)
- [Gakorn](#gakorn)
- [Garissa](#garissa)
- [Gem](#gem)
- [Imenti](#imenti)
- [Imenti North](#imenti north)
- [Imenti South](#imenti south)
- [Isiolo](#isiolo)
- [Kajiado](#kajiado)
- [Kakamega](#kakamega)
- [Kapsowar](#kapsowar)
- [Karatina](#karatina)
- [Kg](#kg)
- [Kibwezi](#kibwezi)
- [Kisii](#kisii)
- [Kisumu](#kisumu)
- [Kitale](#kitale)
- [Kitui](#kitui)
- [Loitokitok](#loitokitok)
- [Machakos](#machakos)
- [Malindi](#malindi)
- [Mandera](#mandera)
- [Marakwet](#marakwet)
- [Marimanti](#marimanti)
- [Mathira](#mathira)
- [Maua](#maua)
- [Meru](#meru)
- [Mombasa](#mombasa)
- [Mwala](#mwala)
- [Mwingi](#mwingi)
- [Nairobi](#nairobi)
- [Nakuru](#nakuru)
- [Nkubu](#nkubu)
- [Nyahururu](#nyahururu)
- [Siaya](#siaya)
- [Tavata](#tavata)
- [Tharaka North](#tharaka north)
- [Tharaka South](#tharaka south)
- [Thika](#thika)
- [Unit](#unit)
- [VARIETY](#variety)
- [Wajir](#wajir)
- [Yala](#yala)
- [date](#date)

#### `Bungoma`

Contains

First 5 non-null values:

```
0   1400.00
1   1000.00
2   4000.00
3   2000.00
6   3400.00
Name: Bungoma, dtype: object
```



#### `Busia`

Contains

First 5 non-null values:

```
0     2430.0
2     4950.0
3     2700.0
10    7200.0
11    6300.0
Name: Busia, dtype: object
```



#### `Chwele`

Contains

First 5 non-null values:

```
0   3200.00
2   5200.00
3   4000.00
6   6000.00
7   5400.00
Name: Chwele, dtype: object
```



#### `Class`

Contains

Unique values in the column:

```
LEGUMES                                     303
CEREAL                                      303
OTHERS                                      303
                                            303
ROOTS & TUBERS                              303
HORTICULTURE                                303
* means the  Commodity is not available.      6
* = Commodity, not available.                 1
Name: Class, dtype: int64
```



#### `Code`

Contains

First 5 non-null values:

```
0   20.00
1   19.00
2   41.00
3   42.00
4   48.00
Name: Code, dtype: float64
```



#### `Commodity`

Contains

First 5 non-null values:

```
0        Dry Maize
1      Green Maize
2    Finger Millet
3          Sorghum
4            Wheat
Name: Commodity, dtype: object
```



#### `Eldoret`

Contains

First 5 non-null values:

```
0    3000.0
1    1620.0
2    6750.0
3    4500.0
4    3300.0
Name: Eldoret, dtype: object
```



#### `Embu`

Contains

First 5 non-null values:

```
0    3000.0
1    2600.0
2    6000.0
3    4000.0
5    6500.0
Name: Embu, dtype: object
```



#### `Gakorn`

Contains

First 5 non-null values:

```
0   2000.00
1   2200.00
2   6500.00
3   1400.00
5   5000.00
Name: Gakorn, dtype: float64
```



#### `Garissa`

Contains

First 5 non-null values:

```
0   4200.00
1   4000.00
2   6400.00
3   5600.00
5   5400.00
Name: Garissa, dtype: float64
```



#### `Gem`

Contains

Unique values in the column:

```
9000.00     4
5600.00     4
4800.00     4
3600.00     4
2600.00     4
800.00      4
10800.00    2
4500.00     2
4400.00     2
3400.00     2
3000.00     2
1200.00     2
650.00      2
Name: Gem, dtype: int64
```



#### `Imenti`

Contains

First 5 non-null values:

```
0    2400.0
1    2600.0
2    8000.0
3    3600.0
4    4000.0
Name: Imenti, dtype: object
```



#### `Imenti North`

Contains

First 5 non-null values:

```
0    2900
1    2700
2    7200
3    3150
4    4000
Name: Imenti North, dtype: object
```



#### `Imenti South`

Contains

Unique values in the column:

```
4500.00    12
2500.00     8
3600.00     4
600.00      4
2300.00     4
8000.00     4
700.00      4
900.00      4
9900.00     2
1200.00     2
300.00      2
650.00      2
1920.00     2
1400.00     2
1800.00     2
2700.00     2
3000.00     2
6300.00     2
250.00      2
Name: Imenti South, dtype: int64
```



#### `Isiolo`

Contains

First 5 non-null values:

```
0   3000.00
1   6000.00
2   9000.00
3   4500.00
4   4500.00
Name: Isiolo, dtype: object
```



#### `Kajiado`

Contains

First 5 non-null values:

```
0    2900.00
5    6500.00
7    6500.00
9    7200.00
14   3200.00
Name: Kajiado, dtype: float64
```



#### `Kakamega`

Contains

First 5 non-null values:

```
0    2800.0
1    2600.0
2    5200.0
3    3200.0
5    8000.0
Name: Kakamega, dtype: object
```



#### `Kapsowar`

Contains

Unique values in the column:

```
6000.00     2
1200.00     2
12000.00    1
4800.00     1
3420.00     1
2800.00     1
1500.00     1
1485.00     1
975.00      1
810.00      1
800.00      1
326.00      1
310.00      1
280.00      1
264.00      1
150.00      1
Name: Kapsowar, dtype: int64
```



#### `Karatina`

Contains

First 5 non-null values:

```
0   3000.00
1   1000.00
2   6500.00
3   5000.00
4   4200.00
Name: Karatina, dtype: float64
```



#### `Kg`

Contains

First 5 non-null values:

```
0    90.00
1   115.00
2    90.00
3    90.00
4    90.00
Name: Kg, dtype: object
```



#### `Kibwezi`

Contains

Unique values in the column:

```
4500.00     6
6500.00     4
7200.00     4
13500.00    2
2500.00     2
650.00      2
1250.00     2
1500.00     2
1800.00     2
1860.00     2
1900.00     2
3400.00     2
2970.00     2
3450.00     2
3500.00     2
3600.00     2
5000.00     2
5400.00     2
6300.00     2
600.00      2
Name: Kibwezi, dtype: int64
```



#### `Kisii`

Contains

First 5 non-null values:

```
0      3600.0
2      6400.0
6      6400.0
13    11400.0
14     4000.0
Name: Kisii, dtype: object
```



#### `Kisumu`

Contains

First 5 non-null values:

```
0    3600.0
1    2400.0
2    7200.0
3    3600.0
5    8200.0
Name: Kisumu, dtype: object
```



#### `Kitale`

Contains

First 5 non-null values:

```
0   2500.00
1   2800.00
2   5400.00
3   3600.00
4   4500.00
Name: Kitale, dtype: object
```



#### `Kitui`

Contains

First 5 non-null values:

```
0    3150.0
1    2500.0
2    7200.0
3    3600.0
5    7200.0
Name: Kitui, dtype: object
```



#### `Loitokitok`

Contains

First 5 non-null values:

```
0     2500.0
1     1500.0
7     4900.0
9     7200.0
14    3000.0
Name: Loitokitok, dtype: object
```



#### `Machakos`

Contains

First 5 non-null values:

```
0    3100.0
1    2600.0
5    5900.0
6    5800.0
7    5500.0
Name: Machakos, dtype: object
```



#### `Malindi`

Contains

First 5 non-null values:

```
0   3420.00
1   3000.00
2   6300.00
3   5400.00
4   5400.00
Name: Malindi, dtype: object
```



#### `Mandera`

Contains

First 5 non-null values:

```
0    3600
3    3000
6    4500
7    4500
8    4500
Name: Mandera, dtype: object
```



#### `Marakwet`

Contains

Unique values in the column:

```
6000.00     2
1200.00     2
12000.00    1
4800.00     1
3420.00     1
2800.00     1
1500.00     1
1485.00     1
1000.00     1
975.00      1
810.00      1
800.00      1
326.00      1
310.00      1
280.00      1
264.00      1
Name: Marakwet, dtype: int64
```



#### `Marimanti`

Contains

First 5 non-null values:

```
0    3200.00
1    1200.00
2   10600.00
3    3000.00
7    6000.00
Name: Marimanti, dtype: float64
```



#### `Mathira`

Contains

First 5 non-null values:

```
0   2000.00
2   4500.00
3   3500.00
6   5000.00
7   4500.00
Name: Mathira, dtype: float64
```



#### `Maua`

Contains

Unique values in the column:

```
1500.00    6
2700.00    6
2600.00    4
4500.00    4
4000.00    4
2500.00    4
8500.00    2
900.00     2
1800.00    2
2200.00    2
3000.00    2
7200.00    2
3600.00    2
5000.00    2
5400.00    2
5700.00    2
600.00     2
Name: Maua, dtype: int64
```



#### `Meru`

Contains

First 5 non-null values:

```
0    1000.0
1    2000.0
2    5800.0
3    2250.0
6    4000.0
Name: Meru, dtype: object
```



#### `Mombasa`

Contains

First 5 non-null values:

```
0    3000.0
1    6200.0
2    8100.0
3    2700.0
6    6300.0
Name: Mombasa, dtype: object
```



#### `Mwala`

Contains

Unique values in the column:

```
5400.00    6
4500.00    6
2800.00    6
2700.00    4
1800.00    4
1400.00    4
1200.00    4
700.00     4
500.00     4
400.00     4
300.00     4
3000.00    2
2500.00    2
450.00     2
350.00     2
250.00     2
Name: Mwala, dtype: int64
```



#### `Mwingi`

Contains

Unique values in the column:

```
6000.00    8
5000.00    8
3000.00    8
2500.00    6
320.00     6
3500.00    6
6400.00    6
3800.00    4
2000.00    4
1750.00    4
1000.00    2
350.00     2
400.00     2
450.00     2
600.00     2
650.00     2
6700.00    2
1500.00    2
2200.00    2
2700.00    2
2800.00    2
3300.00    2
3600.00    2
4500.00    2
300.00     2
Name: Mwingi, dtype: int64
```



#### `Nairobi`

Contains

First 5 non-null values:

```
0    3200.0
1    3500.0
2    6500.0
3    3800.0
5    6500.0
Name: Nairobi, dtype: object
```



#### `Nakuru`

Contains

First 5 non-null values:

```
0    3200.0
1    2000.0
2    6500.0
3    3150.0
4    3150.0
Name: Nakuru, dtype: object
```



#### `Nkubu`

Contains

Unique values in the column:

```
400.00     3
1000.00    3
4500.00    2
900.00     2
8600.00    1
1800.00    1
650.00     1
750.00     1
800.00     1
1750.00    1
2200.00    1
6000.00    1
2400.00    1
2900.00    1
3000.00    1
3800.00    1
4300.00    1
4400.00    1
5300.00    1
250.00     1
Name: Nkubu, dtype: int64
```



#### `Nyahururu`

Contains

First 5 non-null values:

```
0    2700.0
1    1150.0
2    6800.0
3    4800.0
4    3200.0
Name: Nyahururu, dtype: object
```



#### `Siaya`

Contains

Unique values in the column:

```
2000.00    6
2800.00    6
1000.00    4
3000.00    4
2600.00    4
650.00     4
1500.00    4
400.00     2
500.00     2
550.00     2
600.00     2
8800.00    2
6800.00    2
3600.00    2
4200.00    2
6000.00    2
6400.00    2
260.00     2
Name: Siaya, dtype: int64
```



#### `Tavata`

Contains

First 5 non-null values:

```
0    3000.0
1    5500.0
2    5500.0
3    4050.0
4    5500.0
Name: Tavata, dtype: object
```



#### `Tharaka North`

Contains

First 5 non-null values:

```
0    2900.00
1    1800.00
2   10500.00
3    2700.00
7    6100.00
Name: Tharaka North, dtype: float64
```



#### `Tharaka South`

Contains

First 5 non-null values:

```
0   2800.00
2   5850.00
3   5850.00
6   5400.00
8   1800.00
Name: Tharaka South, dtype: float64
```



#### `Thika`

Contains

First 5 non-null values:

```
0    2700.0
1    2200.0
5    5200.0
6    5000.0
7    5000.0
Name: Thika, dtype: object
```



#### `Unit`

Contains

Unique values in the column:

```
Bag          41899
Ext Bag       4362
Lg Box        2908
net           2908
Med Bunch     2908
crate         1454
Dozen         1454
Sm Basket     1454
Tray          1454
Name: Unit, dtype: int64
```



#### `VARIETY`

Contains

Unique values in the column:

```
                  683
LEGUMES           342
CEREAL            342
OTHERS            342
ROOTS & TUBERS    342
HORTICULTURE      342
Name: VARIETY, dtype: int64
```



#### `Wajir`

Contains

Unique values in the column:

```
2400.00    6
2000.00    6
330.00     4
4500.00    4
1800.00    4
400.00     4
3400.00    3
1950.00    3
3600.00    2
2300.00    2
900.00     1
380.00     1
420.00     1
6400.00    1
950.00     1
1600.00    1
3000.00    1
1900.00    1
Name: Wajir, dtype: int64
```



#### `Yala`

Contains

Unique values in the column:

```
3000.00    8
6200.00    4
4500.00    4
2000.00    4
9500.00    2
6000.00    2
4800.00    2
3200.00    2
1300.00    2
1200.00    2
900.00     2
670.00     2
Name: Yala, dtype: int64
```



#### `date`

Contains

First 5 non-null values:

```
0    2014-04-01 00:00:00
1    2014-04-01 00:00:00
2    2014-04-01 00:00:00
3    2014-04-01 00:00:00
4    2014-04-01 00:00:00
Name: date, dtype: object
```

## `raw/Elevation Data`

| Summary   | -                                        |
| --------- | ---------------------------------------- |
| type      | TIF (raster)                             |
| time      | N/A                                      |
| geography | All of Kenya covered by the tiles (not masked to just Kenya). |

This folder was empty except for a link to [SRTM Data](http://srtm.csi.cgiar.org/SELECTION/inputCoord.asp). Downloaded the tiles that cover Kenya:

   | 43 | 44 | 45
 --- | --- | --- | ---
 12 | X | X | X
 13 | X | X | X

Files are of the form `srtm_X_Y/srtm_X_Y.tif`. Values appear to be meters.


## `raw/FAO-AGROECOLOGICAL DATA`

Shapefiles for Agro-ecological zones in Kenya and Africa.


### `raw/FAO-AGROECOLOGICAL DATA/AEZ16_CLAS--SSA.tif`

| Summary   | -             |
| --------- | ------------- |
| type      | TIF           |
| time      | N/A           |
| geography | All of Africa |

Raster of 16 levels of agro-ecological zones in Africa.

### `raw/FAO-AGROECOLOGICAL DATA/aez8_clas--ssa.tif_5`

| Summary   | -             |
| --------- | ------------- |
| type      | TIF           |
| time      | N/A           |
| geography | All of Africa |

Raster of 8 levels of agro-ecological zones in Africa.

### `raw/FAO-AGROECOLOGICAL DATA/Kenya_aezones`

| Summary   | -                                        |
| --------- | ---------------------------------------- |
| type      | Shapefile                                |
| time      | N/A                                      |
| geography | Does not include "non-cultivated" areas. |

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

## `raw/Socio Economic Data/Census2009`

| Summary   | -          |
| --------- | ---------- |
| type      | Excel |
| time      | 2009 |
| geography | Kenya (mostly by district) |
| source | [Kenya Open Data Portal](https://www.opendata.go.ke/) |

Contains files with the questions for:
 - [Household Asset Ownership](https://www.opendata.go.ke/Poverty/Vol-II-q-15-Households-Assets-Ownership/wu73-i6md)
 - [Housing Roofing Material](https://www.opendata.go.ke/Housing-and-Real-Estate/2009-Census-Volume-II-Table-5-Households-by-main-t/qchg-5kp7)
 - [Wall material](https://www.opendata.go.ke/Housing-and-Real-Estate/2009-Census-Volume-II-Table-6-Households-by-main-t/nhkv-ij8n)


## `raw/Socio Economic Data/County Government Expenditure 2013_2014.csv`

| Summary   | -          |
| --------- | ---------- |
| type      | CSV |
| time      | 2103-2014 |
| geography | Kenya (mostly by district) |
| source | [Kenya Open Data Portal( https://data.humdata.org/dataset/county-government-expenditure-2013-2014/resource/45689481-e265-4b51-b6b3-a6abd2c7031e |

Expenditure on different categories by governments.

## `raw/Socio Economic Data/DHS/`

| Summary   | -          |
| --------- | ---------- |
| type      | STATA, SPSS, SAS formats available (we use STATA `.dta`) |
| time      | 1989, 1993, 1998, 2003, 2008-2009, 2014 |
| geography | Kenya (varying levels of geographic resolution)      |
| source | [DHS Program](https://dhsprogram.com/data/dataset_admin/download-datasets.cfm) |

Access to the raw survey data can be requested here:
https://dhsprogram.com/

We have selected the latests DHS data (2014) for inclusion (but other years as listed above are available). The most important variables for our analysis are `HV270` and `HV271`, which is a wealth index estimate.

For complete coverage of this dataset, see the [DHS Recode Manual](http://dhsprogram.com/pubs/pdf/DHSG4/Recode6_DHS_22March2013_DHSG4.pdf).

Note: There is also GPS data available for survey participants. Access to this more sensitive data is pending, but can also be requested through the DHS program site. It is granted separately of the survey data, which has less-fine-grained resolution.

Note: These data formats are painful for modern tools. The most effective route is to use the `read.stata` function in the `foreign` library in R.

## `raw/Socio Economic Data/FinAccess2016`

| Summary   | -          |
| --------- | ---------- |
| type      | Excel |
| time      | 2016 |
| geography | Individuals (w/weights) |
| source | [Kenya Open Data Portal](http://fsdkenya.org/dataset/finaccess-household-2015/) |

Contains its own codebook, but most useful to us are:
 - `a2`: The county
 - `popwgt_normalized`: The normalized population weight
 - `e4_8`: Never used loan/credit product (1 Yes, 2 No)
 - `b11_7`: B11.Over the last year you had to sell some assets in order to repay a loan (Agree, 1; Disagree, 2)		
 - `b11_8`: B11.Over the last year you had to borrow another loan in order to repay a loan (Agree, 1; Disagree, 2)
 - `j8_*`:  J8.How difficult did you find it to repay  Personal loan/business loan from a b [formal loans?]
 - `j14_*`: J14.How difficult did you find it to repay  Personal loan/business loan from a b [informal loans?]


## `raw/Socio Economic Data/KIHBS2005/Final Poverty Estimates All.xls`

| Summary   | -          |
| --------- | ---------- |
| type      | Excel |
| sheetname | `Sublocation` looks most relevant |
| time      | 2005-2006       |
| geography | Kenya (by county, constituency, ward)      |
| source | [Kenya Integrated Household Budget Survey](http://www.knbs.or.ke/index.php?option=com_content&view=article&id=144:kenya-integrated-household-budget-survey-2005-2006&catid=104&Itemid=590). |

Note: Looks like this dataset is [due to be updated this year](http://www.knbs.or.ke/index.php?option=com_phocadownload&view=category&id=129:2015-16-kenya-integrated-household-budget-survey-kihbs&Itemid=1214).

Contains:
 - Poverty incidence by county
 - Poverty gap
 - Gini measure (inequality)
 - Mean Expenditure (up to sublocation)


 ## `raw/Socio Economic Data/KIHBS2005/Proportion_of_Households_Engaged_in_Crop_Farming_by_Region_County_Estimates_-_2005_6.csv`

 | Summary   | -          |
 | --------- | ---------- |
 | type      | CSV |
 | time      | 2005 |
 | geography | By county |
 | source | [Kenya Open Data](https://www.opendata.go.ke/Agriculture/Proportion-of-Households-Engaged-in-Crop-Farming-b/er9s-gbuj) |

County level estimates of the proportion of households engaged in crop farming.


 ## `raw/Socio Economic Data/KIHBS2005/Population_and_Household_Characteristics_County_estimates_2005_6.csv`

 | Summary   | -          |
 | --------- | ---------- |
 | type      | CSV |
 | time      | 2005 |
 | geography | By county |
 | source | [Kenya Open Data](https://www.opendata.go.ke/Population/Population-and-Household-Characteristics-County-es/rbf2-cy4u) |

 Ages, genders, household size, marital status
 2005-2006 estimates by county

 ## `raw/Socio Economic Data/KenInfo_2012_en.csv`

 | Summary   | -          |
 | --------- | ---------- |
 | type      | CSV |
 | time      | 1975 - 2013 (different frequencies for different metrics)       |
 | geography | Kenya (varying levels of geographic resolution)      |
 | source | [KenInfo](http://www.devinfo.org/keninfo/libraries/aspx/home.aspx) |

This contains a number of metrics/indicators at varying geographic resolutions an time scales. Includes things like education, health, poverty.


## `Socio Economic data of Kenya, 2011`

| Summary   | -          |
| --------- | ---------- |
| type      | CSVs |
| time      | 1975 - 2013 (different frequencies for different metrics)       |
| geography | Kenya (varying levels of geographic resolution)      |
| source | [KenInfo](http://www.devinfo.org/keninfo/libraries/aspx/home.aspx) |

Emailed the maintainers of this to get full dataset:
 http://kenya.opendataforafrica.org/SEDK2015/socio-economic-data-of-kenya-2011

Potentially, this is the same data as KenInfo

## `raw/Crop Yield/Admin Level 1 - Crops in Tons.csv`

| Summary   | -          |
| --------- | ---------- |
| type      | CSVs |
| time      | 2005 - 2008 |
| geography | Administrative Level 1 |
| source | [CountryStat](http://www.countrystat.org/home.aspx?c=KEN&ta=114SPD010&tr=21) |

Only at Admin Level 1, 2005-2008. Crop Yield in Tons.


## `raw/Rainfall Data`

| Summary   | -                 |
| --------- | ----------------- |
| type      | TIF               |
| time      | 2012-2015, yearly |
| geography | Worldwide         |

Global rainfall accumulation (Notes say average monthly accumulation) for years 2012-2015. Data is from the NASA TRMM mission. This missions ended and future rainfall collection will [be from TMPA, TMPA-RT, and IMERG](https://pmm.nasa.gov/sites/default/files/document_files/TMPA-to-IMERG_transition.pdf).

Additional data is [available for download](https://pps.gsfc.nasa.gov/register.html#), and getting a higher temporal resolution may be worth exploring.

Files are named `trmm_acc_YYYY.tif`

## `raw/Soil Data/SOTWIS_Kenya_ver1.0`

| Summary   | -          |
| --------- | ---------- |
| type      | Shapefiles |
| time      | N/A        |
| geography | Kenya      |

Soil properties from the [ISRIC Kenya SOTER database](http://www.isric.org/projects/soter-kenya-kensoter). Version 2.0 [is now available for download](http://www.isric.org/data/soil-and-terrain-database-kenya-ver-20-kensoter) so we may consider updating.

Here are the present soil parameters:

- Organic carbon
- Total nitrogen
- Soil reaction (pHH2O)
- Cation exchange capacity (CECsoil)
- Cation exchange capacity of clay size fraction (CECclay) ● ‡
- Base saturation (as % of CECsoil) ‡
- Effective cation exchange capacity (ECEC) † ‡
- Aluminum saturation (as % of ECEC) ‡
- CaCO3 content
- Gypsum content
- Exchangeable sodium percentage (ESP) ‡
- Electrical conductivity of saturated paste (ECe)
- Bulk density
- Coarse fragments (volume %)
- Sand (mass %)
- Silt (mass %)
- Clay (mass %)
- Available water capacity (AWC; from -33 to -1500 kPa; % w/v)


## `raw/User Data`

Data from FarmDrive about their farmers.


### `raw/User Data/tbl_farmer.csv`

| Summary   | -    |
| --------- | ---- |
| type      | CSV  |
| time      | N/A  |
| geography | N/A  |

Raw database table dump for farmers in the FarmDrive system.

- [date_created](#date_created)
- [phone_number](#phone_number)
- [farmer_name](#farmer_name)
- [id_number](#id_number)
- [county](#county)
- [constituency](#constituency)
- [ward](#ward)
- [tocode](#tocode)
- [language_preference](#language_preference)
- [dob](#dob)
- [gender](#gender)
- [marital_status](#marital_status)
- [dependants_number](#dependants_number)
- [sub_location](#sub_location)
- [wards_coded](#wards_coded)

#### `date_created`

Contains

First 5 non-null values:

```
2     2016-05-27 07:58:42.747149+03
8     2016-05-30 13:52:03.299849+03
9      2016-05-31 13:26:33.19348+03
10    2016-06-09 08:59:46.489033+03
11    2016-02-16 11:25:41.941277+03
Name: date_created, dtype: object
```



#### `phone_number`

Contains

First 5 non-null values:

```
2    254714000000.00
8    254717000000.00
9    254728000000.00
10   254714000000.00
11   254728000000.00
Name: phone_number, dtype: float64
```



#### `farmer_name`

Contains

First 5 non-null values:

```
2       Angela De Michele
8        Agathe Blanchard
9            Paris Bosire
10      Benjamin mwasambo
11    FRANCE KAMAU MWAURA
Name: farmer_name, dtype: object
```



#### `id_number`

Contains

First 5 non-null values:

```
2     12345678
8     45678123
9     28229001
10    28279793
11     6819595
Name: id_number, dtype: object
```



#### `county`

Contains

Unique values in the column:

```
Nakuru             106
Kiambu             104
Nyandarua           88
Baringo             50
Uasin Gishu         44
Nyeri                8
Elgeyo/Marakwet      7
Nandi                5
Kericho              4
Embu                 3
Bungoma              3
kiambu               3
Migori               2
Machakos             2
Nairobi              2
KIAMBU               2
nairobi              1
Uansin Gishu         1
tharaka nithi        1
kirinyaga            1
Kisii                1
Mombasa              1
kisumu               1
Nyamira              1
Murang'a             1
Name: county, dtype: int64
```



#### `constituency`

Contains

First 5 non-null values:

```
2     Changamwe
8         Kibra
10       Rongai
11      GATANGA
12       BORABU
Name: constituency, dtype: object
```



#### `ward`

Contains

First 5 non-null values:

```
2       Kipevu
8      Woodley
9       Borabu
10       Visoi
17    kaptagat
Name: ward, dtype: object
```



#### `tocode`

Contains

First 5 non-null values:

```
2     KipevuChangamweMombasa
8        WoodleyKibraNairobi
9                     Borabu
10         VisoiRongaiNakuru
11                   GATANGA
Name: tocode, dtype: object
```



#### `language_preference`

Contains

Unique values in the column:

```
en           920
sw           880
Kiswahili     58
english        7
English        5
ENGLISH        1
Name: language_preference, dtype: int64
```



#### `dob`

Contains

First 5 non-null values:

```
2     1988
8     1995
9     1991
10    1990
11    1963
Name: dob, dtype: object
```



#### `gender`

Contains

Unique values in the column:

```
2    1025
1     846
Name: gender, dtype: int64
```



#### `marital_status`

Contains

Unique values in the column:

```
1    1699
2     156
3      13
4       3
Name: marital_status, dtype: int64
```



#### `dependants_number`

Contains

Unique values in the column:

```
2.00       117
3.00       104
4.00        86
5.00        75
1.00        59
6.00        48
7.00        20
8.00        18
0.00        12
10.00        9
9.00         6
12.00        2
1952.00      1
11.00        1
16.00        1
25.00        1
42.00        1
1940.00      1
1986.00      1
Name: dependants_number, dtype: int64
```



#### `sub_location`

Contains

First 5 non-null values:

```
2         Kaptich
8         Woodley
9         Woodley
10      Chepterit
17    Kokwotendwo
Name: sub_location, dtype: object
```



#### `wards_coded`

Contains

First 5 non-null values:

```
2     PORT REITZ
8     MUGUMU-INI
9         RIGOMA
10         VISOI
11      KILIMANI
Name: wards_coded, dtype: object
```

### `raw/User Data/ward_leve_data.rds`

| Summary   | -    |
| --------- | ---- |
| type      | RDS  |
| time      | N/A  |
| geography | N/A  |

R object file with dataframe that looks like it contains counts of "registrations" for geographies in Kenya.

It's possible that these are voter registrations in Kenya (so can approximate population). Other voter data [seems to be available here](http://www.iebc.or.ke/index.php/2015-01-15-11-10-24/downloads/category/statistics-of-voters). For example, sum of `BARINGO NORTH` rows is ~= to the [voter registrations per Constituency](http://www.iebc.or.ke/index.php/2015-01-15-11-10-24/downloads/item/voters-register-statistics-per-constituency?category_id=56).

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

| Summary   | -          |
| --------- | ---------- |
| type      | Shapefiles |
| time      | N/A        |
| geography | Kenya      |

Geographic boundaries for political units in Kenya.

Contains shapefiles for `ward.results` and `ward.results.formatted`. It looks like `ward.results` is properly projected with WGS84 (4326), so we should favor that one.
