from types import NoneType
import requests
import json
from termcolor import colored


############################################################
#startup vars
############################################################

url = "https://orientplus.ucll.be/api/"  # url to api
normal = True # true for some output false for silent
debug = True # true for extra debug info
verbose = False # true to print db
reeks = 1 # reeks number
times = 500
number = 1  # temp

############################################################
#functions to load/save data
############################################################

def load_db():
    db_content = dict()
    try:
        with open('db.txt', 'r') as db:
           db_content = json.loads(db.read())
           return db_content
    except:
        raise Exception("UNABLE TO LOAD DB FILE")


def load_auth():
    f = open("id.txt", "r")
    id = f.read()
    f.close()
    return id

def save_db(db_content):
    try:
        with open('db.txt', 'w') as db:
           db.write(json.dumps(db_content))
    except:
        raise Exception("UNABLE TO SAVE DB FILE")

############################################################
#functions for requests
############################################################

def question(id, reeks):

    payload = json.dumps({
        "query": "query($url: String!) { exercise(path: $url) { id title unlocked question { assignment renderer_id renderer_props } skills { id props skill_id skillstate { state } milestones { id won value award { icon, color } } } } }",
        "variables": {
            "url": "exercise-{}-B".format(reeks)
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'type=graduaat; id={}'.format(id)
    }

    r = requests.request("POST", url, headers=headers, data=payload).json()
    q = r["data"]['exercise']['question']['assignment']
    ex_id = r["data"]["exercise"]["id"]
    if (debug == True):
        print("----------------------------QUESTION----------------------------")
        print(q)
        print("----------------------------------------------------------------")
    return q, ex_id

def answer(id, ex_id):
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'type=graduaat; id={}'.format(id)
    }

    payload = json.dumps({
        "query": "mutation($exercise_id: Int!, $answer: JSON, $state: JSON) { submitAnswer(exercise_id: $exercise_id, answer: $answer, state: $state) { feedback question { assignment renderer_id renderer_props }   } }",
        "variables": {
            "exercise_id": ex_id,
            "answer": [0]
        }
    })

    r = requests.request("POST", url, headers=headers, data=payload).json()
    sol = r["data"]["submitAnswer"]["feedback"]["solution"]
    if (debug == True):
        print("----------------------------SOLUTION----------------------------")
        print(sol)
        print("----------------------------------------------------------------")
    return sol

############################################################
#finding best way to solve
############################################################

def best_procces(q,sol,db):
    if("words" in q and "texts" in q):
        if(debug == True):
            print("------------------------------TYPE------------------------------")
            print(colored("many ","grey")+"|"+colored(" many","grey"))
            print("----------------------------------------------------------------")
        db = many_many(q,sol,db)

    elif("text" in q and "options" in q):
        if(debug == True):
            print("------------------------------TYPE------------------------------")
            print(colored("one ","magenta")+"|"+colored(" many","grey"))
            print("----------------------------------------------------------------")
        db = one_many(q,sol,db)

    elif("image" in q and "options" in q):
        if(debug == True):
            print("------------------------------TYPE------------------------------")
            print(colored("image ","yellow")+"|"+colored(" many","grey"))
            print("----------------------------------------------------------------")
        db = image(q,sol,db)

    elif(len(q) == 1 and "text" in q or len(sol) == 1 and "text" in q):
        if(debug == True):
            print("------------------------------TYPE------------------------------")
            print(colored("only text ","blue"))
            print("----------------------------------------------------------------")
        only_text(q,sol,db)


    else:
        print("------------------------------TYPE------------------------------")
        print(colored("NO SOLVER FOUND","red"))
        print("----------------------------------------------------------------")
        raise Exception("NO SOLVER FOUND")
    return db

############################################################
#functions for proccesing

# saving as word = text (, prev)
############################################################

############################################################
# many words many texts
############################################################
def many_many(q,sol,db):
    #get words and texts
    words = q["words"]
    texts = q["texts"]
    #for i in solution numbers
    try:
        c=0
        for i in sol:
            #returns index of solution in texts
            
            #check if not -1 = no answer
            if(i != -1):
                word = words[c]
                option = texts[i]  
                #if not yet in db: add to db
                if(word not in db):
                    if(debug == True):
                        print("-----------------------------ACTION-----------------------------")
                        print(colored("adding to db","green"))
                        print("----------------------------------------------------------------")
                    answer_list = []
                    answer_list.append(option)
                    db[word] = answer_list
                #if word is in db: check value for duplicate
                elif(word in db):
                    #check for duplicate: if value is not same as now
                    if(db[word] != option):
                        if(db[word] is None):
                            raise Exception("NONETYPE IN DB")
                        prev = db[word]
                        prev.append(option)
                        #check if now + prev is not in db
                        if(db[word] != prev):
                          if(debug == True):
                              print("-----------------------------ACTION-----------------------------")
                              print(colored("adding to existing entry in db","green"))
                              print("----------------------------------------------------------------")
                          if(prev is None):
                              raise Exception(f"TRYING TO ADD NONETYPE {word}")
                          db[word] = prev
                    #check for duplicate: if value is same as now
                    elif(db[word] == option):
                        if(debug == True):
                            print("-----------------------------ACTION-----------------------------")
                            print(colored("already exists in db","grey"))
                            print("----------------------------------------------------------------")
                        #value same = skip
                        pass
            c+=1
    #exception handeling
    except Exception as e:
        print(colored("---------------------------EXCEPTION----------------------------","red"))
        print("exception = " + repr(e))
        print(i)
        print(c)
        print(colored("----------------------------------------------------------------","red"))
        raise Exception("EXCEPTION")

    return db

############################################################
# 1 word many texts
############################################################
def one_many(q,sol,db):
    # get word and options
    word = q["text"]
    options = q["options"]
    try:
        #make int from sol
        if(isinstance(sol,list)):
            sol = sol[0]
        index = int(sol)
        #get option with index of solution
        option = options[index]
        #if not in db yet
        if(word not in db):
            if(debug == True):
                print("-----------------------------ACTION-----------------------------")
                print(colored("adding to db","green"))
                print("----------------------------------------------------------------")
            #save in db
            answer_list = []
            answer_list.append(option)
            db[word] = answer_list
        #if is in db
        elif(word in db):
            #check for duplicate: if value is not same as now
            if(db[word] != option):
                    if(db[word] is None):
                        raise Exception("NONETYPE IN DB")
                    prev = db[word]
                    prev.append(option)
                    #check if now + prev is not in db
                    if(db[word] != prev):
                        if(debug == True):
                            print("-----------------------------ACTION-----------------------------")
                            print(colored("adding to existing entry in db","green"))
                            print("----------------------------------------------------------------")
                        if(prev is None):
                            raise Exception(f"TRYING TO ADD NONETYPE {prev} | {option} | {prev}")
                        db[word] = prev
            #check for duplicate: if value is same as now
            elif(db[word] == option):
                if(debug == True):
                    print("-----------------------------ACTION-----------------------------")
                    print(colored("already exists in db","grey"))
                    print("----------------------------------------------------------------")
                #value same = skip
                pass
    
    except Exception as e:
        print(colored("---------------------------EXCEPTION----------------------------","red"))
        print("exception = " + repr(e))
        print(colored("----------------------------------------------------------------","red"))
        raise Exception("EXCEPTION")

    return db

############################################################
# image
############################################################
def image(q,sol,db):
    # get word and options
    word = q["image"]
    options = q["options"]
    try:
        #make int from sol
        index = int(sol)
        #get option with index of solution
        option = options[index]
        #if not in db yet
        if(word not in db):
            if(debug == True):
                print("-----------------------------ACTION-----------------------------")
                print(colored("adding to db","green"))
                print("----------------------------------------------------------------")
            #save in db
            answer_list = []
            answer_list.append(option)
            db[word] = answer_list
        #if is in db
        elif(word in db):
            #check for duplicate: if value is not same as now
            if(db[word] != option):
                    prev = db[word]
                    prev.append(option)
                    #check if now + prev is not in db
                    if(db[word] != prev):
                        if(debug == True):
                            print("-----------------------------ACTION-----------------------------")
                            print(colored("adding to existing entry in db","green"))
                            print("----------------------------------------------------------------")
                        db[word] = prev
            #check for duplicate: if value is same as now
            elif(db[word] == option):
                if(debug == True):
                    print("-----------------------------ACTION-----------------------------")
                    print(colored("already exists in db","grey"))
                    print("----------------------------------------------------------------")
                #value same = skip
                pass
    
    except Exception as e:
        print(colored("---------------------------EXCEPTION----------------------------","red"))
        print("exception = " + repr(e))
        print(colored("----------------------------------------------------------------","red"))
        raise Exception("EXCEPTION")

    return db

############################################################
# only text
############################################################
def only_text(q,sol,db):
    word = q["text"]
    option = sol[0]

    try:
        #if not in db yet
        if(word not in db):
            if(debug == True):
                print("-----------------------------ACTION-----------------------------")
                print(colored("adding to db","green"))
                print("----------------------------------------------------------------")
            #save in db
            answer_list = []
            answer_list.append(option)
            db[word] = answer_list
        #if is in db
        elif(word in db):
            #check for duplicate: if value is not same as now
            if(db[word] != option):
                    prev = db[word]
                    prev.append(option)
                    #check if now + prev is not in db
                    if(db[word] != prev):
                        if(debug == True):
                            print("-----------------------------ACTION-----------------------------")
                            print(colored("adding to existing entry in db","green"))
                            print("----------------------------------------------------------------")
                        if(prev is None):
                            raise Exception("TRYING TO ADD NONETYPE")
                        db[word] = prev
            #check for duplicate: if value is same as now
            elif(db[word] == option):
                #value same = skip
                if(debug == True):
                    print("-----------------------------ACTION-----------------------------")
                    print(colored("already exists in db","grey"))
                    print("----------------------------------------------------------------")
                pass
    
    except Exception as e:
        print(colored("---------------------------EXCEPTION----------------------------","red"))
        print("exception = " + repr(e))
        print(colored("----------------------------------------------------------------","red"))
        raise Exception("EXCEPTION")

    return db




############################################################
#main function
############################################################

#main secuence
if (__name__ == "__main__"):
    #load stuf
    id = load_auth()
    db = load_db()
    for reeks in range(25):
        if(normal == True):
            print("-------------------------------MAIN-------------------------------")
            print(f"Currently at reeks {reeks}")
            print("----------------------------------------------------------------")        
        try:
            for i in range(times):
                #get question
                q, ex_id = question(id, reeks)
                #get answer
                sol = answer(id, ex_id)
                #find best way to save based on type of question
                db = best_procces(q,sol,db)
                if(verbose == True):
                    print("-------------------------------DB-------------------------------")
                    print(db)
                    print("----------------------------------------------------------------")
        except:
            pass
    save_db(db)

