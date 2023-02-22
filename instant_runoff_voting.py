import csv
import random


def get_seed(votes: list[dict]) -> int:
    seed = 0
    for vote in votes:
        seed += int(vote['seed'])
    return seed


def convert_votes(votes: list[dict]) -> list[list]:
    new_votes = []
    n_rankings = len(votes[0]) - 1
    for vote in votes:
        new_vote = []
        for i in range(1, n_rankings + 1):
            new_vote.append(vote[f"ranking[{i}]"])
        new_votes.append(new_vote)
    return new_votes


def get_candidates(votes: list[list]) -> list:
    # Calculate number of rankings
    n_rankings = len(votes[0])
    # Get set of all candidates
    candidates = set()
    for vote in votes:
        for i in range(n_rankings):
            candidate = vote[i]
            if candidate:
                candidates.add(candidate)
    return list(sorted(candidates))


def remove_loser(votes: list[list], loser: str) -> list[list]:
    for vote in votes:
        if loser in vote:
            vote.remove(loser)
        else:
            # If loser not in vote, remove standin to preserve length of entries
            vote.remove('')
    return votes


def get_votes_per_candidate(candidates: list, votes: list[list], depth: int = 0) -> dict[str, int]:
    votes_per_candidate = {candidate: 0 for candidate in candidates}
    for vote in votes:
        candidate = vote[depth]
        if candidate and candidate in candidates:
            votes_per_candidate[candidate] += 1
    return votes_per_candidate


def get_losers(votes_per_candidate: dict[str, int]) -> list[str]:
    min_votes = min(votes_per_candidate.values())
    return [candidate for candidate, votes in votes_per_candidate.items() if votes == min_votes]


def irv_step(votes: list[list]) -> list[list]:
    candidates = get_candidates(votes)
    votes_per_candidate = get_votes_per_candidate(candidates, votes)
    potential_losers = get_losers(votes_per_candidate)

    print('Votes per candidate', votes_per_candidate)
    print('Potential losers', potential_losers)
    # Check deeper if zeroth order leads to tie
    depth = 1
    while len(potential_losers) > 1 and depth <= len(votes[0]) - 1:
        candidates = potential_losers
        votes_per_candidate = get_votes_per_candidate(candidates, votes, depth)
        potential_losers = get_losers(votes_per_candidate)
        depth += 1

    if len(potential_losers) == 1:
        votes = remove_loser(votes, potential_losers[0])
    else:
        # Choose randomly if tie persists
        print('Random choice!')
        loser = random.choice(potential_losers)
        votes = remove_loser(votes, loser)
    return votes


def calculate_irv_winner(votes):
    candidates = get_candidates(votes)
    while len(candidates) > 1:
        votes = irv_step(votes)
        candidates = get_candidates(votes)
    print(f'{candidates[0]} has won. Congratulations!')


def main():
    with open("votes.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        votes = list(reader)
    seed = get_seed(votes)
    votes = convert_votes(votes)
    calculate_irv_winner(votes)


if __name__ == "__main__":
    main()
