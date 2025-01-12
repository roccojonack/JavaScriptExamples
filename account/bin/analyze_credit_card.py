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
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

countryValues = "MT|FR|DE|NL|VA|LU|SE|US|CY|GR|IE|TR|AT|PT|IT|MX|GB|FI|HK|CH|IL|ES|CZ|TRY|HU|DK"
chargeValues = "GEBUEHR|Sollzinsen|Verzugszinsen|Habenzinsen|Gutschrift|GUTSCHRIFT|ZAHLUNG|UMBUCHUNG|KORREKTUR|BELASTUNG|JAHRESGEBUEHR|BARGELDAUSZAHLUNGSGEBUEHR|AUSZAHLUNG|REKLAMATIONSBETRAG|RECHNUNGSVERSAND"
dateValue = "\d\d\.\d\d\.*\d*\d*"
weekDayValue = "MO|DI|MI|DO|FR|SA|SO"
amountValue = "-*\d*\.*\d+\s*\,\d\d"
amountValueUS = "-*\d+\s*\.\d\d"
categories = []
categories.append({"key":"Housing","search":"Regus|MIETE|HELPLING|Allianz Lebensvers. AG|WEG Jakob-Hagenbucher-Strase 21-33 v.d.PHIDIAS"})
categories.append({"key":"Sports","search":"DAV WALTERSHAUSEN|MLF Mercator-Leasing|FITrate|FitLane|FIT\s*STAR|SPORT SCHECK|DECATHLON|BROOKS SPORTS|sport.*schuster"})
categories.append({"key":"Food/Groceries","search":"BOUCHERIE|ENOTECA|CUCINA|GASTRONOMIE|Aloha\s*POKE|CHEZ\s*JANOU|RUBENBAUER|Thi Minh Vietnam|GELATERIA|Hael\s*Alias\s*Kheder|BRASSERIE|BURRITO|Food|CREPERIE|LE\s*MOULIN\s*DE\s*FLOR|Taverna|Schlosswirtschaft|YORMAS|Mangostin|brauhaus|STARBUCKS|LE\s*PETIT\s*JOSSEL|affee|LE\s*WAITIKI|LE\s*MOULIN\s*DE\s*PAI|SCHUHBECKS|BANDERILLAS|AU\s*CHIEN\s*QUI\s*FUM|LA\s*ROTONDE|TABLE\s*DE\s*LOUISE|GOURMET|PANTELIAS|Markt|AU\s*PAIN|Bratort|Lowenbra|NORDSEE|yum2take|LES\s*CORMORANS|Augustiner\s*am\s*Dante|FLUNCH|die\s*Fasanerie|Hans\s*im\s*Gluck|Rostwerk|TABLE\s*DE\s*SAVOIE|Dinzler|DM\-Drogerie|COTIDIANO|PANTELIASNAXOS|TABLEDESAVOIE|COMPTOIR|sodexo|autobahnrast|HIT|GASTSTAETTEN|DALLMAYR|Goldhelm|HOFBRAEU|GASTHAUS|der\s*Andechser\*am\s*Dom|Biomarkt|BAECKER WIEDEMANN|au\s*pain\s*de\s*paul|LASARRASINE|BERG\s*AM\s*LAIMER\s*BACKHAU|michaeligarten|amorino|cafe|panera|sportalm|Segafredo|Mamma Bao|LUDWIG RIEDMAIR|CARREFOUR|Hofer|BILLA|REWE|SPAR|MONOPRIX|HIT-MARKT|Eataly|IHRHIT-MARKT|NETTO|Penny|ALDI|LIDL|V-MARKT|TENGELMANN|EDEKA|Rossman|MAX\s*RISCHART|Backhaus Nahrstedt|safeway|COFFEE|VINZENZ MURR|BIOFEINKOST|HITMuen|Ratschiller|Lieferando|Rasthaus|Restaurant|KAUFLAND|Pommefreunde|BAE*CKEREI|KONDITOREI|NORDSEEGMBH|SAFFER WEIN|BURRITO COMPANY|DinzlerAG|Biergarten|Lebensmittel|STERIA|Raststaette|AUTOGRILL|El Espanol|Gasteig|SUZANA|NAMMOS|BISTRO|BAR|DIOS\s*MINGA|Foodora|Pizza|Pizzeria|GASTEIGKULT&SPEISE|RISTORANTE|Zen Panasia|Restaurant|SPATENHAUS|SUSHI.WRAP|Alter\s*Wirt|WIRTSHAUS|gaspis\s*Gerlos|CARREFEXPRESSS|FRANPRIX|sushi|dosminga|villadante|elespanol|apostels|munich-bowling|saroor|backstube|aumeister|food\s*breizh|hirschgar|brioche\s*doree|casino|sangeet|geant|BOULANGERIE"})
categories.append({"key":"Utilities (Electricity, Water, Gas, Phone, Internet, etc.)","search":"Telefonica|E-Plus Service GmbH|SWM Ver|1[u+]1\s*Telecom|M-net Telek|SWM Versorgungs GmbH|undfunk ARD, ZDF, DRadio|stadt muenchen"})
categories.append({"key":"Home improvement", "search":"bauhaus|DEHNER GARTEN-Center|castorama|HOEFFNER|Hoffner|IKEA|V-BAUM|HORNBACH|Hagebau|toom"})
categories.append({"key":"Healthcare/Medical","search":"FIELMANN|Techniker Krankenkasse|DR WILLECKE|DOCTORDUVE|PODOLOGI|Apotheke|APOTHEKE|ZAHNARZT|Praxis|Hautzentrum|Laserzentrum|Medical\s*Spa|pharmacie"})
categories.append({"key":"Insurance (Health, Life, Auto, Home, etc.)","search":"DBV Deutsche Beamten|DEURAG|HDI\s*Global|VERSICHERUNG"})
categories.append({"key":"Debt Payments (Credit cards, Loans, fees, etc.)","search":"Grundgebühr für|INTERNE UMBUCHUNG|ZAHLUNGPERBANKEINZUG|AUSLANDSEINSATZ|DEUTSCHEBANK|BARGELDABHEBUNG|BARGELDAUSZAHLUNG|ATM|HVB|STADTSPARKASSE|DEUTSCHE BANK|UMBUCHUNGBARGELDABHEBUNG|VRBANK|SPARDA-BANK|COMMERZBANK|POSTBANK|ISA SERVICE|FINANZAMT|Finanzamt|DRV BUND|Rundfunk ARD ZDF|KATHI KLEMM"})
categories.append({"key":"Savings/Investments","search":"TARGO VERSICHERUNG|WERTPAPIERKAUF"})
categories.append({"key":"Entertainment/Recreation","search":"GLORIA.*PALAST|Munchen Musik|LOUVRE|cinema|kino|philharmonie|opera"})
categories.append({"key":"Personal Care (Grooming, Toiletries, etc.)","search":"hairstyle|paradiso|ZEROSTORE|deichman|SCHUHE|H&M|RENO|ZARA"})
categories.append({"key":"PayPal","search":"PayPal"})
categories.append({"key":"Income","search":"Minres technologies|GUTSCHRIFT ARTERISINC|Bundesagentur furArbeit-Service-Haus"})
categories.append({"key":"Shopping/Personal Goods","search":"GALERIA KAUFHOF|AMAZON|MEDIA\s*MARKT|Conrad|Saturn|DELL|AMZN|SPORTSCHECK|DM-DrogerieMarkt"})
categories.append({"key":"Travel/Vacation/Transport","search":"Autobus Oberbayern|AIR MALTA|FLUEGEDE|PARKHAUS|METRO\s*DE\s*MADRID|AUTOST|AUTOPISTA|RATP|COFIROUTE|easypark|LELOGIS VERSAILLAIS|steigenberger|skyfall|gerlosperle|SKODA AUTOHAUS LIEBE|MUE VERKEHRSGESELL|escot|mautstelle|FewoDirekt|RATPPARIS|TIER|rentalcars.com|PARKPLATZ|Tankautomat|GIP |AGIP|ESSO |BP |Eni\s*Service|shell|Tankstelle|SNCF|RENT A CAR|G1|ARAL|Aral|GETT|Taxi|uber|TOTAL|Stattauto|AUTO EUROPE|HERTZ|ALAMO|ENTERPRISE|Europcar|RENTALCARS.COM|RENTAL CAR|AUTOEUROPE|TANKSTELLE|DriveNow|Drive Now|DB\s*AUTOMAT|DB VERTRIEB|DB\s*BAHN|DB\s*FERNVERKEHR|LUFTHANSA|airline|MVG|Meridian|Flixbus|EUROPCAR|DBVertrieb|Hotel|HOTEL|appartment|appartement|airbnb|vrbo|united|fox rent a car"})
categories.append({"key":"Subscriptions (Streaming, Magazines, etc.)","search":"kindle|Spotify|Netflix|HEISE|Audible|Google|IWG DEUTSCHLAND|RegusMunchen|GooglePayment|DPV Deutscher Pressevertrieb GmbH|Exaring"})
categories.append({"key":"Cash withdraw","search":"BARGELDABHEBUNG"})
categories.append({"key":"Credit card","search":chargeValues+"|ANFANGSSALDO|ENDSALDO"})
 
