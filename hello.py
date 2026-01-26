def main():
    greetings = {
        "English": "Hello",
        "Korean": "안녕하세요",
        "Spanish": "Hola",
        "French": "Bonjour",
        "Japanese": "こんにちは",
        "Chinese": "你好",
        "German": "Hallo",
        "Russian": "Здравствуйте",
        "Italian": "Ciao",
        "Portuguese": "Olá"
    }

    print("=== Greetings in different languages ===")
    for language, greeting in greetings.items():
        print(f"{language}: {greeting}")

if __name__ == "__main__":
    main()
