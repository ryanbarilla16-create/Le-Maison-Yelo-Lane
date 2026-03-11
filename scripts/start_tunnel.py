from pyngrok import ngrok
url = ngrok.connect(5000, bind_tls=True)
print(f"NGROK_URL={url.public_url}")
input("Press Enter to close ngrok tunnel...")
