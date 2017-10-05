# Arbpy

Arbpy is a simple script that take the btc price from Bitstamp, convert to BRL and compare with BRL btc (There's a big spread between btc in USD and btc in Brazil) and look for a more profitable offer on Localbitcoins. After compare everything, if the profit is inside the profit (You set it) then you will receive a SMS. 

## Running the application

```
# Clone this repository
git clone https://github.com/CoinsOfPixel/arbpy.git

# Go to the project folder
cd arbpy

# Create a virtual enviroment
virtualenv venv

# Activate the virtual enviroment
source venv/bin/activate

# Install the requirements
pip install -r requirements.txt

# Run the application
python arbpy.py
```
