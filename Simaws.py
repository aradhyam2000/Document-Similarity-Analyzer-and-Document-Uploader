


from collections import Counter
from nltk import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import boto3

def lambda_handler(event, context):
  

    s3 = boto3.client('s3')

    # Input text
    data1 = s3.get_object(Bucket='aradhya-data', Key='doc.txt')
    text1=data1['Body'].read()
    textwords1=text1.split()
    data2 = s3.get_object(Bucket='aradhya-data', Key='test2.txt')
    text2=data2['Body'].read()
    textwords2=text2.split()

    print(text1)
    print()
    print(text2)
    
    ps=PorterStemmer()
    lemmatizer=WordNetLemmatizer()
    stopwords1 = stopwords.words('english')

    # Remove stopwords
    resultwords1  = [word for word in textwords1 if word.lower() not in stopwords1]
    resultwords2  = [word for word in textwords2 if word.lower() not in stopwords1]

    # count word occurrences
    a_occ = Counter(resultwords1)
    b_occ = Counter(resultwords2)

    # convert to word-vectors
    words  = list(a_occ.keys() | b_occ.keys())
    a_vect = [a_occ.get(word, 0) for word in words]
    b_vect = [b_occ.get(word, 0) for word in words]
      

    # find cosine
    len_a  = sum(av*av for av in a_vect) ** 0.5             
    len_b  = sum(bv*bv for bv in b_vect) ** 0.5             
    dot    = sum(av*bv for av,bv in zip(a_vect, b_vect))    
    cosine = dot / (len_a * len_b) 

    print()

    print (round(cosine*100,2),"% Similarity")

