const yourEmail = document.querySelector("#yourEmail");
const emailFeedbackArea = document.querySelector(".emailFeedbackArea");
const passwordField = document.querySelector("#passwordField");
const showPasswordToggle = document.querySelector(".showPasswordToggle");
const submitBtn = document.querySelector(".submit-btn");

const handleToggleInput = (e) => {
    if (showPasswordToggle.textContent === "TAMPILKAN") {
        showPasswordToggle.textContent = "SEMBUNYIKAN";
        passwordField.setAttribute("type", "text");
    } else {
        showPasswordToggle.textContent = "TAMPILKAN";
        passwordField.setAttribute("type", "password");
    }
};

showPasswordToggle.addEventListener("click", handleToggleInput);

yourEmail.addEventListener("keyup", (e) => {
    const emailVal = e.target.value;

    yourEmail.classList.remove("is-invalid");

    console.log(emailVal);

    if (emailVal.length > 0) {
        fetch("/authentication/validate-email", {
            body: JSON.stringify({ email: emailVal }),
            method: "POST",
        })
            .then(res => res.json())
            .then(data => {
                console.log("data", data);
                if (data.email_error) {
                    submitBtn.disabled = true;
                    yourEmail.classList.add("is-invalid");
                    emailFeedbackArea.innerHTML = `<p>${data.email_error}</p>`;
                } else {
                    submitBtn.removeAttribute("disabled");
                }
            });
    }
});