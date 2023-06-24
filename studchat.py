import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import sqlite3
from nltk.chat.util import Chat, reflections

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')


map_keys = {
    "one": 1,
    "first": 1,
    "two": 2,
    "second": 2,
    "three": 3,
    "third": 3,
    "four": 4,
    "fourth": 4,
    "five": 5,
    "fifth": 5,
    "six": 6,
    "sixth": 6,
    "seven": 7,
    "seventh": 7,
    "eight": 8,
    "eighth": 8,
    "nine": 9,
    "ninth": 9,
    "zero": 0,
    "zeroth": 0,
}


def uid(username, password):
    conn = sqlite3.connect("chatbot.db")
    c = conn.cursor()
    c.execute(
        "SELECT id FROM users WHERE username=? AND password=?", (username, password)
    )
    userid = c.fetchone()
    conn.close()
    return userid[0]


def preprocess(input_string):
    tokens = word_tokenize(input_string)
    stop_words = set(stopwords.words("english"))
    tokens = [token for token in tokens if token.lower() not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    protext = " ".join(tokens)
    return protext.upper()


def conv_mapping(inp):
    new_inp = ""
    keys = map_keys.keys()
    arr = inp.split()
    for ar in arr:
        if ar in keys:
            new_inp = new_inp + str(map_keys[ar])
        else:
            new_inp = new_inp + ar
    return new_inp


def generate_response(uid, user_input):
    a = ""
    p_inp = preprocess(user_input).split(" ")
    if ("FEE") in p_inp:
        a = "fee"
        b = "pending fees"
        table = "details"
        return quer(a, b, table, uid)
    elif ("ATTENDANCE") in p_inp:
        a = "attendance"
        b = "attendance"
        table = "details"
        return quer(a, b, table, uid)
    elif (("EXAM") in p_inp) and (("DATE") in p_inp):
        a = "examdate"
        b = "next exam date"
        table = "details"
        return quer(a, b, table, uid)
    elif ("CGPA") in p_inp:
        a = "cgpa"
        b = "current cgpa"
        table = "gpa"
        return quer(a, b, table, uid)
    elif (("GPA" in p_inp) or ("SGPA" in p_inp) or ("GRADE" in p_inp)) and (
        ("SEMESTER" in p_inp) or ("SEM" in p_inp)
    ):
        inp = conv_mapping(user_input)
        match = re.search("\\d", inp)
        if match != None:
            sem_id = int(match.group())
            a = "sem" + str(sem_id)
            b = a + " gpa"
            table = "gpa"
        return quer(a, b, table, uid)
    else:
        response = "Sorry, I didnt understand."
        return response


def quer(a, b, table, uid):
    sql_query = "SELECT {} FROM {} WHERE id = '{}'".format(a, table, uid)
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute(sql_query)
    results = cursor.fetchone()
    response = "Your {} is: {}".format(b, results[0])
    return response


# u="SCS9152"
# r="what is my sem 4 gpa"
# generate_response(u,r)


# chat()
