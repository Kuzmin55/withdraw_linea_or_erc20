
# Bulk Token and ETH Sender

## Overview

**Bulk Token and ETH Sender** is a Python script designed to facilitate the mass distribution of ETH or any ERC-20 tokens across multiple addresses on the Ethereum Mainnet or Linea Mainnet. Whether you need to distribute funds for airdrops, rewards, or any other bulk transactions, this script provides a streamlined and efficient solution.

---

## Features

- **Multi-Network Support:** Send transactions on Ethereum Mainnet or Linea Mainnet.
- **Asset Flexibility:** Choose to send ETH or any ERC-20 token by specifying the token contract address.
- **Bulk Transactions:** Distribute funds from multiple private keys to one or multiple recipient addresses.
- **Amount Options:** Send a specific amount or the maximum possible balance (considering gas fees).
- **Gas Fee Tracking:** Automatically calculates and displays the total gas fees incurred during the transaction process.
- **Color-Coded Console Output:** Enhanced readability with color-coded messages indicating successes, errors, and important information.
- **Error Handling:** Robust error management to handle common issues like insufficient funds, invalid addresses, and transaction failures.

---

## Prerequisites

- **Python 3.6 or higher** installed on your system.
- **pip** package manager.
- **Private Keys:** Ensure you have the private keys of the sender addresses. **Handle these with utmost care.**
- **Recipient Addresses:** A list of addresses to receive the funds.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Kuzmin55/withdraw_linea_or_erc20.git
cd withdraw_linea_or_erc20
```

### 2. Install Required Libraries

Ensure you have `web3`, `requests`, and `colorama` installed. You can install them using `pip`:

```bash
pip install web3 requests colorama
```

---

## Configuration

### 1. Prepare Private Keys File

- Create a file named `private_keys.txt` in the script directory.
- Add each private key on a new line. **Ensure this file is kept secure and never shared.**

```text
your_private_key_1
your_private_key_2
your_private_key_3
```

### 2. Prepare Recipients Addresses File (Optional)

- Create a file named `recipients.txt` in the script directory.
- Add each recipient address on a new line. If you prefer to input addresses manually, you can skip creating this file or leave it empty and enter the address manually when prompted.

```text
recipient_address_1
recipient_address_2
recipient_address_3
```

---

## Usage

Run the script using Python:

```bash
python bulk_send.py
```

### Step-by-Step Instructions:

1. **Ether Price Retrieval:**
   - The script fetches the current Ether price in USD using the CoinGecko API.

2. **Select Network:**
   - Choose the network for transactions:
     - `1` - Ethereum Mainnet
     - `2` - Linea Mainnet

3. **Choose Asset Type:**
   - Decide whether to send:
     - `1` - ETH
     - `2` - ERC-20 Token

4. **If Sending ERC-20 Token:**
   - Enter the ERC-20 token contract address.
   - The script will automatically fetch the token's symbol and decimal places.

5. **Recipient Selection:**
   - If multiple recipient addresses are available in `recipients.txt`, choose whether to send to one or multiple addresses.
   - If sending to multiple addresses, the script will cycle through the list.

6. **Choose Sending Method:**
   - `1` - Send a specific amount
   - `2` - Send the maximum possible amount

7. **Enter Amount (If Applicable):**
   - If you chose to send a specific amount, input the desired amount.
   - You can use either a dot `.` or a comma `,` as the decimal separator.

8. **Transaction Processing:**
   - The script processes each private key, sending the specified asset to the chosen recipients.
   - Displays color-coded messages indicating the status of each transaction.

9. **Total Gas Fees:**
   - After processing all transactions, the script displays the total gas fees incurred in both ETH (or Linea ETH) and USD.

---

## Example Interaction

```
Current Ether price: 1800 USD

Select the network for transactions:
1 - Ethereum Mainnet
2 - Linea Mainnet
Enter the number of the chosen network (1 or 2): 2
Successfully connected to Linea Mainnet

Do you want to send ETH or an ERC-20 token?
1 - ETH
2 - ERC-20 Token
Enter your choice (1 or 2): 2
Enter the ERC-20 token contract address: 0xTokenContractAddress
Sending token: USDT with 6 decimals.

Number of private keys found: 3
Number of recipient addresses found: 2
Do you want to send to one address or multiple? (1 - one, 2 - multiple): 2

Choose the sending method:
1 - Send a specific amount
2 - Send the maximum possible amount
Enter your choice (1 or 2): 1
Enter the amount to send (in USDT): 10

[1] Sending from address 0xYourAddress1 to address 0xRecipientAddress1
Sender's balance: 50.0 USDT
Sending: 10.0 USDT (~18000.00 USD)
Transaction fee: 0.00042 ETH (~0.76 USD)
Transaction sent! Hash: 0xTransactionHash1
Sent: 10.0 USDT (~18000.00 USD)
Transaction fee: 0.00042 ETH (~0.76 USD)

[2] Sending from address 0xYourAddress2 to address 0xRecipientAddress2
Sender's balance: 30.0 USDT
Sending: 10.0 USDT (~18000.00 USD)
Transaction fee: 0.00042 ETH (~0.76 USD)
Transaction sent! Hash: 0xTransactionHash2
Sent: 10.0 USDT (~18000.00 USD)
Transaction fee: 0.00042 ETH (~0.76 USD)

[3] Sending from address 0xYourAddress3 to address 0xRecipientAddress1
Sender's balance: 5.0 USDT
Insufficient tokens to send.

----- Total Gas Fees -----
Total gas fees: 0.00084 ETH (~1.52 USD)
--------------------------
```

---

## Security Considerations

- **Protect Private Keys:** Store `private_keys.txt` securely. **Never share your private keys** or expose them in unsecured environments.
- **Verify Addresses:** Double-check recipient and token contract addresses to prevent accidental loss of funds.
- **Monitor Transactions:** Keep an eye on transaction statuses and confirmations through blockchain explorers like [Etherscan](https://etherscan.io/) or Linea's equivalent.

---

## Disclaimer

- **Educational Purpose:** This script is intended for educational and legitimate use cases only.
- **No Liability:** The author is not responsible for any losses or damages resulting from the use of this script.
- **Use at Your Own Risk:** Ensure you understand the implications of sending funds and handling private keys.


---

## Support

If you encounter any issues or have questions, feel free to reach out via Telegram or visit the [GitHub Repository](https://github.com/Kuzmin55/withdraw_linea_or_erc20).

- **Telegram:** [@gurenlagen](https://t.me/gurenlagen)


