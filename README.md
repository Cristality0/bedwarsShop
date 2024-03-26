## About
This is a script that will generate a picture of a Player bedwars quickshop layout using the Hypixel API. \
Output, this is for example gamerboy80 quick shop\
![gamerboy80](/output/gamerboy80.png)
## Install
Clone this repository and install the necessary packages using
```
pip install -r requirements.txt
```
Create a .env file and paste your API key
```.env
HYPIXEL_API_KEY=YourKeyHere
```
## Usage
Simply call it and pass the usename, make sure to be in the same directory as the bedwarsshop.py file.
```
python bedwarsshop.py username
```
You can always run the help command
```
python bedwarsshop.py --help
```
For more customizations check out constants.py file. For adjusting colors, thicknesses or adding more icon support.
I did this project a few years ago and though I would rewrite it with cleaner code and more conventional structure \
Use this script at your own risk
