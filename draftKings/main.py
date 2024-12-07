import json
from TICKET import Ticket
from TICKET_BOOK import TicketBook

LEDGER = "personal_ledger.json"

def save_to_file(ticket_book, filename=LEDGER):
    data = {
        "cash": ticket_book.cash,
        "outstanding_bets": ticket_book.outstanding_bets,
        "payouts": ticket_book.payouts,
        "tickets": [
            {
                "ID": t.ID,
                "date": t.date,
                "wager": t.wager,
                "payout": t.payout,
                "parlay": t.parlay,
                "settled": t.settled,
                "bonus_wager":t.bonus_wager
            }
            for t in ticket_book.tickets
        ]
    }
    with open(filename, "w") as f:
        json.dump(data, f)


def load_from_file(ticket_book, filename=LEDGER):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            ticket_book.cash = data.get("cash", 0.0)
            ticket_book.outstanding_bets = data.get("outstanding_bets", 0.0)
            ticket_book.payouts = data.get("payouts", 0.0)
            for entry in data.get("tickets", []):
                ticket = Ticket(
                    ID=entry["ID"],
                    date=entry["date"],
                    wager=entry["wager"],
                    payout=entry["payout"],
                    parlay=entry["parlay"],
                    settled=entry["settled"],
                    bonus_wager=entry["bonus_wager"]
                )
                ticket_book.tickets.append(ticket)
    except FileNotFoundError:
        pass  # No file means no tickets yet

if __name__ == "__main__":
    print("Welcome to your DraftKings Ticket Book!")

    book = TicketBook()
    load_from_file(book)
    book.recalculate()


    while(True):
        print("-------------------------------------------------")
        print(f"Cash: {book.cash}")
        option = input("Add Ticket (a), Ticket Won (w), Ticket Lost (l), Summary (s), Quit (q), Deposit (d): ")
        print("-------------------------------------------------")


        if option == "a": # Add a new ticket
            print("Fill out ticket info...")
            ID = str( input("Game ID (ex BOS CELTICS): "))
            DATE = str( input("Date (mm-dd-yyyy): ") )
            WAGER = input("Wager (xx.xx): ") # Logic to handle bad inputs ✅
            PAYOUT = float( input("Payout (xx.xx): ") )
            PARLAY = False if input("Parlay (t/f): ") == "f" else True

            if type(WAGER) == str:
                if "B:" in WAGER:
                    WAGER = float( (WAGER.split(":"))[1] )
                    new_ticket = Ticket(ID, DATE, WAGER, PAYOUT, PARLAY, bonus_wager=True)
                else:
                    print("Bruh WAGER has to be either a number or B:__, where __ is the amount of the bonus(free) bet.🤨")
            else:
                try:
                    WAGER = float( WAGER )
                    new_ticket = Ticket(ID, DATE, WAGER, PAYOUT, PARLAY)
                except ValueError as VE:
                    print(VE)
                    print("Bruh WAGER has to be either a number or B:__, where __ is the amount of the bonus(free) bet.🤨")

            book.add_ticket(new_ticket)

            save_to_file(book)

        elif option == "w": # Update a ticket that won
            ID = str( input("Game ID (ex BOS CELTICS): "))
            DATE = str( input("Date (mm-dd-yyyy): ") )
            WAGER = input("Wager (xx.xx): ")

            if type(WAGER) == str:
                if "B:" in WAGER:
                    WAGER = float( (WAGER.split(":"))[1] )
                else:
                    print("Bruh WAGER has to be either a number or B:__, where __ is the amount of the bonus(free) bet.🤨")
            else:
                try:
                    WAGER = float( WAGER )
                    new_ticket = Ticket(ID, DATE, WAGER, PAYOUT, PARLAY)
                except ValueError as VE:
                    print(VE)
                    print("Bruh WAGER has to be either a number or B:__, where __ is the amount of the bonus(free) bet.🤨")


            if WAGER < 0:
                print("-------------------------------------------------")
                print("You can't wage nothing.🤨")

            ticket = next((t for t in book.tickets if t.date == DATE and t.ID == ID and t.wager == WAGER and not t.settled), None)

            if ticket:
                book.process_win(ticket)
                save_to_file(book)

                print("Ticket marked as WON!")
            else:
                print("-------------------------------------------------")
                print("No matching unsettled ticket found.🤨")
        

        elif option == "l": # Update a ticket that lost
            ID = str( input("Game ID (ex BOS CELTICS): "))
            DATE = str( input("Date (mm-dd-yyyy): ") )
            WAGER = float( input("Wager (xx.xx): ") )

            ticket = next((t for t in book.tickets if t.date == DATE and t.ID == ID and t.wager == WAGER and not t.settled), None)

            if ticket:
                book.process_loss(ticket)
                save_to_file(book)

                print("Ticket marked as lost!")
            else:
                print("No matching unsettled ticket found.")

        elif option == "s": # Summarize the book
            book.summary()
        
        elif option == "q": # Quit
            book.summary()
            break
            
        elif option == "d": #Deposit Cash
            print("-------------------------------------------------")
            amount = input("How much would you like to deposit (xx.xx): ")

            try:
                book.deposit(amount)
            except ValueError as e:
                print(e)
