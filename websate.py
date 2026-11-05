from flask import Flask, render_template_string, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">

<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>For Zara ❤️</title>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    min-height: 100vh;
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #ffe0ec, #f8c8dc, #fff0f5);
    color: #783c54;
    text-align: center;
    overflow-x: hidden;
}

/* FLOATING ANIMATION */

#floatingLayer {
    position: fixed;
    inset: 0;
    overflow: hidden;
    pointer-events: none;
    z-index: 0;
}

.floating-item {
    position: absolute;
    bottom: -70px;
    white-space: nowrap;
    font-weight: bold;
    color: #d65d91;
    text-shadow: 0 2px 8px rgba(255,255,255,0.8);
    animation: floatUp linear forwards;
    opacity: 0;
}

@keyframes floatUp {

    0% {
        transform: translateY(0) rotate(-5deg);
        opacity: 0;
    }

    10% {
        opacity: 0.85;
    }

    85% {
        opacity: 0.8;
    }

    100% {
        transform: translateY(-115vh) rotate(8deg);
        opacity: 0;
    }
}

/* SCREENS */

.screen {
    display: none;
    position: relative;
    z-index: 1;
    min-height: 100vh;
    padding: 25px 15px;
    align-items: center;
    justify-content: center;
    flex-direction: column;
}

.screen.active {
    display: flex;
}

/* CARDS */

.card {
    width: 100%;
    max-width: 540px;
    padding: 28px 20px;
    background: rgba(255,255,255,0.88);
    backdrop-filter: blur(8px);
    border-radius: 25px;
    box-shadow: 0 12px 40px rgba(180,80,120,0.2);
}

h1 {
    font-size: clamp(25px, 6vw, 36px);
}

p {
    font-size: 18px;
    line-height: 1.6;
}

.welcome {
    color: #d65d91;
    font-size: 17px;
    font-weight: bold;
    letter-spacing: 2px;
}

button {
    border: none;
    padding: 13px 20px;
    margin: 7px;
    border-radius: 18px;
    background: #f28db5;
    color: white;
    font-size: 16px;
    cursor: pointer;
    transition: 0.2s;
}

button:hover {
    background: #e875a4;
    transform: scale(1.04);
}

button:disabled {
    background: #c9b8c0;
    cursor: not-allowed;
    opacity: 0.7;
    transform: none;
}

.secondary {
    background: #c9a0b2;
}

.emoji {
    font-size: 70px;
    margin: 10px;
}

.options {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
}

.option {
    min-width: 125px;
}

.option.selected {
    background: #b94d7c;
    outline: 3px solid #f5b5cf;
}

textarea {
    width: 100%;
    min-height: 110px;
    padding: 14px;
    border: 2px solid #f5b5cf;
    border-radius: 15px;
    font: inherit;
    resize: vertical;
}

.small {
    font-size: 13px;
}

.spotify-box {
    margin-top: 18px;
    width: 100%;
}

.spotify-box iframe {
    width: 100%;
    height: 152px;
    border: none;
    border-radius: 12px;
}

#restaurantOptions {
    display: none;
    margin-top: 15px;
}

#restaurantOptions.visible {
    display: block;
}

/* ENVELOPE */

.envelope {
    width: 230px;
    height: 150px;
    margin: 30px auto;
    background: #e98eae;
    border-radius: 8px;
    cursor: pointer;
    position: relative;
    box-shadow: 0 8px 20px #d99bb5;
    transition: transform 0.3s;
}

.envelope:hover {
    transform: scale(1.05);
}

.envelope::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    border-left: 115px solid transparent;
    border-right: 115px solid transparent;
    border-top: 90px solid #f5b7ce;
}

.envelope::after {
    content: "❤️";
    position: absolute;
    font-size: 36px;
    top: 63px;
    left: 97px;
}

.letter {
    display: none;
    max-width: 480px;
    margin: 20px auto;
    padding: 25px;
    background: #fffaf0;
    color: #75475a;
    border-radius: 12px;
    text-align: left;
    line-height: 1.8;
    white-space: pre-line;
}

.letter.open {
    display: block;
    animation: letterAppear 0.8s ease;
}

