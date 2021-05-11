class CouchDBConfig:
    domain = ""
    domains = ["127.0.0.1"]
    username = "root"
    password = "123456"
    port = "5984"
    tweet_db = ""
    views = {
        "_id" : "_design/tweet",
        "views" : {
            "get_raw" : {
                "map" : "function(doc){if(doc.isProcessed==0){emit(doc.id,{_id:doc.id,text:doc.text,location:doc.location,geo:doc.geo,hashtags:doc.hashtags,})}}"
            }
            
        },
        "language" : "javascript"
    }