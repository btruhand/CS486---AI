from OverlySensitiveBot_20493097 import OverlySensitiveBot

if __name__ == "__main__":
    pd_agent = OverlySensitiveBot()

    done = False
    iteration = 1
    maxiterations = 15
    agent_score = 0
    client_score = 0
    while iteration < maxiterations and not done:
        print 100*"*"
        print "game "+str(iteration)+": OverlySensitiveBot is thinking ..."
        agent_action = pd_agent.get_play()

        client_action = raw_input("your action (give 2 or take 1, anything else stops play): ")

        print "OverlySensitiveBot's action is to: ",agent_action

        

        if client_action == "give 2" or client_action == "take 1":
            pd_agent.make_play(client_action)
        else:
            done = True

        if client_action == "give 2":
            agent_score += 2
        if agent_action == "give 2":
            client_score += 2
        if agent_action == "take 1":
            agent_score += 1
        if client_action == "take 1":
            client_score += 1

        print "your score:    ",client_score," -:",client_score*"*"
        print "pd-bots score: ",agent_score," -:",agent_score*"*"
        
        iteration += 1
