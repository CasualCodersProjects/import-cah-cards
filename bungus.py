#!/home/chandler/.local/share/virtualenvs/import-cah-cards-Fo8uBFs9/bin/python
import os
import sys
import csv
import psycopg2
import dotenv
import random

# CONSTANTS
WATERMARK = "MELON"
DECK_NAME = "Cult of Melon Pack"
DECK_DESCRIPTION = DECK_NAME
WEIGHT = 255

# DEVELOPMENT MODE -----> (DO NOT TURN OFF EVER!!!!) <------
development_mode = False

# This looks important
dotenv.load_dotenv()

# Database connection details
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_PORT = int(os.getenv("DB_PORT"))

# open csv files with card data
BLACK_FILE = "black.csv"
WHITE_FILE = "white.csv"
black = open(BLACK_FILE, 'r')
white = open(WHITE_FILE, 'r')

# load csv from the files
black_reader = csv.reader(black)
white_reader = csv.reader(white)

# Connect to the DB
database = psycopg2.connect(
    user=DB_USER, password=DB_PASS, host=DB_HOST, dbname=DB_NAME, port=DB_PORT)

# Create query object for making queries
query = database.cursor()

# get the number of cards in the black_cards table
query.execute("SELECT MAX(id) FROM black_cards")
black_count = query.fetchone()[0]

# get the number of white cards in the white_cards table
query.execute("SELECT MAX(id) FROM white_cards")
white_count = query.fetchone()[0]

# Store the card IDs in lists for optimal card-counting
black_IDs = []

# Loop through the black cards, add them to the DB
line_is_header = True
for line in black_reader:
    # First line is garbage
    if line_is_header is True:
        line_is_header = False
        continue

    # Cast the junk to some pretty variables
    draw, pick, text = line

    # Bump the card counter, add it to the card ID list
    black_count += 1
    black_IDs.append(black_count)

    # black_cards: id (auto) | draw # | pick # | text | watermark
    try:
        # SIMULATE the query
        if development_mode:
            print(
                "EXPLAIN INSERT INTO black_cards (id,draw,pick,text,watermark) VALUES (%s, %s, %s, %s, %s)", (
                    black_count, draw, pick, text, WATERMARK)
            )

        # Otherwise RUN the query (scary)
        else:
            query.execute(
                "INSERT INTO black_cards (id,draw,pick,text,watermark) VALUES (%s, %s, %s, %s, %s)", (
                    black_count, draw, pick, text, WATERMARK)
            )
    except Exception as ex:
        print('YOU DUN GOOFED!!\n', ex)
        sys.exit(1)

# Commit the uhhh data?
database.commit()

# Time for the white cards!!!
white_IDs = []

line_is_header = True
for text in white_reader:
    # First line is garbage
    if line_is_header is True:
        line_is_header = False
        continue

    # Oh it's literally just one line
    text = text[0]
    # Yes, the text is made of text

    # Bump the card counter, add it to the card ID list
    white_count += 1
    white_IDs.append(white_count)

    # white_cards: id (NOT auto) | text | watermark
    try:
        # SIMULATE the query
        if development_mode:
            print(
                "EXPLAIN INSERT INTO white_cards (id,text,watermark) VALUES (%s, %s, %s)", (
                    white_count, text, WATERMARK)
            )

        # Otherwise RUN the query (scary)
        else:
            query.execute(
                "INSERT INTO white_cards (id,text,watermark) VALUES (%s, %s, %s)", (
                    white_count, text, WATERMARK)
            )
    except Exception as ex:
        print('YOU DUN GOOFED!!\n', ex)
        sys.exit(1)

# Commit the uhhh data again!
database.commit()

# Create the deck data baby

# card_set: id (auto) | active (true) | base_deck (false) | description (same >>) | name (<<same) | weight (255 for ours)

# get a random number greater than 2375 but less than 60000
random_id = random.randint(2375, 60000)
# they seem to use random numbers, so we'll do the same.

# random_id = 2375 # if you already have a deck, change this to the id

if development_mode:
    print(
        "EXPLAIN INSERT INTO card_set (id,active,base_deck,description,name,weight) VALUES (%s, true, false, %s, %s, %s)", (
            random_id, DECK_DESCRIPTION, DECK_NAME, WEIGHT)
    )
else:
    query.execute(
        "INSERT INTO card_set (id,active,base_deck,description,name,weight) VALUES (%s, true, false, %s, %s, %s)", (random_id, DECK_DESCRIPTION, DECK_NAME, WEIGHT))
    database.commit()

# card_set_black_card: card_set_id (match set^^) | white_card_id

for black_card_id in black_IDs:
    if development_mode:
        print(
            "EXPLAIN INSERT INTO card_set_black_card (card_set_id,black_card_id) VALUES (%s, %s)", (
                random_id, black_card_id)
        )
    else:
        query.execute(
            "INSERT INTO card_set_black_card (card_set_id,black_card_id) VALUES (%s, %s)", (
                random_id, black_card_id)
        )

if not development_mode:
    database.commit()

# card_set_white_card: card_set_id (match set^^) | black_card_id

for white_card_id in white_IDs:
    if development_mode:
        print(
            "EXPLAIN INSERT INTO card_set_white_card (card_set_id,white_card_id) VALUES (%s, %s)", (
                random_id, white_card_id)
        )
    else:
        query.execute(
            "INSERT INTO card_set_white_card (card_set_id,white_card_id) VALUES (%s, %s)", (
                random_id, white_card_id)
        )

if not development_mode:
    database.commit()

# White fields are id(PRIMARY INCREMENT) | text | watermark (MELON)

# For each row, insert into the database

print("New deck ID: ", random_id)
