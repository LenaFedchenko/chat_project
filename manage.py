from project.settings import socketio, main_app
import project

def main():
    try:
        project.execute()
        socketio.run(app= main_app, debug = True, port=7060)
    except Exception as error:
        print(error)


if __name__ == "__main__":
    main()


