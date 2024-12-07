class Ticket():
    def __init__(self, ID:str, date:str, wager:float, payout:float, settled: bool=False, parlay: bool=False):
        self.ID = ID
        self.date = date
        self.parlay = parlay
        self.wager = wager
        self.payout = payout
        self.settled = settled

    def __repr__(self):
        return f" Ticket(ID={self.ID}, date={self.date}, parlay={self.parlay}, wager={self.wager}, payout={self.payout}, settled={self.settled})"
    
    def settle(self):
        self.settled = True
