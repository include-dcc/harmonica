# Annotate data file with ontology terms, run as: make annotate input_file="data/input/TEST/demo_data.xlsx"
annotate:
	@echo "** Annotate data file with ontology terms using config and input_file: $(input_file)"
	python src/harmonize.py -vv annotate \
		--config config/config.yml \
		--input_file $(input_file) \
		$(if $(refresh),--refresh)
