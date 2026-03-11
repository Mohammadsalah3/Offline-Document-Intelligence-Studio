import traceback
import uvicorn

from app.main import app


def main():
    try:
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000
        )
    except Exception:
        traceback.print_exc()
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()