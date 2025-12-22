MILLION = 10**6

def lottery_avg_reward(reward: int = 5*MILLION, numtickets: int = 10*MILLION, cost: float = 1.75, numwinning = 2):
    print("With", numtickets//MILLION, "million tickets which each cost", cost, "bucks when there are only\n", numwinning, "winning tickets with an award of", reward//MILLION, "million bucks:")
    average_result = round((numwinning*(-cost + reward) + (-cost)*(numtickets-numwinning))/numtickets, 2)
    print("Avg. lottery award is", average_result)

if __name__ == "__main__":
    lottery_avg_reward()
    lottery_avg_reward(reward=30*MILLION, cost=3.50, numwinning=10, numtickets=100*MILLION)
