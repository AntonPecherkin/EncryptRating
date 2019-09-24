# from CryptoProvider.provider import CryptoProvider
from BulletinBoard.board import BulletinBoard


board = BulletinBoard(size=5, provider_uri='http://127.0.0.1:5000', device_id=1)
web_controller = board.make_web_controller()
web_controller.run(port=5001)