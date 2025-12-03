from flask import Flask, request, render_template_string
import pyshorteners

app = Flask(__name__)

# --- டிசைன் (HTML) ---
html_code = """
<!DOCTYPE html>
<html>
<head>
    <title>Shortener</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background-color: #f0f2f5; font-family: sans-serif; text-align: center; padding: 20px; }
        .box { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        input { width: 90%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; }
        .result { margin-top: 20px; word-break: break-all; color: green; font-weight: bold;}
    </style>
</head>
<body>
    <div class="box">
        <h2>🔗 Link Shortener</h2>
        <form method="POST">
            <input type="text" name="url" placeholder="Paste link here..." required>
            <br>
            <button type="submit">Shorten</button>
        </form>
        {% if short_url %}
        <div class="result">
            SUCCESS! Copy below:<br>
            <a href="{{ short_url }}">{{ short_url }}</a>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

# --- லாஜிக் (Python) ---
@app.route('/', methods=['GET', 'POST'])
def home():
    short_url = ""
    if request.method == 'POST':
        long_url = request.form.get('url')
        try:
            s = pyshorteners.Shortener()
            short_url = s.tinyurl.short(long_url)
        except:
            short_url = "Error!"
    return render_template_string(html_code, short_url=short_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
