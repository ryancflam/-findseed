const t = new TimelineMax();
const img = document.querySelector(".banner-img");
t.fromTo(img, 2, {height: "0%"}, {height: "100%", ease: Power2.easeInOut});
document.addEventListener("contextmenu", event => event.preventDefault());

const audioURL = "static/assets/4am.mp3";
var AudioContext = window.AudioContext || window.webkitAudioContext;
const ctx = new AudioContext();


function unlockAudioContext() {
    if (ctx.state !== "suspended") {
        return;
    };
    const b = document.body;
    const events = ["touchstart", "touchend", "mousedown", "keydown"];
    events.forEach(e => b.addEventListener(e, unlock, false));

    function unlock() {
        ctx.resume().then(clean);
    }

    function clean() {
        events.forEach(e => b.removeEventListener(e, unlock));
    }
}


function playSound() {
    var sound = ctx.createBufferSource();
    sound.buffer = audio;
    sound.connect(ctx.destination);
    sound.start();
}


function main() {
    var date = new Date();
    var h = date.getHours();
    var m = date.getMinutes();
    var s = date.getSeconds();
    if (h === 4 && m === 0 && s === 0) {
        console.log("The time is 4 AM!");
        playSound();
    }
}


unlockAudioContext();
let audio;

fetch(audioURL)
    .then(res => res.arrayBuffer())
    .then(arrayBuffer => ctx.decodeAudioData(arrayBuffer))
    .then(decodedAudio => {
        audio = decodedAudio;
    });

const interval = 1000;
setInterval(main, interval);
