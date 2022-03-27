//Setting the contents of form__message
function setFormMessage(formElement, type, message) {
    const messageElement = formElement.querySelector(".form__message");

    messageElement.textContent = message;
    messageElement.classList.remove("form__message--success", "form__message--error");
    messageElement.classList.add(`form__message--${type}`);
}

//Setting the messages on the individual input fields
function setInputError(inputElement, message) {
    inputElement.classList.add("form__input--error");
    inputElement.parentElement.querySelector(".form__input-error-message").textContent = message;
}

//Used to hide the error message once the user begins to change their wrong input
function clearInputError(inputElement) {
    inputElement.classList.remove("form__input--error");
    inputElement.parentElement.querySelector(".form__input-error-message").textContent = "";
}

//Once the document is ready to be worked with, we can run this function
document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.querySelector("#login");
    const createAccountForm = document.querySelector("#createAccount");

    //A toggle button to hide and show the create account page
    document.querySelector("#linkCreateAccount").addEventListener("click", e => {
        e.preventDefault();
        loginForm.classList.add("form--hidden");
        createAccountForm.classList.remove("form--hidden");
    });

    document.querySelector("#linkLogin").addEventListener("click", e => {
        e.preventDefault();
        loginForm.classList.remove("form--hidden");
        createAccountForm.classList.add("form--hidden");
    });

    loginForm.addEventListener("submit", e => {
        e.preventDefault();

        // Perform your AJAX/Fetch login

        setFormMessage(loginForm, "error", "Invalid username/password combination");
    });

    //Displaying of error message for "create account" page when given certain inputs by the user
    document.querySelectorAll(".form__input").forEach(inputElement => {
        inputElement.addEventListener("blur", e => {
            if (e.target.id === "signupUsername" && e.target.value.length > 0 && e.target.value.length < 10) {
                setInputError(inputElement, "Username must be at least 10 characters in length");
            }
            if (e.target.id === "signupUsername" && e.target.value.length==0) {
                setInputError(inputElement, "Invalid Username - Username cannot be empty");
            }
            if (e.target.id === "signupEmailAddress" && e.target.value.length==0) {
                setInputError(inputElement, "Invalid Email Address - Email Address cannot be empty");
            }
            if (e.target.id === "signupPassword" && e.target.value.length==0) {
                setInputError(inputElement, "Invalid Password - Password cannot be empty");
            }
        });

        inputElement.addEventListener("input", e => {
            clearInputError(inputElement);
        });
    });
});