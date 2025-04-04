# Harmonica
Harmonize data to ontology terms.

## Prerequisites
The prerequisites to run the script can either be installed using the `requirements.txt` file if using pyenv or `environment.yml` file if using conda.

### Commands
`pip install -r requirements.txt`
 
 Or

 `conda env create -f environment.yml`


## Usage
### Python
`python src/harmonize.py -vv search --oid "mondo,hp" --data_filename "TEST/demo_data.xlsx"`

### Make
`make search oid="mondo,hp" data_filename="demo_data.xlsx"`

_NOTE: Do not include any spaces when passing multiple ontology identifiers (oid)._


## Ontology SQLite Database
Using `get_adapter(f"sqlite:obo:{ontology_id}")` the ontology database is saved at `~/.data/oaklib/`.

NOTE: This method downloads a version of an ontolgy from an AWS S3 bucket (https://s3.amazonaws.com/bbop-sqlite) managed by the OAK developers (https://github.com/INCATools/ontology-access-kit). Only one version of an ontology is present in the S3 bucket.

Since OAK does not have a mechanism to automatically update the local cached ontology database (saved to `~/.data/oaklib/`), a custom method was added to harmonica. This gets the release date from the cached ontology database(s) and displays these to the user with a prompt asking whether to use these cached versions or download updated versions, where these updated versions are the latest version/content that is in the AWS S3 bucket. After downloading the latest content from the S3 bucket, the ontology release date is displayed again to the user and then the annotation process occurs.

There is a cache control option for OAK, however this manages the default cache expiry lifetime of 7 days. This does not ensure that when the data annotation is run that it's using the latest ontology content available. As of this code update (31-Mar-2025), the `refresh` option is only available in the OAK commandline and not in the Python code.

OAK references:
- Cached ontology database is out of date - https://incatools.github.io/ontology-access-kit/faq/troubleshooting.html#my-cached-sqlite-ontology-is-out-of-date

- Cache control - https://incatools.github.io/ontology-access-kit/cli.html#cache-control


TODO: Include other methods to download ontology content and convert to a SQLite database using [semsql](https://github.com/INCATools/semantic-sql).


## Data File
Currently, the script assumes that the data file is an Excel file that has ~~one sheet~~ multiple sheets (TODO: paramterize Sheet name) and that the column with terms to search for matches to an ontology are in the first column.

TODO: Consider whether the input data file formatting assumptions need to be paramterized in the code to handle other varieties of files, e.g. CSV or Excel files where the search data is in another sheet or the first sheet but another column.

The input data file is expected to be stored locally at `data/input/` and the results of the ontology harmonization are stored at `data/ouput/`.

## Other files
- `compare_oak2rdflib.py` - added to check that all classes obtained used rdflib are also found in the semsql database. This was created because there was a confusion about which Mondo version was downloaded and a difference was seen between the content of the semsql database and rdflib using the latest Mondo release. It turns out the semsql database had not been updated when testing to provide the latest release of Mondo.

`rdflib_test.py` - extract classes from Mondo using rdflib


## Further Investigation
Review these items later to see if they can be done with OAK.

### Sort out if/how other parameters work for OAK Search
 # Configure the search -- KEEP!
    # config = SearchConfiguration(syntax=SearchTermSyntax.STARTS_WITH) # Example from: https://github.com/INCATools/ontology-access-kit/blob/main/notebooks/Developers-Tutorial.ipynb

    # Configure the search -- KEEP!
    # config = SearchConfiguration(
    # TODO: Find out how to use object_source to limit results to an ontology as well as 
    # object_source_match and snippet from SearchResult. 
    # See https://incatools.github.io/ontology-access-kit/datamodels/search/ and 
    # https://incatools.github.io/ontology-access-kit/datamodels/search/SearchResult.html 
    #     # properties=[SearchProperty.ALIAS], # matches to label and synonyms
    #     properties=[SearchProperty.LABEL], #matches label only
    #     force_case_insensitive=True,
    #     # is_complete=True,
    #     # is_partial=True, # does not seem to work even with single token label, e.g. ureteroc MONDO:0008628
    #     # is_fuzzy=True, # does not seem to work for fuzzy match to labels (ureteroc MONDO:0008628) or synonyms (intertricular commcation MONDO:0002070)
    # )
