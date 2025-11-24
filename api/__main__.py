"""Module entrypoint for GuardSpecs scaffold."""

from api.app import create_app


if __name__ == "__main__":
    app = create_app()
    print("GuardSpecs scaffold initialized:", app)
