import uvicorn

import whoami


if __name__ == "__main__":
    uvicorn.run(whoami.app, port=8000, host="0.0.0.0")
