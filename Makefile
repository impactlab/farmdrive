.PHONY: clean data lint requirements sync_data_to_s3 sync_data_from_s3

#################################################################################
# GLOBALS                                                                       #
#################################################################################

BUCKET = drivendata-farmdrive

#################################################################################
# COMMANDS                                                                      #
#################################################################################

new_env:
	conda env create -f environment.yml

update_env:
	conda env update environment.yml

create_db:
	createdb farmdrive;
	psql -f src/data/create_postgis_db.sql farmdrive

data:
	python src/data/make_dataset.py

clean:
	find . -name "*.pyc" -exec rm {} \;

lint:
	flake8 --exclude=lib/,bin/,docs/conf.py .

sync_data_to_s3:
	aws s3 sync data/ s3://$(BUCKET)/data/

sync_data_from_s3:
	aws s3 sync s3://$(BUCKET)/data/ data/

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################
