import unittest
import os
from TICKET_BOOK import TicketBook
from TICKET import Ticket
from main import save_to_file, load_from_file  # Adjust imports as needed

class TestTicketBookSystem(unittest.TestCase):

    def setUp(self):
        """Set up a fresh ticket book and a test JSON file before each test."""
        self.test_file = "TEST_TICKET_BOOK.json"
        self.ticket_book = TicketBook()
        save_to_file(self.ticket_book, self.test_file)  # Create a clean test file

    def tearDown(self):
        """Remove the test JSON file after each test."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_valid_deposit(self):
        """Test a valid deposit."""
        self.ticket_book.deposit(100.0)
        self.assertEqual(self.ticket_book.cash, 100.0)

    def test_invalid_deposit_negative(self):
        """Test depositing a negative amount."""
        with self.assertRaises(ValueError):
            self.ticket_book.deposit(-50.0)

    def test_invalid_deposit_zero(self):
        """Test depositing zero."""
        with self.assertRaises(ValueError):
            self.ticket_book.deposit(0.0)

    def test_non_numerical_deposit(self):
        """Test depositing a non-numerical value."""
        with self.assertRaises(ValueError):
            self.ticket_book.deposit("abc")

    def test_add_ticket_with_sufficient_funds(self):
        """Test adding a ticket with sufficient funds."""
        self.ticket_book.deposit(100.0)
        ticket = Ticket(ID="1", date="2023-12-06", wager=50.0, payout=100.0, parlay=False)
        self.ticket_book.add_ticket(ticket)
        self.assertEqual(self.ticket_book.cash, 50.0)
        self.assertEqual(self.ticket_book.outstanding_bets, 50.0)
        self.assertEqual(self.ticket_book.payouts, 100.0)
        self.assertEqual(len(self.ticket_book.tickets), 1)

    def test_add_ticket_without_sufficient_funds(self):
        """Test adding a ticket without sufficient funds."""
        with self.assertRaises(ValueError):
            ticket = Ticket(ID="1", date="2023-12-06", wager=50.0, payout=100.0, parlay=False)
            self.ticket_book.add_ticket(ticket)

    def test_duplicate_ticket(self):
        """Test adding a duplicate ticket."""
        self.ticket_book.deposit(100.0)
        ticket = Ticket(ID="1", date="2023-12-06", wager=50.0, payout=100.0, parlay=False)
        self.ticket_book.add_ticket(ticket)

        with self.assertRaises(ValueError):
            duplicate_ticket = Ticket(ID="1", date="2023-12-06", wager=50.0, payout=100.0, parlay=False)
            self.ticket_book.add_ticket(duplicate_ticket)

    def test_process_win(self):
        """Test processing a winning ticket."""
        self.ticket_book.deposit(100.0)
        ticket = Ticket(ID="1", date="2023-12-06", wager=50.0, payout=100.0, parlay=False)
        self.ticket_book.add_ticket(ticket)
        self.ticket_book.process_win(ticket)
        self.assertEqual(self.ticket_book.cash, 150.0)
        self.assertEqual(self.ticket_book.outstanding_bets, 0.0)
        self.assertEqual(self.ticket_book.payouts, 0.0)

    def test_process_loss(self):
        """Test processing a losing ticket."""
        self.ticket_book.deposit(100.0)
        ticket = Ticket(ID="1", date="2023-12-06", wager=50.0, payout=100.0, parlay=False)
        self.ticket_book.add_ticket(ticket)
        self.ticket_book.process_loss(ticket)
        self.assertEqual(self.ticket_book.cash, 50.0)
        self.assertEqual(self.ticket_book.outstanding_bets, 0.0)
        self.assertEqual(self.ticket_book.payouts, 0.0)

    def test_reload_state(self):
        """Test reloading a complex state from the JSON file."""
        self.ticket_book.deposit(100.0)
        ticket = Ticket(ID="1", date="2023-12-06", wager=50.0, payout=100.0, parlay=False)
        self.ticket_book.add_ticket(ticket)
        self.ticket_book.process_win(ticket)
        save_to_file(self.ticket_book, self.test_file)

        # Reload and verify state
        loaded_book = TicketBook()
        load_from_file(loaded_book, self.test_file)
        self.assertEqual(len(loaded_book.tickets), 1)
        self.assertEqual(loaded_book.cash, 150.0)
        self.assertEqual(loaded_book.outstanding_bets, 0.0)
        self.assertEqual(loaded_book.payouts, 0.0)