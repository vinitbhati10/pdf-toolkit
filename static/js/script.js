const pdfFile = document.getElementById("pdfFile");
const fileName = document.getElementById("fileName");

function showLoading(element, message) {

    element.innerHTML = `
        <span class="tool-loading">
            <span class="loading-spinner"></span>
            ${message}
        </span>
    `;
}

const uploadBox =
    document.getElementById("uploadBox");

const chooseFileButton =
    document.getElementById("chooseFileButton");


// Choose PDF button
chooseFileButton.addEventListener("click", function () {

    pdfFile.click();

});


// Drag over
uploadBox.addEventListener("dragover", function (event) {

    event.preventDefault();

    uploadBox.classList.add("drag-over");

});


// Drag leave
uploadBox.addEventListener("dragleave", function () {

    uploadBox.classList.remove("drag-over");

});


// Drop files
uploadBox.addEventListener("drop", function (event) {

    event.preventDefault();

    uploadBox.classList.remove("drag-over");

    pdfFile.files = event.dataTransfer.files;

    pdfFile.dispatchEvent(
        new Event("change")
    );

});

pdfFile.addEventListener("change", function () {

    if (pdfFile.files.length === 0) {
        fileName.textContent = "";
        return;
    }

    let names = [];

    for (let i = 0; i < pdfFile.files.length; i++) {
        names.push(pdfFile.files[i].name);
    }

    fileName.textContent =
        "Selected files: " + names.join(", ");

});
const mergeButton = document.getElementById("mergeButton");
const mergeStatus = document.getElementById("mergeStatus");
const downloadLink = document.getElementById("downloadLink");


