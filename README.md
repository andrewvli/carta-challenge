# Backend Engineering Challenge: Course Search API
## Andrew Li

### Compiling and Running
Download the directory. If Flask is not installed, install Flask with: 

```
pip3 install flask
```

To run the program, type:

```
python query.py
```

The terminal should read off something similar to "Running on http://127.0.0.1:5000." Enter that
URL into the browser; the program should be able to be ran from there. 

### Major Design and Architectural Decisions
The first major design decision that I made was to weight each course by how closely they matched
the textual query made by the user. In more specifics, I incremented the weight of a course more 
heavily for keyword matches with titles, incremented less heavily for keyword matches with descriptions,
and gave a bonus to courses with matching substrings (either in the title or description) to the 
textual query. I then rank courses in decreasing order of weights, meaning that courses that have 
more matches with the textual query are listed first in the object to be returned. 

Algorithmically, this is slightly slower: you're iterating over two for-loops in O(N^2) time. 
There is also a lot of space being used, which might be an issue with many courses/long queries. Additionally,
of course, this works poorly with typos in the user search and with judging the meaning of the user query
to return results. However, the implementation of this was much simpler to do within the timeframe. Weighting 
presence of keywords in the textual query to rank the relevance of courses was a more effective way of presenting 
the results sought for by the user than, for instance in ExploreCourses, returning an alphabetical list of all 
courses that have same match with the query. Searching for "magic" returns first all courses that deal primarily
with magic (i.e. MAGIC 101 and MAGIC 199) before also listing courses that deal peripherally with magic,
such as some potions classes; it should balance getting specifics that the user desires while also providing
breadth in the search results. 

Another design decision made was to delineate between broader searches and course-code searches. To
identify course code searches, the program looks for textual queries that are two words long in which
the second word begins with a numeric character (i.e. CS 1). I considered, for instance, when I search for
something like "CS 106" on ExploreCourses, I only want to see all of the CS 106 course codes; I don't want
my results to be clogged by the other dozens of classes that have CS 106A or CS 106B as a prerequisite. 
This offers the user greater specificity in their search results if they know exactly what they're looking for; 
however, it comes with the same inflexibility with user typos as does the first design decision made. 

Last, I made the choice to include quarter specificty in the search capabilities. If a user searches for 
"magic summer", it returns only the search results (as identified in the first design decision discussion) that
have a class during the winter quarter. This is especially inflexible; say, for instance, you had a hypothetical
class that dealt with spring mechanics that only occurred in the winter. This class would be excluded from the 
search results. In an ideal scenario, I would have offered an ability to select quarters outside of the textual
query (like in ExploreCourses, where you can select quarters on a side menu); however, due to time constraints, 
I chose to make the simpler choice to offer this option in the textual query. 

The structure of the search endpoint was done with Flask and with an HTML form element; as I don't have that
much experience with Flask, this was the simplest way I felt I could get the user's textual query/design the 
web API while focusing further on the search algorithm. Moving forward, I feel like there is more work that 
could be done here— for instance, having specific URLs for each search (currently, whenever you search, it remains
on the 127.0.0.1:5000 URL). I also chose to not include any search capabilities that deal with the "requirements"
or "units" fields of each course; I felt as though those were the least essential things to implement (requirements
especially), and I would choose to include units in a side menu (as in the quarter specificity).
