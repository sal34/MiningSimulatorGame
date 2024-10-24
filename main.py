#imports
import game_dependencies.btcChainData as btc
import keyboard
import random
import time
import os



#Variables of all the game

#Version Declare
version = "0.0.3b11b" #Beta version

#variables #diff, block, oldblock, hash, hashrate, btcs, bill, watt, elettricitycost
hashrate = 0
totalhashrate = 0


#Chain Data and currency local data
diff, block, oldblock, hash, fdiff, conversion = btc.getData()
money = 2500.0 #default: 2500
btcs = 0.00000000 #10^-8


#Maintain Costs
elettricitycost = 0.10 #kW/h
watt = 0 #Watt consume from the miners
bill = 0 #Elettricity bill elettricitycost*  med of KW/h





global shopitems
shopitems = [{"name": "Bitcoin Miner S19 XP Hyd.", "price": 5911, "consumes": 5345.6, "hashrate": 257},
             {"name": "Bitcoin Miner S21", "price": 5400, "consumes": 3500, "hashrate": 200},
             {"name": "Bitcoin Miner S19j Pro.", "price": 1149, "consumes": 3050, "hashrate": 100},
             {"name": "Bitcoin Miner S9", "price": 200, "consumes": 1350, "hashrate": 14.5},
             {"name": "NerdMiner", "price": 40, "consumes": 1, "hashrate": 0.000000075}#7.5*(10**-8)} # 0.000000075
             ]

InventoryMiner = []

import game_dependencies.save as save

hashrate, totalhashrate, money, btcs, watt, bill, InventoryMiner = save.loadgame()

#Many Functions:

#clear the screen
def clear():
    os.system("cls")


#Shop Func
def Shop():
    global money, shopitems, totalhashrate
    notvalid = False
    while True:
        clear()
        print ('---- select an options from the shop to buy, or type and send q to quit the shop ----\n\n\n')
        print('||                  ASICs Shop - Buy And Mine! - ASICs Shop                  ||')

        print('||      Name:                     Hashrate:  Watt:         Price:            ||')
        print('|| 1.    Bitcoin Miner S19 XP Hyd. ± 257TH/s  ± 5345.6W      5911$           ||\n'
              '|| 2.    Bitcoin Miner S21         ± 200TH/s  ± 3500  W      5400$           ||\n'
              '|| 3.    Bitcoin Miner S19j Pro    ± 100TH/s  ± 3050  W      1149$           ||\n' #96/104 TH/s
              '|| 4.    Bitcoin Miner S9          ± 14.5TH/s ± 1350  W      200$            ||\n' #13.5/14TH/s
              '|| 5.    NerdMiner                 ± 75KH/s   ± 1     W      40$             ||\n')
        
        shopch = input(f'Select [Money: {money}]: ') 
        
        if isinstance(shopch, str):
            try:
                shopch = int(shopch)-1
            except Exception as e:
                print("Error: " + str(e))
                print("Your selection is invalid, try again in 3 seconds.")
                notvalid = True
                time.sleep(3)
                break

        if shopch > 5:
            print("Your selection is invalid, try again in 3 seconds.")
            notvalid = True
            time.sleep(3)
            break
        else:
            while True:
                qt = input('Enter the quantity: ')
                try:
                    qt = int(qt)
                    break
                except Exception as e:
                    print("Invalid value: " + str(e), "try again.")

        print(f'Selection: {shopch}\nQuantity: {qt}')

        if money - shopitems[shopch]["price"]*qt < 0:
            print("You don't have enough money, retry in 3 seconds.")
            time.sleep(3)
            notvalid = True
            break
        else:
            money -= shopitems[int(shopch)]["price"]*qt
            for i in range(qt):
                InventoryMiner.append({"name": shopitems[int(shopch)]["name"], "watt": shopitems[int(shopch)]["consumes"], "hashrate": shopitems[int(shopch)]["hashrate"]})
                totalhashrate += shopitems[int(shopch)]["hashrate"]
                #print(f'Added {InventoryMiner}')
            print(f'Your successifully bought {qt}x {shopitems[shopch]["name"]}!!, closing shop in 3 seconds.')
            notvalid = False
            time.sleep(3)
            break
            


    if notvalid:
        Shop()
    else:
        Menu()

    
    



