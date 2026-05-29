from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

# Run once
nltk.download("punkt_tab")
nltk.download("stopwords")
nltk.download("wordnet")