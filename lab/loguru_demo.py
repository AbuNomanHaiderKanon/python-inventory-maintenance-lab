from loguru import logger

from target import run_workload


logger.add(
    "lab/loguru_output.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {function} | {message}",
    level="DEBUG",
    diagnose=False,
)


def main() -> None:
    logger.info("Starting inventory maintenance workload")
    result = run_workload()
    logger.success("Workload completed: {}", result)


if __name__ == "__main__":
    main()
