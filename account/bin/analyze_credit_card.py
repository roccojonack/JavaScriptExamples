from PyPDF2 import PdfReader
import re
import logging
import glob
import time
import datetime
import json
import sys
import pandas as pd

from optparse import OptionParser

logger = logging.getLogger(__name__)

countryValues = "FR|DE|NL|VA|LU|SE|US|CY|GR|IE|TR|AT|PT|IT|MX|GB|FI|HK"
chargeValues = "Sollzinsen|Verzugszinsen|Habenzinsen|Gutschrift|GUTSCHRIFT|ZAHLUNG|UMBUCHUNG|KORREKTUR|BELASTUNG|JAHRESGEBUEHR|BARGELDAUSZAHLUNGSGEBUEHR|REKLAMATIONSBETRAG|RECHNUNGSVERSAND"
dateValue = "\d\d\.\d\d\.\d*\d*"
amountValue = "-*\d*\.*\d+\,\d\d"
categories = []
categories.append({"key":"Housing","search":"MIETE|HELPLING"})
categories.append({"key":"Sports","search":"FITrate|FitLane|FIT STAR|SPORT SCHECK|DECATHLON|BROOKS SPORTS"})
categories.append({"key":"Food/Groceries","search":"CARREFOUR|Hofer|BILLA|REWE|SPAR|MONOPRIX|HIT-MARKT|Eataly|IHRHIT-MARKT|NETTO|Netto|Penny|aldi|ALDI|LIDL|Lidl|V-MARKT|TENGELMANN|EDEKA|Rossman|MAX RISCHART|Backhaus Nahrstedt|COFFEE FELLOW|VINZENZ MURR|BIOFEINKOST|HITMuen|Ratschiller|Lieferando|Rasthaus|Restaurant|KAUFLAND|Pommefreunde|BAECKEREI|KONDITOREI|NORDSEEGMBH|SAFFER WEIN|BURRITO COMPANY|DinzlerAG|MichaeligartenBiergartenMuenchen|Lebensmittel|STERIA|Raststaette|AUTOGRILL|El Espanol|Gasteig Kult|SUZANA|NAMMOS|BISTRO|BAR|ARS|DIOS MINGA|Foodora|Pizza|Pizzeria|GASTEIGKULT&SPEISE|RISTORANTE|Zen Panasia|IndischesRestaurant|SPATENHAUS|SUSHI.WRAP|Alter\s*Wirt|WIRTSHAUS"})
categories.append({"key":"Utilities (Electricity, Water, Gas, Internet, etc.)","search":"SWM Ver|O2 |1u1 Telecom|M-net Telek"})
categories.append({"key":"Home improvement", "search":"DEHNER GARTEN-Center|HOEFFNER|Hoffner|www.hoeffner.de|IKEA|V-BAUM|HORNBACH|Hagebau"})
categories.append({"key":"Healthcare/Medical","search":"FIELMANN|Techniker Krankenkasse|DR WILLECKE|DOCTORDUVE|PODOLOGI|Apotheke|APOTHEKE|ZAHNARZT|Praxis|Hautzentrum|Laserzentrum|Medical\s*Spa"})
categories.append({"key":"Insurance (Health, Life, Auto, Home, etc.)","search":"DEURAG|HDI Global|VERSICHERUNG"})
categories.append({"key":"Debt Payments (Credit cards, Loans, fees, etc.)","search":"INTERNE UMBUCHUNG|ZAHLUNGPERBANKEINZUG|AUSLANDSEINSATZ|DEUTSCHEBANK|BARGELDABHEBUNG|BARGELDAUSZAHLUNG|ATM|HVB|STADTSPARKASSE|DEUTSCHE BANK|UMBUCHUNGBARGELDABHEBUNG|VRBANK|SPARDA-BANK|COMMERZBANK|POSTBANK|ISA SERVICE|FINANZAMT|Finanzamt|DRV BUND|Rundfunk ARD ZDF|KATHI KLEMM"})
#categories.append({"key":"Savings/Investments","search":""})
categories.append({"key":"Entertainment/Recreation","search":"GLORIA\s*PALAST|Gloria(.*)Palast|Munchen Musik|NETFLIX|Google Music|LOUVRE"})
categories.append({"key":"Personal Care (Grooming, Toiletries, etc.)","search":"ZEROSTORE|SCHUHE|H&M|RENO|ZARA"})
#categories.append({"key":"Education","search":""})
#categories.append({"key":"Charitable Giving","search":""})
categories.append({"key":"Shopping/Personal Goods","search":"AMAZON|Amazon|Media Markt|MediaMarkt|MEDIAMARKT|Conrad|SaturnElectro|DELL|AMZN|SPORTSCHECK|DM-DrogerieMarkt"})
categories.append({"key":"Travel/Vacation/Transport","search":"FewoDirekt|RATPPARIS|TIER|rentalcars.com|PARKPLATZ|Tankautomat|GIP |ESSO |BP |Eni\s*Service|Tankstelle|SNCF|RENT A CAR|G1|ARAL|Aral|GETT|Taxi|TOTAL|Stattauto|AUTO EUROPE|HERTZ|ALAMO|ENTERPRISE|Europcar|RENTALCARS.COM|AUTOEUROPE|TANKSTELLE|DriveNow|Drive Now|DB AUTOMAT|DB VERTRIEB|DBBAHNAUTOMAT|LUFTHANSA|MVG|Meridian|Flixbus|EUROPCAR|DBVertrieb|Hotel|HOTEL"})
categories.append({"key":"Subscriptions (Streaming, Magazines, etc.)","search":"Spotify|Netflix|HEISE|HeiseMedien|Audible|IWG DEUTSCHLAND|RegusMunchen|GooglePayment"})
#categories.append({"key":"Miscellaneous/Other","search":""})

