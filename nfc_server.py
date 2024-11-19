import asyncio
# import websockets
from websockets.asyncio.server import serve
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString
from py122u import nfc
import time
import json

ws_connected = set()

class NFCObserver(CardObserver):
    """A simple card observer that prints card events."""

    def __init__(self, websocket, loop):
        super().__init__()
        self.websocket = websocket
        self.loop = loop

    def update(self, observable, actions):
        # 分別處理卡片插入和移除事件
        (added_cards, removed_cards) = actions
        # 只在 request 的 path 為 '/nfc' 時處理卡片事件
        if self.websocket.request.path == '/nfc':
            # 卡插入事件
            for card in added_cards:
                asyncio.run_coroutine_threadsafe(self.handle_card_inserted(card), self.loop)

            # 卡移除事件
            for card in removed_cards:
                asyncio.run_coroutine_threadsafe(self.handle_card_removed(card), self.loop)


    async def handle_card_inserted(self, card):
        # 當卡片插入時被呼叫
        uid = None
        try:
            reader = nfc.Reader()   
            reader.connect()
            uid = reader.get_uid()  # 嘗試獲取卡片的 UID
        except Exception as e:
            print(f"Error occurred: {e}")
        
        if uid:
            # 如果成功獲取 UID，建立訊息並透過 WebSocket 發送
            message = {
                "uid": toHexString(uid),
                "atr": toHexString(card.atr),
                "type": "insert"
            }
            print(message)
            await self.websocket.send(json.dumps(message))
            await self.websocket.close()  # 斷開 WebSocket 連接

    async def handle_card_removed(self, card):
        # 當卡片移除時被呼叫
        message = {
            "atr": toHexString(card.atr),
            "type": "remove"
        }
        print(message)
        await self.websocket.send(json.dumps(message))
        await self.websocket.close()  # 斷開 WebSocket 連接

async def RFID_monitor(websocket):
    ws_connected.add(websocket)

    # 啟動卡片監控
    loop = asyncio.get_event_loop()
    card_monitor = CardMonitor()
    card_observer = NFCObserver(websocket, loop)

    card_monitor.addObserver(card_observer)

    print("Monitoring NFC card events. Press Ctrl+C to exit.")
    try:
        while True:
            await asyncio.sleep(1)  # 每秒休眠一次，等待卡片事件
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        card_monitor.deleteObserver(card_observer)
        ws_connected.remove(websocket)

async def main():
    # 啟動 WebSocket 伺服器，監聽本地主機的 8865 埠
    # server = await websockets.serve(RFID_monitor, "localhost", 8865)
    async with serve(RFID_monitor, "localhost", 8865) as server:
        print("WebSocket server started on ws://localhost:8865")
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())  # 使用 asyncio.run 啟動應用程式
