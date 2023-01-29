const create_button = document.getElementById("create_restaurant"); 
const form1 = document.getElementById("manage-form-1"); 
const res_button = document.getElementById("show_restaurants"); 
const res_div = document.getElementById("owner-all-restaurants-div");
const contents = [form1, res_div]; 

// hide and show buttons 
[create_button, res_button].forEach((button, index) => { 
    const content = contents[index]; 
    
    button.onclick = () => { 
        let status = button.value;      

        if (status === "hidden") 
        {
            content.style.display = "block"; 
            button.value = "shown"; 

            if (index === 0)
            {
                button.innerHTML = "Hide the form"; 
            } 
            else 
            {
                button.innerHTML = "Hide restaurants"; 
            }
        } 
        else 
        {
            content.style.display = "none"; 
            button.value = "hidden"; 
            
            if (index === 0)
            {
                button.innerHTML = "Open a restaurant";   
            } 
            else 
            {
                button.innerHTML = "Show my restaurants"; 
            }
        } 
    }
    
});   