def isDate(TestString):
     matchObj = re.search(r'\d+\.\d+\.',TestString)
     if matchObj:
          logging.debug ("Match for date %s"%(matchObj.group()))
          return True
     return False

def findCategory (word):
 
    for entry in categories:
        matchObj = re.search(entry['search'],word)
        if matchObj:
            logging.debug("Match for %s : %s"%(entry['key'], word))
            return(entry['key'])

    logging.warning ("no Match for category in : %s"%(word))
    return('unknown')

def cleanAmount(value):
    newValue = value.replace(".","")
    newValue = newValue.replace(",",".")
    return newValue

def assignEntry(date, desc, shortDesc, location, amount, yearOfStatement, assignCategory=True):
    tmp = {}
    # logger.debug(date+":"+ desc+":"+ shortDesc+":"+ location+":"+ amount+":"+ yearOfStatement)
    tmp['date'] = date
    if tmp['date'].split('.')[2]!="":
        tmp['formated date'] = datetime.datetime.strptime(tmp['date'], '%d.%m.%y')
    else:
        if tmp['date'].split('.')[1]=="01":
            tmp['formated date'] = datetime.datetime.strptime(tmp['date']+yearOfStatement, '%d.%m.%y')
        else:   
            tmp['formated date'] = datetime.datetime.strptime(tmp['date']+str(int(yearOfStatement)-1), '%d.%m.%y')
    tmp['short desc'] = desc
    tmp['desc'] = shortDesc
    if assignCategory:
        tmp['category'] = findCategory(tmp['desc'])
    tmp['location'] = location
    tmp['amount'] = cleanAmount(amount)
    return tmp

def textInterpretation(filename, outfile, found):
    with open(filename,encoding='utf-8') as txt_file:
        txt = txt_file.read()
        dateOfStatement = re.findall(r'Rechnungsdatum\s+\d\d\.\d\d\.\d\d(\d\d).*', txt)
        singleMatches = re.findall(r'^('+dateValue+')\s+('+dateValue+')\s+(\S+)\s+(.*)('+countryValues+')\s*('+amountValue+')(.*)$', txt, re.MULTILINE)
        multiMatches = re.findall(r'^('+dateValue+')\s+('+dateValue+')\s+(\S+)(.*)\n(\S*)\s*(\S*)('+countryValues+')\s*('+amountValue+')(.*)$', txt, re.MULTILINE)
        auslandMatches = re.findall(r'^('+dateValue+')\s+('+dateValue+')\s+(\d+\,\d+\%AUSLANDSEINSATZENTG\.V\.)\n(EUR|USD|MXN)\s*(\d+\.\d\d)\s*('+amountValue+')(.*)$', txt, re.MULTILINE)
        saldoMatches = re.findall(r'^('+dateValue+')\s+('+dateValue+')\s+('+chargeValues+')(.*)\s+('+amountValue+')(.*)$', txt, re.MULTILINE)
        saldoMatches1 = re.findall(r'^('+dateValue+')\s+('+dateValue+')\s+('+chargeValues+')(.*)\n([^0-9].*)\s+('+amountValue+')(.*)$', txt, re.MULTILINE)
        yearOfStatment = 0
        for i in dateOfStatement:
            logging.info("date "+",".join(i))
            yearOfStatment = i
        for i in singleMatches:
            logging.debug("single "+",".join(i))
            tmp = assignEntry(i[0], i[2], i[2]+i[3], i[4], i[5], yearOfStatment)
            found.append(tmp)
        for i in multiMatches:
            logging.debug("multi "+",".join(i))
            tmp = assignEntry(i[0], i[2], i[2]+i[3]+i[4]+i[5], i[6], i[7],yearOfStatment)
            found.append(tmp)
        for i in auslandMatches:
            logging.debug("ausland "+",".join(i))
            tmp = assignEntry(i[0], i[2], i[2]+i[3]+i[4], "DE", i[5],yearOfStatment)
            found.append(tmp)
        for i in saldoMatches:
            logging.debug("interst "+",".join(i))
            tmp = assignEntry(i[0], i[2], i[2]+i[3], "DE", i[4],yearOfStatment)
            found.append(tmp)
        for i in saldoMatches1:
            logging.debug("interst "+",".join(i))
            tmp = assignEntry(i[0], i[2], i[2]+i[3]+i[4], "DE", i[5],yearOfStatment)
            found.append(tmp)
    found.sort(key=lambda x:x['formated date'])
    fout = open(outfile, 'w', encoding='utf-8')    
    for entry in found:
        print(entry, file=fout)
    logging.info("found %s entries in file"%(len(found)))
    return (found, yearOfStatment)

