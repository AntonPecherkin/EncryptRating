import click
import nufhe

from CryptoProvider.provider import CryptoProvider
from BulletinBoard.board import BulletinBoard



# provider = CryptoProvider(device_id=1)
# web_controller = provider.make_web_controller()
# web_controller.run()

# board = BulletinBoard(size=5)
# web_controller = board.make_web_controller()
# web_controller.run()

@click.command()
@click.option('--api', default=None, help='Execution environment: CUDA/OpenCL')
@click.option('--device-id', help="Computation device identifier", type=click.INT, default=0)
@click.option('--bulletin-board', help="Run as BulletinBoard", is_flag=True)
@click.option('--crypto-provider', help="Run as CryptoProvider", is_flag=True)
@click.option('--uri', help='URI of crypto-provider')
@click.option('--port', help="Port", type=click.INT, default=5000)
def main(api,
         device_id,

         ## Mode
         bulletin_board,
         crypto_provider,
         
         ## Web
         uri,
         port):
    devices = nufhe.find_devices(api=api)
    ctx = nufhe.Context(device_id=devices[device_id])

    if bulletin_board:
        board = BulletinBoard(size=5, provider_uri=uri, ctx=ctx)
        web_controller = board.make_web_controller()

    if crypto_provider:
        provider = CryptoProvider(ctx)
        web_controller = provider.make_web_controller()


    web_controller.run(port=port)

if __name__ == "__main__":
    main()