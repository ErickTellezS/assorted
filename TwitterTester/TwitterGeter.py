import tweepy

most_wanted = ["Apple TV", "Xbox One X", "Days Gone", "iPhone XS", "Mortal Kombat", "iPhone XR",
               "Yoshi's Crafted World", "Galaxy A50", "Sekiro", "Galaxy S10", "The Division 2", "Surface Pro",
               "Bumblebee", "iPad Air", "Playstation 4"]

best_sellers = ["Apple TV",
                "Xbox One X",
                "The Division 2",
                "iPhone XS",
                "Dead Or Alive 6",
                "iPhone 8",
                "Ralph Breaks The Internet",
                "Galaxy A8",
                "Anthem",
                "Galaxy S10",
                "Dragon Ball Heroes",
                "Surface Pro",
                "Yoshi's Crafted World",
                "iPad Air",
                "Playstation 4"]

# Authenticate to Twitter
auth = tweepy.OAuthHandler('**********')
auth.set_access_token('*********',
                      '***********')

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

'''for prod in best_sellers:
    c = 1
    print('--', prod, '--')
    for tweet in api.search(q=prod, lang="es", count=100, tweet_mode='extended', geocode="19.451054,-99.125519,150km"):
        if tweet.user.location:
            print(tweet.user.location)
        c += 1'''

'''c = 1
for tweet in api.search(q=['TV', 'Apple'], lang="es", count=100, tweet_mode='extended',
                        geocode="19.451054,-99.125519,150km"):
    if tweet.place:
        print(c, tweet.place.full_name)
    c += 1'''

c = 1
for tweet in api.search(q=['TV', 'Apple'], lang="es", count=100, tweet_mode='extended',
                        geocode="19.451054,-99.125519,150km"):
    if tweet.user.location:
        print(c, tweet.user.location)
    c += 1
