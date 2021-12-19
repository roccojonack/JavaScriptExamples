#! /usr/bin/python
####################################################################
#
# description : the script is reading both CSV from Targo bank account
#               as well as files from PDF miner based on credit card 
#               output is a clean CSV file with unified layout
#               for display in browser
#
####################################################################
import re
import datetime

def isDate(TestString):
     matchObj = re.search(r'\d+\.\d+\.\d+',TestString)
     if matchObj:
          print ("Info: Match for date ",matchObj.group())
          return True
     return False

def addEntries(data) :   
    newEntry = []
    for line in data:
        words = line.split()
        if len(words)>2:
             if isDate(words[0]) and isDate(words[1]) :
                  print ("  found account statement {} with {} entires".format(words[0],len(newEntry)))
                  newEntry.append(handleCreditCardStatement(line))
                  continue
        print ("Warning: no new entry with {}".format(line))
    return newEntry

def formatOutput(DataSet):
    print ("Debug: finally sorting and printing")
    # newData = sortForDate(DataSet)
    for data in DataSet:
        print ("Debug: sorted output:", data)
        #fout.write(','.join(data))
        #fout.write('\n')
    
# function is a callback in sortForDate
# it defines the order of the date elements in order to
# compensate for european date versus plotly expected date
def sorting(L):
     first_splitup = L.split(',')
     second_splitup = first_splitup[0].split('-')
     return second_splitup[0], second_splitup[1], second_splitup[2]

# function is sorting the lines before writing out
# it also fills in an hour in order to avoid statements on same day
def sortForDate(data):
    d = data
    d = sorted(d, key=sorting)
    hour = 0
    rememberDate = ''
    newData = []
    for line in d:
        date = line.split(',')
        if rememberDate==date[0]:
            hour+=1
        else:
            hour=0
        rememberDate=date[0]
        date[0] += " "+str(hour).zfill(2)
        print ("Debug sorted ",date)
        newData.append(date)
    return newData

# function cleans up comma inside a string in quote
# otherwise some other functions may fail
def cleanCommaInLine (line):
    myLine = ""
    words = line.split("\"")
    if len(words)==1:
        return line
    odd = words[1::2]
    counter = 0
    for word in odd:
        newWord = word.replace(',','.')
        myLine += words[counter] + newWord
        counter += 2
    print ("blabla:",myLine)
    return myLine

# converts european amounts with . and , to US style with . as decimal
def convertEuropeanAmount2USStyle (line):
    myLine = line.replace('.','')
    myLine = myLine.replace(',','.')
    return myLine

