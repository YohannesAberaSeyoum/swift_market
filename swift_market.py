class Product:
    def __init__(self, obj, amount, time, market, person):
        self.Objects = obj
        self.Amount = amount
        self.Time = time
        self.Market = market
        self.Person = person


def sellProduct():
    oList = objectList()
    name = objectInput(oList)
    while True:
        amount = amountInput(name)
        detail = specificProductByObject(name)
        if detail[-1] >= amount:
            pList = personList()
            person = personInput(pList)
            time = timeInput()
            product = Product(obj=name, amount=str(amount),
                              time=time, market='Sell', person=person)
            saveProduct(product=product)
            break
        else:
            print("We have {} amount of {}".format(str(detail[-1]), name))
    print("The product is sold")


def buyProduct(buy=True):
    oList = objectList()
    name = objectInput(oList, True if buy else False)
    amount = amountInput(name)
    pList = personList()
    person = personInput(pList)
    time = timeInput()
    product = Product(obj=name, amount=str(amount),
                      time=time, market='Buy' if buy else 'Defect', person=person)
    saveProduct(product=product)
    print("The product is registered")


def saveProduct(product):
    newDF = df.append(product.__dict__, ignore_index=True)
    newDF.to_csv('new_swift_market.csv', index=False)


def overallStatistic(obj, person):
    if person:
        if type(obj) == str:
            dateFrame = df[df.Person == obj]
            printing(obj=obj, person=person, dateDF=dateFrame)
        else:
            for o in obj:
                dateFrame = df[df.Person == o]
                printing(obj=o, person=person, dateDF=dateFrame)
            totalDataFrame = df[df.Person.isin(obj)]
            printing(obj="Summary", person=person, dateDF=totalDataFrame)
    else:
        if type(obj) == str:
            dateFrame = df[df.Objects == obj]
            printing(obj=obj, person=person, dateDF=dateFrame)
        else:
            for o in obj:
                dateFrame = df[df.Objects == o]
                printing(obj=o, person=person, dateDF=dateFrame)


def specificProductByObject(name, dfb=True):
    if type(dfb) == bool:
        dfb = df
    data = dfb[dfb.Objects == name]
    buy = int(data[data.Market == 'Buy'].Amount.sum())
    sell = int(data[data.Market == 'Sell'].Amount.sum())
    defect = int(data[data.Market == 'Defect'].Amount.sum())
    remain = buy - sell - defect
    return (buy, sell, defect, remain)


def specificProductByPerson(person, dfb=True):
    if type(dfb) == bool:
        dfb = df
    data = dfb[dfb.Person == person]
    buy = int(data[data.Market == 'Buy'].Amount.sum())
    sell = int(data[data.Market == 'Sell'].Amount.sum())
    defect = int(data[data.Market == 'Defect'].Amount.sum())
    remain = buy - sell + defect
    return (buy, sell, defect, remain)


def specificProductByDate(date, obj, person):
    if type(date) == tuple:
        prevDF = df[df.Time >= date[0]]
        nextDF = prevDF[prevDF.Time <= date[1]]
        if person:
            dateDF = nextDF[nextDF.Person == obj]
        else:
            dateDF = nextDF[nextDF.Objects == obj]
    else:
        semiDF = df[df.Time == date]
        if person:
            dateDF = semiDF[semiDF.Person == obj]
        else:
            dateDF = semiDF[semiDF.Objects == obj]
    return dateDF


def takingDate():
    print("Enter The Year: ")
    year = inputCheck('year')
    print("Enter The Month: ")
    month = inputCheck('month')
    print("Enter The Date: ")
    day = inputCheck('day')
    date = timeInput("{}-{}-{}".format(year, month, day))
    return date


def specificDateStatistic(obj, person):
    date = takingDate()
    if type(obj) == str:
        dateDF = specificProductByDate(date=date, obj=obj, person=person)
        printing(obj, person, dateDF)
    else:
        for o in obj:
            dateDF = specificProductByDate(date=date, obj=o, person=person)
            printing(o, person, dateDF)


def printing(obj, person, dateDF):
    print()
    print(obj + "\n")
    buy = 0
    sell = 0
    defect = 0
    remaining = 0
    if person:
        print("Object Name\t\tBuy\tSell\tDefect\tRemaining")
        oList = objectList()
        for o in oList:
            product = specificProductByObject(o, dfb=dateDF)
            buy += product[0]
            sell += product[1]
            defect += product[2]
            remaining += product[3]
            print("{}\t{}\t{}\t{}\t{}".format(
                o, *product))
    else:
        print("Person\tBuy\tSell\tDefect\tRemaining")
        pList = personList()
        for p in pList:
            product = specificProductByPerson(p, dfb=dateDF)
            buy += product[0]
            sell += product[1]
            defect += product[2]
            remaining += product[3]
            print("{}\t{}\t{}\t{}\t{}".format(
                p, *product))
    print()
    print("Total\t{}\t{}\t{}\t{}".format(buy, sell, defect, remaining))
    print()


def rangeOfDateStatistic(obj, person):
    print("From")
    prevDate = takingDate()
    print("To")
    nextDate = takingDate()
    if type(obj) == str:
        dateDF = specificProductByDate(
            date=(prevDate, nextDate), obj=obj, person=person)
        printing(obj, person, dateDF)
    else:
        for o in obj:
            dateDF = specificProductByDate(
                date=(prevDate, nextDate), obj=o, person=person)
            printing(o, person, dateDF)


def showStatistic():
    while True:
        command = input(
            "Enter 1.To know about Objects\nEnter 2.To know about Person\nEnter 3.To return back\n")
        if command == "1":
            objectInfo()
        elif command == "2":
            personInfo()
        elif command == "3":
            break
        else:
            print("Please Enter Only the Options")


