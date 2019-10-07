import subprocess
import os
import time
import slack
import datetime



delayMinutes = 5
client = slack.WebClient(token="--YOUR-TOKEN-HERE(good idea if passed through an ENV Variable)")
apps = ["--app=APP1","--app=APP2"]
appToChannelMap = {
	"--app=APP1":"#APP1-log-t",
	"--app=APP2":"#APP2-log-t"
}


def getNextAction(dynoAppParameter:str):
	if isDown(dynoAppParameter):
		informSlack(dynoAppParameter)
		return restartDyno(dynoAppParameter)
	return False


def isDown(dynoAppParameter:str)-> bool :
	rawStatus=subprocess.run(["heroku","ps",str(dynoAppParameter)],stdout=subprocess.PIPE)
	return str(rawStatus.stdout).split("\\")[1].split(" ")[1] != "up"

def restartDyno(dynoAppParameter:str)->bool:
	os.system("heroku ps:restart "+dynoAppParameter)
	return True

def informSlack(dynoAppParameter:str)->None:
	response = client.chat_postMessage(channel=appToChannelMap[dynoAppParameter],text="Dyno status was : DOWN , ps:restart triggered at "+str(datetime.datetime.now()).split(".")[0])


os.system("heroku login")
while(True):
	results = [getNextAction(everyApp) for everyApp in apps]
	print("LOOP"+str(results))
	time.sleep(60*delayMinutes)
