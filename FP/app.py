import os
import random
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

app=Flask(__name__)

#dictionary is formatted as =question:[question id,[list of options],correct answer]
questions={"Who orchestrated The Night Of The Black Knives":["q1",["Ranni","Rykard","Maliketh","Tiche"],"Ranni"],
           "Who was the Tarnished that got the closest to becoming Elden Lord":["q2",["Vyke","Goldmask","Fia","Dungeater"],"Vyke"],
           "Which NPC takes over Bloody Finger Hunter Yura's body":["q3",["Shabriri","Patches","Kale","Gostoc"],"Shabriri"],
           "Which character fought Malenia, Blade of Miquella, to a stalemate in Caelid?":["q4",["Radahn","Messmer","Morgott","Godrick"],"Radahn"],
           "Which dragon fought with Placidusax":["q5",["Bayle","Lansseax","Fortissax","Senessax",],"Bayle"],
           "How many Legendary Armaments are in the game?":["q6",["9","16","25","3"],"9"],
           "What race is Queen Marika":["q7",["Numen","Hornsent","Nightfolk","Draconian"],"Numen"],
           "The main theme of Elden Ring is used as the OST for which of the following boss fight":["q8",["Radagon","Godfrey","Gideon","Placidusax"],"Radagon"],
           "Which of the these endings removes the influence of the Greater Will from The Lands Between":["q9",["Stars","Order","Duskborn","Fracture"],"Stars"],
           "What manga series serves as a main source of inspiration for the entire souls series":["q10",["Berserk","Vagabond","Vinland","Naruto"],"Berserk"]
           }

db = SQL("sqlite:///score.db")

user=None

#shuffle the possible options
for key,value in questions.items():
     random.shuffle(value[1])
     

@app.route("/",methods=['GET', 'POST'])
def hello():
    return render_template("index.html")

     
     



@app.route("/question" ,methods=['GET', 'POST'])
def question():
        global user
        user=request.form.get("username")

        return render_template ("question.html",questions=questions)


@app.route("/results",methods=['GET', 'POST'])
def results():
    if request.method=="POST":


        correct_answers=0
        for key,value in questions.items():
            help=request.form.get(value[0])
            if help==value[2]:
                correct_answers+=1



        usernames=db.execute("SELECT * FROM users")
        if not usernames:
             db.execute("INSERT INTO USERS(username) VALUES(?)",(user,))#insert new user into db

        
        found=False
        for i in usernames:
            if i['username']==user:
                found=True
                break
            else:
                print("no")
    
        if not found:

            db.execute("INSERT INTO USERS(username) VALUES(?)",(user,))#insert new user into db
                 

        userid=db.execute("SELECT id from users where username=?",(user))

        userid=userid[0]
        userid=userid.get('id')
        score=db.execute("SELECT * FROM scores where userid=?",(userid))


        if not score:

            db.execute("INSERT INTO scores(score,userid) VALUES(?)",(correct_answers,userid))#update new score
        else:

            score=score[0]
            score=score.get('score')
            if correct_answers>score:
                 db.execute("UPDATE scores SET score=? WHERE userid=?",correct_answers,userid)#update score for existing user
                 

        
        
                 



        return render_template("results.html",correct_answers=correct_answers)
    else:
        return 'ERERER' 


@app.route("/leaderboard",methods=['GET', 'POST'])
def leaderboard():

    board=db.execute("SELECT users.username, scores.score FROM users INNER JOIN scores ON users.id=scores.userid ORDER BY score DESC")
    #retrieve records based on descending order of score


    return render_template("leaderboard.html",board=board)