from project.bitcoinz.transaction import Transaction
from . import config
from typing import List, Optional
from project.bitcoinz.mixer import Mixer, APIBasedMixer
from project.bitcoinz.exceptions import DepositAddressDoesntExistException, InsufficientBalanceException
from decimal import Decimal

class BitcoinZNetwork:
    """
    User-facing network class that interacts with the user's input.
    Extension: Polls the network to check for transactions for any deposit address on the bitcoinz Network.

    Raises:
        DepositAddressDoesntExistException
        InsufficientBalanceException
    """
    MINTED = "(new)"

    def __init__(self):        
        self.mixer = Mixer()
        self.network_minted_coins = Decimal(0)

    def add_addresses(self, addresses: List[str]) -> str:
        """
        Adds a list of addresses to the network and assigns a deposit address.

        Args:
            addresses (List[str]): A list of user's private addresses

        Returns:
            str: Unique deposit address allocated by Mixer
        """        
        return self.mixer.get_deposit_address(addresses)

    def send(self, sender: str, receiver: str, amount: str):
        """
        Send an amount from sender to receiver.

        Args:
            sender (str): Sender's deposit address
            receiver (str): Receiver's deposit address
            amount (str): Amount to be sent

        Raises:
            DepositAddressDoesntExistException: If sender's or receiver's deposit address doesn't exist in Mixer.
            InsufficientBalanceException: If sender has insufficient balance to cover amount.
        """        
        if sender != BitcoinZNetwork.MINTED and not self.mixer.contains_key(sender):
            raise DepositAddressDoesntExistException(sender)
        if not self.mixer.contains_key(receiver):
            raise DepositAddressDoesntExistException(receiver)
        if sender != BitcoinZNetwork.MINTED and self.mixer.get_balance(sender) < Decimal(amount):
            raise InsufficientBalanceException()
        
        if sender == BitcoinZNetwork.MINTED:
            self.mint_coins(amount)
            
        transaction = Transaction(sender, receiver, amount)
        is_minted = sender == BitcoinZNetwork.MINTED
        self.mixer.execute_transaction(transaction, is_minted)

    def get_transactions(self, address=None) -> str:
        """
        Returns a list of transactions associated with a given deposit address.
        If address is None, get all transactions in Mixer.

        Args:
            address ([type], optional): Deposit address associated with a wallet. Defaults to None.

        Returns:
            str: A balance and list of transactions associated with address as JSON string. If no address, get all transactions from mixer.
        """        
        return self.mixer.get_transactions(address)

    def mint_coins(self, amount: str) -> None:
        """
        Mint/mine coins from BitcoinZ Network.

        Args:
            amount (str): Number of bitcoinzs to mint
        """        
        self.network_minted_coins += Decimal(amount)

    def get_num_coins_minted(self) -> Decimal:
        """
        Returns number of coins minted by the BitcoinZ Network.

        Returns:
            Decimal: Number of bitcoinzs minted so far
        """        
        return self.network_minted_coins

    def get_fees_collected(self) -> Decimal:
        """
        Returns amount of fees that the Mixer has collected so far

        Returns:
            Decimal: Fees collected so far
        """        
        return self.mixer.get_fees_collected()

class BitcoinZAPINetwork:
    """
    User-facing network class that interacts with the user's input to call APIBasedMixer.
    """
    MINTED = "(new)"

    def __init__(self):        
        self.mixer = APIBasedMixer()

    def add_addresses(self, addresses: List[str]) -> str:
        """
        Adds a list of addresses to the network and assigns a deposit address.

        Args:
            addresses (List[str]): A list of user's private addresses

        Returns:
            str: Unique deposit address allocated by Mixer
        """        
        return self.mixer.get_deposit_address(addresses)

    def send(self, sender: str, receiver: str, amount: str) -> Optional[str]:
        """
        Send an amount from sender to receiver.

        Args:
            sender (str): Sender's deposit address
            receiver (str): Receiver's deposit address
            amount (str): Amount to be sent
        """                    
        is_minted = sender == BitcoinZAPINetwork.MINTED
        response = self.mixer.execute_transaction(sender, receiver, amount, is_minted)
        return response

    def get_transactions(self, address=None) -> str:
        """
        Returns a list of transactions associated with a given deposit address.
        If address is None, get all transactions in Mixer.

        Args:
            address ([type], optional): Deposit address associated with a wallet. Defaults to None.

        Returns:
            str: A balance and list of transactions associated with address as JSON string. If no address, get all transactions from mixer.
        """        
        return self.mixer.get_transactions(address)

    def get_fees_collected(self) -> Decimal:
        """
        Returns amount of fees that the Mixer has collected so far

        Returns:
            Decimal: Fees collected so far
        """        
        return self.mixer.get_fees_collected()