mergeButton.addEventListener("click", async function () {

    if (pdfFile.files.length < 2) {

        mergeStatus.textContent =
            "❌ Please select at least 2 PDF files.";

        return;
    }

    const formData = new FormData();

    for (let i = 0; i < pdfFile.files.length; i++) {

        formData.append(
            "files",
            pdfFile.files[i]
        );

    }

  showLoading(
    mergeStatus,
    "Merging PDFs..."
);

    try {

        const response = await fetch("/merge", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        if (result.success) {

            mergeStatus.textContent =
                "✓ " + result.message;

            downloadLink.href =
                result.download_url;

            downloadLink.style.display =
                "inline-block";

        } else {

            mergeStatus.textContent =
                "❌ " + result.message;

        }

    } catch (error) {

        mergeStatus.textContent =
            "❌ Merge failed.";

        console.error(error);

    }

});

// =============================
// Split PDF
// =============================

const splitButton =
    document.getElementById("splitButton");

const splitStatus =
    document.getElementById("splitStatus");

const splitDownloadLink =
    document.getElementById("splitDownloadLink");

const splitStart =
    document.getElementById("splitStart");

const splitEnd =
    document.getElementById("splitEnd");


splitButton.addEventListener("click", async function () {

    // Check PDF
    if (pdfFile.files.length === 0) {

        splitStatus.textContent =
            "❌ Please select a PDF first.";

        return;
    }


    // Only one PDF for splitting
    const file = pdfFile.files[0];


    // Check page range
    if (!splitStart.value || !splitEnd.value) {

        splitStatus.textContent =
            "❌ Please enter start and end pages.";

        return;
    }


    const formData = new FormData();

    formData.append("file", file);

    formData.append(
        "start_page",
        splitStart.value
    );

    formData.append(
        "end_page",
        splitEnd.value
    );


  showLoading(
    splitStatus,
    "Splitting PDF..."
);

    splitDownloadLink.style.display =
        "none";


    try {

        const response = await fetch("/split", {

            method: "POST",

            body: formData

        });


        const result = await response.json();


        if (result.success) {

            splitStatus.textContent =
                "✓ " + result.message;

            splitDownloadLink.href =
                result.download_url;

            splitDownloadLink.style.display =
                "inline-block";

        } else {

            splitStatus.textContent =
                "❌ " + result.message;

        }


    } catch (error) {

        console.error("Split error:", error);

        splitStatus.textContent =
            "❌ Split failed.";

    }

});

// =============================
// Compress PDF
// =============================

const compressButton =
    document.getElementById("compressButton");

const compressStatus =
    document.getElementById("compressStatus");

const compressDownloadLink =
    document.getElementById("compressDownloadLink");


compressButton.addEventListener("click", async function () {

    // Check if PDF is selected
    if (pdfFile.files.length === 0) {

        compressStatus.textContent =
            "❌ Please select a PDF first.";

        return;
    }

    // Use the first selected PDF
    const file = pdfFile.files[0];

    const formData = new FormData();

    formData.append("file", file);

   showLoading(
    compressStatus,
    "Compressing PDF..."
);

    compressDownloadLink.style.display =
        "none";

    try {

        const response = await fetch("/compress", {

            method: "POST",

            body: formData

        });

        const result = await response.json();

        if (result.success) {

            compressStatus.textContent =
                "✓ " + result.message;

            compressDownloadLink.href =
                result.download_url;

            compressDownloadLink.style.display =
                "inline-block";

        } else {

            compressStatus.textContent =
                "❌ " + result.message;

        }

    } catch (error) {

        console.error("Compress error:", error);

        compressStatus.textContent =
            "❌ Compression failed.";

    }

});

// =============================
// Rotate PDF
// =============================

const rotateButton =
    document.getElementById("rotateButton");

const rotateStatus =
    document.getElementById("rotateStatus");

const rotateDownloadLink =
    document.getElementById("rotateDownloadLink");

const rotateAngle =
    document.getElementById("rotateAngle");


rotateButton.addEventListener("click", async function () {

    // Check PDF
    if (pdfFile.files.length === 0) {

        rotateStatus.textContent =
            "❌ Please select a PDF first.";

        return;
    }

    const file = pdfFile.files[0];

    const formData = new FormData();

    formData.append("file", file);

    formData.append(
        "angle",
        rotateAngle.value
    );

   showLoading(
    rotateStatus,
    "Rotating PDF..."
);

    rotateDownloadLink.style.display =
        "none";

    try {

        const response = await fetch("/rotate", {

            method: "POST",

            body: formData

        });

        const result = await response.json();

        if (result.success) {

            rotateStatus.textContent =
                "✓ " + result.message;

            rotateDownloadLink.href =
                result.download_url;

            rotateDownloadLink.style.display =
                "inline-block";

        } else {

            rotateStatus.textContent =
                "❌ " + result.message;

        }

    } catch (error) {

        console.error("Rotate error:", error);

        rotateStatus.textContent =
            "❌ Rotation failed.";

    }

});

// =============================
// PDF → Images
// =============================

const pdfToImagesButton =
    document.getElementById("pdfToImagesButton");

const pdfToImagesStatus =
    document.getElementById("pdfToImagesStatus");

const pdfToImagesDownloadLink =
    document.getElementById("pdfToImagesDownloadLink");


pdfToImagesButton.addEventListener("click", async function () {

    if (pdfFile.files.length === 0) {

        pdfToImagesStatus.textContent =
            "❌ Please select a PDF first.";

        return;
    }

    const file = pdfFile.files[0];

    const formData = new FormData();

    formData.append("file", file);

    pdfToImagesStatus.textContent =
        "Converting PDF to images...";

    pdfToImagesDownloadLink.style.display =
        "none";

    try {

        const response = await fetch("/pdf-to-images", {

            method: "POST",

            body: formData

        });

        const result = await response.json();

        if (result.success) {

            pdfToImagesStatus.textContent =
                "✓ " + result.message;

            pdfToImagesDownloadLink.href =
                result.download_url;

            pdfToImagesDownloadLink.style.display =
                "inline-block";

        } else {

            pdfToImagesStatus.textContent =
                "❌ " + result.message;

        }

    } catch (error) {

        console.error(
            "PDF to Images error:",
            error
        );

        pdfToImagesStatus.textContent =
            "❌ Conversion failed.";

    }

});

// =============================
// Images → PDF
// =============================

const imagesToPdfInput =
    document.getElementById("imagesToPdfInput");

const imagesToPdfFileName =
    document.getElementById("imagesToPdfFileName");

const imagesToPdfButton =
    document.getElementById("imagesToPdfButton");

const imagesToPdfStatus =
    document.getElementById("imagesToPdfStatus");

const imagesToPdfDownloadLink =
    document.getElementById("imagesToPdfDownloadLink");


imagesToPdfInput.addEventListener("change", function () {

    if (imagesToPdfInput.files.length === 0) {

        imagesToPdfFileName.textContent = "";

        return;
    }

    imagesToPdfFileName.textContent =
        imagesToPdfInput.files.length +
        " image(s) selected";

});


imagesToPdfButton.addEventListener("click", async function () {

    if (imagesToPdfInput.files.length === 0) {

        imagesToPdfStatus.textContent =
            "❌ Please select at least one image.";

        return;
    }

    const formData = new FormData();

    for (
        let i = 0;
        i < imagesToPdfInput.files.length;
        i++
    ) {

        formData.append(
            "images",
            imagesToPdfInput.files[i]
        );

    }

showLoading(
    pdfToImagesStatus,
    "Converting PDF to images..."
);

    imagesToPdfDownloadLink.style.display =
        "none";

    try {

        const response = await fetch(
            "/images-to-pdf",
            {
                method: "POST",
                body: formData
            }
        );

        const result = await response.json();

        if (result.success) {

            imagesToPdfStatus.textContent =
                "✓ " + result.message;

            imagesToPdfDownloadLink.href =
                result.download_url;

            imagesToPdfDownloadLink.style.display =
                "inline-block";

        } else {

            imagesToPdfStatus.textContent =
                "❌ " + result.message;

        }

    } catch (error) {

        console.error(
            "Images to PDF error:",
            error
        );

        imagesToPdfStatus.textContent =
            "❌ Conversion failed.";

    }

});

// =============================
// Watermark PDF
// =============================

const watermarkText =
    document.getElementById("watermarkText");

const watermarkButton =
    document.getElementById("watermarkButton");

const watermarkStatus =
    document.getElementById("watermarkStatus");

const watermarkDownloadLink =
    document.getElementById("watermarkDownloadLink");


watermarkButton.addEventListener("click", async function () {

    // Check PDF
    if (pdfFile.files.length === 0) {

        watermarkStatus.textContent =
            "❌ Please select a PDF first.";

        return;
    }

    // Check watermark text
    if (watermarkText.value.trim() === "") {

        watermarkStatus.textContent =
            "❌ Please enter watermark text.";

        return;
    }

    const file = pdfFile.files[0];

    const formData = new FormData();

    formData.append("file", file);

    formData.append(
        "text",
        watermarkText.value.trim()
    );
showLoading(
    watermarkStatus,
    "Adding watermark..."
);

    watermarkDownloadLink.style.display =
        "none";

    try {

        const response = await fetch(
            "/watermark",
            {
                method: "POST",
                body: formData
            }
        );

        const result = await response.json();

        if (result.success) {

            watermarkStatus.textContent =
                "✓ " + result.message;

            watermarkDownloadLink.href =
                result.download_url;

            watermarkDownloadLink.style.display =
                "inline-block";

        } else {

            watermarkStatus.textContent =
                "❌ " + result.message;

        }

    } catch (error) {

        console.error(
            "Watermark error:",
            error
        );

        watermarkStatus.textContent =
            "❌ Watermark failed.";

    }

});

// =============================
// Protect PDF
// =============================

const protectPassword =
    document.getElementById("protectPassword");

const protectButton =
    document.getElementById("protectButton");

const protectStatus =
    document.getElementById("protectStatus");

const protectDownloadLink =
    document.getElementById("protectDownloadLink");


protectButton.addEventListener("click", async function () {

    // Check PDF
    if (pdfFile.files.length === 0) {

        protectStatus.textContent =
            "❌ Please select a PDF first.";

        return;
    }

    // Check password
    if (protectPassword.value.trim() === "") {

        protectStatus.textContent =
            "❌ Please enter a password.";

        return;
    }

    const file = pdfFile.files[0];

    const formData = new FormData();

    formData.append("file", file);

    formData.append(
        "password",
        protectPassword.value
    );

   showLoading(
    protectStatus,
    "Protecting PDF..."
);

    protectDownloadLink.style.display =
        "none";

    try {

        const response = await fetch(
            "/protect",
            {
                method: "POST",
                body: formData
            }
        );

        const result = await response.json();

        if (result.success) {

            protectStatus.textContent =
                "✓ " + result.message;

            protectDownloadLink.href =
                result.download_url;

            protectDownloadLink.style.display =
                "inline-block";

        } else {

            protectStatus.textContent =
                "❌ " + result.message;

        }

    } catch (error) {

        console.error(
            "Protect PDF error:",
            error
        );

        protectStatus.textContent =
            "❌ Protection failed.";

    }

});

// =============================
// Delete PDF Pages
// =============================

const deletePdfInput =
    document.getElementById("deletePdfInput");

const deletePagesInput =
    document.getElementById("deletePagesInput");

const deletePagesButton =
    document.getElementById("deletePagesButton");

const deletePagesStatus =
    document.getElementById("deletePagesStatus");

const deletePagesDownloadLink =
    document.getElementById("deletePagesDownloadLink");


deletePagesButton.addEventListener("click", async function () {

    if (deletePdfInput.files.length === 0) {

        deletePagesStatus.textContent =
            "❌ Please select a PDF.";

        return;
    }

    if (deletePagesInput.value.trim() === "") {

        deletePagesStatus.textContent =
            "❌ Enter pages to delete.";

        return;
    }

    const file = deletePdfInput.files[0];

    const formData = new FormData();

    formData.append(
        "file",
        file
    );

    formData.append(
        "pages",
        deletePagesInput.value.trim()
    );

   showLoading(
    deletePagesStatus,
    "Deleting pages..."
);

    deletePagesDownloadLink.style.display =
        "none";

    try {

        const response = await fetch(
            "/delete-pages",
            {
                method: "POST",
                body: formData
            }
        );

        const result = await response.json();

        if (result.success) {

            deletePagesStatus.textContent =
                "✓ " + result.message;

            deletePagesDownloadLink.href =
                result.download_url;

            deletePagesDownloadLink.style.display =
                "inline-block";

        } else {

            deletePagesStatus.textContent =
                "❌ " + result.message;

        }

    } catch (error) {

        console.error(
            "Delete pages error:",
            error
        );

        deletePagesStatus.textContent =
            "❌ Delete operation failed.";

    }

});

// =============================
// Reorder PDF Pages
// =============================

const reorderPdfInput =
    document.getElementById("reorderPdfInput");

const pageOrderInput =
    document.getElementById("pageOrderInput");

const reorderPagesButton =
    document.getElementById("reorderPagesButton");

const reorderPagesStatus =
    document.getElementById("reorderPagesStatus");

const reorderPagesDownloadLink =
    document.getElementById("reorderPagesDownloadLink");


reorderPagesButton.addEventListener("click", async function () {

    if (reorderPdfInput.files.length === 0) {

        reorderPagesStatus.textContent =
            "❌ Please select a PDF.";

        return;
    }

    if (pageOrderInput.value.trim() === "") {

        reorderPagesStatus.textContent =
            "❌ Enter the new page order.";

        return;
    }

    const order = pageOrderInput.value
        .split(",")
        .map(page => parseInt(page.trim()))
        .filter(page => !isNaN(page));

    if (order.length === 0) {

        reorderPagesStatus.textContent =
            "❌ Enter a valid page order.";

        return;
    }

    const file = reorderPdfInput.files[0];

    const formData = new FormData();

    formData.append(
        "file",
        file
    );

    // Convert page numbers from 1-based
    // to Python's 0-based numbering.
    const pageOrder = order.map(
        page => page - 1
    );

    formData.append(
        "page_order",
        pageOrder.join(",")
    );

    reorderPagesStatus.textContent =
        "Reordering pages...";

    reorderPagesDownloadLink.style.display =
        "none";

    try {

        const response = await fetch(
            "/organize",
            {
                method: "POST",
                body: formData
            }
        );

        const result = await response.json();

        if (result.success) {

            reorderPagesStatus.textContent =
                "✓ " + result.message;

            reorderPagesDownloadLink.href =
                result.download_url;

            reorderPagesDownloadLink.style.display =
                "inline-block";

        } else {

            reorderPagesStatus.textContent =
                "❌ " + result.message;

        }

    } catch (error) {

        console.error(
            "Reorder pages error:",
            error
        );

        reorderPagesStatus.textContent =
            "❌ Reorder operation failed.";

    }

});