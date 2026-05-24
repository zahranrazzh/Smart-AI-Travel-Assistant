from utils.llm_helper import get_gemini_response


def generate_itinerary(destination, days, budget):

    prompt = f"""
    Buat itinerary traveling.

    Destinasi: {destination}
    Durasi: {days} hari
    Budget: {budget}

    Berikan:
    - itinerary harian
    - tempat wisata
    - estimasi biaya
    - tempat makan
    """

    return get_gemini_response(prompt)