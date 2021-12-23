const buttons = document.querySelectorAll('button');
let displayValue = '';
// regex for arthmetic operations
let exp = /(\d+(?:\.\d+)?) ?\^ ?(\d+(?:\.\d+)?)/
let mul = /(\d+(?:\.\d+)?) ?\* ?(\d+(?:\.\d+)?)/
let div = /(\d+(?:\.\d+)?) ?\/ ?(\d+(?:\.\d+)?)/
let add = /(\d+(?:\.\d+)?) ?\+ ?(\d+(?:\.\d+)?)/
let sub = /(\d+(?:\.\d+)?) ?- ?(\d+(?:\.\d+)?)/

function evaluate(expr)
{
	if(isNaN(Number(expr)))
	{
	    if(exp.test(expr))
	    {
	        let newExpr = expr.replace(exp, function(match, base, pow) {
	            return Math.pow(Number(base), Number(pow));
	        });
	        return evaluate(newExpr);
	    }
	    else if(mul.test(expr))
	    {
	        let newExpr = expr.replace(mul, function(match, a, b) {
	            return Number(a) * Number(b);
	        });
	        return evaluate(newExpr);
	    }
	    else if(div.test(expr))
	    {
	        let newExpr = expr.replace(div, function(match, a, b) {
	            if(b != 0)
	                return Number(a) / Number(b);
	            else
	                throw new Error('Division by zero');
	        });
	        return evaluate(newExpr);
	    }
	    else if(add.test(expr))
	    {
	        let newExpr = expr.replace(add, function(match, a, b) {
	            return Number(a) + Number(b);
	        });
	        return evaluate(newExpr);
	    }
	    else if(sub.test(expr))
	    {
	        let newExpr = expr.replace(sub, function(match, a, b) {
	            return Number(a) - Number(b);
	        });
	        return evaluate(newExpr);
	    }
	    else
	    {
	        return expr;
	    }
	}
	return Number(expr);
}

function updateDisplay(button){
	const display = document.getElementById('display');
	displayValue +=button.value;
    display.innerText = displayValue;
}

function changeDisplayValue(newValue){
	const display = document.getElementById('display');
	displayValue = newValue;
    display.innerText = displayValue;
}

function deleteDisplay(){
	const display = document.getElementById('display');
	letter = displayValue[displayValue.length-1];
	displayValue = displayValue.replace(letter,'');
	display.innerText = displayValue;
}

function buttonClick(event){
	const button = event.target;
	if (button.classList[0] == "del"){
		deleteDisplay();
	}
	else if(button.classList[0] == "number"){
		updateDisplay(button);
	}
	else if(button.classList[0] == "operator"){
		updateDisplay(button);
	}
	else if(button.classList[0] == "AC"){
		changeDisplayValue('');
	}
	else if(button.classList[0] == "equal"){
		let value = evaluate(displayValue);
	    changeDisplayValue(value);
	}
}

buttons.forEach((button) => {
	button.addEventListener("click", function(event) {
		buttonClick(event);
	});
});