def findCategory (word): 
    for entry in categories:
        matchObj = re.search(entry['search'],word,re.IGNORECASE)
        if matchObj:
            logging.debug("Match for %s : %s"%(entry['key'], word))
            return(entry['key'])

    logging.warning ("no Match for category in : %s"%(word))
    return('unknown')

def cleanAmount(value):
    newValue = value.replace(".","")
    newValue = newValue.replace(",",".")
    newValue = newValue.replace(" ","")
    return newValue

def assignEntry(date, desc, shortDesc, location, amount, yearOfStatement, monthOfStatment, assignCategory=True, saldo="0.0", prevSaldo="0.0"):
    tmp = {}
    logger.debug(date+":"+ desc+":"+ shortDesc+":"+ location+":"+ amount+":"+str(yearOfStatement)+":"+str(monthOfStatment)+":"+saldo+":"+prevSaldo)
    if not date.endswith('.'):
        if len(date.split('.'))==2:
            tmp['date'] = date+'.'
        else:
            tmp['date'] = date
    else:
        tmp['date'] = date
    if tmp['date'].split('.')[2]!="":
        tmp['formated date'] = datetime.datetime.strptime(tmp['date'], '%d.%m.%y')
    else:
        if monthOfStatment=="01":
            if tmp['date'].split('.')[1]=="12":
                tmp['formated date'] = datetime.datetime.strptime(tmp['date']+str(int(yearOfStatement)-1), '%d.%m.%y')
            else:   
                tmp['formated date'] = datetime.datetime.strptime(tmp['date']+yearOfStatement, '%d.%m.%y')
        else:
            tmp['formated date'] = datetime.datetime.strptime(tmp['date']+yearOfStatement, '%d.%m.%y')

    tmp['short desc'] = desc
    tmp['desc'] = shortDesc
    if assignCategory:
        tmp['category'] = findCategory(tmp['desc'])
    tmp['location'] = location
    if float(cleanAmount(saldo))>=float(cleanAmount(prevSaldo)):
        tmp['amount'] = cleanAmount(amount)
    else:
        tmp['amount'] = '-'+cleanAmount(amount)
    tmp['saldo'] = cleanAmount(saldo)
    return tmp

