import csv
import urllib2
import json

def openFiles(fileToRead,fileToWrite):
    #open file to read
    with open(fileToRead, 'rb') as f:
        #open file to write
        with open(fileToWrite, "wb") as of:
            #use csv lib to for all .csv handling (read/write)
            csvRead = csv.DictReader(f, delimiter=',')
            writer = csv.writer(of, delimiter=',')
            #get column headers
            headers = csvRead.fieldnames
            #pass to read function
            rowRead(csvRead,writer)


def rowRead(csvRead,writer):
    #read CSV by rows
    for row in csvRead:
        #for each row, take call value from pixel column
        cellValue = row['impression_pixel_json']
        #if cell value isn't empty, pass for further processing
        if cellValue != '[]' and cellValue != 'NULL':
            rowWrite(csvRead,writer,cellValue)


def rowWrite(csvRead,writer,cellValue):
    try:
        #parse JSON to get URL string
        y = json.loads(cellValue)
        for var in y:
            #check if URL is secure
            e = checkHTTPS(var)
            #get URL response code
            i = urllib2.urlopen(var, timeout=5).getcode()
            #clean URL string for output
            l = json.dumps([var])
            #write results to new file
            writer.writerow(zip([l],[i],[e]))
            #The below is for debugging - left so you can see what's happening
            #var = URL string, i = status code
            print(var)
            print('\n')
            print(i)

    #if not valid JSON throw error
    except ValueError:
        print "Not Valid"
        print('\n')

    #if URL times out, throw error
    except urllib2.URLError:
        print "URL error occured"
        print('\n')


def checkHTTPS(urlString):
    #check if https is in the url and mark secure/unsecure
    if "https:" not in urlString:
        e='unsecure'
        return e
    else:
        e='secure'
        return e


#call this with desired input and output files (file to read from, file to write to)
openFiles('/Users/georgeseed/tl_test/SolutionsData.csv','/Users/georgeseed/tl_test/SolutionsData-Parsed.csv')