@keyframes letterAppear {
    from {
        opacity: 0;
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.end-message {
    font-size: 17px;
    color: #c34e80;
    font-weight: bold;
    margin-top: 25px;
}

</style>
</head>

<body>

<div id="floatingLayer"></div>


<!-- SCREEN 1 -->

<section class="screen active" id="screen1">

<div class="card">

<div class="welcome">FOR ZARA, WITH LOVE</div>

<div class="emoji">❤️</div>

<h1>Zara, do u love me?</h1>

<p>Just think carefully...</p>

<button onclick="showScreen('screen2')">
Yes ❤️
</button>

<button onclick="showScreen('screen2')">
YES OF COURSE!!!! ❤️‍🔥
</button>

</div>

</section>


<!-- SCREEN 2 -->

<section class="screen" id="screen2">

<div class="card">

<div class="emoji">😺🥺</div>

<h1>You sure?</h1>

<p>Come on, answer again!</p>

<button class="secondary"
onclick="showScreen('screen1')">
Try again!
</button>

<br>

<button id="runaway">
Yes
</button>

<button onclick="showScreen('screen3')">
YES OF COURSE!! 💕
</button>

</div>

</section>


<!-- SCREEN 3: MUSIC -->

<section class="screen" id="screen3">

<div class="card">

<div class="emoji">🎧</div>

<h1>What song will we listen to?</h1>

<p>Choose what is closer to your soul.</p>

<div class="options">

<button class="option song-option"
onclick="chooseSong('star', this)">
Lil Peep - Star Shopping
</button>

<button class="option song-option"
onclick="chooseSong('hunt', this)">
Lil Peep - Hunt U
</button>

<button class="option song-option"
onclick="chooseSong('true', this)">
XXXTentacion - True Love
</button>

<button class="option song-option"
onclick="chooseSong('villain', this)">
Madk1d - VILLIAN / 8 миля
</button>

</div>

<div id="spotifyPlayer" class="spotify-box">
<p class="small">Choose a song ❤️</p>
</div>

<p class="small">
If Spotify blocks autoplay, press Play in the player.
</p>

<button id="songContinue"
onclick="continueFromSong()"
disabled>
Continue ❤️‍🔥
</button>

</div>

</section>


<!-- SCREEN 5: QUESTION -->

<section class="screen" id="screen5">

<div class="card">

<div class="emoji">💌</div>

<h1>What do you like most about me?</h1>

<p>I really want to know it.</p>

<textarea
id="answer"
placeholder="Text me here...">
</textarea>

<p class="small">
Your answer will be sent to Edward and stored on his server.
</p>

<button id="answerButton" onclick="saveAnswer()">
Answer 💝
</button>

</div>

</section>


<!-- SCREEN 6 -->

<section class="screen" id="screen6">

<div class="card">

<div class="emoji">🐣💓🐣</div>

<h1>And I want you to know...</h1>

<p>
I love you. And I'm happy that you exist in this world.
</p>

<p>
You make my world a better place.
</p>

<button onclick="showScreen('screen7')">
Let's choose a date 🌹
</button>

</div>

</section>


<!-- SCREEN 7: DATE -->

<section class="screen" id="screen7">

<div class="card">

<div class="emoji">🌹</div>

<h1>Where shall we go together?</h1>

<p>Choose one option ❤️</p>

<div class="options">

<button class="option date-option"
onclick="dateChoose('tea', this)">
Drink tea 🫖
</button>

<button class="option date-option"
onclick="dateChoose('pasta', this)">
Eat pasta 🍝
</button>

<button class="option date-option"
onclick="dateChoose('restaurant', this)">
Restaurant 🕯️
</button>

<button class="option date-option"
onclick="dateChoose('walk', this)">
Go for a walk 🌦️
</button>

<button class="option date-option"
onclick="dateChoose('cinema', this)">
Cinema 🎥
</button>

</div>

<div id="dateResponse"></div>

<div id="restaurantOptions">

<p>Which cuisine will we choose?</p>

<button class="option cuisine-option"
onclick="chooseCuisine('Japanese', this)">
Japanese 🏯
</button>

<button class="option cuisine-option"
onclick="chooseCuisine('French', this)">
French 🗼
</button>

<button class="option cuisine-option"
onclick="chooseCuisine('Italian', this)">
Italian 🍝
</button>

</div>

<div id="walkMusic" class="spotify-box"></div>

<br>

<button id="dateContinue"
onclick="continueFromDate()"
disabled>
The last surprise 💌
</button>

<p class="small" id="dateHint">
Choose where we will go first.
</p>

</div>

</section>


<!-- SCREEN 8: LETTER -->

<section class="screen" id="screen8">

<div class="card">

<h1>For you, my dear Zara 💌</h1>

<p>Click the envelope.</p>

<div class="envelope" onclick="openLetter()"></div>

<div class="letter" id="loveLetter">

<h2>For my dear Zara 💓</h2>

Hello, darling.

I created this website to make you happy and to tell you how much I love you.

Yes, yes, I love you so much. You are a miracle, and I'm so grateful to have you in my life.

I wish I could see you every single day.

I hope these daily 20-minute meetings of ours will soon come to an end, and we'll be able to spend much more time together.

But no matter what, I'm happy even with just five minutes with you.

You are my happiness, the light that brightens my soul.

I love you so, so much.

<h3>Your Edward 🖤</h3>

</div>

<p class="end-message">
This is not the end. I want a lifetime of memories with you. ❤️
</p>

</div>

</section>


<script>


// SCREEN NAVIGATION

function showScreen(id) {

    document.querySelectorAll(".screen").forEach(function(screen) {
        screen.classList.remove("active");
    });

    const target = document.getElementById(id);

    if (target) {
        target.classList.add("active");
    }

    window.scrollTo(0, 0);
}



// FLOATING WORDS AND HEARTS

const floatingMessages = [

    "I LOVE YOU ❤️",

    "You're too cute 💗",

    "You're the most beautiful girl on the planet",

    "Let's be together forever 💞",

    "My favorite person ❤️",

    "I choose you. Always.",

    "You make my world better 💓",

    "I wish I could see you every day",

    "You're my little happiness",

    "My favorite girl in the universe",

    "Every day with you is special",

    "I love your smile ❤️",

    "You're my sunshine",

    "Forever yours 💗",

    "You are my happiness"

];


function createFloatingItem() {

    const layer = document.getElementById("floatingLayer");

    const item = document.createElement("div");

    item.className = "floating-item";

    const isHeart = Math.random() < 0.3;

    if (isHeart) {

        item.textContent = ["❤️", "💗", "💞", "💓", "💕"][
            Math.floor(Math.random() * 5)
        ];

    } else {

        item.textContent = floatingMessages[
            Math.floor(Math.random() * floatingMessages.length)
        ];

    }

    item.style.left = Math.random() * 80 + 5 + "vw";

    item.style.fontSize =
        (isHeart ? 20 + Math.random() * 20 : 13 + Math.random() * 7) + "px";

    const duration = 8 + Math.random() * 6;

    item.style.animationDuration = duration + "s";

    layer.appendChild(item);

    setTimeout(function() {
        item.remove();
    }, duration * 1000);

}


setInterval(createFloatingItem, 900);



// HEART BURST

function heartBurst() {

    const layer = document.getElementById("floatingLayer");

    for (let i = 0; i < 25; i++) {

        const heart = document.createElement("div");

        heart.className = "floating-item";

        heart.textContent = ["❤️", "💗", "💞", "💓"][
            Math.floor(Math.random() * 4)
        ];

        heart.style.left = Math.random() * 90 + "vw";

        heart.style.bottom = "30%";

        heart.style.fontSize = (20 + Math.random() * 25) + "px";

        const duration = 3 + Math.random() * 3;

        heart.style.animationDuration = duration + "s";

        layer.appendChild(heart);

        setTimeout(function() {
            heart.remove();
        }, duration * 1000);

    }

}



// RUNAWAY BUTTON

const runawayButton = document.getElementById("runaway");

function moveButton() {

    const x = Math.random() * 180 - 90;

    const y = Math.random() * 100 - 50;

    runawayButton.style.transform =
        "translate(" + x + "px, " + y + "px)";

}

runawayButton.addEventListener("mouseover", moveButton);

runawayButton.addEventListener("touchstart", function(event) {

    event.preventDefault();

    moveButton();

});



// SONGS

const songs = {

    star: "https://open.spotify.com/track/5ePUUBW4kMKWoP3RItbiQB",

    hunt: "https://open.spotify.com/track/1PpXKypkmVKJJvendn19Vf",

    true: "https://open.spotify.com/track/1lXHSDFD4ljZLyLB58hpvd",

    villain: "https://open.spotify.com/track/67llqAFIyR6d6JMjDImDyU",

    falling: "https://open.spotify.com/track/0XkifPsgC2kymXSJvhGrtk"

};


let selectedSong = null;


function spotifyUrl(link) {

    const match = link.match(
        /open\.spotify\.com\/(track|album|playlist)\/([a-zA-Z0-9]+)/
    );

    if (!match) {
        return null;
    }

    return "https://open.spotify.com/embed/" +
        match[1] + "/" + match[2] +
        "?utm_source=generator&autoplay=1";

}


function showSpotify(link, containerId) {

    const container = document.getElementById(containerId);

    const url = link ? spotifyUrl(link) : null;

    if (!url) {

        container.innerHTML =
            "<p class='small'>Spotify link not found.</p>";

        return;

    }

    container.innerHTML = "";

    const iframe = document.createElement("iframe");

    iframe.src = url;

    iframe.allow =
        "autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture";

    iframe.loading = "eager";

    iframe.title = "Spotify music player";

    container.appendChild(iframe);

}


function chooseSong(key, button) {

    selectedSong = key;

    document.querySelectorAll(".song-option").forEach(function(item) {

        item.classList.remove("selected");

    });

    button.classList.add("selected");

    showSpotify(songs[key], "spotifyPlayer");

    document.getElementById("songContinue").disabled = false;

}


function continueFromSong() {

    if (!selectedSong) {

        alert("Please choose a song first ❤️");

        return;

    }

    showScreen("screen5");

}



// SAVE ANSWER

async function saveAnswer() {

    const answer = document.getElementById("answer").value.trim();

    const button = document.getElementById("answerButton");

    if (!answer) {

        alert("Write at least a couple of words ❤️");

        return;

    }

    button.disabled = true;

    button.textContent = "Sending...";

    try {

        const response = await fetch("/save-answer", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                answer: answer
            })

        });

        if (!response.ok) {

            throw new Error("Server error");

        }

        localStorage.setItem("zaraAnswer", answer);

        alert("Your answer has been sent ❤️");

        showScreen("screen6");

    } catch (error) {

        alert("Something went wrong. Please try again.");

        console.error(error);

    } finally {

        button.disabled = false;

        button.textContent = "Answer 💝";

    }

}



