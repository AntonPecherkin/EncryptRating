from CryptoProvider.provider import CryptoProvider
# from BulletinBoard.board import BulletinBoard

provider = CryptoProvider(device_id=1)
web_controller = provider.make_web_controller()
web_controller.run()

# board = BulletinBoard(size=5)
# web_controller = board.make_web_controller()
# web_controller.run()