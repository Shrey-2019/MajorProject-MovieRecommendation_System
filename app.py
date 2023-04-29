from flask import Flask, jsonify, render_template, request
import func
import firebase_admin
import requests, json


default_app = firebase_admin.initialize_app()

app = Flask(__name__)



@app.route('/')
def home():
    movies = ()

    carouselData = func.getCarouselItems()
    popularMovies = func.getPopularMovies()
    #watchlist = func.getWatchlistMovies()
    return render_template('index.html', carouselData=carouselData, popularMovies=popularMovies)

@app.route("/createUser", methods=["GET", "PUT"])
def createUsers():
    url = "https://w5xj3edx56.execute-api.ap-south-1.amazonaws.com/createUser"
    if request.method == 'PUT':
        requestBody = {}
        requestBody["Email"] = request.json["emailValue"]
        res = func.getUser(request.json["emailValue"])
        print(res)
        if(res == False):
            requestBody["First_Name"] = request.json["fnameValue"]
            requestBody["Last_Name"] = request.json["lnameValue"]
            requestBody["Password"] = request.json["pwdValue"]
            requestBody["User_Name"] = request.json["unameValue"]
            response = requests.put(
                url, data=json.dumps(requestBody),
                headers={'Content-Type': 'application/json'}
            )
            return {"status": "Account Created"}
        
        return {"status": "Already Exists"}

@app.route("/getUser", methods=["GET", "POST"])
def getUsers():
    if request.method == "POST":
        email = request.json['emailValue']
        users = func.getUser(email)
        if(users):
            return (users)
        else:
            return 0
        
@app.route("/getMovie", methods=["GET", "POST"])
def getMovieById():
    if request.method == "POST":
        movie = request.json['movieId']
        users = func.getMovie(movie)
        if(users):
            return (users)
        else:
            return 0

@app.route("/getMovieWatchlist", methods=["GET", "POST"])
def getMovieWatchlist():
    if request.method == "POST":
        movie = request.json['emailValue']
        watchlist = func.getWatchlistMovies(movie)
        if(watchlist):
            watchlist = map(dict, set(tuple(sorted(d.items())) for d in watchlist))
            # list_set = set(watchlist)
            # # convert the set to the list
            # watchlist = (list(list_set))
            return (list(watchlist))
        else:
            return 0      

        
@app.route("/addMovieWatchlist", methods=["GET", "PUT"])
def addMovie():
    url = "https://mv77u9kxij.execute-api.ap-south-1.amazonaws.com/addMovie"
    if request.method == 'PUT':
        print(request.json)
        response = requests.put(
                url, data=json.dumps(request.json),
                headers={'Content-Type': 'application/json'})
        
        return response.content
@app.route("/getRecommendation/<name>", methods=["GET", "PUT"])   
def getRecommended(name):
    movies = ()
    if request.method == 'GET':
        movies = func.recommend(name)
        return list(movies)
    return movies

if __name__ == "__main__":
    app.run(debug=True, port=3000)