# very specific to my needs; sorting based on description to find category
# default is "unknown"; will be updated based on experience
def findCategory (word):
    print ("check for category in ",word)
    matchObj = re.search(r'MIETE',word)
    if matchObj:
        print ("Info: Match for rent : ",matchObj.group())
        return('rent')
    else:
        print ("Debug: No match for rent")

    matchObj = re.search(r'HIT-MARKT|IHRHIT-MARKT|NETTO|Penny|aldi|ALDI|LIDL|Lidl|V-MARKT|TENGELMANN|EDEKA',word)
    if matchObj:
        print ("Info: Match for groceries : ",matchObj.group())
        return('groceries')
    else:
        print ("Debug: No match for groceries")

    matchObj = re.search(r'HOEFFNER|www.hoeffner.de|IKEA|V-BAUM',word)
    if matchObj:
        print ("Info: Match for home improvement : ",matchObj.group())
        return('home improvement')
    else:
        print ("Debug: No match for home improvement")

    matchObj = re.search(r'ZEROSTORE|H&M',word)
    if matchObj:
        print ("Info: Match for cloths : ",matchObj.group())
        return('cloths')
    else:
        print ("Debug: No match for cloths")

    matchObj = re.search(r'AMAZON|Amazon|Media Markt|MediaMarkt|Conrad|SaturnElectro',word)
    if matchObj:
        print ("Info: Match for electronic : ",matchObj.group())
        return('electronic')
    else:
        print ("Debug: No match for electronic")

    matchObj = re.search(r'INTERNE UMBUCHUNG|ZAHLUNGPERBANKEINZUG',word)
    if matchObj:
        print ("Info: Match for refill : ",matchObj.group())
        return('refill')
    else:
        print ("Debug: No match for refill")

    matchObj = re.search(r'AUSLANDSEINSATZ',word)
    if matchObj:
        print ("Info: Match for cardFee : ",matchObj.group())
        return('cardFee')
    else:
        print ("Debug: No match for cardFee")

    matchObj = re.search(r'TARGO VERSICHERUNG',word)
    if matchObj:
        print ("Info: Match for investment : ",matchObj.group())
        return('invest')
    else:
        print ("Debug: No match for invest")

    matchObj = re.search(r'Stattauto|RENTALCARS.COM|AUTOEUROPE|TANKSTELLE|DriveNow|Drive Now|DB AUTOMAT|DB VERTRIEB|DBBAHNAUTOMAT|LUFTHANSA|MVG|Meridian|Flixbus|EUROPCAR',word)
    if matchObj:
        print ("Info: Match for transport : ",matchObj.group())
        return('transport')
    else:
        print ("Debug: No match for transport")

    matchObj = re.search(r'DEUTSCHEBANK|BARGELDABHEBUNG|BARGELDAUSZAHLUNG|ATM|HVB|STADTSPARKASSE|UMBUCHUNGBARGELDABHEBUNG|VRBANK|SPARDA-BANK|COMMERZBANK|POSTBANK',word)
    if matchObj:
        print ("Info: Match for cash : ",matchObj.group())
        return('cash')
    else:
        print ("Debug: No match for cash")

    matchObj = re.search(r'GLORIAPALAST|GloriaPalast|MunchenMusik|NETFLIX|Google Music',word)
    if matchObj:
        print ("Info: Match for entertainment : ",matchObj.group())
        return('entertainment')
    else:
        print ("Debug: No match for entertainmant")

    matchObj = re.search(r'FIELMANN|Techniker Krankenkasse|DR WILLECKE|DOCTORDUVE|Apotheke',word)
    if matchObj:
        print ("Info: Match for health : ",matchObj.group())
        return('health')
    else:
        print ("Debug: No match for health")

    matchObj = re.search(r'FITrate|FitLane|FIT STAR|SPORTSCHECK',word)
    if matchObj:
        print ("Info: Match for sport : ",matchObj.group())
        return('sport')
    else:
        print ("Debug: No match for sport")

    matchObj = re.search(r'DEURAG|HDI Global',word)
    if matchObj:
        print ("Info: Match for insurance : ",matchObj.group())
        return('insurance')
    else:
        print ("Debug: No match for insurance")

    matchObj = re.search(r'SWM Ver',word)
    if matchObj:
        print ("Info: Match for utilities : ",matchObj.group())
        return('utilities')
    else:
        print ("Debug: No match for utilities")

    matchObj = re.search(r'FINANZAMT|Finanzamt|DRV BUND|Rundfunk ARD ZDF|KATHI KLEMM',word)
    if matchObj:
        print ("Info: Match for tax : ",matchObj.group())
        return('tax')
    else:
        print ("Debug: No match for tax")

    matchObj = re.search(r'1u1 Telecom|M-net Telek',word)
    if matchObj:
        print ("Info: Match for communication : ",matchObj.group())
        return('communication')
    else:
        print ("Debug: No match for communication")

    matchObj = re.search(r'VISA SERVICE',word)
    if matchObj:
        print ("Info: Match for ccredit card : ",matchObj.group())
        return('credit card')
    else:
        print ("No match for credit card")

    matchObj = re.search(r'GITHUB',word)
    if matchObj:
        print ("Info: Match for software : ",matchObj.group())
        return('software')
    else:
        print ("No match for software")

    matchObj = re.search(r'NETSPEED SYSTEMS',word)
    if matchObj:
        print ("Info: Match for income : ",matchObj.group())
        return('income')
    else:
        print ("No match for software")

    matchObj = re.search(r'Foodora|GASTEIGKULT&SPEISE|RISTORANTE|ZenPanasia|IndischesRestaurant|SPATENHAUS|SUSHI.WRAP',word)
    if matchObj:
        print ("Info: Match for resto : ",matchObj.group())
        return('resto')
    else:
        print ("No match for resto")

    return('unknown')

# this function looks crazy, but it offsets weird effects in the PDF reader
# some wild adaptations are necessary in order to have a unified format later
def prehandleCreditCardStatement (DataArray) :
    newData = []
    for data in DataArray:
        words    = data.split(" ")
        if not data.size() :
            insideStatement=False
            continue
        if isDate(words[0]) and isDate(words[1]) :
            insideStatement = True
        else :
            statement = data
    return newData

