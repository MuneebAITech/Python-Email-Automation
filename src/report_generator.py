from datetime import datetime


def create_report(
    total,
    sent,
    failed
):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        "outputs/summary_report.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            f"Date: {timestamp}\n\n"
        )

        file.write(
            f"Total Emails : {total}\n"
        )

        file.write(
            f"Sent         : {sent}\n"
        )

        file.write(
            f"Failed       : {failed}\n"
        )