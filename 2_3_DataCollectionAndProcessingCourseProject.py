import requests_with_caching

def get_movies_from_tastedive(name):
    key_pairs={}
    key_pairs['q']=name
    key_pairs['type']='movies'
    key_pairs['limit']='5'
    baseurl='https://tastedive.com/api/similar'
    resp=requests_with_caching.get(baseurl,params=key_pairs)
    respDic=resp.json()
    return respDic

def extract_movie_titles(respDic):
    movietitles = [movie['Name'] for movie in respDic['Similar']['Results']]
    return movietitles

def get_related_titles(lst):
    movielst = []
    for movie in lst:
        tempDic = extract_movie_titles(get_movies_from_tastedive(movie))
        for relatedmovie in tempDic:
            if relatedmovie in movielst:
                continue
            else:
                movielst.append(relatedmovie)
    return movielst

def get_movie_data(title):
    key_pairs={}
    key_pairs['t'] = title
    key_pairs['r'] = 'json'
    baseurl = 'http://www.omdbapi.com/'
    resp=requests_with_caching.get(baseurl,params=key_pairs)
    movieinfo=resp.json()
    return movieinfo

def get_movie_rating(movieinfo):
    score = '0'
    for source in movieinfo['Ratings']:
        if source['Source'] == 'Rotten Tomatoes':
            score = source['Value'].replace('%','')
    return int(score)

def get_sorted_recommendations(lst):
    templist = get_related_titles(lst)
    newlist = sorted(templist,key=lambda name: (get_movie_rating(get_movie_data(name)), name), reverse = True )
    return newlist