# this function looks crazy, but it offsets weird effects in the PDF reader
# some wild adaptations are necessary in order to have a unified format later
# check that line starts with date as day.month with 2 digits
# followed by day of the week (MO,DI,MI...), but day of the week might be with of without ;
# also checking that last 2 entries are amounts
def prehandleGiroStatement (string1,string2):
     newString = string1
     words     = string1.split(";")
     if len(words)<4:
          print ("Debug: skiping because single or no character is weird in line :",string1)
          return ''
     else:
          print ("Debug: checking in strings ", words[0], " and ", words[1])
          matchObj1 = re.search(r'\d\d\.(0|1)\d',words[0])
          matchObj2 = re.search(r'\d\d\.(0|1)\d',words[1])
          if (matchObj1 or matchObj2):
               if matchObj1:
                    print ("Info: Match for date : ",matchObj1.group())
                    myDate = matchObj1.group()
                    myDate = myDate.replace('.', '/')+ "/" + year
                    matchObj1 = re.search(r'(MO|DI|MI|DO|FR|SA|SO)',words[0])
                    matchObj2 = re.search(r'(MO|DI|MI|DO|FR|SA|SO)',words[1])
                    if (not matchObj1 and not matchObj2):
                         print ("Debug: still no Match for date : ",words[0])
                         print ("Debug: skiping because single or no character is weird in line :",string1)
                         return ''
                    if matchObj1:
                         newString = ' '.join(words[1:-2])
                    else:
                         newString = ' '.join(words[2:-2])
                    newString = myDate + ";\"" + newString
               else:
                    print ("Info: Match for date : ",matchObj2.group())
                    myDate = matchObj2.group()
                    myDate = myDate.replace('.', '/')+ "/" + year
                    matchObj1 = re.search(r'(MO|DI|MI|DO|FR|SA|SO)',words[1])
                    matchObj2 = re.search(r'(MO|DI|MI|DO|FR|SA|SO)',words[2])
                    if (not matchObj1 and not matchObj2):
                         print ("Debug: still no Match for date : ",words[1])
                         print ("Debug: skiping because single or no character is weird in line :",string1)
                         return ''
                    if matchObj1:
                         newString = ' '.join(words[2:-2])
                    else:
                         newString = ' '.join(words[3:-2])
                    newString = myDate + ";\"" + newString
               matchObj1 = re.search(r'\d*\.*\d+,\d\d',words[len(words)-1])
               matchObj2 = re.search(r'\d*\.*\d+,\d\d',words[len(words)-2])
               if (matchObj1 and matchObj2):
                    print ("Debug: amount ", matchObj1.group()," ", matchObj2.group())
                    matchObj3 = re.search(r'GUTSCHRIFT',newString)
                    if matchObj3:
                         newString = newString + "\";+" + matchObj2.group()+ ";" + matchObj1.group()
                    else:
                         newString = newString + "\";-" + matchObj2.group()+ ";" + matchObj1.group()
               else:
                    return ''
               print ("Debug : returned : ", newString)
               return newString;
          print ("Debug : couldn't find anything returning empty string for line : ", newString)
          return ''

# here we are assuming a line from the PDF miner out of a Credit card statement
def handleCreditCardStatement (string):
    counter = 0
    newYear = 0
    newLine = ""
    newCategory = ""
    words = string.split()
    LineLength=len(words)
    print ("handleCreditCardStatement for string {} with length {}".format(string,LineLength))
    return string
    for word in words:
        if counter==0:
            myDateList = word.split(".")
            print ("dateList: ", myDateList[1]," length ",len(myDateList)," ",word)
            if myDateList[1]=='01' and int(rollover)==1:
                 newYear = int(year)+1
            myNewDateList = [myDateList[1], myDateList[0]]
            myDate = ""
            myDate = '-'.join(myNewDateList)
            myDate = str(newYear)+'-'+myDate   
            newLine      = myDate
            print ("new date: ", myDate)
        if counter==LineLength-1:
            # deal with description
            category = findCategory(newCategory)
            newLine += ",\""+newCategory.replace(',',';')+"\""
            # deal with Betrag
            amount = convertEuropeanAmount2USStyle(word.rstrip())
            print ("found amount:",amount)
            newLine += ","+amount
            newLine += ",\""+category+"\"" 
            newLine += ",\""+accountName+"\""
            continue
        if counter>1:
            newCategory += word+" " 
            print ("found desription:",word)
        counter+=1   
        print ("found word:", word,":",counter)
    return newLine

# here we are assuming a line coming from a targo account exported
# CSV file
def handleAccountStatement(string,hour,rememberDate):
    counter = 0
    newLine = ""
    print ("handleAccount : ",string)
    words = string.split(";")
    for word in words:
        if counter==0:
            # handle date
            myDateList = word.split("/")
            print ("dateList: ", myDateList," length ",len(myDateList)," ",word)
            #myDateList.reverse()
            #myDate = '-'.join(myDateList)
            myDate = myDateList[2]+'-'+myDateList[0]+'-'+myDateList[1]
            counter = 1   
            if myDate==rememberDate:
                hour += 1
            else:
                hour  = 0
            newLine      = myDate
            rememberDate = myDate
            # myDate += " "+str(hour).zfill(2)
            newLine      = myDate
            print ("new date: ", myDate)
            continue
        if counter==1:
            # deal with description
            category = findCategory(word)
            newLine = newLine+","+word
            counter = 2
            continue
        if counter==2:
            # deal with amount
            amount = word.strip("\"")
            newLine = newLine+","+amount 
            counter = 3
            continue
        if counter==3:
            # handle category
            counter = 4
            newLine = newLine+",\""+category+"\""
            continue
        if counter==4:
            print ("found : ", word)
            counter = 5
            continue
        if counter==5:
            counter = 6
            print ("found account: ", word)
            newLine = newLine+","+word
            continue
        counter+=1   
        print ("found word: ", word)
        newLine = newLine+","+word
    return newLine, hour, rememberDate

class transaction:
    amount      = 0
    description = ""
    date        = ""
    source      = ""
    account     = ""
    category    = "unkown"
    
    def __self__(self,name,soure):
        self.name = name
        print ("constructing a new transaction entry from : ", source)
