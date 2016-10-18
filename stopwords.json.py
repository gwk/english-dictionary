# Generate list of stopwords.

from nltk.corpus import stopwords
from pithy.json_utils import out_json

words = stopwords.words('english') # Loading from NLTK corpus is a little slow (~0.4 seconds).

out_json(words)
