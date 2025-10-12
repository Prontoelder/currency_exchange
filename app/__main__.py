import sys
from http.server import HTTPServer

from app.config import config
from app.container import container
from app.database.db_init import init_db
from app.routing.request_handler import RequestHandler


def main() -> None:
    init_db()
    RequestHandler.configurate(container.router, container.response_renderer)

    server_address = (config.host, config.port)
    server = HTTPServer(server_address, RequestHandler)
    print(f"Start server on: {server_address[0]}:{server_address[1]}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("Server has stopped")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Unexpected error: {error}")
        sys.exit(1)