def textInterpretationCredit(filename, outfile, found):
    with open(filename,encoding='utf-8') as txt_file:
        txt = txt_file.read()
        dateOfStatement = re.findall(r'Rechnungsdatum\s+\d\d\.(\d\d)\.\d\d(\d\d).*', txt)
        singleMatches = re.findall(r'^('+dateValue+')\s+('+dateValue+')\s+(.*)('+countryValues+')\s+('+amountValue+')(.*)$', txt, re.IGNORECASE|re.MULTILINE)
        multiMatches = re.findall(r'^('+dateValue+')\s+('+dateValue+')\s+(\S+)(.*)\n(\S*)\s*(\S*)('+countryValues+')\s*('+amountValue+')(.*)$', txt, flags=re.MULTILINE|re.IGNORECASE)
        auslandMatches = re.findall(r'^('+dateValue+')\s+('+dateValue+')\s+(\d+\,\d+\%AUSLANDSEINSATZENTG\.V\.)\n*\s*(TRY|GBP|EUR|USD|MXN|F\.CHF)\s*('+amountValueUS+')\s*('+amountValue+')(.*)$', txt, re.MULTILINE)
        auslandMatches1 = re.findall(r'^('+dateValue+')\s+('+dateValue+')\s+(AUSLANDSEINSATZENTG\.)\s+F\.(EUR|USD|MXN|CHF|ILS|HUF|DKK|CZK)\s*('+amountValueUS+')\s*('+amountValue+')(.*)$', txt, re.MULTILINE)
        auslandMatches2 = re.findall(r'^('+dateValue+')\s+('+dateValue+')\s+(GUTSCHRIFT\s+AUSLANDSEINSATZENTGELT)\n+(.*)('+amountValue+')$', txt, re.MULTILINE)
        saldoMatchesSingle = re.findall(r'^('+dateValue+')\s+('+dateValue+')\s+.*('+chargeValues+')(.*)\s+('+amountValue+')(.*)$', txt, re.MULTILINE)
        saldoMatchesMulti = re.findall(r'^('+dateValue+')\s+('+dateValue+')\s+('+chargeValues+')(.*)\n([^0-9][a-zA-Z]*)\s*('+amountValue+')(.*)$', txt, re.MULTILINE)
        conditionMatchesSingle = re.findall(r'^('+dateValue+')\s+('+dateValue+')\s+(\+\+\+Danke)(.*)$', txt, re.MULTILINE)
        yearOfStatment = 0
        monthOfStatement = 0
        for i in dateOfStatement:
            monthOfStatement = i[0]
            yearOfStatment = i[1]
            logging.debug("Rechnungsdatum "+monthOfStatement+" "+yearOfStatment)
        for i in singleMatches:
            logging.debug("single "+":".join(i))
            tmp = assignEntry(i[0], i[2], i[2], i[3], i[4], yearOfStatment, monthOfStatement)
            found.append(tmp)
        for i in multiMatches:
            logging.debug("multi "+",".join(i))
            tmp = assignEntry(i[0], i[2], i[2]+i[3]+i[4]+i[5], i[6], i[7], yearOfStatment, monthOfStatement)
            found.append(tmp)
        for i in auslandMatches:
            logging.debug("ausland "+",".join(i))
            tmp = assignEntry(i[0], i[2], i[2]+i[3]+i[4], "DE", i[5], yearOfStatment, monthOfStatement)
            found.append(tmp)
        for i in auslandMatches1:
            logging.debug("ausland1 "+",".join(i))
            tmp = assignEntry(i[0], i[2], i[2], i[3], i[5], yearOfStatment, monthOfStatement)
            found.append(tmp)
        for i in auslandMatches2:
            logging.debug("ausland2 "+",".join(i))
            tmp = assignEntry(i[0], i[2], i[2]+i[3], "DE", i[4], yearOfStatment, monthOfStatement)
            found.append(tmp)
        for i in saldoMatchesSingle:
            logging.debug("interst "+",".join(i))
            tmp = assignEntry(i[0], i[2], i[2]+i[3], "DE", i[4],yearOfStatment,monthOfStatement)
            found.append(tmp)
        for i in saldoMatchesMulti:
            logging.debug("interst1 "+",".join(i))
            tmp = assignEntry(i[0], i[2], i[2]+i[3]+i[4], "DE", i[5],yearOfStatment,monthOfStatement)
            found.append(tmp)
        for i in conditionMatchesSingle:
            logging.debug("condition "+",".join(i))
            tmp = assignEntry(i[0], i[2], i[2]+i[3], "DE", "0,0",yearOfStatment,monthOfStatement)
            found.append(tmp)

    found.sort(key=lambda x:x['formated date'])
    fout = open(outfile, 'w', encoding='utf-8')    
    for entry in found:
        print(entry, file=fout)
    logging.info("found %s entries in file"%(len(found)))
    return (found, yearOfStatment, monthOfStatement)