// DATE SELECTION

let selectedDate = null;

let selectedCuisine = null;


function dateChoose(choice, button) {

    selectedDate = choice;

    selectedCuisine = null;

    document.querySelectorAll(".date-option").forEach(function(item) {

        item.classList.remove("selected");

    });

    button.classList.add("selected");

    const response = document.getElementById("dateResponse");

    const restaurant = document.getElementById("restaurantOptions");

    const walkMusic = document.getElementById("walkMusic");

    const continueButton = document.getElementById("dateContinue");

    const hint = document.getElementById("dateHint");

    restaurant.classList.remove("visible");

    walkMusic.innerHTML = "";

    document.querySelectorAll(".cuisine-option").forEach(function(item) {

        item.classList.remove("selected");

    });

    continueButton.disabled = false;

    hint.textContent = "You can continue ❤️";

    if (choice === "tea") {

        response.innerHTML = "<h2>Oh, you want puer? 🫖</h2>";

    }

    else if (choice === "pasta") {

        response.innerHTML = "<h2>Mmmm, did you dream about it? 🍝</h2>";

    }

    else if (choice === "restaurant") {

        response.innerHTML = "<h2>Choose a cuisine 💓</h2>";

        restaurant.classList.add("visible");

        continueButton.disabled = true;

        hint.textContent = "Choose a cuisine before continuing.";

    }

    else if (choice === "walk") {

        response.innerHTML =
            "<h2>Let's go for a walk in the rain? 🌦️🖤</h2>";

        showSpotify(songs.falling, "walkMusic");

    }

    else if (choice === "cinema") {

        response.innerHTML = "<h2>Let's go watch Twilight 🌙</h2>";

    }

}



