from app_demo.config import create_app

if __name__ == "__main__":
    app = create_app("default")
    app.run(port=8880, debug=True)
