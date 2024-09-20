import requests
from web3 import Web3
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Standard ABI for ERC-20 tokens
erc20_abi = '''
[
    {"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"type":"function"},
    {"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[],"type":"function"},
    {"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"type":"function"},
    {"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[],"type":"function"},
    {"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"},
    {"constant":true,"inputs":[],"name":"version","outputs":[{"name":"","type":"string"}],"type":"function"},
    {"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"},
    {"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"type":"function"},
    {"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"type":"function"},
    {"fallback":{},"type":"fallback"}
]
'''

# Function to get the current Ether price in USD
def get_eth_price():
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price', params={
            'ids': 'ethereum',
            'vs_currencies': 'usd'
        })
        data = response.json()
        eth_price = data['ethereum']['usd']
        return eth_price
    except Exception as e:
        print(Fore.RED + f"Error fetching Ether price: {e}")
        return None

# Get the current Ether price in USD
eth_price_usd = get_eth_price()
if eth_price_usd is None:
    print(Fore.RED + "Failed to retrieve current Ether price. Please check your internet connection.")
    exit()
else:
    print(Fore.GREEN + f"Current Ether price: {eth_price_usd} USD")

# Select network
print("\n" + "Select the network for transactions:")
print("1 - Ethereum Mainnet")
print("2 - Linea Mainnet")
network_choice = input("Enter the number of the chosen network (1 or 2): ")

if network_choice == '1':
    # Settings for Ethereum Mainnet
    rpc_url = 'https://mainnet.infura.io/v3/'  # Public RPC for Ethereum Mainnet
    chain_id = 1  # Chain ID for Ethereum Mainnet
    network_name = 'Ethereum Mainnet'
elif network_choice == '2':
    # Settings for Linea Mainnet
    rpc_url = 'https://rpc.linea.build'
    chain_id = 59144  # Chain ID for Linea Mainnet
    network_name = 'Linea Mainnet'
else:
    print(Fore.RED + "Invalid network selection.")
    exit()

# Connect to the selected network
w3 = Web3(Web3.HTTPProvider(rpc_url))

# Check connection
if w3.is_connected():
    print(Fore.GREEN + f"Successfully connected to {network_name}")
else:
    print(Fore.RED + f"Failed to connect to {network_name}")
    exit()

# Check if the user wants to send ETH or a token
print("\n" + "Do you want to send ETH or an ERC-20 token?")
print("1 - ETH")
print("2 - ERC-20 Token")
token_choice = input("Enter your choice (1 or 2): ")

if token_choice == '1':
    is_token = False
    currency_symbol = 'ETH' if network_choice == '1' else 'Linea ETH'
elif token_choice == '2':
    is_token = True
    # Input token contract address
    token_address_input = input("Enter the ERC-20 token contract address: ")
    try:
        token_address = w3.to_checksum_address(token_address_input)
    except Exception as e:
        print(Fore.RED + f"Invalid token contract address: {e}")
        exit()
    # Create contract object
    try:
        token_contract = w3.eth.contract(address=token_address, abi=erc20_abi)
        # Get token symbol and decimals
        currency_symbol = token_contract.functions.symbol().call()
        decimals = token_contract.functions.decimals().call()
        print(Fore.GREEN + f"Sending token: {currency_symbol} with {decimals} decimals.")
    except Exception as e:
        print(Fore.RED + f"Failed to retrieve token information: {e}")
        exit()
else:
    print(Fore.RED + "Invalid choice.")
    exit()

# Path to private keys file
private_keys_file = 'private_keys.txt'

# Path to recipients addresses file
recipients_file = 'recipients.txt'

# Read private keys from file
try:
    with open(private_keys_file, 'r') as file:
        private_keys = [line.strip() for line in file if line.strip()]
except FileNotFoundError:
    print(Fore.RED + f"File {private_keys_file} not found.")
    exit()

# Read recipient addresses from file
try:
    with open(recipients_file, 'r') as file:
        recipient_addresses = [line.strip() for line in file if line.strip()]
except FileNotFoundError:
    recipient_addresses = []

# Display the number of private keys and recipient addresses
print(Fore.YELLOW + f"\nNumber of private keys found: {len(private_keys)}")
print(Fore.YELLOW + f"Number of recipient addresses found: {len(recipient_addresses)}")

# Ask the user whether to send to one address or multiple
if len(recipient_addresses) == 0:
    to_address = input("Enter the recipient address: ")
    recipient_addresses = [to_address]
else:
    choice = input("Do you want to send to one address or multiple? (1 - one, 2 - multiple): ")
    if choice == '1':
        to_address = input("Enter the recipient address: ")
        recipient_addresses = [to_address]

# Ask the user to choose sending a specific amount or the maximum
print("\n" + "Choose the sending method:")
print("1 - Send a specific amount")
print("2 - Send the maximum possible amount")
send_choice = input("Enter your choice (1 or 2): ")

