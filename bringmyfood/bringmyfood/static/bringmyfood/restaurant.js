const buyDivs = document.querySelectorAll(".buy"); 
const submit = document.getElementById("buy-submit"); 
const orderFeedback = document.getElementById("order-feedback"); 

// allow users to change amount of products 
buyDivs.forEach(div => {
    const [product_element, decrease_button, quantity, increase_button] = div.children; 
    const product_id = product_element.value;                             
    decrease_button.onclick = () => {  
        console.log(product_id);        
        quantity.value = parseInt(quantity.value) > 0 ? parseInt(quantity.value) - 1 : 0; 
    }
        
    increase_button.onclick = () => {  
        console.log(product_id);        
        quantity.value = parseInt(quantity.value) + 1; 
    }
        
});

// customer attempts to create a new order 
if (submit)
{
    submit.onclick = () => {
        const order = {}; 
        
        buyDivs.forEach(div => {
            const [product_element, decrease_button, quantity, increase_button] = div.children; 
            const product_id = product_element.value;  
            order[product_id] = parseInt(quantity.value); 
        });
        
        let count = 0; 
    
        for (const id in order) 
        {
            if (order[id] === 0)
            {
                count++; 
            }
        }
    
        // customer does not add any products 
        if (count === Object.keys(order).length) 
        {
            handleBuy("You have not added any product yet."); 
            
        } 

        // send POST request to API route 'order' so that a new order can be created 
        else 
        { 
            fetch('/bringmyfood/order', {
                method: 'POST',
                body: JSON.stringify(order)
            })
            .then(response => response.json())
            .then(result => {
                console.log(result); 
                if (result.status)
                {
                    console.log("order successful");
                    handleBuy(`Order Successful </br> Total Amount: $${result.order_total.toFixed(2)}`); 
                    document.getElementById("balance").innerHTML = result.balance.toFixed(2); 
                    resetAmount(); 
                }
                else 
                { 
                    // error occured 
                    if (result.error !== undefined) 
                    {
                        handleBuy("An error occured, order failed."); 
                        
                    } 
                    
                    // customer can not afford the price 
                    else 
                    { 
                        console.log("order failed"); 
                        handleBuy("You cannot order. Insufficient balance"); 
                    }
                } 
            });
        }
    }
}

const add_product_button = document.getElementById("add_product_button"); 
const show_orders_button = document.getElementById("show_orders_button"); 

// show and hide buttons 
if (add_product_button && show_orders_button)
{
    [add_product_button, show_orders_button].forEach((button, index) => {
        const div_id = index === 0 ? "add-product" : "show-orders";     
        const other_div_id = index === 1 ? "add-product" : "show-orders";     
        const div = document.getElementById(div_id); 
        button.onclick = () => {
            if (!(div.style.display)) 
            {
                div.style.display = "block"; 
                document.getElementById(other_div_id).style.display = ""; 
            }
            else 
            {
                div.style.display = ""; 
            }
        }
    });
} 

const ready_buttons = document.querySelectorAll(".ready");
const delete_buttons = document.querySelectorAll(".delete"); 

// order is ready 
ready_buttons.forEach(button => { 
    button.onclick = function() { 
        const parent_div = this.parentNode.parentNode; 
        const order_id = parseInt(parent_div.querySelector(".order_id").innerHTML);  
        const restaurant_id = parseInt(parent_div.querySelector("input[type=hidden]").value); 
        const order_status_element = parent_div.querySelector(".order_status"); 
        const order_status = order_status_element.innerHTML === "Active" ? true : false ;  
        console.log(`order_status: ${order_status}`); 
        if (order_status)
        {
            fetch(`/bringmyfood/restaurant/${restaurant_id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    order_id: order_id,  
                    delete: false,
                    has_restaurant_deleted: false  
                })
            }) 
            .then(res => {
                if (res.ok) 
                { 
                    console.log("HTTP request successful"); 
                    order_status_element.innerHTML = "Not Active";  
                }
                else 
                { 
                    console.log("HTTP request unsuccessful"); 
                    document.getElementById("cannot-order").innerHTML = `An error happened. Order with an id of ${order_id} is still active`;
                }
                return res
            })
        }
    }
});  

// order is attempted to be deleted by restaurant 
// must be clicked on ready button first 
delete_buttons.forEach(button => {
    button.onclick = function() {
        const parent_div = this.parentNode.parentNode; 
        const order_id = parseInt(parent_div.querySelector(".order_id").innerHTML);   
        const restaurant_id = parseInt(parent_div.querySelector("input[type=hidden]").value); 
        const order_status = parent_div.querySelector(".order_status").innerHTML === "Active" ? true : false ;
        console.log(order_status); 
        if (order_status)
        {
            alert("This order is still active, you cannot delete it now."); 
        }
        else 
        { 
            fetch(`/bringmyfood/restaurant/${restaurant_id}`, {
                method: 'PUT',
                body: JSON.stringify({ 
                    order_id: order_id,  
                    delete: false,
                    has_restaurant_deleted: true  
                })
            })
            .then(res => {
                if (res.ok) 
                { 
                    console.log("HTTP request successful"); 
                    parent_div.remove();  
                }
                else 
                { 
                    console.log("HTTP request unsuccessful"); 
                    document.getElementById("cannot-order").innerHTML = `An error happened. Order with an id of ${order_id} is still active`;
                }
                return res
            })
        }
    }
});

// function to make amounts 0 after creating an order 
function resetAmount() 
{
    buyDivs.forEach(div => {
        div.querySelector("input[type='number']").value = 0; 
    }); 
} 

// function to handle buy operation 
function handleBuy(message) 
{ 
    orderFeedback.innerHTML = message; 
    orderFeedback.classList.add("feedback"); 
    window.scrollTo(0, 0); 
    setTimeout(() => {
        orderFeedback.innerHTML = ""; 
        orderFeedback.classList.remove("feedback"); 
    }, 5000); 
} 