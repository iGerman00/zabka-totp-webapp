// DOM Elements
const totpCodeElement = document.getElementById("totp-code");
const qrCodeUrlElement = document.getElementById("qrcode-url");
const totpSection = document.getElementById("totp-section");
const qrCodeCanvas = document.getElementById("qrcode-canvas");
const qrCodeCanvasAlt = document.getElementById("qrcode-canvas-alt");
const clearSecretsButton = document.getElementById("clear-secrets");
const alternateDesignButton = document.getElementById("alternate-design");
const closeAlternateDesignButton = document.getElementById("close-alternate-design");
const secretsHint = document.getElementById("secrets-hint");

const manualInputForm = document.getElementById("manual-input-form");
const manualInputSecret = document.getElementById("manual-input-secret");

function hexStringToBytes(hexString) {
    const bytes = [];
    for (let i = 0; i < hexString.length; i += 2) {
        bytes.push(parseInt(hexString.substr(i, 2), 16));
    }
    return new Uint8Array(bytes);
}

function bytesToUint32(bytes, offset) {
    let result = 0;
    for (let i = 0; i < 4; i++) {
        result = (result << 8) | bytes[offset + i];
    }
    return result;
}

async function sha1hmac(secret, message) {
    const key = await crypto.subtle.importKey(
        'raw',
        secret, // Secret is already a Uint8Array
        { name: 'HMAC', hash: { name: 'SHA-1' } }, // Specify hash as an object
        false,
        ['sign']
    );

    // No need to encode message, it's already a Uint8Array (time step)
    const signature = await crypto.subtle.sign('HMAC', key, message);

    return new Uint8Array(signature);
}

async function generateTOTP(secretHex, time) {
    let timeStep = Math.floor(time / 30);
    const timeStepBytes = new Uint8Array(8);
    for (let i = 7; i >= 0; i--) {
        timeStepBytes[i] = timeStep & 0xFF;
        timeStep >>= 8;
    }

    const secretBytes = hexStringToBytes(secretHex);
    const hmacResult = await sha1hmac(secretBytes, timeStepBytes);

    const offset = hmacResult[hmacResult.length - 1] & 0x0F;
    const truncatedHash = bytesToUint32(hmacResult, offset) & 0x7FFFFFFF;
    const totp = (truncatedHash % 1000000).toString().padStart(6, '0');

    return totp;
}

async function generateQRCodeURL(secretHex, id, time) {
    const totp = await generateTOTP(secretHex, time);
    const qrCodeURL = `https://srln.pl/view/dashboard?ploy=${id}&loyal=${totp}`;
    return qrCodeURL;
}

function storeSecrets(secrets) {
    localStorage.setItem("secrets", JSON.stringify(secrets));
}

function loadSecrets() {
    const storedSecrets = localStorage.getItem("secrets");
    if (storedSecrets) {
        return JSON.parse(storedSecrets);
    }
    return null;
}

function clearSecrets() {
    localStorage.removeItem("secrets");
}

function updateBorder(timeInPeriod) {
    const canvas = document.getElementById('qrcode-canvas');
    const progress = timeInPeriod / 30; // 0 to 1

    let color;
    if (progress < 0.5) {
        color = '#10B981';
    } else if (progress < 0.85) {
        color = '#F59E0B';
    } else {
        color = '#EF4444';
    }

    const angle = progress * 360;
    canvas.style.borderImage = `conic-gradient(${color} ${angle}deg, transparent ${angle}deg) 1`;
}

async function updateTOTPDisplay(secret, ployId) {
    const now = Math.floor(Date.now() / 1000);
    const timeInPeriod = now % 30;
    const url = await generateQRCodeURL(secret, ployId, now);

    totpCodeElement.textContent = url.split("loyal=")[1];

    const sanitizedUrl = DOMPurify.sanitize(url);
    qrCodeUrlElement.textContent = sanitizedUrl;
    qrCodeUrlElement.href = sanitizedUrl;

    const prefersDarkMode = window.matchMedia("(prefers-color-scheme: dark)").matches;

    new QRious({
        element: qrCodeCanvas,
        value: sanitizedUrl,
        size: 500,
        level: 'Q',
        background: 'transparent',
        foreground: prefersDarkMode ? 'white' : 'black',
    });

    new QRious({
        element: qrCodeCanvasAlt,
        value: sanitizedUrl,
        size: 500,
        level: 'Q',
        background: 'white',
        foreground: 'black',
    });

    updateBorder(timeInPeriod);
}

// -- Initialization --

const urlParams = new URLSearchParams(window.location.search);
const secretsParam = urlParams.get("secrets");
const alternateDesignParam = urlParams.get("alternate");
const alternateDesign = localStorage.getItem("alternateDesign");

// 1000-9999 random number
document.getElementById("fake-zappsy").innerText = Math.floor(Math.random() * 9000) + 1000 + ' żappsów';

if (alternateDesignParam !== null || alternateDesign === "true") {
    localStorage.setItem("alternateDesign", true);
    document.getElementById("alternate-design-overlay").classList.remove("hidden");
    document.getElementById("main-container").classList.toggle("hidden");
}

if (secretsParam) {
    try {
        const decodedSecrets = JSON.parse(decodeURIComponent(secretsParam));
        storeSecrets(decodedSecrets);
        totpSection.classList.remove("hidden");
        secretsHint.classList.add("hidden");
        updateTOTPDisplay(decodedSecrets.secret, decodedSecrets.ployId);
        setInterval(() => updateTOTPDisplay(decodedSecrets.secret, decodedSecrets.ployId), 1000);
    } catch (error) {
        console.error("Error parsing secrets from URL parameter:", error);
        alert("Invalid secrets in URL parameter.");
    }
} else {
    const storedSecrets = loadSecrets();
    if (storedSecrets) {
        totpSection.classList.remove("hidden");
        updateTOTPDisplay(storedSecrets.secret, storedSecrets.ployId);
        setInterval(() => updateTOTPDisplay(storedSecrets.secret, storedSecrets.ployId), 1000);
    } else {
        manualInputForm.classList.remove("hidden");
        manualInputForm.addEventListener("submit", (event) => {
            event.preventDefault();
            const secret = manualInputSecret.value;
            try {
                const parsedSecret = JSON.parse(secret);
                storeSecrets(parsedSecret);
                manualInputForm.classList.add("hidden");
                totpSection.classList.remove("hidden");
                updateTOTPDisplay(parsedSecret.secret, parsedSecret.ployId);
                setInterval(() => updateTOTPDisplay(parsedSecret.secret, parsedSecret.ployId), 1000);
            } catch (error) {
                console.error("Error parsing secrets from manual input:", error);
                alert("Invalid secrets input.");
            }
        });
    }
}

clearSecretsButton.addEventListener("click", () => {
    clearSecrets();
    location.reload();
});

alternateDesignButton.addEventListener("click", () => {
    localStorage.setItem("alternateDesign", true);
    document.getElementById("alternate-design-overlay").classList.remove("hidden");
    document.getElementById("main-container").classList.add("hidden");
});

closeAlternateDesignButton.addEventListener("click", () => {
    localStorage.setItem("alternateDesign", false);
    document.getElementById("alternate-design-overlay").classList.add("hidden");
    document.getElementById("main-container").classList.remove("hidden");
});