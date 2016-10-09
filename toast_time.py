#!/home/kalilsn/toast_time/env/bin/python

#toast time twitter bot
#Kalil Smith-Nuevelle
#7/31/2015

import tweepy, sys, os, markov, random, pickle

#utf-8 just in case
reload(sys)
sys.setdefaultencoding("utf-8")

dir = os.path.abspath(os.path.dirname(sys.argv[0]))
last_tweet_filename = dir + "/last.txt"
corpus_file = dir + "/toast_corp.txt"

#Authentication and api object initialization
consumer_key = "mvXU9DsjScUZty7hIqOnwcL2B"
consumer_secret = "Jo95NOhTMYEOShsPvP4pmFXPEdLINKrqFmHIglhyPFbbsQ2k4S"
access_token = "1646351022-IuLj3FsfFx2syNMfypDndvkO7JmCoLu4PAVwF5h"
access_token_secret = "vSmGnp8MSnp63TS8WdyOkDe0GqZUQGMnZVGjHLP9WL3Qr"

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.secure = True
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

#Get last tweet retrieved
with open(last_tweet_filename, "r+") as last_tweet:
	last = int(last_tweet.read())

	#Get tweets since last update
	timeline = api.home_timeline(since_id=last, count=1000)
	print "Retrieved " + str(len(timeline)) + " statuses"

	#Update the file containing the id of the most recently retrieved status
	last_tweet.seek(0)
	last_tweet.write(timeline[0].id_str)
	last_tweet.truncate()


#Retweets any toast-related tweets from people I follow
print "Retweeted: "

for status in timeline:
	text = status.text.lower()
	if ("toast" in text or "bread" in text or "loaf" in text) and not status.retweeted and status.user.id != api.me().id:
		api.retweet(status.id)
		print status.user.name + ": " + text + "\n"

#Posts new tweet if passed "tweet" argument
try:
	if sys.argv[1] == "tweet":
		status = generate_markov_status()
		api.update_status(status)
		print "\nTweeted:\n" + status
except IndexError:
	pass


def generate_markov_status():
# Generates a tweet via markov chains and a given corpus. Randomly chooses a length between 30 and 140 characters
# and an ngram length from 2-4 for variation. Runs until it generates a tweet with "toast" or "bread"
	with open(corpus_file) as f:
		corpus = f.read()
	gen = markov.MarkovGenerator(corpus,length=random.randint(50,140),ngram=random.randint(2,4))
	status = ""

	status = gen.generate_words()
	status_tokenized = nltk.word_tokenize(status)
	status_tokenized_clean = [word for word in nltk.word_tokenize(status) if word not in string.punctuation]
	rand_words = random.sample(status_tokenized_clean, random.randint(1,int(len(status_tokenized_clean)/3)))
	text = nltk.Text(word.lower() for word in nltk.corpus.brown.words())
	for i in range(len(status_tokenized)):
		word = status_tokenized[i]
		if word in rand_words:
			status_tokenized[i] = text.similar(word)


	while not ("toast" in status) or ("bread" in status):
		status = gen.generate_words()
	return status




status = gen.generate_words()
status_tokenized = nltk.word_tokenize(status)
status_tokenized_clean = [word for word in nltk.word_tokenize(status) if word not in string.punctuation]
rand_words = random.sample(status_tokenized_clean, random.randint(1,int(len(status_tokenized_clean)/3)))
idx = nltk.text.ContextIndex([word.lower( ) for word in nltk.corpus.brown.words( )])
for i in range(len(status_tokenized)):
	word = status_tokenized[i]
	if word in rand_words:
		status_tokenized[i] = random.choice(idx.similar_words(word))  #need to make sure similar words finds anything, filter rand_words, choose better corpus?
