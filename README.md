# Skyblock Data Analyzer

**Skyblock Data Analyzer** is a program that interprets the Hypixel Skyblock API and finds profitable craft-flips in the Bazaar.

![Demo image of Skyblock Data Analyzer](resources/sda_demo.png?raw=true)

## How does this program work?

This program finds craft-flips in Hypixel Skyblock's in-game item market known as the Bazaar. Resources can be bought from the Bazaar, crafted into higher-tier or more complex items, and sold back to the Bazaar. This program tracks all possible craft-flips and returns those that are the most profitable.

The user passes in their current in-game coin count, and the program does the following for every craftable item listed on the Bazaar:

- The program looks up the current price of all items needed to craft the resulting item via the Hypixel Skyblock API.
- Given the user's in-game coin count, finds the number of resulting items that can be crafted.
- Returns a table of information to the user, containing the names of resulting items and the profit gained per craftable item.

Once the table has been returned, the user can place orders for the required items in-game, craft the desired number of items, and re-sell said items at a profit, reported by this program.

## How can I install this program?

**Step 1: Clone this repository to a directory on your machine:**

``` bash
cd your/directory
git clone https://github.com/PMarr62/SkyblockDataAnalyzer.git
``` 

**Step 2: Create a virtual environment to install program dependencies and libraries.**

If you are on Windows, run this:

```powershell
python -m venv .venv
.venv\Scripts\Activate
```

If you are on Linux / macOS, run this:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Step 3: Install dependencies:**

```bash
pip install -r requirements.txt
```

You have now successfully installed the program and activated the virtual environment. To run the program, simply run:

```bash
python main.py
```

## What kind of features does this program offer?

Apart from allowing you to access and easily interpret the Hypixel Skyblock API, this application offers many ease-of-access features for your convenience:

- Sorting data table by a respective column, simply by clicking the column.
- Searching for a specific item by typing its name in the search bar.
- Automatically filters out negative profit flips.
- Light / dark mode for user convenience.
- Ability to export table as a CSV file.

If you would like to report any bugs in this program or request new features, please create a new issue and let me know! Thank you for your support!