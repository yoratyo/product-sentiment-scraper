from textblob import TextBlob

analysis = TextBlob('not a very great experiment')
print(analysis.sentiment)