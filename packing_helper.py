from utils.llm_helper import get_gemini_response


def generate_packing(destination):

    prompt = f"""
    Buat packing checklist untuk traveling ke {destination}.
    """

    return get_gemini_response(prompt)