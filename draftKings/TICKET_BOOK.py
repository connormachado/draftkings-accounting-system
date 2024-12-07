class TicketBook():
    def __init__(self):
        self.cash = 0.0              # Asset
        self.tickets = []            # List of ALL tickets
        self.payouts = 0.0           # Deferred Revenue Asset
        self.outstanding_bets = 0.0  # Liability

    
    def deposit(self, amount):
        try:
            amount = float(amount)
        except Exception as e:
            raise ValueError("Deposit must be numerical.🤨")


        if amount <= 0:
            raise ValueError("Deposit must be greater than zero.🤨")
        else:
            self.cash += amount
            print(f"Deposited ${amount:.2f}. Current cash: ${self.cash:.2f}")

    
    def add_ticket(self, ticket):
        if self.cash < ticket.wager:
            print("-------------------------------------------------")
            raise ValueError("You don't have the money to make this bet.🤨")

        if any(t.ID == ticket.ID and t.date == ticket.date and t.wager == ticket.wager for t in self.tickets):
            print("-------------------------------------------------")
            raise ValueError("Error: Ticket already exists.🤨")

        self.cash -= ticket.wager               # Credit Cash
        self.payouts += ticket.payout           # Debit Deferred Revenue
        self.outstanding_bets += ticket.wager   # Debit Outstanding Bets
        self.tickets.append(ticket)
        self.recalculate()

        print("-------------------------------------------------")
        print(f"Added ticket: {ticket}. Updated cash: ${self.cash:.2f}")


    def process_win(self, ticket):
        if not ticket.settled:
            self.cash += ticket.payout              # Debit Cash 
            self.payouts -= ticket.payout           # Credit Deferred Revenue
            self.outstanding_bets -= ticket.wager   # Credit Outstanding Bets
            ticket.settle()
            self.recalculate()
        else:
            self.recalculate()
            raise ValueError("Ticket already settled🤨")
        
        

    def process_loss(self, ticket):
        if not ticket.settled:
            self.outstanding_bets -= ticket.wager   # Credit Outstanding Bets
            self.payouts -= ticket.wager            # Credit Deferred Revenue
            ticket.settle()
            self.recalculate()
        else:
            self.recalculate()
            raise ValueError("Ticket already settled🤨")


    def summary(self):
        # print(self.tickets)
        unsettled = len([ticket for ticket in self.tickets if not ticket.settled])

        print(f"Cash: ${self.cash:.2f}")
        print(f"Outstanding Bets : ${self.outstanding_bets:.2f}")
        print(f"Potential Payouts: ${self.payouts:.2f}")
        print(f"Number of Tickets: {len(self.tickets)}")
        print(f"Unsettled Tickets: {unsettled}")


    def recalculate(self):
        self.payouts = sum(ticket.payout for ticket in self.tickets if not ticket.settled)
        self.outstanding_bets = sum(ticket.wager for ticket in self.tickets if not ticket.settled)