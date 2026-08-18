from dataclasses import dataclass


@dataclass(frozen=True)
class Credentials:
    username: str
    password: str


THE_INTERNET_VALID = Credentials(username="tomsmith", password="SuperSecretPassword!")
THE_INTERNET_INVALID = Credentials(username="tomsmith", password="wrong-password")

SAUCEDEMO_VALID = Credentials(username="standard_user", password="secret_sauce")
