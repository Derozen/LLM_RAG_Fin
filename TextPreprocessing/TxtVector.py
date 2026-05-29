import fitz  
import spacy
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
import string
import math
from sentence_transformers import SentenceTransformer

def preprocess_pdf(files_path):
    """
    files_path: str or list of str, path(s) to the PDF file(s) to be processed.
    """
    text = ""
    if isinstance(files_path, str):
        files_path = [files_path]
    for file in files_path:
        doc = fitz.open(file)
        txt = ""
        for page in doc:
            txt += page.get_text()
        text += txt + "\n" if len(files_path) >1 else txt


    nlp = spacy.load("en_core_web_sm")

    doc = nlp(text)

    tokens = [sent.text for sent in doc.sents]


    # Lowercase
    tokens= [t.lower() for t in tokens]

    # Remove punctuation
    tokens = [" ".join([t for t in word_tokenize(wtks) if t not in string.punctuation]) for wtks in tokens]
    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    tokens = [" ".join([t for t in word_tokenize(tks) if t not in stop_words]) for tks in tokens]
    # Lemmatize
    lemmatizer = WordNetLemmatizer()
    tokens = [" ".join([lemmatizer.lemmatize(t) for t in word_tokenize(tks)]) for tks in tokens]
    print(f"Total number of tokens after preprocessing: {len(tokens)}")
    return tokens

def CreateChunks(tokens, chunkSize=128):
    filtered_doc = [t for t in tokens if len(word_tokenize(t))>=3]
    LenDocs = [len(word_tokenize(t)) for t in filtered_doc]
    totalTokens = sum(LenDocs)
    numChunks = math.ceil(totalTokens/chunkSize)

    cumsumLenDocs = [LenDocs[0]] + [sum(LenDocs[0:i+1]) for i in range(1, len(LenDocs))]
    mask = [math.ceil(d/chunkSize) for d in cumsumLenDocs]
    textChunks = {'text':[], 'numTokens':[]}
    ValidIdx = [j for j in range( 1,numChunks+1) if j in mask]
    for i in ValidIdx:
        start_idx = mask.index(i)
        idx = ValidIdx.index(i)
        if idx == len(ValidIdx)-1:
            end_idx = len(mask)
        else:
            end_idx = mask.index(ValidIdx[idx+1])

        if end_idx == start_idx:
            groupedSentences = [filtered_doc[start_idx]]
        elif  end_idx == len(mask):
            groupedSentences = filtered_doc[start_idx:]
        else :
            groupedSentences =   filtered_doc[start_idx:end_idx] #filteredDocs(start_idx:end_idx);
        textChunks['text'].append(" ".join(groupedSentences))
        textChunks['numTokens'].append(sum([len(word_tokenize(t)) for t in groupedSentences]))
    return textChunks

def EmbedChunks(file_path, chunksize=128):
    tokens = preprocess_pdf(file_path)
    textChunks = CreateChunks(tokens, chunkSize=chunksize)
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L12-v2")

    # Your text chunks
    chunks = textChunks['text']

    # Generate embeddings
    embeddings = model.encode(chunks)

    print(embeddings.shape)
    print(f"Embeddings succesfully generated for {len(chunks)} chunks")
    return embeddings, textChunks['text']
    