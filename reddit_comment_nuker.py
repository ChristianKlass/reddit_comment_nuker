import praw
import secrets
import string
import random
import requests
import os
import configparser
import logging

import logging

# configure the logging module
logging.basicConfig(filename='reddit_comment_nuker.log', level=logging.DEBUG)

# create a ConfigParser object and read the config.ini file
config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')

# get the values from the [reddit] section of the config.ini file
client_id = config.get('reddit', 'client_id')
client_secret = config.get('reddit', 'client_secret')
username = config.get('reddit', 'username')
password = config.get('reddit', 'password')

# print all the values gotten from the config.ini file
logging.info("client_id: " + client_id)
logging.info("client_secret: " + client_secret)
logging.info("username: " + username)
logging.info("password: " + password)

# create a reddit instance
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    username=username,
    password=password,
    user_agent='do not tell me what to do/0.0.1234882399/xx',
    validate_on_submit=True
)

# get all comments as a list
comments = list(reddit.user.me().comments.new(limit=None))

def generate_random_paragraph():
    # generate a random number of sentences between 5 and 10
    num_sentences = random.randint(3,7)

    # generate a list of words using the Random Word API
    words = requests.get('https://random-word-api.herokuapp.com/word?number=1000').json()

    # create a list of sentences
    sentences = []
    for i in range(num_sentences):
        # generate a random number of words between 10 and 20
        num_words = random.randint(10, 15)

        # create a sentence by joining a random selection of words
        sentence = ' '.join(random.sample(words, num_words))

        # capitalize the first letter of the sentence and add a period at the end
        sentence = sentence.capitalize() + '.'

        # add the sentence to the list of sentences
        sentences.append(sentence)

    # join the sentences into a paragraph
    paragraph = ' '.join(sentences)

    # add a double newline character to create a new paragraph
    paragraph += '\n\n'

    return paragraph

# generate a random number of paragraphs between 5 and 8
num_paragraphs = random.randint(5, 8)

# generate random paragraphs
random_string = ''
for i in range(num_paragraphs):
    random_string += generate_random_paragraph()

# print the total comments in comments:
print("There are " + str(len(comments)) + " comments to change!")


for comment in comments:
    random_string = ''
    index = comments.index(comment)
    num_paragraphs = random.randint(5, 8)
    logging.info("Changing comment {}.".format(index))
    logging.info("The new comment will have " + str(num_paragraphs) + " nonsensical paragraphs.")

    for i in range(num_paragraphs):
        random_string += generate_random_paragraph()
    
    comment.edit(random_string)
    logging.info ("Done!")
