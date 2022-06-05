from src import init_app

app = init_app()


if __name__ == '__main__':
    import logging
    logging.basicConfig(filename='info.log', level=logging.INFO)
    app.run(host='0.0.0.0', port=5090, debug=True, use_reloader=False)
