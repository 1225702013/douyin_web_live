# ! IMPORT ! make sure you ran mitmproxy with this script, 
# eg: `/path/to/mitmproxy -s mitmproxy.py`

import uuid
from mitmproxy import http
import re

class Writer:
    def websocket_message(self, flow: http.HTTPFlow) :
        re_c = re.search('webcast3-ws-web-.*\.douyin\.com', flow.request.host)
        if re_c :
            with open('./dir/' + uuid.uuid4().hex, 'wb') as f:
                mess = flow.websocket.messages[-1].content
                f.write(bytes(mess))

addons = [Writer()]
