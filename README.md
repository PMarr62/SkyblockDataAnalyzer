# Skyblock Data Analyzer

**Skyblock Data Analyzer** is a program that interprets the Hypixel Skyblock API and finds profitable craft-flips.

**Status:** In active development (as of July 2025). Once the program is completed, it may be used by others through cloning this repository.

# How does this program work?

This program finds craft-flips in Hypixel Skyblock's in-game item market known as the Bazaar. Resources can be bought from the Bazaar, crafted into higher-tier or more complex items, and sold back to the Bazaar. This program tracks all possible craft-flips and returns those that are the most profitable.

The user passes in their current in-game coin count, and the program does the following for every craftable item listed on the Bazaar:

- The program looks up the current price of all items needed to craft the resulting item via the Hypixel Skyblock API.
- Given the user's in-game coin count, finds the number of resulting items that can be crafted.
- Returns a table of information to the user, containing the names of resulting items and the profit gained per craftable item.

Once the table has been returned, the user can place orders for the required items in-game, craft the desired number of items, and re-sell said items at a profit, reported by this program.

# What kind of features can I expect?

As of July 2025, this program is a command-line based program. I am looking into making an application version for easier accessibility and filtering results.