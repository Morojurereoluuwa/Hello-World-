import html
import random

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hello World Motion Lab", page_icon="✨", layout="wide")
st.title("✨ Hello World Motion Lab")
st.write("Enter a name, choose its style, and add animated effects.")

with st.sidebar:
    st.header("Controls")
    name = st.text_input("Enter your name or message", value="Hello World", max_chars=100)
    font_family = st.selectbox(
        "Font type",
        ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana",
         "Trebuchet MS", "Impact", "Comic Sans MS"],
    )
    font_size = st.slider("Font size (px)", 20, 100, 52, step=2)
    background = st.selectbox(
        "Background", ["Light", "Dark", "Ocean", "Sunset", "Forest", "Lavender"]
    )
    name_mode = st.selectbox("Name display mode", ["Centered", "Ticker Tape", "Repeated"])
    effect = st.selectbox(
        "Dynamic action",
        ["None", "Rain", "Snow", "Hail", "Wind Gust", "Confetti", "Tornado"],
    )
    speed = st.select_slider("Animation speed", options=["Slow", "Normal", "Fast"], value="Normal")

themes = {
    "Light": ("#ffffff", "#161616", "#d9e8f5"),
    "Dark": ("#10131f", "#ffffff", "#313956"),
    "Ocean": ("#dff6ff", "#10354a", "#9adff5"),
    "Sunset": ("#ffe0cf", "#54284f", "#ffb18e"),
    "Forest": ("#153d32", "#f3ffed", "#28634d"),
    "Lavender": ("#f0e7ff", "#34245c", "#d7c2ff"),
}
bg_color, text_color, accent_color = themes[background]
speed_multiplier = {"Slow": 1.6, "Normal": 1.0, "Fast": 0.6}[speed]
safe_name = html.escape(name.strip() or "Hello World")
safe_font = font_family.replace('"', "")

# Build particles once per Streamlit render. CSS animates them continuously in the browser.
rng = random.Random(42)
particles = []

if effect in ("Rain", "Snow", "Hail"):
    symbols = {"Rain": "💧", "Snow": "❄", "Hail": "🧊"}
    for _ in range(48 if effect == "Rain" else 34):
        left = rng.randint(0, 100)
        delay = rng.uniform(-8, 0)
        duration = rng.uniform(1.4, 3.0) * speed_multiplier
        size = rng.randint(10, 22)
        particles.append(
            f'<span class="particle" style="left:{left}%;animation-delay:{delay:.2f}s;'
            f'animation-duration:{duration:.2f}s;font-size:{size}px">{symbols[effect]}</span>'
        )
elif effect == "Confetti":
    colors = ["#ff477e", "#ffd166", "#06d6a0", "#4cc9f0", "#9b5de5", "#f77f00"]
    for _ in range(65):
        left = rng.randint(0, 100)
        delay = rng.uniform(-7, 0)
        duration = rng.uniform(2.0, 4.5) * speed_multiplier
        width, height = rng.randint(5, 10), rng.randint(8, 15)
        color = rng.choice(colors)
        particles.append(
            f'<span class="confetti" style="left:{left}%;animation-delay:{delay:.2f}s;'
            f'animation-duration:{duration:.2f}s;width:{width}px;height:{height}px;'
            f'background:{color}"></span>'
        )
elif effect == "Wind Gust":
    for _ in range(14):
        top = rng.randint(4, 96)
        delay = rng.uniform(-5, 0)
        duration = rng.uniform(1.6, 3.2) * speed_multiplier
        particles.append(
            f'<span class="wind-line" style="top:{top}%;animation-delay:{delay:.2f}s;'
            f'animation-duration:{duration:.2f}s"></span>'
        )
elif effect == "Tornado":
    for i in range(32):
        delay = rng.uniform(-4, 0)
        duration = rng.uniform(1.8, 3.4) * speed_multiplier
        symbol = "✦" if i % 3 == 0 else "•"
        particles.append(
            f'<span class="tornado-bit" style="--i:{i};animation-delay:{delay:.2f}s;'
            f'animation-duration:{duration:.2f}s">{symbol}</span>'
        )

effect_markup = "".join(particles)

