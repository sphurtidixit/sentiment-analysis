import sys
import urllib
import json
from os import path
from nltk import stem
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import sys

audio_files=["file1.wav","file2.wav","file3.wav","file4.wav","file5.wav"]
aggregate_sentiment={"pos_count":0,"neg_count":0,"neutral_count":0}

for file_name in audio_files:
	try:
		filename = path.join(path.dirname(path.realpath(__file__)), file_name)
		print(filename)
	except IndexError:
		print ('Usage: transcribe.py <file>')
		sys.exit(1)

	f = open(filename)
	data = f.read()
	f.close()

	req = urllib.Request('https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang=en-US', data=data, headers={'Content-type': 'audio/x-flac; rate=16000'})

	try:
		ret = urllib.urlopen(req)
	except urllib.URLError:
		print ("Error Transcribing speech")
		sys.exit(1)

	resp = ret.read()
	text = json.loads(resp)['hypotheses'][0]['utterance']
	print (text)

	word_tokens = word_tokenize(text)

	positive_sentiment_unstemmed=["encourage","congratulatory","happy","motivate","delight","excite","pleased"]
	negative_sentiment_unstemmed=["miserable","sad","gloomy","depressed","bored","droopy","tired","alarmed","tense","afraid","angry","annoyed","frustrated","distressed"]
	neutral_sentiment_unstemmed=["tranquil","calm","at ease","relaxed"]

	stemmer = nltk.stem.PorterStemmer()
	new_list = [stemmer.stem(word) for word in word_tokens]
	positive_sentiment = [stemmer.stem(word) for word in positive_sentiment_unstemmed]
	negative_sentiment = [stemmer.stem(word) for word in negative_sentiment_unstemmed] 
	neutral_sentiment = [stemmer.stem(word) for word in neutral_sentiment_unstemmed] 

	positive_sentiment_dict={}
	negative_sentiment_dict={}
	neutral_sentiment_dict={}

	pos_count=0
	neg_count=0
	neutral_count=0

	for pos in positive_sentiment:
		positive_sentiment_dict[pos]=0

	for neg in negative_sentiment:
		negative_sentiment_dict[neg]=0

	for neu in neutral_sentiment:
		neutral_sentiment_dict[neu]=0
	
	for word in new_list:
		if positive_sentiment_dict[word]:
			positive_sentiment_dict[word]+=1
		if negative_sentiment_dict[word]:
			negative_sentiment_dict[word]+=1
		if neutral_sentiment_dict[word]:
			neutral_sentiment_dict[word]+=1	

	for word in positive_sentiment_dict:
		pos_count+=positive_sentiment_dict[word]
		aggregate_sentiment[pos_count]+=positive_sentiment_dict[word]

	for word in negative_sentiment_dict:
		neg_count+=negative_sentiment_dict[word]
		aggregate_sentiment[neg_count]+=negative_sentiment_dict[word]
		
	for word in neutral_sentiment_dict:
		neutral_count+=neutral_sentiment_dict[word]
		aggregate_sentiment[neutral_count]+=neutral_sentiment_dict[word]
	
	if (pos_count >= neg_count) and (pos_count >= neutral_count):
		sentiment="positive"
	if neg_count >= pos_count and neg_count >= neutral_count:
		sentiment="negative"
	if neutral_count >= pos_count and neutral_count >= neg_count:
		sentiment="neutral"
		
	if (aggregate_sentiment[pos_count] >= aggregate_sentiment[neg_count]) and (aggregate_sentiment[pos_count] >= aggregate_sentiment[neutral_count]):
		aggregate_sentiment_value="positive"
	if aggregate_sentiment[neg_count] >= aggregate_sentiment[pos_count] and aggregate_sentiment[neg_count] >= aggregate_sentiment[neutral_count]:
		aggregate_sentiment_value="negative"
	if aggregate_sentiment[neutral_count] >= aggregate_sentiment[pos_count] and aggregate_sentiment[neutral_count] >= aggregate_sentiment[neg_count]:
		aggregate_sentiment_value="neutral"
	

	
	
