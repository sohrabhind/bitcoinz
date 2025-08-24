#!/usr/bin/env python
import sys

import click
from project.bitcoinz.exceptions import DepositAddressDoesntExistException, InsufficientBalanceException
from project.bitcoinz.bitcoinz_network import BitcoinZAPINetwork


@click.command()
def main(args=None):
    click.echo('Welcome to the BitcoinZ network!\n')

    help_string = """
    This BitcoinZ Network API supports the following commands:
        a) add_address address1[,address2,...]                  Add addresses to the BitcoinZ Mixer and allocate a new deposit address
        b) send [sender] [receiver] [amount]                    Send amount from sender to receiver, sender should be empty to mint 50 coins
        c) get_transactions                                     Get all transactions in the BitcoinZ Mixer
        d) get_transactions [address]                           Get all transactions associated with address in the BitcoinZ Mixer
        e) help                                                 See help docstring
        f) blank (enter)                                        Exit from this CLI tool
    """

    network = BitcoinZAPINetwork()

    while True:
        try:
            input_ = click.prompt(
                'Please enter your command',
                prompt_suffix='\n[blank to quit] > ',
                default='',
                show_default=False)

            if input_.strip() == '':
                sys.exit(0)

            if "add_address" in input_:
                command, args = input_.split(' ', 1)
                addresses = args.replace(' ', '').split(",")
                deposit_address = network.add_addresses(addresses)
                click.echo(
                '\nYou may now send BitcoinZs to address {deposit_address}. They '
                'will be mixed and sent to your destination addresses.\n'
                .format(deposit_address=deposit_address))
            
            elif "send" in input_:
                command, args = input_.split(' ', 1)
                transaction_metadata = args.split(' ')
                if len(transaction_metadata)==2:
                    sender, receiver, amount = BitcoinZAPINetwork.MINTED, transaction_metadata[0], "50"
                elif len(transaction_metadata)==3:
                    sender, receiver, amount = transaction_metadata[0], transaction_metadata[1], transaction_metadata[2]
                else:
                    raise ValueError

                network.send(sender, receiver, amount)
                click.echo(
                '\n{amount} sent from {sender} to {receiver} via BitcoinZ Mixer API.\n'
                .format(amount=amount, sender=sender, receiver=receiver))
            
            elif "get_transactions" in input_:
                output = input_.split(' ')
                if len(output) == 1:
                    click.echo("\n{}\n".format(network.get_transactions()))
                else:
                    click.echo("\n{}\n".format(network.get_transactions(output[1])))

            elif "help" in input_:
                click.echo(help_string)

            else:
                raise NotImplementedError()

        except ValueError:
            click.echo('\nMalformed input! Type help for usage.\n')

        except NotImplementedError:
            click.echo('\nCommand not found! Type help for usage.\n')
        
        except InsufficientBalanceException as e:
            click.echo('\n{}\n'.format(e))
        
        except DepositAddressDoesntExistException as e:
            click.echo('\n{}\n'.format(e))

if __name__ == '__main__':
    sys.exit(main())
