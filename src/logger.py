from datetime import datetime


def log_success(name, email):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        "outputs/success.log",
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            f"{timestamp} | {name} | {email}\n"
        )


def log_failed(email, error):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        "outputs/failed.log",
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            f"{timestamp} | {email} | {error}\n"
        )