// CUISINE SELECTION

function chooseCuisine(cuisine, button) {

    selectedCuisine = cuisine;

    document.querySelectorAll(".cuisine-option").forEach(function(item) {

        item.classList.remove("selected");

    });

    button.classList.add("selected");

    document.getElementById("dateResponse").innerHTML =

        "<h2>Ohhh, I understand your wishes! " +
        "I'll prepare a dish for you from " +
        cuisine + " cuisine ❤️</h2>";

    document.getElementById("dateContinue").disabled = false;

    document.getElementById("dateHint").textContent =
        "Perfect! Let's continue ❤️";

}



// CHECK DATE

function continueFromDate() {

    if (!selectedDate) {

        alert("Please choose where we will go ❤️");

        return;

    }

    if (selectedDate === "restaurant" && !selectedCuisine) {

        alert("Please choose a cuisine first ❤️");

        return;

    }

    showScreen("screen8");

}



// OPEN LETTER

function openLetter() {

    const letter = document.getElementById("loveLetter");

    letter.classList.toggle("open");

    if (letter.classList.contains("open")) {

        heartBurst();

    }

}

</script>

</body>
</html>
"""


@app.route("/")
def home():

    return render_template_string(HTML)


@app.route("/save-answer", methods=["POST"])
def save_answer():

    data = request.get_json(silent=True)

    if not data or not isinstance(data.get("answer"), str):

        return jsonify({"success": False}), 400

    answer = data["answer"].strip()

    if not answer or len(answer) > 2000:

        return jsonify({"success": False}), 400

    entry = {

        "answer": answer,

        "date": datetime.now().isoformat()

    }

    with open("answers.jsonl", "a", encoding="utf-8") as file:

        file.write(json.dumps(entry, ensure_ascii=False) + "\n")

    return jsonify({"success": True})


if __name__ == "__main__":

    app.run(debug=True)