def objectInfo():
    while True:
        command = input(
            "Enter 1.To know about Single Object\nEnter 2.To know about Multiple Objects\nEnter 3.To know about All Objects\nEnter 4.To get back\n")
        if command == "1":
            singleObjectInfo()
        elif command == "2":
            multipleObjectsInfo()
        elif command == "3":
            allObjectsInfo()
        elif command == "4":
            break
        else:
            print("Please Enter Only the Options")


def getDate(obj, person):
    while True:
        command = input(
            "Enter 1.To know Specific Date Activity\nEnter 2.To know range of Date Activity\nEnter 3.To know Overall Activity\nEnter 4.To get back\n")
        if command == "1":
            specificDateStatistic(obj, person)
        elif command == "2":
            rangeOfDateStatistic(obj, person)
        elif command == "3":
            overallStatistic(obj, person)
        elif command == "4":
            break
        else:
            print("Please Enter Only the Options")


def singleObjectInfo(person=False):
    if person:
        pList = personList()
        obj = personInput(pList, info=True)
    else:
        oList = objectList()
        obj = objectInput(oList)
    getDate(obj, person)


def multipleObjectsInfo(person=False):
    obj = True
    objList = []
    while obj:
        if person:
            pList = personList()
            obj = personInput(pList, multi=True)
            objList.append(obj)
        else:
            oList = objectList()
            obj = objectInput(oList, multi=True)
            objList.append(obj)
    getDate(obj=objList[:-1], person=person)


def allObjectsInfo(person=False):
    if person:
        obj = personList()
    else:
        obj = objectList()
    getDate(obj=obj, person=person)


def personInfo():
    while True:
        command = input(
            "Enter 1.To know about Single Person\nEnter 2.To know about Multiple People\nEnter 3.To know about All People\nEnter 4.To get back\n")
        if command == "1":
            singleObjectInfo(True)
        elif command == "2":
            multipleObjectsInfo(True)
        elif command == "3":
            allObjectsInfo(True)
        elif command == "4":
            break
        else:
            print("Please Enter Only the Options")


def objectList():
    return df.Objects.unique()


def personList():
    return df.Person.unique()


def dataFrame():
    import pandas as pd
    return pd.read_csv('new_swift_market.csv')


def amountInput(obj):
    print("Amount of {}: ".format(obj))
    inp = inputCheck("Amount")
    return inp


def objectInput(lst, buy=False, multi=False):
    if list(lst):
        while True:
            print("List of Products")
            for i, l in enumerate(lst):
                print("{}.{}".format(i+1, l))
            if buy:
                print(
                    "Enter the number from above list to select\n or Enter 0 to add new: ")
                inp = inputCheck('Object')
                if inp == 0:
                    return input("Enter the new Product: ")
            else:
                if multi:
                    print(
                        "Enter the number from above list to select\n or Enter 0 if you finish the list: ")
                else:
                    print("Enter the number from above list to select: ")
                inp = inputCheck('Object')
                if inp == 0 and multi:
                    return inp
            if len(lst) >= inp > 0:
                return lst[inp-1]
            print("Please Enter Valid Number")
    else:
        print("No Products Found")
        return input("Enter the new Product: ")


def inputCheck(option):
    while True:
        try:
            inp = int(input())
            if option == 'month' and inp > 12 or inp < 0:
                raise
            elif option == 'day' and inp > 31 or inp < 0:
                raise
            return inp
        except:
            if option in ['product', 'object']:
                print(
                    "Please Enter only listed number or 0 to add new {}".format(option))
            else:
                print("Please Enter valid number")
            continue


def personInput(lst, info=False, multi=False):
    if list(lst):
        while True:
            print("List of Persons")
            for i, l in enumerate(lst):
                print("{}.{}".format(i+1, l))
            if not (info or multi):
                print(
                    "Enter the number from above list to select\n or Enter 0 to add new: ")
                inp = inputCheck("Person")
                if inp == 0:
                    return input("Enter the new User: ")
            else:
                if multi:
                    print(
                        "Enter the number from above list to select\n or Enter 0 if you finish the list: ")
                    inp = inputCheck("Person")
                    if inp == 0:
                        return inp
                else:
                    print("Enter the number from above list to select")
                    inp = inputCheck("Person")
            if len(lst) >= inp > 0:
                return lst[inp-1]
            print("Please Enter Valid Number")
    else:
        print("No Person Found")
        return input("Enter the new Person: ")


def timeInput(dateB=False):
    from datetime import date, datetime
    if dateB:
        return str(datetime.strptime(dateB, "%Y-%m-%d").date())
    return str(date.today())


def writeCSV():
    import csv
    header = ["Objects", "Amount", "Time", "Market", "Person"]
    with open('new_swift_market.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)


if __name__ == "__main__":
    import os.path

    if not os.path.isfile("new_swift_market.csv"):
        writeCSV()
    else:
        if os.path.getsize("new_swift_market.csv") < 20:
            writeCSV()

    while True:
        df = dataFrame()
        command = input(
            "Enter 1.To sell product\nEnter 2.To buy product\nEnter 3.To return product\nEnter 4.To borrow from other user\nEnter 5.For Statistic\nEnter 6.To Exit\n")
        if command == "1":
            sellProduct()
        elif command == "2":
            buyProduct()
        elif command == "3":
            buyProduct(False)
        elif command == "4":
            returnProduct()
        elif command == "5":
            showStatistic()
        elif command == "6":
            break
        else:
            print("Please Enter Only the Options")
