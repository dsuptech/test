def print_greetings():
    greetings = {
        "Korean": "안녕하세요",
        "English": "Hello",
        "Japanese": "こんにちは",
        "Chinese": "你好",
        "French": "Bonjour",
        "Spanish": "Hola",
        "German": "Hallo",
        "Russian": "Здравствуйте",
        "Italian": "Ciao",
        "Portuguese": "Olá"
    }

    print("Greetings in different languages:")
    print("-" * 30)
    for language, greeting in greetings.items():
        print(f"{language}: {greeting}")

if __name__ == "__main__":
    print_greetings()
