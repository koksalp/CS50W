const links = document.querySelectorAll("#ul-links a"); 

const home = document.getElementById("index-container"); 
const manage= document.getElementById("owner-manage-container"); 
const myOrders = document.getElementById("order-text-div"); 
const profile = document.getElementById("profile-container"); 
const login = document.getElementById("login-container"); 
const register = document.getElementById("register-container"); 

// links are not active when a page is first displayed 
const removeActiveLink = () => {
    links.forEach(link => {
        if (link.classList.contains("active"))
        {
            link.classList.remove("active"); 
        }
    }); 
} 

// remove active link 
removeActiveLink(); 

// activate link based on which page the user in 
if (home) 
{
    document.getElementById("home").classList.add("active"); 
} 
else if (manage) 
{
    document.getElementById("manage").classList.add("active"); 
}
else if (myOrders) 
{
    document.getElementById("my-orders").classList.add("active"); 
}
else if (profile) 
{
    document.getElementById("profile").classList.add("active"); 
}
else if (login) 
{
    document.getElementById("login").classList.add("active"); 
}
else if (register) 
{
    document.getElementById("register").classList.add("active"); 
}