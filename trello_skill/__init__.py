from .intents import alex

wsgi = alex.create_wsgi_app()  # use in production


if __name__ == '__main__':
    # run debug server locally
    alex.run('127.0.0.1', 8080, debug=True)
