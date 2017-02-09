.PHONY: clean data lint requirements sync_data_to_s3 sync_data_from_s3

#################################################################################
# GLOBALS                                                                       #
#################################################################################

BUCKET = drivendata-client-farmdrive

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Create a new conda environment for the project
new_env:
	conda env create -f environment.yml

## If the environment.yml file has changed, run this to add new dependencies to your environment. Afterwards, script will add additional locally installed packages to environment.yml
update_env:
	conda env update environment.yml;
	conda env export -n farmdrive | grep -v '^prefix' > environment.yml;

## Create an empty postgis database and initialize it
create_db:
	createdb farmdrive;
	psql -f src/data/create_postgis_db.sql farmdrive;
	psql -f src/data/postgis_addons.sql farmdrive;

## Load data into the postgis database and create any other processed data files
data:
	python src/data/make_dataset.py

## Download visual planet data for Maize + Nakuru and resize for InceptionV3
download_planet_maize_nakuru_visual:
	python src/data/download_planet.py Nakuru 'maiz_p--ssa' maize --aoi_selector 5 --resize --asset_type analytic --cloud_cover 0.1 --season summer

## Activate the planet images for Kenya (but don't download yet)
activate_planet_kenya:
	python src/data/download_planet.py Kenya 'maiz_p--ssa' maize --asset_type visual --cloud_cover 0.05 --season summer --activate_only

## Download visual plan data for Maize + full country of kenya and resize for InceptionV3
download_planet_maize_kenya:
	python src/data/download_planet.py Kenya 'maiz_p--ssa' maize --resize --asset_type analytic --cloud_cover 0.05 --season fall

## Collects just the target data for beans, maize, and potatoes from the database
collect_target_data:
	python src/data/download_planet.py Kenya 'bean_p--ssa' beans --collect_crop_yield_only
	python src/data/download_planet.py Kenya 'maiz_p--ssa' maize --collect_crop_yield_only
	python src/data/download_planet.py Kenya 'pota_p--ssa' potato --collect_crop_yield_only

## Trains the model for Nakuru
train_keras_model_nakuru:
	python src/models/train_model.py data/raw/planet/Nakuru/ data/raw/planet/Nakuru/maize_yield.csv test_model.kmodel --n_epoch 10

## Trains a model for all of Kenya
train_keras_model_kenya_maize:
	python src/models/gather_target.py data/raw/planet/Kenya/ data/raw/planet/Kenya/maize_yield.csv geojson_epsg4326_maize.geojson --crop maize;
	python src/models/train_model.py data/raw/planet/Kenya/ data/raw/planet/Kenya/maize_yield.csv --season fall --n_epoch 60 --model VGG16 --asset_type=visual --loss=mean_absolute_error

## Trains a model for all of Kenya
train_keras_model_kenya_beans:
	python src/models/gather_target.py data/raw/planet/Kenya/ data/raw/planet/Kenya/beans_yield.csv geojson_epsg4326_beans.geojson --crop beans;
	python src/models/train_model.py data/raw/planet/Kenya/ data/raw/planet/Kenya/beans_yield.csv --season fall --n_epoch 60 --model VGG16 --asset_type=visual --loss=mean_absolute_error --crop beans

## Trains a model for all of Kenya
train_keras_model_kenya_potato:
	python src/models/gather_target.py data/raw/planet/Kenya/ data/raw/planet/Kenya/potato_yield.csv geojson_epsg4326_potato.geojson --crop potato;
	python src/models/train_model.py data/raw/planet/Kenya/ data/raw/planet/Kenya/potato_yield.csv --season fall --n_epoch 60 --model VGG16 --asset_type=visual --loss=mean_absolute_error --crop potato

## Create county-level geographic features
county_geo_features:
	runipy notebooks/1.5-pjb-county-geo-features.ipynb

## Create county-level demographic features
county_demo_features:
	runipy notebooks/1.6-pjb-county-demo-features.ipynb

## Create all county-level features
county_features: demo_features geo_features

## Remove compiled python files.
clean:
	find . -name "*.pyc" -exec rm {} \;

## Check for flake8 style
lint:
	flake8 --exclude=lib/,bin/,docs/conf.py .

## Push local data folder to S3 bucket for storage + sharing
sync_data_to_s3:
	aws s3 sync data/ s3://$(BUCKET)/data/

## Pull whatever is on S3 down to local storage
sync_data_from_s3:
	aws s3 sync s3://$(BUCKET)/data/ data/

## Sync training images for algorithms to S3
sync_training_data_to_s3:
	aws s3 cp data/raw/planet/Kenya/ s3://drivendata-client-farmdrive/data/processed/training-images/ --exclude "*" --include "*_2*x2*.tif" --recursive

## Sync training images for algorithms from S3
sync_training_data_from_s3:
	aws s3 cp s3://drivendata-client-farmdrive/data/processed/training-images/ data/processed/training-images/ --recursive

## Execute the test suite.
test:
	py.test src

#################################################################################
# Self Documenting Commands                                                                #
#################################################################################

.DEFAULT_GOAL := show-help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: show-help
show-help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) == Darwin && echo '--no-init --raw-control-chars')
