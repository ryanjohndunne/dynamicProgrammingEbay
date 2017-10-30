# dynamicProgrammingEbay
Use dynamic programming to maximise profits on a list of items selling through ebay

# Description
### Maximising profit without an item limit
1. First, we take a list of product objects which have a name/price/profit (these are read in from a file named products.txt).
2. Using dynamic programming, for each value in the price limit, we find the optimal solution that value. Using the previous optimal solutions we can calculate the next.
3. Now we take all the items that were used to calculate the optimal solution, and their count, then print them to the user along with number of items sold and the total profit.

Time complexity: O(NC) Where N is the list of products and C is the price limit.
Space complexity: O(C + N) where N is the list of products and C is the price limit.

### Maxmimising profit with a limit on each item
1. Create a new list that is products * their individual limits.
2. Each time we pop one product off the list.
3. Once we've met the price limit we print the items used.

# How to run
Using python 3.6, navigate to the destination folder and run:

python ebayland.py
Enter the price limit (ebay sets price limits on how much an account can sell in one month)

Products.txt contains products the file uses, this can be changed to users desired products.