if name_mode == "Ticker Tape":
    name_markup = (
        '<div class="ticker"><div class="ticker-track">'
        f"<span>{safe_name}</span><span>{safe_name}</span><span>{safe_name}</span>"
        "</div></div>"
    )
elif name_mode == "Repeated":
    name_markup = '<div class="repeated">' + "".join(
        f"<span>{safe_name}</span>" for _ in range(6)
    ) + "</div>"
else:
    name_markup = f'<div class="center-name">{safe_name}</div>'

scene_html = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; }}
.scene {{
  position: relative; width: 100%; height: 560px; overflow: hidden;
  border-radius: 18px; background: {bg_color}; color: {text_color};
  font-family: "{safe_font}", sans-serif;
  box-shadow: inset 0 0 0 1px {accent_color};
}}
.effects {{ position: absolute; inset: 0; overflow: hidden; pointer-events: none; }}
.name-layer {{
  position: absolute; inset: 0; z-index: 5; display: flex; align-items: center;
  justify-content: center; padding: 30px; overflow: hidden; overflow-wrap: anywhere;
  font-size: {font_size}px; line-height: 1.2; font-weight: 700;
  text-shadow: 0 2px 12px rgba(0,0,0,.10);
}}
.center-name {{ max-width: 100%; text-align: center; }}
.ticker {{ width: 100%; overflow: hidden; white-space: nowrap; }}
.ticker-track {{
  display: flex; width: max-content; gap: 1.2em;
  animation: ticker {18 * speed_multiplier:.2f}s linear infinite;
}}
.ticker-track span {{ flex: 0 0 auto; }}
.repeated {{
  display: grid; width: 100%; grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px; text-align: center;
}}
.particle {{ position: absolute; top: -35px; opacity: .9; animation: fall linear infinite; }}
@keyframes fall {{
  from {{ transform: translateY(-40px) rotate(0deg); }}
  to {{ transform: translateY(650px) rotate(360deg); }}
}}
.confetti {{
  position: absolute; top: -25px; border-radius: 2px;
  animation: confetti-fall linear infinite;
}}
@keyframes confetti-fall {{
  from {{ transform: translateY(-30px) rotate(0deg); }}
  to {{ transform: translateY(630px) rotate(900deg); }}
}}
.wind-line {{
  position: absolute; left: -35%; width: 30%; height: 3px; border-radius: 99px;
  opacity: .7; background: linear-gradient(90deg, transparent, {accent_color}, transparent);
  animation: gust ease-in-out infinite;
}}
.wind-line:nth-child(3n) {{ height: 5px; }}
@keyframes gust {{
  0% {{ transform: translateX(0) skewX(-20deg); opacity: 0; }}
  20% {{ opacity: .8; }}
  100% {{ transform: translateX(500%) skewX(-20deg); opacity: 0; }}
}}
.tornado-bit {{
  position: absolute; left: 50%; top: 50%; color: {accent_color}; font-size: 22px;
  opacity: .8; animation: swirl ease-in-out infinite; transform-origin: 0 0;
}}
@keyframes swirl {{
  0% {{ transform: rotate(0deg) translateX(calc(18px + var(--i) * 2px)) scale(.7); opacity: .2; }}
  50% {{ opacity: .9; }}
  100% {{ transform: rotate(360deg) translateX(calc(18px + var(--i) * 2px)) scale(1); opacity: .2; }}
}}
.scene-footer {{
  position: absolute; right: 14px; bottom: 10px; z-index: 8;
  font: 11px/1.3 Arial, sans-serif; opacity: .55;
}}
@keyframes ticker {{
  from {{ transform: translateX(0); }}
  to {{ transform: translateX(-33.333%); }}
}}
@media (prefers-reduced-motion: reduce) {{
  .particle, .confetti, .wind-line, .tornado-bit, .ticker-track {{
    animation-duration: 30s !important;
  }}
}}
</style>
</head>
<body>
<div class="scene">
  <div class="effects">{effect_markup}</div>
  <div class="name-layer">{name_markup}</div>
  <div class="scene-footer">HELLO WORLD MOTION LAB</div>
</div>
</body>
</html>
"""

components.html(scene_html, height=580, scrolling=False)
st.caption(
    "Learning note: Streamlit handles the controls; Python prepares the display; "
    "HTML and CSS draw the scene and animate its effects."
)
