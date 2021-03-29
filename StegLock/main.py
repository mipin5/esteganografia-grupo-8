from website import create_app

app = create_app()

if __name__ == '__main__':
    # Si el servidor está en pruebas (debug=True)
    # Si está en producción (debug=False)
    app.run(debug=True)
