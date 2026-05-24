from utils.llm_helper import get_gemini_response


def generate_budget(destination, days):

    prompt = f"""
    Buat estimasi budget traveling.

    Destinasi: {destination}
    Durasi: {days} hari

    Berikan:
    - hotel
    - transportasi
    - makan
    - wisata
    - total estimasi
    """

    return get_gemini_response(prompt)