#Show Own Miners Func
def ShowMiners():
    clear()
    print("|| Press q to quit ||")
    try:
        n=0
        for i in InventoryMiner:
            n += 1 
            if (i.get("name", "N/A") != "N/A" and i.get("name", "N/A") == "NerdMiner"): 
                hs = str(format(float(i.get("hashrate", 0)), '.9f')) 
            elif (i.get("name", "N/A") != "N/A"): 
                hs = str(format(float(i.get("hashrate", 0)), '9g'))
            print(f'|| {str(n)}.   Miner: {i.get("name", "N/A")}    Wattage: {i.get("watt", "N/A")}    Hashrate: {hs}TH/s\n') # format(float(i.get("hashrate", "N/A")), '.20f')
    except Exception as e:
        print("Error: ", str(e))
    
    while True:
        if (keyboard.is_pressed('q')):
            Menu()
            break
        else:
            continue




#Show realtime data Func
def ShowData():
    global btcs, hashrate, diff, block
    clear()
    continueshowdata = True
    while continueshowdata:
        #Function Variables
        timeD = 0
        quit = False
        diff, block, oldblock, hash, fdiff, conversion = btc.getData()
        print ('\\ The stats will reload every 15 seconds, press q to quit. //')

        print("||  Actual mining Difficulty: ", diff,
              "\n||  Block to Mine: ", block+1,
              "\n||  Your total mining Hashrate: ", hashrate, #hashrate
              "\n||  Your total mined coin: ", btcs) #btcs
              #"\nOld Block: ", oldblock,
              #"\nOld Block Hash: ", hash)


        #Quit sys.
        timestamp = int(round(time.time()))
        while (timeD < 15):
            timeD = int(round(time.time())) - timestamp
            #print (timeD)
            if (keyboard.is_pressed('q')):
               quit = True
               break
            else:
                quit = False
                continue

        if quit:
            timeD = 0
            quit = False
            continueshowdata = False
            Menu()
        else:
            timeD = 0
            clear()
            

        
#-------- Mining Logic ----------



#Randomize hasharte of the player to make a similar mining effect.
def RandomizeHashrate(totalhashrate):
    totalhashratemod = totalhashrate
    if (totalhashrate < 0.5):
        totalhashratemod += random.uniform(-0.000000025, 0.000000035)
        totalhashratemod = str(format(totalhashratemod, '.9f'))
    else:
        totalhashratemod += random.uniform(-0.005, 0.15)
        totalhashratemod = str(format(totalhashratemod, '.4g'))

    return totalhashratemod



#5 petahash = 5000000000000000
#((37885054421573 * 2^32 / 5000000000000000) / (3600)) = 9039 hours. [9039/24 = 376,625 * 144 = +-54234 blocks]
def getProbability(fdiff, totalhashrate):
    blockprob = round((((fdiff * 2**32 / (totalhashrate * 10**12)) / (3600)) / 24) * 144) #Good enough for a sim. game
    return blockprob

def solomine(maxblock):
    mineprob = random.randint(0, maxblock)
    if (mineprob == maxblock):
        return True
    else:
        return False



def Mining():
    global totalhashrate, diff, fdiff, btcs
    timeD = 0
    quit = False
    minedblocks = 0
    i = 0
    blockprob = getProbability(fdiff, totalhashrate)
    #check if all is already loaded and the player have a miner to start the mining simulation
    if (diff != 0): #totalhashrate != 0 and
        while True:
            totalhashratemod = RandomizeHashrate(totalhashrate)
            #Clear screen
            clear()
            print ("\\ Click q to stop the mining process //")
            print(f'|| Hash Difficulty: {diff}',
                  f'\n|| You are mining with: {str(totalhashratemod)} TH/s',
                  f'\nMined Blocks: {str(minedblocks)}',
                  f'\nYour mining probability is {blockprob}')
            
            #Mine from 7 to 32 * 2 seconds like 7*2=14seconds and it try to mine a block
            if (i == 5):
                if (solomine(blockprob)):
                    print(f'You mined a Bitcoin block!!')
                    minedblocks = int(minedblocks) + 1
                    btcs =+ 3.125
            elif (i > 6):
                i = 0
            else:
                i += 1
            

            print("\n\n\n--- In beta phase you can mine only in solo ---")
            
            #Quit sys.
            timestamp = int(round(time.time()))
            while (timeD < 2):
                timeD = int(round(time.time())) - timestamp
                #print (timeD)
                if (keyboard.is_pressed('q')):
                   quit = True
                   break
                else:
                    quit = False
                    continue

            if quit:
                timeD = 0
                quit = False
                continueshowdata = False
                Menu()
            else:
                timeD = 0
            #Return totalhashrate var into float to avoid "TypeError: can only concatenate str (not "float") to str".
            totalhashratemod = float(totalhashratemod)

    elif (diff == 0):
        print ("Error: Impossible to retrieve difficulty from network.")
        time.sleep(3)
        Menu()
    else:
        print ("Please buy a miner to start mining process.")
        time.sleep(3)
        Menu()
    

