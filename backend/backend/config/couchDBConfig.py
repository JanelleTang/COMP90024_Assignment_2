class CouchDBConfig:
    domain = "127.0.0.1"
    domains = ['172.26.128.53', '172.26.133.176', '172.26.133.116']
    username = "admin"
    password = "admin"
    port = "5984"
    tweet_db_name = "twitter"
    views={
        'twitter':{
                "_id" : "_design/tweet",
                "views" : {
                        "get_raw" : {
                            "map" : "function(doc){if(doc.isProcessed==0){emit(doc.id,{_id:doc.id,text:doc.text,location:doc.location,geo:doc.geo,hashtags:doc.hashtags,date_created:doc.date_created,})}}"
                        }

                    },
                    "language" : "javascript"
                },
    }