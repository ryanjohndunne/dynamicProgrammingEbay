"""
1. Take input file
2. Show maximum profit when there is no product limit
3. Show maximum profit with both product limit and price limit

"""
# groups all the items into one position for printing
from itertools import groupby


class productObj(object):
    def __init__(
        self,
        productID=None,
        productName=None,
        productPrice=None,
        productProfit=None,
        productLimit=None
    ):
        self.productID = productID
        self.productName = productName
        self.productPrice = productPrice
        self.productProfit = productProfit
        self.productLimit = productLimit


def readInFile(productList, itemLimit):
    """ Read in file, storing each line as an object
        which has ID, name, price and profit """
    with open('products.txt') as f:
        for line in f:
            line = line.rstrip()
            splitLine = line.split(':')
            product = productObj()

            product.productID = splitLine[0]
            product.productName = splitLine[1]
            product.productPrice = int(splitLine[2])
            product.productProfit = int(splitLine[3])
            product.productLimit = itemLimit

            productList.append(product)


def printProfit1(items, priceLimit, productList, memo, dollar):
    # Takes a list of items used in maximizeProfit1
    # + the price limit, + the list of products
    # prints out the used products in the maximizeProfit1
    # function
    # Time Complexity = O(n+k) where n is the price limit
    # and k is the size of the product list

    limit = priceLimit - 1
    instances = [0] * len(productList)

    # While there's still dollars left in the price limit
    while limit >= 0:
        currentItem = items[limit]

        # Positions that aren't used are set to -1
        if(currentItem != -1):
            instances[currentItem] += 1
            limit -= productList[items[limit]].productPrice
        else:
            # -1 has been detected so we've gone top-down
            # to the end of the list of used words
            break

    print("\nStrategy for price limit only")
    print("*******************************")

    # Prints out every instance that occurs at least once
    # It will *most likely* print the highest occuring value first
    # There are some values where it won't, for example: 23
    totalPrice = 0
    itemCount = 0
    for i in range(0, len(productList)):
        if instances[i] > 0:
            # I know, this is really ugly, but for whatever reason str(intValue)
            # would not let me concatenate for whatever reason, so uhhh,
            # this will do...
            print(instances[i], end='')
            print(" X ['", end='')
            print(productList[i].productName, end='')
            print("', ", end='')
            print(productList[i].productPrice, end='')
            print(", ", end='')
            print(productList[i].productProfit, end='')
            print("]")
            totalPrice += (productList[i].productPrice * instances[i])
            itemCount += instances[i]

    print("Total Price of items sold: ", totalPrice)
    print("Total Items sold: ", itemCount)
    print("Total Profit: " + str(memo[dollar]))


def maximizeProfit1(productList, priceLimit):
    # Takes a list of products to use
    # calculates the maximum profit to be made from these
    # products for any given price limit. Item's can be
    # reused an unlimited amount of times.
    # Time complexity = O(NC) Where n is the list of products and C is the price limit
    # Space complexity = O(C + N) Where n is the list of products and C is the price limit
    memo = [0] * (priceLimit + 1)
    items = [0 for i in range(priceLimit)]
    items[0] = -1

    # For each dollar in the price limit, calculate the highest profit
    # that can be made to reach that dollar value
    for dollar in range(1, priceLimit):
        # Items contains a list of what we've used,
        # set it to the previous value so if it doesn't change
        # it will be -1 and we don't have to go through the entire list
        # of items to know when it ends. (-1 denotes not used)
        items[dollar] = items[dollar - 1]

        # The maxValue is the best value that makes up the current dollar value
        maxValue = memo[dollar - 1]

        # Check against each product in the product list if a better fit exists
        for i in range(1, len(productList)):
            val = dollar - productList[i].productPrice
            # if the value is above 0, and it's better profit than the current
            # maxValue, we get it's value and save it as maxValue
            if val >= 0 and memo[val] + productList[i].productProfit > maxValue:
                # Better max value has been found
                maxValue = memo[val] + productList[i].productProfit
                # Store which product we used into the array of used items
                items[dollar] = i

        # memoization list contains all the maxValues from 1->priceLimit
        memo[dollar] = maxValue

    # Print out all the items that were used
    printProfit1(items, priceLimit, productList, memo, dollar)


def printProfit2(profit2Result):
    # take a list of item[entry, entry, entry] and print out formated
    # result

    print("\nStrategy for both items and price limit")
    print("*****************************************")

    for item, grp in groupby(sorted(profit2Result)):
        print(len(list(grp)), end='')
        print(" X ['", end='')
        print(item[0], end='')
        print("', ", end='')
        print(item[1], end='')
        print(", ", end='')
        print(item[2], end='')
        print("]")

    print("Total Price of items sold:", sum(product[1] for product in profit2Result))
    print("Total Items sold:", len(profit2Result))
    print("Total Profit:", sum(product[2] for product in profit2Result))


def maximizeProfit2(itemsPartTwo, priceLimit, itemLimit):
    priceLimit = priceLimit - 1
    # Takes a list of products to use
    # calculates the maximum profit to be made from these
    # products for any given price limit. Item's can be limited by a itemLimit.
    # Time complexity = O(NC) Where n is the list of products and C is the price limit
    # Space complexity = O(NC) Where n is the list of products and C is the price limit

    memo = [[0 for i in range(priceLimit + 1)] for j in range(len(itemsPartTwo) + 1)]

    # For each product in the product list
    for i in range(1, len(itemsPartTwo) + 1):
        # Get the product/price/profit values of the previous position
        product, price, profit = itemsPartTwo[i - 1]
        # For each dollar in the price limit
        for j in range(1, priceLimit + 1):
            # If price is greater than j it doesn't fit
            if price > j:
                memo[i][j] = memo[i - 1][j]
            # Other wise get the maximum of list[previous value][currentValue],
            # or list[previous value][current value - price] + profit
            else:
                memo[i][j] = max(memo[i - 1][j],
                                 memo[i - 1][j - price] + profit)

    # Now we want to build the result list
    result = []
    limit = priceLimit
    # For each product in the product list
    for i in range(len(itemsPartTwo), 0, -1):
        # If the previous value is equal to current value,
        # it means we have added that product
        itemAdded = memo[i][limit] != memo[i - 1][limit]

        # If the product was added
        if itemAdded:
            product, price, profit = itemsPartTwo[i - 1]
            # Append it to the result list
            result.append(itemsPartTwo[i - 1])
            # Take it's price from the priceLimit
            limit -= price

    printProfit2(result)


def main():
    # The price limit
    priceLimit = int(input("Enter the price limit: ")) + 1
    # The product limit
    itemLimit = int(input("Enter the product limit: "))

    productList = []
    # Read in the text file to get a list of product objects
    readInFile(productList, itemLimit)

    # Highest profit no product limit
    maximizeProfit1(productList, priceLimit)

    # Create a list of items to use for part two
    itemsPartTwo = []
    for product in productList:
        entry = [product.productName, product.productPrice, product.productProfit]
        # Each product is placed in the list the same amount of times as the product limit
        # this means each time we use it we can check that it doesn't exceed limit
        for i in range(itemLimit):
            itemsPartTwo.append(entry)

    # Highest profit with product limit
    maximizeProfit2(itemsPartTwo, priceLimit, itemLimit)


main()
