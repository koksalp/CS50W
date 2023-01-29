const addMoneyDiv= document.getElementById("add-money-div"); 
const [inputMoney, addMoneyButton] = addMoneyDiv.children; 
const showAddMoneyButton= document.getElementById("show-add-money-button"); 
const profileMessage = document.getElementById("profile-message"); 

// show and hide button    
showAddMoneyButton.onclick = () => { 
    addMoneyDiv.style.display = addMoneyDiv.style.display === "" ? "block" : ""; 
} 

// hide message after 3 seconds 
if (profileMessage) 
{ 
    setTimeout(() => { 
        profileMessage.innerHTML = "";  
    }, 3000); 
} 
