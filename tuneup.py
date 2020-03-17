#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tuneup assignment"""

__author__ = "???"

import cProfile
import pstats
import timeit
from io import BytesIO as StringIO


def profile(func):
    """A function that can be used as a decorator to measure performance"""
    def inner(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = func(*args, **kwargs)
        pr.disable()
        s = StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval
    return inner


def read_movies(src):
    """Returns a list of movie titles"""
    print('Reading file: {}'.format(src))
    with open(src, 'r') as f:
        return f.read().splitlines()


# def is_duplicate(title, movies):
#     """returns True if title is within movies list"""
#     for movie in movies:
#         if movie == title:
#             return True
#     return False


@profile
def find_duplicate_movies(src):
    """Returns a list of duplicate movies from a src list"""
    movies = read_movies(src)
    movies = [movie.lower() for movie in movies]
    movies.sort()
    duplicates = [movie1 for movie1, movie2 in zip(
        movies[:-1], movies[1:]) if movie1 == movie2]
    # duplicates = []
    # while movies:
    #     movie = movies.pop()
    #     if movie in movies:
    #         duplicates.append(movie)
    return duplicates


def timeit_helper():
    """Part A:  Obtain some profiling measurements using timeit"""
    setup = '''def find_duplicate_movies(src):
    movies = read_movies(src)
    duplicates = []
    while movies:
        movie = movies.pop()
        if is_duplicate(movie, movies):
            duplicates.append(movie)
    return duplicates'''
    t = timeit.Timer(stmt='pass', setup=setup)
    results = t.repeat(repeat=7, number=1000)
    avg_results = []
    for result in results:
        avg_result = result/1000
        avg_results.append(avg_result)
    print('Best time across 7 repeats of 1000 runs per repeat: {}'.format(
        min(avg_results)))


def main():
    """Computes a list of duplicate movie entries"""
    timeit_helper()
    result = find_duplicate_movies('movies.txt')
    print('Found {} duplicate movies:'.format(len(result)))
    print('\n'.join(result))


if __name__ == '__main__':
    main()
