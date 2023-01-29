const cancel_buttons = document.querySelectorAll(".cancel-customer");

// iterate over each cancel buttons 
cancel_buttons.forEach(button => {
    button.onclick = function() {
        const parent_div = this.parentNode; 
        const order_id = parseInt(parent_div.querySelector(".order_id").innerHTML);   
        const restaurant_id = parseInt(parent_div.querySelector("input[type=hidden]").value);
        
        // delete order 
        fetch(`/bringmyfood/restaurant/${restaurant_id}`, {
            method: 'PUT',
            body: JSON.stringify({
                order_id: order_id,  
                delete: true, 
                has_restaurant_deleted: false   
            }) 
        })
        .then(res => {
            if (res.ok) 
            { 
                console.log("HTTP request successful"); 
                parent_div.remove(); 
                if (!document.querySelectorAll(".order-div").length) 
                {
                    document.getElementById("no-orders").innerHTML = "There are no orders yet."; 
                } 
            }
            else 
            { 
                console.log("HTTP request unsuccessful"); 
            }
            return res
        })
        
    }
}) 

   