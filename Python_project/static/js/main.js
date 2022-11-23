const body=document.querySelector('body'),
    header=document.querySelector('header'),
    modeChange=document.querySelector('.dark-light'),
    result=document.querySelector(".disply_text"),
    soundBtn = document.querySelector(".sound"),
    copydBtn = document.querySelector(".copy");


modeChange.addEventListener("click",()=>
{
   modeChange.classList.toggle('active');
   body.classList.toggle('dark');
})
soundBtn.addEventListener("click",()=>{
    let uttrance= new SpeechSynthesisUtterance(`${result.innerText}`);
    speechSynthesis.speak(uttrance)
    });

 copydBtn.addEventListener("click",()=>{
   navigator.clipboard.writeText(result.innerText);
 });  
       
      