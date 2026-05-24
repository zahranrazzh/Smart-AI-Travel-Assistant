def load_css():

    with open("styles/style.css") as f:
        css = f.read()

    return f"<style>{css}</style>"