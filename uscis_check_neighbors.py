import requests as r
import datetime
import sys

dic_res = {"Pass":[],"Pending":[]}

def cmdArgument():
    receipt_num, no_neighs, ctr = '$', -45, 0

    if(len(sys.argv) != 5):
        print("Usage: uscis_check_neighbors.py -r [receipt_num] -n [no_neighs]")
        sys.exit(0)

    for i in range(1,len(sys.argv)):
        if(sys.argv[i] == '-r'):
            if(len(sys.argv[i+1]) != 13):
                print("Usage: uscis_check_neighbors.py -r [receipt_num] -n [no_neighs]")
                sys.exit(0)
                
            receipt_num, ctr = sys.argv[i+1], ctr + 1
            
        elif(sys.argv[i] == '-n'):
            try:
                no_neighs = int(sys.argv[i+1])
            except ValueError:
                print("Usage: uscis_check_neighbors.py -r [receipt_num] -n [no_neighs]")
                sys.exit(0)
            
            if(no_neighs < 0):
                print("Usage: uscis_check_neighbors.py -r [receipt_num] -n [no_neighs]")
                sys.exit(0)
                
            ctr += 1
                
    if(ctr != 2):
        print("Usage: uscis_check_neighbors.py -r [receipt_num] -n [no_neighs]")
        sys.exit(0)

    return receipt_num, no_neighs

def automated_search(receipt_num, no_neighs):
    for i in range(no_neighs+1):
        case1, case2 = receipt_num[:3] + str(int(receipt_num[3:]) - i), receipt_num[:3] + str(int(receipt_num[3:]) + i)
        tmp1, tmp2 = r.post('https://egov.uscis.gov/casestatus/mycasestatus.do' ,data={'appReceiptNum':case1}), r.post('https://egov.uscis.gov/casestatus/mycasestatus.do',data={'appReceiptNum':case2})

        profile = {'receipt_num':'','date_time':'','status':''}
        profile['receipt_num'], profile['date_time'] = case1, datetime.datetime.now().strftime('20%y/%m/%d - %H:%M:%S')
        
        if(tmp1.text.find('new card')!= -1):
            profile['status'] = 'Pass'
            dic_res['Pass'].append(profile)
        else:
            profile['status'] = 'Pending'
            dic_res['Pending'].append(profile)

        profile = {'receipt_num':'','date_time':'','status':''}
        profile['receipt_num'], profile['date_time'] = case2, datetime.datetime.now().strftime('20%y/%m/%d - %H:%M:%S')
        
        if(tmp2.text.find('new card')!= -1):
            profile['status'] = 'Pass'
            dic_res['Pass'].append(profile)
        else:
            profile['status'] = 'Pending'
            dic_res['Pending'].append(profile)
            

def analysis_result():
    filee = open("result.txt",'a+')
    filee.write('-------------------------------------------------------------------------------------------------------------------------------------------\n')
    filee.write('| ' + datetime.datetime.now().strftime('20%y/%m/%d') + ' | ' + "Total Pass: %d | and | Total Pending: %d\n" % (len(dic_res['Pass']), len(dic_res['Pending'])))
    filee.write('-------------------------------------------------------------------------------------------------------------------------------------------\n\n')
    filee.write('For Pass\n')

    for profile in dic_res['Pass']:
        filee.write( 'Case Number: ' + profile['receipt_num']+ '  ' + 'Date Time: ' + profile['date_time'] + '  ' + 'Status: ' + profile['status'] + '\n')

    filee.write('\n\nFor Pending\n')

    for profile in dic_res['Pending']:
        filee.write('Case Number: ' + profile['receipt_num']+ '  ' + 'Date Time: ' + profile['date_time'] + '  ' + 'Status: ' + profile['status'] + '\n')

    filee.write('\n\n')
    
    filee.close()
    
def main():
    receipt_num, no_neighs = cmdArgument()
    automated_search(receipt_num, no_neighs)
    analysis_result()

if __name__ == '__main__':
    main()
