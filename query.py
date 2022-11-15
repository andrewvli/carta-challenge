"""
query.py
---
Calls API over an HTTP request, returning a JSON representing an ordered list of 
search results from a course list according to a user's search string (a textual
query).
"""

import json
from flask import Flask, render_template, request

app = Flask(__name__)

TITLE_WEIGHT = 100
DESCRIPTION_WEIGHT = 10

def get_weight(course_weight_pair: list):
    """
    Gets the calculated weight from a (course, weight) pair.
    """
    return course_weight_pair[1]


def check_course_codes(data: dict, text: str):
    """
    Returns a list of courses whose course codes contain a match with the user's
    query. 
    """
    return [course for course in data if text in course["course_code"].lower()]


def check_quarters(courses: list, text_tokens: list):
    """
    If a quarter is specified during the user's textual query (i.e. "magic summer"),
    this function eliminates courses that do not occur in the desired time frame from 
    the JSON to be returned. 
    """
    seasons = ["spring", "summer", "autumn", "winter"]
    seasons_specified = [season for season in seasons if season in text_tokens]

    res = courses
    if seasons_specified:   # if no seasons are specified, we return all identified courses
        res = [course for course in courses if (any(season in course["quarters"] for season in seasons_specified))]
    return res


def process_query(data: dict, text: str):
    """
    Processes the user's query, returning an ordered list of search results that are
    ranked via relevance to the user's query. Utilizes a simple algorithm that weights
    each course via keywords identified in the user's query, weighted more heavily for
    keywords in the query that match a title than for keywords that match a word in the
    description.
    """
    if not text: 
        return data

    text_tokens = text.split()
    course_weights = [[i, 0] for i in range(1, len(data) + 1)] # initializing weights for each id

    if len(text_tokens) == 2:   # identifies if user input is a course ID
        if text_tokens[1][0].isnumeric():
            return check_course_codes(data, text)

    for i, course in enumerate(data):
        substr = ""
        for token in text_tokens: 
            # title matches more heavily weighted than description matches
            if token in course["title"].lower():
                course_weights[i][1] += TITLE_WEIGHT
            if course["description"]:
                if token in course["description"].lower():
                    course_weights[i][1] += DESCRIPTION_WEIGHT

            # want to prioritize queries that more closely match a title/description
            substr += token
            if substr in course["title"].lower():   
                course_weights[i][1] += TITLE_WEIGHT
            if course["description"]:
                if substr in course["description"].lower():
                    course_weights[i][1] += DESCRIPTION_WEIGHT
            substr += " "

    res = []
    course_weights.sort(key=get_weight, reverse=True) 

    for elem in course_weights:
        if elem[1]: # want to exclude elements with 0 weight; no matches to query
            for course in data:
                if course["id"] == elem[0]:
                    res.append(course)

    res = check_quarters(res, text_tokens)

    return res


@app.get('/')
def main():
    """
    Renders HTML template to collect user's textual query.
    """
    return render_template('form.html')


@app.route('/', methods=['POST'])
def my_form_post():
    """
    Receives user's textual query and loads in course data from its JSON file.
    Calls process_query to return response data as a dictionary/JSON.
    """
    text = request.form['text']
    with open('backend-course-data.json', 'r') as f:
        data = json.load(f)
    return process_query(data, text.lower())


if __name__ == "__main__":
    app.run(debug=True)     # starts our server & the flask application