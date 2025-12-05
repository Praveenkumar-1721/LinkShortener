import os
from flask import Flask, request, render_template_string
import pyshorteners

app = Flask(__name__)

# --- UNNODA SAME DESIGN (No Changes in HTML/CSS) ---
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>InstaShort</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            background: linear-gradient(135deg, #5b55fa 0%, #a666f7 100%);
            font-family: 'Poppins', sans-serif;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
            padding: 20px;
        }

        .box {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            padding: 40px 30px;
            border-radius: 20px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
            width: 100%;
            max-width: 400px;
            text-align: center;
        }

        h2 {
            font-weight: 600;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        
        p.subtitle {
            font-size: 14px;
            opacity: 0.9;
            margin-bottom: 30px;
        }

        input[type="text"] {
            width: 100%;
            padding: 15px;
            border: 1px solid rgba(255,255,255,0.3);
            border-radius: 30px;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            font-size: 16px;
            outline: none;
            margin-bottom: 20px;
            text-align: center;
        }
        
        input::placeholder { color: rgba(255, 255, 255, 0.7); }

        button.generate-btn {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 30px;
            background: linear-gradient(90deg, #ff512f, #f09819);
            color: white;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
            box-shadow: 0 4px 15px rgba(240, 152, 25, 0.4);
        }

        button.generate-btn:hover { transform: scale(1.02); }

        .result-box {
            margin-top: 25px;
            background: rgba(0, 0, 0, 0.3);
            padding: 20px;
            border-radius: 15px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .short-link {
            color: #64ffda;
            font-weight: 600;
            word-break: break-all;
            text-decoration: none;
            font-size: 16px;
        }

        .action-buttons {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-top: 10px;
        }

        .action-btn {
            padding: 8px 15px;
            border: 1px solid rgba(255,255,255,0.3);
            border-radius: 8px;
            background: rgba(255,255,255,0.1);
            color: white;
            cursor: pointer;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 5px;
            transition: background 0.3s;
        }

        .action-btn:hover { background: rgba(255,255,255,0.3); }

        .footer {
            margin-top: 30px;
            font-size: 12px;
            opacity: 0.6;
        }
    </style>
</head>
<body>

    <div class="box">
        <h2><i class="fas fa-link"></i> InstaShort</h2>
        <p class="subtitle">Shorten your Large links.</p>
        
        <form method="POST">
            <input type="text" name="url" placeholder="Paste your long link here..." required autocomplete="off">
            <br>
            <button type="submit" class="generate-btn">
                <i class="fas fa-magic"></i> Shorten Now
            </button>
        </form>

        {% if short_url %}
        <div class="result-box">
            <span style="font-size: 12px; opacity: 0.8;">Your Short Link:</span>
            <a href="{{ short_url }}" target="_blank" class="short-link" id="myLink">{{ short_url }}</a>
            
            <div class="action-buttons">
                <button onclick="copyToClipboard()" class="action-btn">
                    <i class="fas fa-copy"></i> Copy
                </button>
                <button onclick="shareLink()" class="action-btn">
                    <i class="fas fa-share-alt"></i> Share
                </button>
            </div>
        </div>
        {% endif %}

        <div class="footer">
            Designed & Developed by <b>Praveenkumar</b>
        </div>
    </div>

    <script>
        function copyToClipboard() {
            var copyText = document.getElementById("myLink");
            navigator.clipboard.writeText(copyText.href);
            alert("Link Copied: " + copyText.href);
        }

        function shareLink() {
            var url = document.getElementById("myLink").href;
            if (navigator.share) {
                navigator.share({
                    title: 'InstaShort Link',
                    text: 'Check out this link:',
                    url: url
                }).catch(console.error);
            } else {
                alert("Share not supported on this browser. Use Copy instead!");
            }
        }
    </script>
</body>
</html>
"""

# --- LOGIC ---
@app.route('/', methods=['GET', 'POST'])
def home():
    short_url = ""
    if request.method == 'POST':
        long_url = request.form.get('url')
        try:
            s = pyshorteners.Shortener()
            # Try IS.GD first (Direct Link)
            short_url = s.isgd.short(long_url)
        except:
            # Fallback to TinyURL if is.gd fails
            try:
                s = pyshorteners.Shortener()
                short_url = s.tinyurl.short(long_url)
            except:
                short_url = "Error: Check URL or Try Later"
    return render_template_string(html_code, short_url=short_url)

if __name__ == '__main__':
    # MUKKIYAM: Render Dynamic Port Handling
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
