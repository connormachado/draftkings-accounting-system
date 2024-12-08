import json

def save_to_file(ticket_book, filename):
    data = {
        "cash": ticket_book.cash,
        "outstanding_bets_cash": ticket_book.outstanding_bets_cash,
        "outstanding_bets_bonus": ticket_book.outstanding_bets_bonus,
        "payouts": ticket_book.payouts,
        "tickets": [
            {
                "ID": t.ID,
                "date": t.date,
                "wager": t.wager,
                "payout": t.payout,
                "parlay": t.parlay,
                "settled": t.settled,
                "bonus_wager":t.bonus_wager,
                "won":t.won
            }
            for t in ticket_book.tickets
        ]
    }
    with open(filename, "w") as f:
        json.dump(data, f)