def textInterpretationGiro(filename, outfile, found):
    with open(filename,encoding='utf-8') as txt_file:
        txt = txt_file.read()
        dateOfStatement = re.findall(r'Girokontoauszug\s+vom\s+\d\d\.(\d\d)\.\d\d(\d\d)\s*-\s*\d\d\.(\d\d)\.\d\d(\d\d)', txt)
        saldoMatches = re.findall(r'^('+dateValue+')\s+('+weekDayValue+')\s+('+amountValue+')\s+(ANFANGSSALDO|ENDSALDO)$', txt, re.MULTILINE)
        singleMatches = re.findall(r'^('+dateValue+')\s+('+weekDayValue+')\s+('+amountValue+')\s+('+amountValue+')\s+(.*)\n(.*)$', txt, re.MULTILINE)
        yearOfStatment = 0
        monthOfStatement = 0
        prevSaldo = "0,0"
        for i in dateOfStatement:
            monthOfStatement = i[0]
            yearOfStatment = i[1]
            logging.debug("Rechnungsdatum "+monthOfStatement+" "+yearOfStatment)
        for i in saldoMatches:
            logging.debug("saldo "+",".join(i))
            tmp = assignEntry(i[0], i[3], i[3], "DE", i[2], yearOfStatment, monthOfStatement,False)
            found.append(tmp)
            if i[3]=="ANFANGSSALDO":
                prevSaldo = i[2]
        for i in singleMatches:
            logging.debug("single "+",".join(i))
            tmp = assignEntry(i[0], i[4], i[4]+" "+i[5], "DE", i[2], yearOfStatment, monthOfStatement,True,i[3],prevSaldo)
            prevSaldo = i[3]
            found.append(tmp)
    found.sort(key=lambda x:x['formated date'])
    fout = open(outfile, 'w', encoding='utf-8')    
    for entry in found:
        print(entry, file=fout)
    logging.info("found %s entries in file"%(len(found)))
    return (found, yearOfStatment, monthOfStatement)

