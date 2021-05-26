# ============= COMP90024 - Assignment 2 ============= #
#                               
# The University of Melbourne           
# Team 37
#
# ** Authors: **
# 
# JJ Burke              1048105
# Janelle Tang          694209
# Shuang Qiu            980433
# Declan Baird-Watson   640975
# Avinash Rao           1024577 
# 
# Location: Melbourne
# ==================================================== 

from nltk.corpus import stopwords
import nltk
import re
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
import string

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

nltk.download([
    "names",
    "stopwords",
    "state_union",
    "twitter_samples",
    "movie_reviews",
    "averaged_perceptron_tagger",
    "vader_lexicon",
    "punkt",
])
sia = SentimentIntensityAnalyzer()
geolocator = Nominatim(user_agent="tweets")
stemmer = PorterStemmer()

## Check geo tag ##

class CleanTweet:
    def __init__(self, text,location,hashtags,coordinates=False):
        self.cleaned_text = self.process_text(text)
        self.hashtags = [x.lower() for x in hashtags]
        self.sentiment_dict = sia.polarity_scores(self.cleaned_text)
        self.sentiment_value =  self.sentiment_dict['compound']
        location = self.get_lga(location,coordinates)
        if location!= None:
            self.lga,self.city,self.state = location
        else:
            self.city = None

    def __str__(self):
        print("This tweet has sentiment: ".format(self.sentiment_dict["compound"]))

    def process_text(self,text):
        #lowercase text
        text = text.lower()
        
        #remove urls
        text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)

        #remove tweet mentions and hashtags
        text = re.sub(r'\@\w+|\#\w+|','', text)

        #remove numbers
        text = ''.join([x for x in text if not x.isdigit()])

        #remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))

        #tokenize 
        tweet_tokens = word_tokenize(text)

        #remove stopwords
        processed_tweet = [x for x in tweet_tokens if not x in stopwords.words('english')]
        stemmed_tweet = [stemmer.stem(x) for x in processed_tweet]

        return " ".join(stemmed_tweet)
    
    def get_lga(self,input,coordinates=False):
        """
        convert user location or geotag into LGA, City, and State labels.
        """
        try:
            if coordinates:
                location = geolocator.reverse(""+str(input[1])+", "+str(input[0]),addressdetails=True,timeout=1000)
                print('coordinates location {}'.location)
            else:    
                location = geolocator.geocode(input,addressdetails=True,timeout=1000)
        except GeocoderTimedOut as e:
            print("Error: geocode failed on input %s with message %s"%(input, e.message))
            return self.get_lga(input)
        if location == None:
            return None
        address = location.raw['address']
        if len(address) < 3:
            return None
        try:
            if address['country']!="Australia":
                return None
        except:
            return None

        if 'territory' in address:
            pass

        if 'town' in address:
            address.pop('municipality', None)

        try:
            lga = address["municipality"].lower()
            city = address["city"].lower() 
            state = address["state"].lower()
        except KeyError:
            try:
                city = address["city"].lower() 
                lga="no_lga"
                state = address["state"].lower() 
            except KeyError:
                return None
        return([lga,city,state])

    def get_dict(self):
        if self.city == None:
            return None
        result = {"lga": self.lga,
                "city": self.city,
                "state":self.state,
                "hashtags":self.hashtags_to_dict(),
                'aggregate_data':{"total_sentiment":self.sentiment_value,
                                    "total_tweets":1}}
        return result

    def hashtags_to_dict(self):
        results ={}
        for tag in self.hashtags:
            results[tag] = self.hashtags.count(tag)
        return results
            