def referenceOutput(filename, outfilename, yearOfStatment, references):
    with open(filename,encoding='utf-8') as txt_file:
        lines = txt_file.readlines()
        for line in lines:
            matches = re.search(r'^('+dateValue+')\s+('+dateValue+')\s+(\S+)(.*)', line)
            if matches:
                logging.debug("reference %s"%(line.rstrip()))
                tmp = assignEntry(matches.group(1), matches.group(3), matches.group(4), "","",yearOfStatment,False)
                references.append(tmp)

    references.sort(key=lambda x:x['formated date'])
    fout = open(outfilename, 'w', encoding='utf-8')    
    for item in references:
        print("%s %s %s %s"%(item['date'], item['formated date'], item['short desc'],item['desc']), file=fout)
    logging.info("found %s entries in reference"%(len(references)))
    return references

def pdf_to_text(pdf_path, output_txt):
    # Open the PDF file in read-binary mode
    with open(pdf_path, 'rb') as pdf_file:
        # Create a PdfReader object instead of PdfFileReader
        pdf_reader = PdfReader(pdf_file)

        # Initialize an empty string to store the text
        text = ''

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

    # Write the extracted text to a text file
    with open(output_txt, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

def entries_per_month(found):
    first = True
    counter=1
    endDate=datetime.date.today()
    for entry in found:
        if entry['formated date'].month==endDate.month:
            counter+=1
        else:
            if not first:
                print ("entries for month %s year %s : %s"%(endDate.month, endDate.year,counter))
            first = False
            counter=1

        endDate = entry['formated date']
        logging.debug(entry)
    print ("entries for month %s year %s : %s"%(endDate.month, endDate.year,counter))

def format_as_json(list, filename):
    new_list = []
    for entry in list:
        new_entry = {}
        for key, value in entry.items():
            if key=='formated date':
                time = value.strftime("%Y-%m-%d")
                new_entry['formated date'] = time
            else:
                new_entry[key] = value
        new_list.append(new_entry)

    with open(filename, 'w') as f: 
        json.dump(new_list, f)

def sortEntries(filename):
    print("sorting json  entries %s"%(filename))
    df = pd.read_json(filename)
    print("done")
    print(df.sort_values(by=['amount']))
    zinsList = ['Sollzinsen', 'Habenzinsen','Verzugszinsen']
    gutschriftList = ['Gutschrift', 'GUTSCHRIFT']
    print(df[df['short desc'].isin(zinsList)].sort_values(by=['amount']))
    print(df[df['short desc'].isin(gutschriftList)].sort_values(by=['amount']))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                  help="FILENAME to be analyzeds", metavar="FILE")
    parser.add_option("--jsonfile", dest="jsonfile",
                  help="Json FILENAME to be analyzeds", metavar="FILE")
    parser.add_option("-d", "--directory", dest="directory",
                  help="FILENAME to be analyzeds", metavar="FILE")
    parser.add_option("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="don't print status messages to stdout")

    (options, args) = parser.parse_args()
    pdf_path = options.filename
    output1_txt = 'trans.txt'
    output2_txt = 'found.txt'
    output3_txt = 'references.txt'
    output4_txt = 'found.json'
    if options.verbose:
        logger.setLevel(logging.DEBUG)
    if options.jsonfile:
        sortEntries(options.jsonfile)
        sys.exit(0)
    fileList = []
    if options.directory:
        for file in glob.glob(options.directory+"/Ihre*.pdf"):
            fileList.append(file)
    else:
        fileList.append(options.filename)
    found = []
    references = []
    for filename in fileList:
        pdf_to_text(filename, output1_txt)
        logging.info("PDF %s converted to text file %s"%(filename, output1_txt))
        (found, yearOfStatment) = textInterpretation(output1_txt, output2_txt, found)
        references = referenceOutput(output1_txt, output3_txt, yearOfStatment, references)
        logging.info("finished Interpretation")
    format_as_json(found, output4_txt)
    entries_per_month(found)