if send_choice == '1':
    # Specific amount to send
    amount_input = input(f"Enter the amount to send (in {currency_symbol}): ")
    amount_input = amount_input.replace(',', '.')
    try:
        amount_to_send = float(amount_input)
        if amount_to_send <= 0:
            print(Fore.RED + "Amount must be positive.")
            exit()
    except ValueError:
        print(Fore.RED + "Invalid number format. Please enter a valid amount.")
        exit()
    send_max = False
elif send_choice == '2':
    send_max = True
    amount_to_send = None  # To be calculated later
else:
    print(Fore.RED + "Invalid choice.")
    exit()

# Initialize variables to track total gas fees
total_gas_fees_eth = 0
total_gas_fees_usd = 0

# Process each private key
num_recipients = len(recipient_addresses)
for idx, private_key in enumerate(private_keys):
    try:
        # Get account from private key
        account = w3.eth.account.from_key(private_key)
        from_address = account.address

        recipient_index = idx % num_recipients
        to_address = recipient_addresses[recipient_index]

        print(Fore.CYAN + f"\n[{idx+1}] Sending from address {from_address} to address {to_address}")

        if not is_token:
            # Check balance in the selected network
            balance = w3.eth.get_balance(from_address)
            balance_eth = w3.from_wei(balance, 'ether')
            balance_usd = float(balance_eth) * eth_price_usd
            print(Fore.YELLOW + f"Sender's balance: {balance_eth} {currency_symbol} (~{balance_usd:.2f} USD)")

            if send_max:
                # Calculate current gas price and fee
                gas_price = w3.eth.gas_price  # Gas price in Wei
                gas_limit = 21000  # Standard gas limit for simple ETH transfer
                gas_fee_wei = gas_price * gas_limit
                gas_fee_eth = w3.from_wei(gas_fee_wei, 'ether')
                gas_fee_usd = float(gas_fee_eth) * eth_price_usd

                # Maximum amount to send
                max_amount_wei = balance - gas_fee_wei
                if max_amount_wei <= 0:
                    print(Fore.RED + "Insufficient funds to send after deducting gas fee.")
                    continue
                amount_to_send_eth = w3.from_wei(max_amount_wei, 'ether')
                print(Fore.YELLOW + f"Maximum amount to send: {amount_to_send_eth:.18f} {currency_symbol} (~{float(amount_to_send_eth) * eth_price_usd:.2f} USD)")
                amount_wei = max_amount_wei
            else:
                # Calculate amount in Wei
                amount_wei = w3.to_wei(amount_to_send, 'ether')
                # Calculate gas fee
                gas_price = w3.eth.gas_price
                gas_limit = 21000
                gas_fee_wei = gas_price * gas_limit
                gas_fee_eth = w3.from_wei(gas_fee_wei, 'ether')
                gas_fee_usd = float(gas_fee_eth) * eth_price_usd

                # Check if sufficient funds including gas fee
                total_cost = amount_wei + gas_fee_wei
                if balance < total_cost:
                    print(Fore.RED + "Insufficient funds to send including gas fee.")
                    continue

                print(Fore.YELLOW + f"Sending: {w3.from_wei(amount_wei, 'ether')} {currency_symbol} (~{float(w3.from_wei(amount_wei, 'ether')) * eth_price_usd:.2f} USD)")
                print(Fore.YELLOW + f"Transaction fee: {gas_fee_eth} {currency_symbol} (~{gas_fee_usd:.2f} USD)")

            # Build transaction
            tx = {
                'nonce': w3.eth.get_transaction_count(from_address),
                'to': to_address,
                'value': amount_wei,
                'gas': gas_limit,
                'gasPrice': gas_price,
                'chainId': chain_id
            }

            # Sign the transaction
            signed_tx = account.sign_transaction(tx)

            # Send the transaction
            tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

            if send_max:
                sent_amount_eth = w3.from_wei(amount_wei, 'ether')
                sent_amount_usd = float(sent_amount_eth) * eth_price_usd
                print(Fore.GREEN + f"Transaction sent! Hash: {tx_hash.hex()}")
                print(Fore.GREEN + f"Sent: {sent_amount_eth:.18f} {currency_symbol} (~{sent_amount_usd:.2f} USD)")
                print(Fore.GREEN + f"Transaction fee: {gas_fee_eth} {currency_symbol} (~{gas_fee_usd:.2f} USD)")

                # Add fee to total
                total_gas_fees_eth += float(gas_fee_eth)
                total_gas_fees_usd += gas_fee_usd
            else:
                sent_amount_eth = w3.from_wei(amount_wei, 'ether')
                sent_amount_usd = float(sent_amount_eth) * eth_price_usd
                print(Fore.GREEN + f"Transaction sent! Hash: {tx_hash.hex()}")
                print(Fore.GREEN + f"Sent: {sent_amount_eth} {currency_symbol} (~{sent_amount_usd:.2f} USD)")
                print(Fore.GREEN + f"Transaction fee: {gas_fee_eth} {currency_symbol} (~{gas_fee_usd:.2f} USD)")

                # Add fee to total
                total_gas_fees_eth += float(gas_fee_eth)
                total_gas_fees_usd += gas_fee_usd

        else:
            # Sending ERC-20 token
            try:
                # Check token balance
                token_balance = token_contract.functions.balanceOf(from_address).call()
                token_balance_adjusted = token_balance / (10 ** decimals)
                print(Fore.YELLOW + f"Sender's balance: {token_balance_adjusted} {currency_symbol}")

                if send_max:
                    amount_token = token_balance  # Send all tokens
                    print(Fore.YELLOW + f"Sending maximum amount of tokens: {token_balance_adjusted} {currency_symbol}")
                else:
                    # Calculate amount to send considering decimals
                    amount_token = int(amount_to_send * (10 ** decimals))
                    if token_balance < amount_token:
                        print(Fore.RED + "Insufficient tokens to send.")
                        continue
                    print(Fore.YELLOW + f"Sending: {amount_to_send} {currency_symbol}")

                if send_max:
                    # Get current gas price and set gas limit
                    gas_price = w3.eth.gas_price
                    gas_limit = 100000  # Estimated gas limit for token transfers

                    # Check if sender has enough ETH for gas fee
                    eth_balance = w3.eth.get_balance(from_address)
                    gas_fee_wei = gas_price * gas_limit
                    if eth_balance < gas_fee_wei:
                        print(Fore.RED + "Insufficient ETH to cover gas fees.")
                        continue
                    gas_fee_eth = w3.from_wei(gas_fee_wei, 'ether')
                    gas_fee_usd = float(gas_fee_eth) * eth_price_usd

                    print(Fore.YELLOW + f"Transaction fee: {gas_fee_eth} ETH (~{gas_fee_usd:.2f} USD)")

                else:
                    # Get current gas price and set gas limit
                    gas_price = w3.eth.gas_price
                    gas_limit = 100000  # Estimated gas limit for token transfers

                    # Check if sender has enough ETH for gas fee
                    eth_balance = w3.eth.get_balance(from_address)
                    gas_fee_wei = gas_price * gas_limit
                    if eth_balance < gas_fee_wei:
                        print(Fore.RED + "Insufficient ETH to cover gas fees.")
                        continue
                    gas_fee_eth = w3.from_wei(gas_fee_wei, 'ether')
                    gas_fee_usd = float(gas_fee_eth) * eth_price_usd

                    print(Fore.YELLOW + f"Transaction fee: {gas_fee_eth} ETH (~{gas_fee_usd:.2f} USD)")

                # Build transaction to call transfer function
                tx = token_contract.functions.transfer(to_address, amount_token).build_transaction({
                    'chainId': chain_id,
                    'gas': gas_limit,
                    'gasPrice': gas_price,
                    'nonce': w3.eth.get_transaction_count(from_address),
                })

                # Sign the transaction
                signed_tx = account.sign_transaction(tx)

                # Send the transaction
                tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

                if send_max:
                    sent_amount_token = token_balance_adjusted
                    print(Fore.GREEN + f"Transaction sent! Hash: {tx_hash.hex()}")
                    print(Fore.GREEN + f"Sent: {sent_amount_token} {currency_symbol}")
                    print(Fore.GREEN + f"Transaction fee: {gas_fee_eth} ETH (~{gas_fee_usd:.2f} USD)")

                    # Add fee to total
                    total_gas_fees_eth += float(gas_fee_eth)
                    total_gas_fees_usd += gas_fee_usd
                else:
                    sent_amount_token = amount_to_send
                    print(Fore.GREEN + f"Transaction sent! Hash: {tx_hash.hex()}")
                    print(Fore.GREEN + f"Sent: {sent_amount_token} {currency_symbol}")
                    print(Fore.GREEN + f"Transaction fee: {gas_fee_eth} ETH (~{gas_fee_usd:.2f} USD)")

                    # Add fee to total
                    total_gas_fees_eth += float(gas_fee_eth)
                    total_gas_fees_usd += gas_fee_usd

            except Exception as e:
                print(Fore.RED + f"Error sending token: {e}")
                continue

    except Exception as e:
        print(Fore.RED + f"Error processing private key: {e}")
        continue

# Display total gas fees
print("\n" + Fore.MAGENTA + Style.BRIGHT + "----- Total Gas Fees -----")
print(Fore.MAGENTA + f"Total gas fees: {total_gas_fees_eth} ETH (~{total_gas_fees_usd:.2f} USD)")
print(Fore.MAGENTA + "--------------------------")
