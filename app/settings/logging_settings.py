import logging


def setup_logger():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),  # Write logs to a file
            logging.StreamHandler()  # Print logs to the terminal
        ]
    )
