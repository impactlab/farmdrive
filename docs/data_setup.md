# Pull latest data from S3

-----

    make sync_data_from_s3

# Create Postgres database
 - OSX [`Postgres.app`](http://postgresapp.com/)
 - Ubuntu: `apt-get`

From commandline run:

    $ make create_db

This will create a database in Postgres named `farmdrive` and install the PostGIS extensions.

# Import files into PostGIS

    $ make data

This will load all of the shapefiles and `.tif` raster files into the PostGIS database.

To make sure that your database looks right, you can run the following:

    $ psql farmdrive
    farmdrive=# \dt

Which will output:

    List of relations
    Schema |             Name              | Type  | Owner
    --------+-------------------------------+-------+-------
    public | 2015_07_31_sum                | table | bull
    public | 3b42.20150731.00.7            | table | bull
    public | 3b42.20150731.03.7            | table | bull
    public | 3b42.20150731.06.7            | table | bull
    public | 3b42.20150731.09.7            | table | bull
    public | 3b42.20150731.12.7            | table | bull
    public | 3b42.20150731.15.7            | table | bull
    public | 3b42.20150731.18.7            | table | bull
    public | 3b42.20150731.21.7            | table | bull
    public | aez16_clas--ssa               | table | bull
    public | aez8_clas--ssa                | table | bull
    public | ke_soterunitcomposition       | table | bull
    public | ke_terrainproperties          | table | bull
    public | kenya_aezones                 | table | bull
    public | kenya_wards                   | table | bull
    public | o_10_2015_07_31_sum           | table | bull
    public | o_10_3b42.20150731.00.7       | table | bull
    public | o_10_3b42.20150731.03.7       | table | bull
    public | o_10_3b42.20150731.06.7       | table | bull
    public | o_10_3b42.20150731.09.7       | table | bull
    public | o_10_3b42.20150731.12.7       | table | bull
    public | o_10_3b42.20150731.15.7       | table | bull
    public | o_10_3b42.20150731.18.7       | table | bull
    public | o_10_3b42.20150731.21.7       | table | bull
    public | o_10_aez16_clas--ssa          | table | bull
    public | o_10_aez8_clas--ssa           | table | bull
    public | o_10_kenya_wards              | table | bull
    public | o_10_trmm_acc_2012            | table | bull
    public | o_10_trmm_acc_2013            | table | bull
    public | o_10_trmm_acc_2014            | table | bull
    public | o_10_trmm_acc_2015            | table | bull
    public | o_2_2015_07_31_sum            | table | bull
    public | o_2_3b42.20150731.00.7        | table | bull
    public | o_2_3b42.20150731.03.7        | table | bull
    public | o_2_3b42.20150731.06.7        | table | bull
    public | o_2_3b42.20150731.09.7        | table | bull
    public | o_2_3b42.20150731.12.7        | table | bull
    public | o_2_3b42.20150731.15.7        | table | bull
    public | o_2_3b42.20150731.18.7        | table | bull
    public | o_2_3b42.20150731.21.7        | table | bull
    public | o_2_aez16_clas--ssa           | table | bull
    public | o_2_aez8_clas--ssa            | table | bull
    public | o_2_kenya_wards               | table | bull
    public | o_2_trmm_acc_2012             | table | bull
    public | o_2_trmm_acc_2013             | table | bull
    public | o_2_trmm_acc_2014             | table | bull
    public | o_2_trmm_acc_2015             | table | bull
    public | o_4_2015_07_31_sum            | table | bull
    public | o_4_3b42.20150731.00.7        | table | bull
    public | o_4_3b42.20150731.03.7        | table | bull
    public | o_4_3b42.20150731.06.7        | table | bull
    public | o_4_3b42.20150731.09.7        | table | bull
    public | o_4_3b42.20150731.12.7        | table | bull
    public | o_4_3b42.20150731.15.7        | table | bull
    public | o_4_3b42.20150731.18.7        | table | bull
    public | o_4_3b42.20150731.21.7        | table | bull
    public | o_4_aez16_clas--ssa           | table | bull
    public | o_4_aez8_clas--ssa            | table | bull
    public | o_4_kenya_wards               | table | bull
    public | o_4_trmm_acc_2012             | table | bull
    public | o_4_trmm_acc_2013             | table | bull
    public | o_4_trmm_acc_2014             | table | bull
    public | o_4_trmm_acc_2015             | table | bull
    public | soilparameterestimated_t1s1d1 | table | bull
    public | spatial_ref_sys               | table | bull
    public | trmm_acc_2012                 | table | bull
    public | trmm_acc_2013                 | table | bull
    public | trmm_acc_2014                 | table | bull
    public | trmm_acc_2015                 | table | bull
    public | ward.results                  | table | bull
    public | ward.results.formatted        | table | bull
    tiger  | addr                          | table | bull
    tiger  | addrfeat                      | table | bull
    tiger  | bg                            | table | bull
    tiger  | county                        | table | bull
    tiger  | county_lookup                 | table | bull
    tiger  | countysub_lookup              | table | bull
    tiger  | cousub                        | table | bull
    tiger  | direction_lookup              | table | bull
    tiger  | edges                         | table | bull
    tiger  | faces                         | table | bull
    tiger  | featnames                     | table | bull
    tiger  | geocode_settings              | table | bull
    tiger  | geocode_settings_default      | table | bull
    tiger  | loader_lookuptables           | table | bull
    tiger  | loader_platform               | table | bull
    tiger  | loader_variables              | table | bull
    tiger  | pagc_gaz                      | table | bull
    tiger  | pagc_lex                      | table | bull
    tiger  | pagc_rules                    | table | bull
    tiger  | place                         | table | bull
    tiger  | place_lookup                  | table | bull
    tiger  | secondary_unit_lookup         | table | bull
    tiger  | state                         | table | bull
    tiger  | state_lookup                  | table | bull
    tiger  | street_type_lookup            | table | bull
    tiger  | tabblock                      | table | bull
    tiger  | tract                         | table | bull
    tiger  | zcta5                         | table | bull
    tiger  | zip_lookup                    | table | bull
    tiger  | zip_lookup_all                | table | bull
    tiger  | zip_lookup_base               | table | bull
    tiger  | zip_state                     | table | bull
    tiger  | zip_state_loc                 | table | bull
    (104 rows)
