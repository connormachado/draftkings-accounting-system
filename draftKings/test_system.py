import unittest
from io import StringIO
import sys
from TICKET import Ticket
from TICKET_BOOK import TicketBook

class TestTicketBookSystem(unittest.TestCase):

    def setUp(self):
        """Set up a fresh ticket book before each test."""
        self.ticket_book = TicketBook()

    # 🟢 1️⃣ Deposit Tests
    def test_deposit_valid_amount(self):
        """Test depositing a valid amount."""
        self.ticket_book.deposit(100)
        self.assertEqual(self.ticket_book.cash, 100)

    def test_deposit_invalid_amount(self):
        """Test deposit with non-numerical input."""
        captured_output = StringIO()
        sys.stdout = captured_output

        self.ticket_book.deposit('abc')

        sys.stdout = sys.__stdout__
        self.assertIn("Deposit must be numerical.🤨", captured_output.getvalue())
        self.assertEqual(self.ticket_book.cash, 0)  # Cash shouldn't change

    def test_deposit_negative_amount(self):
        """Test deposit with negative amount."""
        captured_output = StringIO()
        sys.stdout = captured_output

        self.ticket_book.deposit(-50)

        sys.stdout = sys.__stdout__
        self.assertIn("Deposit must be greater than zero.🤨", captured_output.getvalue())
        self.assertEqual(self.ticket_book.cash, 0)  # Cash shouldn't change

    def test_deposit_zero_amount(self):
        """Test deposit with zero amount."""
        captured_output = StringIO()
        sys.stdout = captured_output

        self.ticket_book.deposit(0)

        sys.stdout = sys.__stdout__
        self.assertIn("Deposit must be greater than zero.🤨", captured_output.getvalue())
        self.assertEqual(self.ticket_book.cash, 0)  # Cash shouldn't change

    # 🟢 2️⃣ Add Ticket Tests
    def test_add_ticket_with_sufficient_funds(self):
        """Test adding a cash wager ticket."""
        self.ticket_book.deposit(50)
        ticket = Ticket(ID="1", date="12-08-2024", wager=20, payout=40)
        self.ticket_book.add_ticket(ticket)
        self.assertEqual(len(self.ticket_book.tickets), 1)
        self.assertEqual(self.ticket_book.cash, 30)  # 50 - 20 = 30
        self.assertEqual(self.ticket_book.outstanding_bets_cash, 20)

    def test_add_ticket_with_insufficient_funds(self):
        """Test adding a ticket without enough cash."""
        captured_output = StringIO()
        sys.stdout = captured_output

        ticket = Ticket(ID="1", date="12-08-2024", wager=50, payout=100)
        self.ticket_book.add_ticket(ticket)

        sys.stdout = sys.__stdout__
        self.assertIn("You don't have the money to make this bet.🤨", captured_output.getvalue())
        self.assertEqual(len(self.ticket_book.tickets), 0)  # No ticket should be added

    def test_add_duplicate_ticket(self):
        """Test adding a duplicate ticket."""
        captured_output = StringIO()
        sys.stdout = captured_output

        self.ticket_book.deposit(50)
        ticket1 = Ticket(ID="1", date="12-08-2024", wager=20, payout=40)
        self.ticket_book.add_ticket(ticket1)
        self.ticket_book.add_ticket(ticket1)  # Try to add the same ticket

        sys.stdout = sys.__stdout__
        self.assertIn("Error: Ticket already exists.🤨", captured_output.getvalue())
        self.assertEqual(len(self.ticket_book.tickets), 1)  # Only 1 ticket should be added

    # 🟢 3️⃣ Bonus Ticket Tests
    def test_add_bonus_ticket(self):
        """Test adding a bonus wager ticket."""
        ticket = Ticket(ID="B1", date="12-08-2024", wager=20, payout=40, bonus_wager=True)
        self.ticket_book.add_ticket(ticket)
        self.assertEqual(len(self.ticket_book.tickets), 1)
        self.assertEqual(self.ticket_book.outstanding_bets_bonus, 20)

    # 🟢 4️⃣ Win/Loss Ticket Processing Tests
    def test_process_win_ticket(self):
        """Test processing a winning ticket."""
        self.ticket_book.deposit(50)
        ticket = Ticket(ID="1", date="12-08-2024", wager=20, payout=40)
        self.ticket_book.add_ticket(ticket)
        self.ticket_book.process_win(ticket)
        self.assertEqual(ticket.settled, True)
        self.assertEqual(ticket.won, True)
        self.assertEqual(self.ticket_book.cash, 70)  # 50 - 20 + 40 = 70
        self.assertEqual(self.ticket_book.outstanding_bets_cash, 0)

    def test_process_loss_ticket(self):
        """Test processing a losing ticket."""
        self.ticket_book.deposit(50)
        ticket = Ticket(ID="1", date="12-08-2024", wager=20, payout=40)
        self.ticket_book.add_ticket(ticket)
        self.ticket_book.process_loss(ticket)
        self.assertEqual(ticket.settled, True)
        self.assertEqual(ticket.won, False)
        self.assertEqual(self.ticket_book.cash, 30)  # 50 - 20 = 30
        self.assertEqual(self.ticket_book.outstanding_bets_cash, 0)

    # 🟢 5️⃣ Summary Check Tests
    def test_summary_correct_values(self):
        """Test the summary after adding and processing multiple tickets."""
        self.ticket_book.deposit(100)
        ticket1 = Ticket(ID="1", date="12-08-2024", wager=20, payout=40)
        ticket2 = Ticket(ID="2", date="12-08-2024", wager=10, payout=30, bonus_wager=True)
        self.ticket_book.add_ticket(ticket1)
        self.ticket_book.add_ticket(ticket2)
        self.ticket_book.process_win(ticket1)
        self.ticket_book.process_loss(ticket2)

        self.assertEqual(self.ticket_book.cash, 120)  # 100 - 20 + 40 = 120
        self.assertEqual(self.ticket_book.outstanding_bets_cash, 0)
        self.assertEqual(self.ticket_book.outstanding_bets_bonus, 0)
        self.assertEqual(len(self.ticket_book.tickets), 2)

    # 🟢 6️⃣ Recalculation Tests
    def test_recalculate(self):
        """Test the recalculate method for all balances."""
        self.ticket_book.deposit(100)
        ticket1 = Ticket(ID="1", date="12-08-2024", wager=20, payout=40)
        ticket2 = Ticket(ID="2", date="12-08-2024", wager=10, payout=30, bonus_wager=True)
        self.ticket_book.add_ticket(ticket1)
        self.ticket_book.add_ticket(ticket2)
        self.ticket_book.process_win(ticket1)
        self.ticket_book.recalculate()

        self.assertEqual(self.ticket_book.cash, 120)
        self.assertEqual(self.ticket_book.outstanding_bets_cash, 0)
        self.assertEqual(self.ticket_book.outstanding_bets_bonus, 10)
        self.assertEqual(self.ticket_book.payouts, 30)  # From ticket2

if __name__ == "__main__":
    unittest.main()