#Trading sys. to sell/buy btc
def Trade():
    global conversion, btcs, money
    """timeD = 0
    quit = False
    soldbtcs = False"""
    while True:
        clear()
        print ("\\ Click 'q' to quit trade, or 's' to sell all your btc //")
        print (f'\nActual bitcoin conversion is: 1 BTC for {conversion}$')
        
        
        
        print ("\n\nNext conversion price in 60 seconds")
        print ("\n\n\n\n---- In beta phase you can only sell btc ----")

        print("\nInput 1. To sell, or 2. to quit.")
        ch = int(input("Enter your choice: "))
        if (ch == 1):
            conversion = float(conversion)
            print(f'Selling {btcs}₿ for {float(btcs)*conversion}..')
            time.sleep(3)
            print(f'You sold all {btcs}₿ for {float(btcs)*conversion}')
            money += btcs * conversion
            btcs = 0
        elif (ch == 2):
            Menu()
        else:
            print("\nWrong number, try again.")
        
        
        #Quit sys.
        """timestamp = int(round(time.time()))
        while (timeD < 60):
            timeD = int(round(time.time())) - timestamp
            #print (timeD)
            if (keyboard.is_pressed('q')):
                quit = True
                break
            elif (keyboard.wait('s') and conversion != 0.0 and btcs != 0.0 and not soldbtcs):
                soldbtcs = True
                conversion = float(conversion)
                print(f'Selling {btcs}₿ for {float(btcs)*conversion}..')
                time.sleep(3)

                #print(f'normal: {conversion}')
                
                #print(f'float: {conversion}')
                print(f'You sold all {btcs}₿ for {float(btcs)*conversion}')
                money += btcs * conversion
                btcs = 0
                
            elif (btcs == 0.0):
                print("You don't have any btcs to sell, try later.")
                quit = False
                continue
            else:
                quit = False
                continue

        if (quit):
            quit = False
            break"""
            
        


#Menu Function
def Menu():
    global version
    clear()
    #print(f'####### --- DEBUG:   {fdiff} \n\n')
    print(f'\\ \\ Welcome to RealBTC Mining Simulator: {version} // // \n\n\n')
    print(
        '||  1. Real Time Data\n\n'
        '||  2. My Miners\n\n'
        '||  3. Shop\n\n'
        '||  4. Mine\n\n'
        '||  5. Trade\n\n'
        '\n\n||  Type exit or quit, to close the game.\n'
    )

    ch = input('--- Select -->  ')
    ch = str(ch)
    clear()

    if ch == '1':
        ShowData()
    elif ch == '2':
        ShowMiners()
    elif ch == '3':
        Shop()
    elif ch == '4':
        Mining()
    elif ch == '5':
        Trade()
    elif ch.lower() == 'exit' or ch.lower() == 'quit':
        print("Saving, don't close..")
        global hashrate, totalhashrate, money, btcs, watt, bill, InventoryMiner
        save.savegame(hashrate, totalhashrate, money, btcs, watt, bill, InventoryMiner)
        print("Saved")
        print('\n\nClosing..')
        quit()
    else:
        print('Invalid selection, please try another one in 3 seconds.')
        time.sleep(3)
        clear()
        Menu()
        


#Application Startup
clear()
Menu()

#TODO:
#Trade btc to usd, enhance some logic
#other stuff [after or at beta ending] (like sell miner)
#Enhance mining

#Doing Trade Sys.

#Doing Pool mining