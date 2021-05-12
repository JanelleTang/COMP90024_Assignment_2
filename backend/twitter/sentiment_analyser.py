import nltk
from nltk.corpus import stopwords
import re
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
import string

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

nltk.download('stopwords')
sia = SentimentIntensityAnalyzer()
geolocator = Nominatim(user_agent="tweets")

## add geo tag ##

class CleanTweet:
    def __init__(self, text,location,coordinates=False):
        self.cleaned_text = self.process_text(text)
        self.sentiment_dict = sia.polarity_scores(self.cleaned_text)
        self.sentiment_value =  self.sentiment_dict['compound']
        if coordinates:
            location = self.get_lga_by_coordinates(location)
        else:
            location = self.get_lga_by_name(location)
        
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

        return " ".join(processed_tweet)
    
    def get_lga_by_name(self,input):
        try:
            location = geolocator.geocode(input,addressdetails=True)
        except GeocoderTimedOut:
            return self.get_lga_by_name(input)
        if location == None:
            return None, None,None
        address = location.raw['address']
        try:
            if address['country']!="Australia":
                return None
        except:
            return None
        try:
            lga = address["municipality"].lower()
            city = address["city"].lower() 
            state = address["state"].lower() 
        except KeyError:
            try:
                city = address["city"].lower() 
                lga="none_"+city
                state = address["state"].lower() 
            except KeyError:
                return None,None,None
        return lga,city,state

    def get_lga_by_coordinates(self,input):
        try:
            location = geolocator.reverse(input[0],input[1])
        except GeocoderTimedOut:
            return None
        
        if location == None:
            return 
        address = location.raw['address']
        if address['country']!="Australia":
            return None
        try:
            lga = address["municipality"].lower()
            city = address["city"].lower() 
            state = address["state"].lower() 
        except KeyError:
            try:
                city = address["city"].lower() 
                lga="none_"+city
                state = address["state"].lower() 
            except KeyError:
                return None
        return lga,city,state
    
    def get_dict(self):
        if self.city == None:
            return None
        result = {"lga": self.lga,
                "city": self.city,
                "state":self.state,
                "total_sentiment":self.sentiment_value,
                "total_tweets":1}
        return result
