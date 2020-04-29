#Ver.1 By JamieChang
#Simulator for WoWs Ranked Mode, you can define parameters below.

import random
import matplotlib.pyplot as plt

def init():

    #Define parameters here!!
    #=======================================================================================================#
    target_rank = 1 #The rank you want to reach
    winrate = 0.9 # Type in the winrate
    init_rank = 10 # Rank the player starting with
    irrevocable_ranks = {10,9,8,5,3,1} # The set of irrevocable ranks
    stars_stat = {10:-1, 9:-2, 8:-2, 7:-2, 6:-2, 5:-3, 4:-3, 3:-3, 2:-3, 1:-1} # the stars in each rank (should be minus)
    #=======================================================================================================#

    stars_player = stars_stat.copy()
    battles = 0
    battles_list = [0]
    rank_list = [init_rank]
    stars_list = [stars_stat[init_rank]]
    return target_rank,winrate,init_rank,irrevocable_ranks,stars_stat,stars_player,battles,battles_list,rank_list,stars_list
    

def battle_result(probability):
    return int(random.choices([-1,1],[(1-probability),probability])[0])

def sim():
    target_rank,winrate,init_rank,irrevocable_ranks,stars_stat,stars_player,battles,battles_list,rank_list,stars_list = init()
    while True:
        if init_rank == target_rank:
            break
        result = battle_result(winrate)
        battles += 1
        if result == 1: # win
            stars_player[init_rank] += 1
        else: #lose
            if stars_player[init_rank] == stars_stat[init_rank]: # rank down
                if init_rank not in irrevocable_ranks:
                    init_rank += 1
                    stars_player[init_rank] = -1
            else:
                stars_player[init_rank] -= 1

        if stars_player[init_rank] == 0: #rank up
            if (init_rank in irrevocable_ranks) and (init_rank-1 in irrevocable_ranks):
                init_rank -= 1
                stars_player[init_rank] += 1
            else:
                init_rank -= 1

        battles_list.append(battles)
        rank_list.append(init_rank)
        stars_list.append(stars_player[init_rank])
    return (target_rank,winrate,init_rank,irrevocable_ranks,stars_stat,stars_player,battles,battles_list,rank_list,stars_list)


def average_battles(times):
    L = 0
    for i in range(times):
        battles = sim()[7][-1]
       # print(battles)
        L+=battles
    return int(L/times)


def plot():
    target_rank,winrate,init_rank,irrevocable_ranks,stars_stat,stars_player,battles,battles_list,rank_list,stars_list = sim()
    avg_battles = average_battles(1000)
    plt.figure(figsize=(16,9),dpi=120)
    plt.scatter(battles_list,rank_list,cmap=plt.get_cmap('cool',abs(min(stars_stat.values()))),c=stars_list,norm=plt.Normalize(vmin=min(stars_stat.values()),vmax=0))
    plt.ylim(10,0)
    plt.xticks([10*i for i in range(0,((battles_list[-1]//10)+1))], [10*i for i in range(0,((battles_list[-1]//10)+1))])
    plt.yticks([i for i in range(1,11)],[f"R{i}" for i in range(1,11)])
    plt.gca().yaxis.grid(linestyle='dotted')
    for i,v in enumerate(plt.yticks()[0]):
        if int(v) in irrevocable_ranks:
            plt.gca().get_yticklabels()[i].set_color("red")

    cb = plt.colorbar(ticks=[(-0.5-i) for i in range(abs(min(stars_stat.values())))])
    cb.ax.set_yticklabels([f"{-i-1} stars" for i in range(abs(min(stars_stat.values())))])

    text = f"Total battles:{battles_list[-1]}, Average battles (1000 rounds):{avg_battles}, Winrate:{winrate*100}%"
    plt.text(0.0,1.5,text)
    plt.title("WoWs Ranked Sprint Simulation")
    plt.xlabel("Battles")
    plt.ylabel("Rank")
    plt.show()

plot()