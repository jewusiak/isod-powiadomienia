import functions
from jsoncomparison import Compare, NO_DIFF

import passes

last_resp_json=functions.getOldJson()
new_resp_response=functions.getNewResp(passes.getUsername(), passes.getWAPI())
new_resp_json=new_resp_response.json()




it=0
first_old = last_resp_json["items"][0]["hash"]
if first_old!=new_resp_json["items"][0]["hash"]:
    while it<10:
        if first_old!=new_resp_json["items"][it]["hash"]:
            it+=1
        else:
            break
#czyli elementy od 0 do it-1 są nowe
if(it>0):
    functions.sendUpdates(new_resp_json["items"][0:it], passes.getToEmail())

functions.writeToFile(new_resp_response.text)



