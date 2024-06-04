const signText = document.querySelector('.player-view')
const normText = document.querySelector('#player-text')

const fromText = document.querySelector(".from-text"),
toText = document.querySelector(".to-text"),
exchageIcon = document.querySelector(".exchange"),
selectTag = document.querySelectorAll("select"),
icons = document.querySelectorAll(".row i");
translateBtn = document.querySelector("button")

// selectTag.forEach((tag, id) => {
//     for (let country_code in countries) {
//         let selected = id == 0 ? country_code == "ur-PK" ? "selected" : "" : country_code == "en-GB" ? "selected" : "";
//         let option = `<option ${selected} value="${country_code}">${countries[country_code]}</option>`;
//         tag.insertAdjacentHTML("beforeend", option);
//     }
// });

// exchageIcon.addEventListener("click", () => {
//     let tempText = fromText.value,
//     tempLang = selectTag[0].value;
//     fromText.value = toText.value;
//     toText.value = tempText;
//     selectTag[0].value = selectTag[1].value;
//     selectTag[1].value = tempLang;
// });

// fromText.addEventListener("keyup", () => {
//     if(!fromText.value) {
//         toText.value = "";
//     }
// });

// translateBtn.addEventListener("click", () => {
//     let text = fromText.value.trim(),
//     translateFrom = selectTag[0].value,
//     translateTo = selectTag[1].value;
//     if(!text) return;
//     toText.setAttribute("placeholder", "Translating...");
//     let apiUrl = `https://api.mymemory.translated.net/get?q=${text}&langpair=${translateFrom}|${translateTo}`;
//     fetch(apiUrl).then(res => res.json()).then(data => {
//         toText.value = data.responseData.translatedText;
//         data.matches.forEach(data => {
//             if(data.id === 0) {
//                 toText.value = data.translation;
//             }
//         });
//         toText.setAttribute("placeholder", "Translation");
//     });
// });

// icons.forEach(icon => {
//     icon.addEventListener("click", ({target}) => {
//         if(!fromText.value || !toText.value) return;
//         if(target.classList.contains("fa-copy")) {
//             if(target.id == "from") {
//                 navigator.clipboard.writeText(fromText.value);
//             } else {
//                 navigator.clipboard.writeText(toText.value);
//             }
//         } else {
//             let utterance;
//             if(target.id == "from") {
//                 utterance = new SpeechSynthesisUtterance(fromText.value);
//                 utterance.lang = selectTag[0].value;
//             } else {
//                 utterance = new SpeechSynthesisUtterance(toText.value);
//                 utterance.lang = selectTag[1].value;
//             }
//             speechSynthesis.speak(utterance);
//         }
//     });
// });

const textArea = document.querySelector('#textplayer')

const msgInput = document.querySelector('.to-text')
const sendBtn = document.querySelector('#send-btn')



let newText = "";
sendBtn.addEventListener('click', function() {
    // textArea.value = ''
    textArea.innerHTML = ''
    let text = msgInput.value;
    msgInput.value = ''


    for (let i = 0; i < text.length; i++) {
        setTimeout(function() {
            signText.innerHTML = text[i]
            normText.innerHTML = text[i]


            const letter = text.charAt(i);
            const isLastLetter = (i === text.length - 1);

            if (isLastLetter) {
                // newText += `<p style="background-color:red;">${letter}</p>`;
                newText += letter


            } else {
                newText += letter;
            }

            textArea.innerHTML = newText;
            // await new Promise(r => setTimeout(r, 1000));

            // if (isLastLetter) {
            //     const lastLetterElement = textArea.lastChild.lastChild;
            //     lastLetterElement.classList.add("highlight");
            // }



            // const letter = text.charAt(i);
            // const isLastLetter = (i === text.length - 1);

            // if (isLastLetter) {
            //     newText += `<span class="highlight">${letter}</span>`;
            // } else {
            //     newText += letter;
            // }

            // textArea.value = newText;



            // const lastLetter = text.slice(-1);
            // const lastIndex = text.lastIndexOf(lastLetter);
            // const newText = text.slice(0, lastIndex) + `<span class="highlight">${text[i]}</span>` + text.slice(lastIndex + 1);

            // textArea.innerHTML = newText;

            console.log(i)
        }, i * 1000)
    }
})