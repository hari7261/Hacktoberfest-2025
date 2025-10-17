
const generateBtn = document.getElementById("generate-btn");
const numberElement = document.getElementById("random-number");

generateBtn.addEventListener("click",()=>{

    const randomNumber = Math.floor(Math.random() * 100) + 1;

    numberElement.textContent = randomNumber;
});