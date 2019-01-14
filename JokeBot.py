import time, csv, sys, requests, json

def deliver_joke(prompt, punchline):
    print(prompt)
    time.sleep(2)
    print(punchline)


def read_user_input():
    user_input = input('Type "next" for new joke or "quit" to quit \n')
    while(user_input != ("next" ) and user_input!=("quit")):
        user_input = input("I don't understand \n")
    return user_input == "next"

def read_jokes_from_CSV(filename):
    jokes = []
    with open(filename) as csvfile:
        jokereader = csv.reader(csvfile)
        for joke in jokereader:
            jokes.append((joke[0], joke[1]))
    return jokes

def read_jokes_from_Reddit():
    jokes = []

    r = requests.get("https://www.reddit.com/r/dadjokes.json", headers = {'User-agent': 'your bot 0.1'})
    posts = r.json()['data']['children']

    for post in posts:
        post_data = post['data']

        over_18 = post_data['over_18']
        title = post_data['title']
        selftext = post_data['selftext']

        # (title.lowercase().beginswith("why") or title.lowercase().beginswith("what") or title.lowercase().beginswith("how"))
        if(not over_18 and title.endswith('?')): 
            jokes.append((title, selftext))

    return jokes


if __name__ == "__main__":
    if(len(sys.argv) != 2):
        jokes = read_jokes_from_Reddit()
    else:
        jokes = read_jokes_from_CSV(sys.argv[1])

    if(len(jokes) == 0):
        print("No jokes found")
    else:
        joke_index = 0
        while (read_user_input() == True):
            current_joke = jokes[joke_index % len(jokes)]
            deliver_joke(current_joke[0], current_joke[1])
            joke_index += 1
