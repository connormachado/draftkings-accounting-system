class Ticket():
    def __init__(self, ID:str, date:str, wager:float, payout:float, settled: bool=False, parlay: bool=False, bonus_wager: bool=False, won: bool=None):
        self.ID = ID
        self.date = date
        self.parlay = parlay
        self.wager = wager
        self.payout = payout
        self.settled = settled
        self.bonus_wager = bonus_wager
        self.won = won

    def __repr__(self):
        return f" Ticket || ID={self.ID}, date={self.date}, wager={self.wager}, parlay={self.parlay}, payout={self.payout}, settled={self.settled}, bonus={self.bonus_wager}, won={self.won})"
    
    def settle(self, won:bool):
        self.settled = True
        self.won = won