def referenceOutput(filename, outfilename, yearOfStatment, monthOfStatement, references):
    with open(filename,encoding='utf-8') as txt_file:
        lines = txt_file.readlines()
        for line in lines:
            matches = re.search(r'^('+dateValue+')\s+('+dateValue+')\s+(\S+)(.*)', line)
            if matches:
                logging.debug("reference %s"%(line.rstrip()))
                tmp = assignEntry(matches.group(1), matches.group(3), matches.group(4), "","",yearOfStatment,monthOfStatement, False)
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
                logger.ino("entries for month %s year %s : %s"%(endDate.month, endDate.year,counter))
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
                # print(key, value)
                new_entry[key] = value
        new_list.append(new_entry)

    with open(filename, 'w') as f: 
        json.dump(new_list, f, ensure_ascii=False, indent=4)

def sortEntries(filename):
    logger.info("sorting json entries %s"%(filename))
    df = pd.read_json(filename)
    print(df.sort_values(by=['amount']))
    zinsList = ['Sollzinsen', 'Habenzinsen','Verzugszinsen']
    gutschriftList = ['Gutschrift', 'GUTSCHRIFT']
    bonusList = ['GUTSCHRIFT FUER EINGELOESTEBONUSPUNKTE', 'GUTSCHRIFT FUER EINGELOESTE BONUSPUNKTE']
    costList = ['BELASTUNG JAHRESBEITRAG', 'JAHRESGEBUEHR ZUSATZKARTE']
    print(df[df['short desc'].isin(zinsList)].sort_values(by=['amount']))
    print(df[df['short desc'].isin(gutschriftList)].sort_values(by=['amount']))
    print(df[df['desc'].isin(bonusList)].sort_values(by=['amount']))
    print(df[df['desc'].isin(costList)])
    print(df.groupby(['category']).count())
    print(df.loc[df['category']=="Credit card"].groupby(['short desc']).count())
    df2 = df.loc[df['category']=="Subscriptions (Streaming, Magazines, etc.)"]
    print(df2.groupby('short desc').sum())
    print(df2['amount'].sum())
    df1 = df[df['desc'].isin(bonusList)]
    df1 = df1[['formated date','amount']]
    df1["amount"] = pd.to_numeric(df1["amount"])
    print(df1)
    #df1.plot.bar(x='formated date')
    #plt.show()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                  help="FILENAME to be analyzeds", metavar="FILE")
    parser.add_option("--giro", dest="giro_mode",
                  help="FILENAME to be analyzed as Giro", action="store_true", default=False)
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
        for file in glob.glob(options.directory+"/*.pdf"):
            fileList.append(file)
    else:
        if options.filename:
            fileList.append(options.filename)
    found = []
    references = []
    for filename in fileList:
        pdf_to_text(filename, output1_txt)
        logging.info("PDF %s converted to text file %s"%(filename, output1_txt))
        if options.giro_mode:
            (found, yearOfStatment, monthOfStatement) = textInterpretationGiro(output1_txt, output2_txt, found)
        else:
            (found, yearOfStatment, monthOfStatement) = textInterpretationCredit(output1_txt, output2_txt, found)
            references = referenceOutput(output1_txt, output3_txt, yearOfStatment, monthOfStatement, references)
        logging.info("finished Interpretation")
    format_as_json(found, output4_txt)
    # entries_per_month(found)