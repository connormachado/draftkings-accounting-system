import json
from TICKET import Ticket

def load_from_file(ticket_book, filename):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            ticket_book.cash = data.get("cash", 0.0)
            ticket_book.outstanding_bets = data.get("outstanding_bets_cash", 0.0)
            ticket_book.outstanding_bets_bonus = data.get("outstanding_bets_bonus", 0.0)
            ticket_book.payouts = data.get("payouts", 0.0)
            for entry in data.get("tickets", []):
                ticket = Ticket(
                    ID=entry["ID"],
                    date=entry["date"],
                    wager=entry["wager"],
                    payout=entry["payout"],
                    parlay=entry["parlay"],
                    settled=entry["settled"],
                    bonus_wager=entry["bonus_wager"],
                    won=entry["won"]
                )
                ticket_book.tickets.append(ticket)
    except FileNotFoundError:
        pass  # No file means no tickets yet