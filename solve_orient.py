def setup(self):

    import requests
    import json
    from termcolor import colored
    import ast
    self.solution_list = dict()

    try:
        with open('db.txt', 'r') as db:
            self.solution_list = json.loads(db.read())
    except:
        print("")
        self.solution_list = dict()




def words_solve(self):
    import requests
    import json
    from termcolor import colored
    print(len(self.words))
    for i in self.words:
        try:
            try:
                print(colored(i,"blue"))
                print(colored(self.solution_list[i],"yellow"))
                if(isinstance(self.solution_list[i], list)):
                    for o in self.solution_list[i]:
                        
                        if(self.texts.count(o) > 0):
                            print(colored("found answer","green"))
                            print(o)
                            self.answers[i] = o
                            #print(o)
                else:
                    sol = self.solution_list[i]
                    #print(colored(sol,"yellow"))
                    if(self.texts.count(sol) > 0):
                        print(colored("found answer","green"))
                        self.answers[i] = sol
                        print(sol)
                print("--------------------------------")
            except:

                print("no answer")
                print("--------------------------------")
        except:
            print("mayor error in other solver")
    return self.answers













def main_solve(self):
    import requests
    import json
    from termcolor import colored
    self.url = "https://orientplus.ucll.be/api/"

    self.payload = json.dumps({
    "query": "query($url: String!) { exercise(path: $url) { id title unlocked question { assignment renderer_id renderer_props } skills { id props skill_id skillstate { state } milestones { id won value award { icon, color } } } } }",
    "variables": {
        "url": self.reeks
    }
    })
    self.headers = {
    'Content-Type': 'application/json',
    'Cookie': 'id={};  type=graduaat'.format(self.id)
    }

    self.response = requests.request("POST", self.url, headers=self.headers, data=self.payload).json()


    #print(response)

    self.texts = []
    c=0
    try:
        for i in self.response["data"]["exercise"]["question"]["assignment"]["texts"]:
            #print(str(c) + ")" + str(response["data"]["exercise"]["question"]["assignment"]["texts"][c]))
            self.texts.append(self.response["data"]["exercise"]["question"]["assignment"]["texts"][c])
            c = c + 1
    except:
        try:
            self.texts.append(self.response["data"]["exercise"]["question"]["assignment"]["text"])
        except:
            self.texts.append(self.response["data"]["exercise"]["question"]["assignment"]["image"])
            #blank(response["data"]["exercise"]["id"])
            



    c=0
    self.words = []
    #get all answer options
    try:
        for i in self.response["data"]["exercise"]["question"]["assignment"]["words"]:
            #print(c)
            self.words.append(self.response["data"]["exercise"]["question"]["assignment"]["words"][c])
            c = c + 1
    except:
        self.words.append(self.response["data"]["exercise"]["question"]["assignment"]["options"])


    self.answers = dict()
    
    if(isinstance(self.words[0], list)):
        self.words = self.words[0]

    print(colored(self.texts, "yellow"))
    print(colored(self.words, "red"))



    #for every question
    for i in self.texts:
        try:
            print(colored(i,"blue"))
            if(".jpg" in self.solution_list[i]):
                self.image_urls=self.solution_list[i].split(",", 1)
                for i in self.image_urls:
                    if(".jpg" in i):
                        self.solution_list[i] = i.strip()
            print(colored(self.solution_list[i],"yellow"))
            if(isinstance(self.solution_list[i], list)):
                for o in self.solution_list[i]:
                    print(self.words.count(o))
                    if(self.words.count(o) > 0):
                        print(colored("found answer","green"))
                        print(o)
                        self.answers[i] = o
                        #print(o)
            else:
                sol = self.solution_list[i]
                #print(colored(sol,"yellow"))
                print(self.words.count(sol))
                if(self.words.count(sol) > 0):
                    print(colored("found answer","green"))
                    self.answers[i] = sol
                    print(sol)
            print("--------------------------------")
        except:

            print("no answer")
            print("--------------------------------")


    if(len(self.answers) == 0):
        print("no answers found trying other way")
        self.answers = words_solve(self)
        

    print(self.answers)
    return self.answers  



    # url = "https://orientplus.ucll.be/api/"

    # if(len(texts) == 1):
    #         payload = json.dumps({
    #         "query": "mutation($exercise_id: Int!, $answer: JSON, $state: JSON) { submitAnswer(exercise_id: $exercise_id, answer: $answer, state: $state) { feedback question { assignment renderer_id renderer_props }   } }",
    #         "variables": {
    #             "exercise_id": response["data"]["exercise"]["id"],
    #             "answer":ans
    # }
    # })
    # else:
    #     payload = json.dumps({
    #     "query": "mutation($exercise_id: Int!, $answer: JSON, $state: JSON) { submitAnswer(exercise_id: $exercise_id, answer: $answer, state: $state) { feedback question { assignment renderer_id renderer_props }   } }",
    #     "variables": {
    #         "exercise_id": response["data"]["exercise"]["id"],
    #         "answer":answers
    #     }
    #     })
    # #print(payload)
    # response = requests.request("POST", url, headers=headers, data=payload).json()

    # print(response)

    # solution = response["data"]["submitAnswer"]["feedback"]["solution"]


    # c=0
    
    # #print("--------------------------------------------------")
    # if(isinstance(solution,int)):

    #     #print(str(words[0][solution]) + " = " + str(texts[0]))
    #     solution_list[texts[0]] = words[0][solution]

    # else:
    #     for i in solution:
    #         if(i != -1):
    #         #    print(str(words[c]) + " = " + str(texts[i]))
    #             solution_list[texts[i]] = words[c]
    #         c=c+1

    
    words = []
    texts = []
    #print("########################################################################################")


