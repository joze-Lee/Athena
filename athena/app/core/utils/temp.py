from nltk.tokenize import sent_tokenize
import nltk
import os

# import nltk
# nltk.download('punkt_tab')

os.environ['NLTK_DATA'] = '/Users/braddy/nltk_data'
nltk.data.find('tokenizers/punkt')  # validate punkt is there

text = "This is a test. This should split into two sentences."
sentences = sent_tokenize(text)  # ✅ will use the correct tokenizer
print(sentences)