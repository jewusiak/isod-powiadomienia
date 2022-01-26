import functions
from jsoncomparison import Compare, NO_DIFF

import passes

last_resp=functions.getOldJson()
new_raw_resp=functions.getNewResp(passes.getUsername(), passes.getWAPI())
new_resp=new_raw_resp.json()

diff=Compare().check(last_resp, new_raw_resp.json())


it=0
if diff != NO_DIFF:
    first_old = last_resp["items"][0]
    while it<10:
        if Compare().check(first_old, new_resp["items"][it])!=NO_DIFF:
            it+=1
        else:
            break
#czyli elementy od 0 do it-1 są nowe
if(it>0):
    functions.sendUpdates(new_resp["items"][0:it],passes.getToEmail())

functions.writeToFile(new_raw_resp)



