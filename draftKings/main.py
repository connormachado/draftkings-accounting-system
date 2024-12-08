import json
from TICKET import Ticket
from TICKET_BOOK import TicketBook
from save_to_file import save_to_file
from load_from_file import load_from_file

# LEDGER = "personal_ledger.json"
LEDGER = "LEDGER.json"

if __name__ == "__main__":
    print("Welcome to your DraftKings Ticket Book!")

    book = TicketBook()
    load_from_file(book, LEDGER)
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

            if type(WAGER) == str and "B:" in WAGER:
                WAGER = float( (WAGER.split(":"))[1] )
                new_ticket = Ticket(ID, DATE, WAGER, PAYOUT, parlay=PARLAY, bonus_wager=True)
            else:
                try:
                    WAGER = float( WAGER )
                    new_ticket = Ticket(ID, DATE, WAGER, PAYOUT, parlay=PARLAY)
                except ValueError as VE:
                    print(VE)
                    print("Bruh WAGER has to be either a number or B:__, where __ is the amount of the bonus(free) bet.🤨")

            book.add_ticket(new_ticket)
            save_to_file(book, LEDGER)

        elif option == "w": # Update a ticket that won
            ID = str( input("Game ID (ex BOS CELTICS): "))
            DATE = str( input("Date (mm-dd-yyyy): ") )
            WAGER = input("Wager (xx.xx): ")

            if type(WAGER) == str and "B:" in WAGER:
                WAGER = float( (WAGER.split(":"))[1] )
            else:
                try:
                    WAGER = float( WAGER )
                except ValueError as VE:
                    print(VE)
                    print("Bruh WAGER has to be either a number or B:__, where __ is the amount of the bonus(free) bet.🤨")


            if WAGER < 0:
                print("-------------------------------------------------")
                print("You can't wage nothing.🤨")

            ticket = next((t for t in book.tickets if t.date == DATE and t.ID == ID and t.wager == WAGER and not t.settled), None)

            if ticket:
                book.process_win(ticket)
                save_to_file(book, LEDGER)

                print("-------------------------------------------------")
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
                save_to_file(book, LEDGER)

                print("-------------------------------------------------")
                print("Ticket marked as lost!")
            else:
                print("No matching unsettled ticket found.")

        elif option == "s": # Summarize the book
            book.summary()
        
        elif option == "q": # Quit
            book.summary()
            break
            
        elif option == "d": #Deposit Cash
            amount = input("How much would you like to deposit (xx.xx): ")
            book.deposit(amount)
            save_to_file(book, LEDGER)