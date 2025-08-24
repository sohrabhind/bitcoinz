# BitcoinZ: Crypto Mixer

**To run tests:**
```zsh
pip install pyenv # Install pyenv if not already installed
pyenv install 3.6.5 # Install Python 3.6.5 for our project
pyenv virtualenv 3.6.5 sohrabhind # Creates a new virtualenv named 'sohrabhind'
pyenv activate sohrabhind # Activate virtualenv 'sohrabhind'
pipenv install -r requirements.txt # Install requirements for project
pipenv run pytest # Run tests
```

```zsh
# From /btc-mixer run
python -m project.api_client
>>>
Welcome to the BitcoinZ network!
Please enter your command
[blank to quit] > help # Type 'help' inside tool to see list of supported commands`
```

**To interact with the application via cli:**
```zsh
# From /btc-mixer run
python -m project.cli
>>>
Welcome to the BitcoinZ network!
Please enter your command
[blank to quit] > help # Type 'help' inside tool to see list of supported commands
```
