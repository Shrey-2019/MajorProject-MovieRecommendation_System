import pickle
import requests, json

movies = pickle.load(open('./models/movie_list.pkl','rb'))
similarity = pickle.load(open('./models/similarity.pkl','rb'))
#movie_list = movies['title'].values

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    index = movies[(movies['title']).str.title() == movie.title()].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names,recommended_movie_posters


def getCarouselItems():
    url = "https://13tsc5rszh.execute-api.ap-south-1.amazonaws.com/carouselItems"
    data = requests.get(url)
    data = data.json()
    return data

def getPopularMovies():
    url = "https://igzztey5qd.execute-api.ap-south-1.amazonaws.com/popularMovies"
    data = requests.get(url)
    data = data.json()
    return data

def getWatchlistMovies(userid):
    url = "https://mv77u9kxij.execute-api.ap-south-1.amazonaws.com/getWatchlist/"+userid
    data = requests.get(url)
    data = data.json()
    return data

def getUser(email):
    api_url = 'https://w5xj3edx56.execute-api.ap-south-1.amazonaws.com/getUser/'+email
    r = requests.get(url=api_url, params = email)
    if(len(r.text) > 0):
        return json.loads(r.text)
    else:
        return False
    
def getMovie(movieId):
    api_url = 'https://igzztey5qd.execute-api.ap-south-1.amazonaws.com/MovieDetail/'+movieId
    r = requests.get(url=api_url, params = movieId)
    if(len(r.text) > 0):
        return json.loads(r.text)
    else:
        return False