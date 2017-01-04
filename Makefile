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

## Find planet scenes with query in Makefile; write scenes ids to planet_scene_list.txt
planet_search:
	planet search \
		--aoi_id dJ6L8Yp5wgXpogzy \
		-s ortho \
		--where image_statistics_image_quality gte standard \
		--where acquired gte "2016-07-31T04:00:00.000Z" \
		--where acquired lte "2016-09-30T04:00:00.000Z" \
		--where cloud_cover.estimated lte 15 \
		--where image_statistics.gsd gte 1 \
		--where image_statistics.gsd lte 30 \
		--where sat.off_nadir lte 62 \
		--where published gte "2009-01-01T05:00:00.000Z" | jq '.features[].id' > \
		data/interim/planet_scene_list.txt

## Download scenes listed in planet_scene_list.txt
planet_dl:
	xargs -P 12 planet download -d data/raw/planet/nakuru/ {} < data/interim/planet_scene_list.txt

## Run query in makefile and then download the raw data
planet: planet_search planet_dl

## Create county-level geographic features
geo_features:
	runipy notebooks/1.5-pjb-county-geo-features.ipynb

## Create county-level demographic features
demo_features:
	runipy notebooks/1.6-pjb-county-demo-features.ipynb

## Create all county-level features
features: demo_features geo_features

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
