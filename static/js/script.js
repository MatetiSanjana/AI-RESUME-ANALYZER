document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("analyzeForm");
    const submitBtn = document.getElementById("submitBtn");
    const resumeInput = document.getElementById("resume");

    // Elements used to display selected filename
    const fileLabel = document.getElementById("fileLabel");
    const fileName = document.getElementById("fileName");
    if (resumeInput) {

        resumeInput.addEventListener("change", function () {

            if (this.files && this.files.length > 0) {

                const file = this.files[0];

                // Show selected filename
                if (fileLabel) {
                    fileLabel.textContent = "Resume selected";
                }

                if (fileName) {
                    fileName.textContent = file.name;
                }

            } else {

                // Reset when no file is selected
                if (fileLabel) {
                    fileLabel.textContent = "Click to upload your resume";
                }

                if (fileName) {
                    fileName.textContent =
                        "PDF or DOCX • Maximum supported file size";
                }

            }

        });

    }

    if (!form) return;

    form.addEventListener("submit", function (e) {

        // Basic client-side extension check
        const file = resumeInput.files[0];

        if (file) {

            const ext = file.name
                .split(".")
                .pop()
                .toLowerCase();

            if (ext !== "pdf" && ext !== "docx") {

                e.preventDefault();

                alert("Only PDF and DOCX files are allowed.");

                return;
            }
        }


        // Show loading state
        submitBtn.disabled = true;

        submitBtn.innerHTML =
            '<span class="spinner-border spinner-border-sm me-2"></span>Analyzing...';

    });

});