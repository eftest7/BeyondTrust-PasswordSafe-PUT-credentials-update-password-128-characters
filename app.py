import config
import requests
import urllib3
import random
import string

#disable https warnings
urllib3.disable_warnings()

#bi server and header info
BIServer = "bi.ef.lab"
BaseURL="https://bi.ef.lab/BeyondTrust/api/public/v3"
auth_head='PS-Auth key={}; runas={};'.format(config.APIKey,config.biUsername)
header = {'Authorization': auth_head}
DataType={'Content-type':'application/json'}
session = requests.Session()
session.headers.update(header)

#Sign into BeyondInsight with URL and header information
url=BaseURL + '/Auth/SignAppin'
session.post(url=url,verify=False)

#asset and account information to PUT password for
assetname = "DC112"
manacct = "apiadmin"
#domainname = "ef.lab"

### - Password Generation
#input the length of password
#length = int(input('\nEnter the length of password: '))                      
#define data
lower = string.ascii_lowercase
upper = string.ascii_uppercase
num = string.digits
#symbols = string.punctuation
#string.ascii_letters

#combine the data
all = lower + upper + num

#use random generated password with 24 characters
temp = random.sample(all,24)

#create the password 
genpassword = "".join(temp)

#print the password
print(genpassword)

#get hostname and instance name from managed system list
urlMansys = BaseURL + '/ManagedSystems'
mansyslist = session.get(urlMansys,verify=False)
mansysjson = mansyslist.json()

#loop managed system list by asset name to find assetID and system ID
for asset in mansysjson:
    if asset['HostName'] == assetname:
        assetID = asset['HostName']
        #print(assetID)
        #instance01 = asset['InstanceName']
        #dbname = '{}/{}'.format(assetID,instance01)
        mansysID = asset['ManagedSystemID']
        #print(mansysID)

        #get managed account list
        urlManAcct = BaseURL + '/ManagedAccounts'
        manacctlist = session.get(urlManAcct,verify=False)
        manacctjson = manacctlist.json()

        #loop managed accounts list by account name to find assetID
        for account in manacctjson:
            if account['AccountName'] == manacct:
                accountID = account['AccountId']
                
                #build password update request in json
                urlcredupdate = BaseURL + '/ManagedAccounts/{}/Credentials'.format(accountID)
                #print(urlcredupdate)
                req = {
                    'Password': genpassword,
                    'PublicKey': config.APIKey,
                    'UpdateSystem': 'false'
                    }
                # #submit request to update the password
                reqnum = session.put(urlcredupdate, data=req)
                print(reqnum)

                #if statement to return status code 204 for success
                if reqnum.status_code == 204:
                    print("Success! The password was updated to the generated password")
                else:
                    print("Error: Please check the request config")
        break
        #         # print(account['SystemName'])
        #         # print(account['AccountName'])
