from project.settings import main_app

def main():
    try:
        main_app.run(debug = True, port=7070)
    except Exception as error:
        print(error)


if __name__ == "__main__":
    main()


