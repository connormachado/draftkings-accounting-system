class TicketBook():
    def __init__(self):
        self.cash = 0.0                     # Asset
        self.tickets = []                   # List of ALL tickets
        self.payouts = 0.0                  # Deferred Revenue Asset
        self.outstanding_bets_cash = 0.0    # Liability
        self.outstanding_bets_bonus = 0.0   # SUPER ASSET FREE MONEY

    
    def deposit(self, amount):
        try:
            try:
                amount = float(amount)
            except Exception as e:
                raise ValueError("Deposit must be numerical.🤨")


            if amount <= 0:
                raise ValueError("Deposit must be greater than zero.🤨")
            else:
                self.cash += amount
                self.cash = round(self.cash, 2)
                print(f"Deposited ${amount:.2f}. Current cash: ${self.cash:.2f}")
        except ValueError as e:
            print(e)

    
    def add_ticket(self, ticket):
        try:
            if not ticket.bonus_wager:

                if self.cash < ticket.wager or self.cash == 0:
                    print("-------------------------------------------------")
                    raise ValueError("You don't have the money to make this bet.🤨")

                if any(t.ID == ticket.ID and t.date == ticket.date and t.wager == ticket.wager for t in self.tickets):
                    print("-------------------------------------------------")
                    raise ValueError("Error: Ticket already exists.🤨")

                self.cash -= ticket.wager               # Credit Cash
                self.outstanding_bets_cash += ticket.wager   # Debit Outstanding Bets
            
            else:
                self.outstanding_bets_bonus += ticket.wager
            
            self.payouts += ticket.payout           # Debit Deferred Revenue
            self.tickets.append(ticket)
            self.recalculate()

            print("-------------------------------------------------")
            print(f"Added ticket: {ticket}. Updated cash: ${self.cash:.2f}")
        except ValueError as e:
            print(e)


    def process_win(self, ticket):
        if not ticket.settled:
            self.cash += ticket.payout              # Debit Cash 
            self.payouts -= ticket.payout           # Credit Deferred Revenue
            if not ticket.bonus_wager:
                self.outstanding_bets_cash -= ticket.wager   # Credit Outstanding Bet Cash
            else:
                self.outstanding_bets_bonus -= ticket.wager  # Credit Outstanding Bet Bonus

            ticket.settle(won=True)
            self.recalculate()
        else:
            self.recalculate()
            raise ValueError("Ticket already settled🤨")
        
        

    def process_loss(self, ticket):
        if not ticket.settled:
            if not ticket.bonus_wager:
                self.outstanding_bets_cash -= ticket.wager   # Credit Outstanding Bets Cash
            else:
                self.outstanding_bets_bonus -= ticket.wager  # Credit Outstanding Bets Bonus Bets
            
            self.payouts -= ticket.wager            # Credit Deferred Revenue
            ticket.settle(won=False)
            self.recalculate()
        else:
            self.recalculate()
            raise ValueError("Ticket already settled🤨")


    def summary(self):
        # print(self.tickets)
        unsettled = len([ticket for ticket in self.tickets if not ticket.settled])

        print(f"Cash: ${round(self.cash, 2):.2f}")
        print(f"Outstanding Bets (Cash Wagers): ${self.outstanding_bets_cash:.2f}")
        print(f"Outstanding Bets (Bonus Wagers): ${self.outstanding_bets_bonus:.2f}")
        print(f"Potential Payouts: ${self.payouts:.2f}")
        print(f"Number of Tickets: {len(self.tickets)}")
        print(f"Unsettled Tickets: {unsettled}")


    def recalculate(self):
        self.payouts = sum(t.payout for t in self.tickets if not t.settled)
        self.outstanding_bets_cash = sum(t.wager for t in self.tickets if not t.settled and not t.bonus_wager)
        self.outstanding_bets_bonus = sum(t.wager for t in self.tickets if t.bonus_wager and not t.settled)