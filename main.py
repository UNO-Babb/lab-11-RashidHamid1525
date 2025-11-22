#GroceryStoreSim.py
#Name:
#Date:
#Assignment:
import simpy
import random

eventLog = []
waitingShoppers = []
idleTime = 0

def shopper(env, id):
    arrive = env.now
    items = random.randint(5, 20)
    shoppingTime = items // 2
    yield env.timeout(shoppingTime)
    waitingShoppers.append((id, items, arrive, env.now))

def checker(env):
    global idleTime
    while True:
        while len(waitingShoppers) == 0:
            idleTime += 1
            yield env.timeout(1)
        customer = waitingShoppers.pop(0)
        items = customer[1]
        checkoutTime = items // 10 + 1
        yield env.timeout(checkoutTime)
        eventLog.append((customer[0], customer[1], customer[2], customer[3], env.now))

def customerArrival(env, rate=2):
    customerNumber = 0
    while True:
        customerNumber += 1
        env.process(shopper(env, customerNumber))
        yield env.timeout(rate)

def processResults():
    totalWait = 0
    totalShoppers = len(eventLog)
    totalItems = 0
    shoppingTimes = []
    maxWait = 0

    for e in eventLog:
        wait = e[4] - e[3]
        totalWait += wait
        totalItems += e[1]
        shoppingTimes.append(e[3] - e[2])
        if wait > maxWait:
            maxWait = wait

    print("Shoppers processed:", totalShoppers)
    print("Average items purchased:", totalItems / totalShoppers)
    print("Average shopping time:", sum(shoppingTimes) / totalShoppers)
    print("Average wait time:", totalWait / totalShoppers)
    print("Max wait time:", maxWait)
    print("Total idle time:", idleTime)

def main():
    numberCheckers = 5
    simLength = 180

    env = simpy.Environment()
    env.process(customerArrival(env))

    for _ in range(numberCheckers):
        env.process(checker(env))

    env.run(until=simLength)
    processResults()

if __name__ == '__main__':
    main()
