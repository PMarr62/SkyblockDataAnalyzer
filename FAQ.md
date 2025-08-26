# Skyblock Data Analyzer FAQ

For any questions you may have about this application, refer here.

## How is this program's data gathered?

This program uses the Hypixel's public API for Skyblock. The API contains information such as Bazaar buy / sell prices, the number of orders active for a specific item, as well as the amount of items sold and purchased per week.

Because this API is publically listed, you do not need to provide an API key to access this data.

## What does each column mean?

- Item Name: The name of the item you will eventually sell back to the Bazaar.
- Buy Price: The maximum amount of coins you will spend at the Bazaar acquiring the necessary materials to craft the resulting items.
- Sell Price: The minimum quantity you can list your resulting items at in the "sell offer" section of the Bazaar. Note that you can list your crafted items for more, but note that it may take longer for your order to fill.
- Quantity: The amount of items you will sell back to the Bazaar.
- Profit: The profit you will make from listing your items at the minimum price reported by sell price.
- Leftover: The amount of coins you will not spend after using as many coins as possible to buy the necessary materials.
- Buy Wait: This is the amount of time, in hours, on average for your buy order of your materials to fill.
- Sell Wait: This is the amount of time, in hours, on average for your sell offer of your materials to sell.
- Total Wait: Considering Buy Wait and Sell Wait, this is the total amount of time, in hours, on average you will have to wait for your round transaction to complete.

## An item is not coming up in the search, why?

When an item does not appear in the search results, this can happen for two main reasons:

1. (The most likely): The item you are searching for is not a profitable craft flip at this current point in time. Items can fluctuate in price, and profits can scale as the days and weeks go on. In other words, crafting the desired item will result in you losing coins.
2. The item is very new to Skyblock, and I have not added the recipe to the list of recipes to check.

## An error appeared in the console, what should I do?

Open a new issue and descibe your issue. If it is reproducible, list the steps to cause the error. I will attend to fix it as soon as possible.

