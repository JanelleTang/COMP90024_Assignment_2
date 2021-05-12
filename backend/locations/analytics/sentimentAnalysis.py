import nltk
from nltk.corpus import stopwords
import re
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize

from geopy.geocoders import Nominatim


nltk.download('stopwords')
sia = SentimentIntensityAnalyzer()
geolocator = Nominatim(user_agent="tweets")

class CleanTweet:
    def __init__(self, text,location,coordinates=False):
        self.cleaned_text = process_text(text)
        self.sentiment_dict = sia.polarity_scores(self.cleaned_text)
        self.sentiment_value =  self.sentiment_dict['compound']
        if coordinates:
            self.lga,self.state = get_lga_by_coordinates(location)
        else:
            self.lga,self.state = get_lga_by_name(location)

    def __str__(self):s
        print("This tweet has sentiment: ".format(self.sentiment_dict["compound"]))

    def process_text(text):
        
        #lowercase text
        text = text.lower()
        
        #remove urls
        text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)

        #remove tweet mentions and hashtags
        text = re.sub(r'\@\w+|\#\w+|','', text)

        #remove numbers
        text = ''.join([x for x in tweet if not x.isdigit()])

        #remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))

        #tokenize 
        tweet_tokens = word_tokenize(text)

        #remove stopwords
        processed_tweet = [x for x in tweet_tokens if not x in stopwords.words('english')]

        return " ".join(processed_tweet)
    
    def get_lga_by_name(location):
        location = geolocator.geocode(location,addressdetails=True)
        address = location.raw['address']
        if address['country']!="Australia":
            print("Check this tweet location")
            return None,None
        if len(address) <3:
            return None,None
        return address["municipality"].lower(),address["state"].lower() 

    def get_lga_by_coordinates(location):
        location = geolocator.reverse(location[0],location[1])
        address = location.raw['address']
        if address['country']!="Australia":
            print("Check this tweet location")
            return None,None
        if len(address) <3:
            return None,None
        return address["municipality"].lower(),address["state"].lower() 
    
    def get_dict(self):
        #Check Format
        result = {self.lga:{'name': self.lga
                            'state':self.state,
                            'total_sentiment':self.sentiment_value,
                            'total_tweets':1}}
        return result
