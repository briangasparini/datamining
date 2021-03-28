URL_DATA = "https://query.wikidata.org/sparql?query=SELECT%20%3Fitem%20%3FitemLabel%20%3Fpic%20WHERE%20%7B%0A%20%20%3Fitem%20wdt%3AP31%20wd%3AQ515%3B%0A%20%20%20%20wdt%3AP18%20%3Fpic%3B%0A%20%20%20%20rdfs%3Alabel%20%3FitemLabel.%0A%20%20FILTER(lang(%3FitemLabel)%3D%22en%22)%0A%7D%0ALIMIT%2050&format=json"
URL_DATA_RECOM = "https://query.wikidata.org/sparql?query=SELECT%20%3Fitem%3FitemLabel%3Fpic%20WHERE%20%7B%0A%3Fitem%20wdt%3AP31%20wd%3AQ515%3B%0Awdt%3AP18%20%3Fpic%3B%0Ardfs%3Alabel%3FitemLabel.%0AFILTER(lang(%3FitemLabel)%3D%20%22en%22)%7D%0ALIMIT%2020&format=json"
DATA_PATH = "./DATA/"
IMAGE_PATH = "./IMAGES/"
IMAGE_TO_CHECK = "./IMAGES/TOCHECK/"
IMAGE_CHECKED = "./IMAGES/CHECKED/"
IMAGE_CHECKED_RECOM = "./IMAGES/CHECKED/RECOM/"
allData = []