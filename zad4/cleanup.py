from collections import Counter
import json
import re

HOW_MANY_GENRES = 6


def read_data():
    with open("booksummaries.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        books = []

        for line in lines:
            temp = line.split("\t")
            books.append([temp[5], temp[6]])

        return books


def clean(text):
    t = re.sub("\'", "", text)
    t = re.sub("[^a-zA-Z]", " ", t)
    t = ' '.join(t.split())
    t = t.lower()

    return t


def top_7_genres(books):
    genres = {}
    for book in books:
        jsonified = book[0]
        if jsonified == '':
            continue
        else:
            pyObj = json.loads(jsonified)
            for id in pyObj.keys():
                if pyObj[id] in genres.keys():
                    genres[pyObj[id]] += 1
                else:
                    genres[pyObj[id]] = 1

    return dict(Counter(genres).most_common(HOW_MANY_GENRES))


def filter_books(books, genres):
    filtered = []
    for book in books:
        jsonified = book[0]
        if jsonified == '':
            continue
        else:
            pyObj = json.loads(jsonified)
            for id in pyObj.keys():
                if pyObj[id] in genres.keys() and len(book[1]) > 100:
                    filtered.append([pyObj[id], clean(book[1])])
                    break

    return filtered


def get_labels(books):
    labels = []
    for book in books:
        labels.append(book[0])
    return labels


def get_descriptions(books):
    descs = []
    for book in books:
        descs.append(book[1])
    return descs


def get_data():
    books = read_data()
    genres = top_7_genres(books)
    print(genres)
    filtered_books = filter_books(books, genres)
    labels = get_labels(filtered_books)
    descs = get_descriptions(filtered_books)
    return (labels, descs)


if __name__ == "__main__":
    books = read_data()
    genres = top_7_genres(books)
    filtered_books = filter_books(books, genres)
    labels = get_labels(filtered_books)
    descs = get_descriptions(filtered_books)
