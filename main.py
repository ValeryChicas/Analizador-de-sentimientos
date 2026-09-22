import time
from textblob import TextBlob
from deep_translator import GoogleTranslator, MyMemoryTranslator


def translate_to_english(text, retries=2, delay=1.5):
    """
    Traduce a inglés con reintentos. Si Google falla, intenta con MyMemory
    (un traductor gratuito alternativo) antes de rendirse.
    Devuelve (texto_traducido, se_pudo_traducir).
    """
    # Intento 1: Google Translate, con reintentos
    for attempt in range(retries):
        try:
            translated = GoogleTranslator(source='es', target='en').translate(text)
            if translated:
                return translated, True
        except Exception:
            time.sleep(delay)

    # Intento 2: MyMemory como respaldo si Google sigue fallando
    try:
        translated = MyMemoryTranslator(source='es-ES', target='en-GB').translate(text)
        if translated:
            return translated, True
    except Exception:
        pass

    # Si ambos fallan, avisamos en vez de analizar español crudo con TextBlob (inglés)
    return text, False


def analyze_comments(comments_list):
    total_polarity = 0
    counts = {"Positivo": 0, "Negativo": 0, "Neutral": 0}
    
    print("--- ANÁLISIS DE CADA COMENTARIO ---")
    for idx, comment in enumerate(comments_list, 1):
        # Se traduce al inglés para mayor precisión con TextBlob
        translated, ok = translate_to_english(comment)
        if not ok:
            print(f"   ⚠️  No se pudo traducir el comentario {idx} (falló Google y MyMemory). "
                  f"El resultado puede ser poco confiable.")

        blob = TextBlob(translated)
        polarity = blob.sentiment.polarity
        total_polarity += polarity

        # Clasificación
        if polarity > 0.1:
            sentiment = "Positivo :D"
            counts["Positivo"] += 1
        elif polarity < -0.1:
            sentiment = "Negativo :("
            counts["Negativo"] += 1
        else:
            sentiment = "Neutral"
            counts["Neutral"] += 1

        print(f"{idx}. Comentario: '{comment}'")
        print(f"   Sentimiento: {sentiment} | Polaridad: {polarity:.2f}\n")

    # Cálculos finales solicitados
    total_comments = len(comments_list)
    avg_polarity = total_polarity / total_comments if total_comments > 0 else 0
    prevalent_sentiment = max(counts, key=counts.get)

    print("="*40)
    print("--- RESUMEN GLOBAL ---")
    print(f"Total de comentarios: {total_comments}")
    print(f"Positivos: {counts['Positivo']}")
    print(f"Negativos: {counts['Negativo']}")
    print(f"Neutrales: {counts['Neutral']}")
    print(f"Promedio de sentimiento (Polaridad): {avg_polarity:.2f}")
    print(f"El sentimiento que MÁS PREVALECE es: {prevalent_sentiment}")
    print("="*40)

if __name__ == "__main__":
    # Puedes cambiar o agregar las opiniones de restaurante/tienda que quieras aquí:
    mis_comentarios = [
        "La comida estuvo excelente y la atención muy buena.",
        "El servicio fue pésimo y la comida llegó fría.",
        "El lugar es bonito pero los precios son normales.",
        "Me encantó el postre, una maravilla de lugar.",
        "Atención muy lenta y mala calidad."
    ]
    
    analyze_comments(mis_comentarios)