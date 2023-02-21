import csv

def calculate_irv_winner(votes):
    candidates = set()
    for vote in votes:
        for i in range(1, 4):
            candidate = vote["ranking[{}]".format(i)]
            if candidate:
                candidates.add(candidate)
    candidates = list(candidates)
    
    while True:
        votes_per_candidate = {candidate: 0 for candidate in candidates}
        for vote in votes:
            candidate = vote["ranking[1]"]
            if candidate:
                votes_per_candidate[candidate] += 1
        
        min_votes = min(votes_per_candidate.values())
        if min_votes == 0:
            return None
        
        losers = [candidate for candidate, votes in votes_per_candidate.items() if votes == min_votes]
        if len(losers) == 1:
            return losers[0]
        
        for vote in votes:
            for loser in losers:
                if vote["ranking[1]"] == loser:
                    for i in range(2, 4):
                        candidate = vote["ranking[{}]".format(i)]
                        if candidate and candidate not in losers:
                            vote["ranking[1]"] = candidate
                            break
        
        candidates = [candidate for candidate in candidates if candidate not in losers]

def main():
    with open("votes.csv", "r") as f:
        reader = csv.DictReader(f)
        votes = list(reader)
    
    winner = calculate_irv_winner(votes)
    if winner:
        print("The winner is: {}".format(winner))
    else:
        print("No winner could be determined.")

if __name__ == "__main__":
    main()
