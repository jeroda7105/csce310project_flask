from flask import Flask, render_template, request, redirect
import requests
import json
from epicstore_api import EpicGamesStoreAPI
from datetime import datetime
from operator import itemgetter
import harperdb
#from harperDB import harperdb_request
 
app = Flask(__name__)

@app.route('/',methods = ['GET','POST'])
def index():

    games_list = []
    
    #Stores user search input in q
    q = request.args.get('query')
    if type(q) != str:
        q =""


    db = harperdb.HarperDB(url="https://gamesearch-whatislife.harperdbcloud.com", username="csce_db_project", password="csce_db_project")

    query_string = "SELECT games.title, sell.price, sell.initialprice, sell.discount, stores.store_name, sell.thumbnail, sell.link" \
                   " FROM game_search.games AS games" \
                   " INNER JOIN game_search.sell AS sell" \
                   " ON games.game_id = sell.game_id" \
                   " INNER JOIN game_search.stores AS stores ON sell.store_id = stores.store_id;"

    #app.run(debug=True)
    database_games = db.sql(query_string)
    
    for i in database_games:
        
        game_data_2 = {
            'title' : i['title'],
            'price' : i['price'],
            'initialprice' : i['initialprice'],
            'discount' : i['discount'],
            'store' : i['store_name'],
            'link' : i['link'],
            'thumbnail' : i['thumbnail']

        }
        games_list.append(game_data_2)


    games_list.sort(key=itemgetter("price"))
    #games_list = sorted(games_list, key = lambda i: i['price'])
    #Implements Search Functionality
    for i in games_list:
        i['price']=format(i['price'],".2f")
        i['initialprice']=format(i['initialprice'],".2f")

    if q:
        games_list = [games for games in games_list if q.lower() in games['title'].lower()]
        
    else:
        games_list
        
    return render_template('index1.html', games = games_list)
