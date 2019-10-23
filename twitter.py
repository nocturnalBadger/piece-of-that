"""
Authenticates to Twitter API and tweets a jingle
"""
import logging

import tweepy

import rhyming
from credentials import (consumer_key, consumer_secret, token, secret)


if __name__ == "__main__":
    logging.basicConfig(format='%(filename)s: %(message)s', level=logging.DEBUG)

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(token, secret)
    api = tweepy.API(auth)

    rhyme = rhyming.find_rhyme(3, "bar")
    jingle = f"🎶 Break me off a piece of that {rhyme} 🎶"

    logging.info(jingle)

    api.update_status(jingle)
