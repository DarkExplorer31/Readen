function showLoadingOverlay() {
    overlay.style.display = 'block';
    loadingModal.style.display = 'block';
}

function hideLoadingOverlay() {
    overlay.style.display = 'none';
    loadingModal.style.display = 'none';
}

function showVideoModal() {
    overlay.style.display = 'block';
    signUpVideoModal.style.display = 'block';

    signUpVideo.play();
    signUpVideo.addEventListener('ended', hideVideoModal);
}

function hideVideoModal() {
    overlay.style.display = 'none';
    signUpVideoModal.style.display = 'none';
    signUpVideo.pause();
}

async function fetchAndSetAudio(audioPlayer, audioUrl) {
    try {
        showLoadingOverlay();
        const response = await fetch(audioUrl);
        const blob = await response.blob();
        const objectURL = URL.createObjectURL(blob);
        audioPlayer.src = objectURL;
        audioPlayer.addEventListener('canplaythrough', () => {
            hideLoadingOverlay();
            audioPlayer.controls = true;
        });
    } catch (error) {
        console.error('Error fetching audio file:', error);
        hideLoadingOverlay();
    }
}

function setupPlaybackControls(audioPlayer, backwardButton, forwardButton) {
    backwardButton.addEventListener('click', () => {
        audioPlayer.currentTime -= 10;
    });

    forwardButton.addEventListener('click', () => {
        audioPlayer.currentTime += 10;
    });
}

function setupVideoSync(audioPlayer, videoPlayer) {
    audioPlayer.addEventListener('play', function () {
        videoPlayer.src = "/media/lomelindya/Lomelindya_read_corner_reading.mp4";
    });

    audioPlayer.addEventListener('pause', function () {
        videoPlayer.src = "/media/lomelindya/Lomelindya_read_corner_waiting.mp4";
    });
}

async function initialize() {
    const audioPlayer = document.getElementById('audioPlayer');
    const backwardButton = document.getElementById('backwardButton');
    const forwardButton = document.getElementById('forwardButton');
    const readingVideo = document.getElementById('readingVideo');
    const signUpVideo = document.getElementById('signUpVideo');

    if (signUpVideo) {
        showVideoModal();
    } else {
        if (audioPlayer) {
            await fetchAndSetAudio(audioPlayer, audioPlayer.dataset.audioUrl);
            setupPlaybackControls(audioPlayer, backwardButton, forwardButton);
            setupVideoSync(audioPlayer, readingVideo);
        }
    }
}


initialize();

/*Menu Modal*/
const openMenu = document.getElementById("menu-button");
const closeMenu = document.getElementById("close-button");
const menuOverlay = document.getElementById("menu-overlay");
const sideMenu = document.getElementById("side-menu");

function toggleMenu() {
    openMenu.classList.add("open");
    sideMenu.classList.add("open");
    menuOverlay.classList.add("open");
    sideMenu.style.display = "block";
    menuOverlay.style.display = "block";
}

function hideMenu() {
    openMenu.classList.remove("open");
    sideMenu.classList.remove("open");
    menuOverlay.classList.remove("open");
    sideMenu.style.display = "none";
    menuOverlay.style.display = "none";
}

openMenu.addEventListener('click', toggleMenu);
closeMenu.addEventListener('click', hideMenu);
menuOverlay.addEventListener('click', hideMenu);

/* Book Animation*/
const container = document.querySelector("#book-container");
const prevBtn = document.querySelector("#prev-btn");
const nextBtn = document.querySelector("#next-btn");
const book = document.querySelector("#book");

pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.11.338/pdf.worker.min.js';

const pdfPath = book.getAttribute('data-pdf');
const fullPDFPath = '/media/' + pdfPath;
let numOfPapers = 0;

function getPDFPageCount(fullPDFPath, callback) {
    pdfjsLib.getDocument(fullPDFPath).promise.then(pdf => {
        callback(pdf.numPages);
    }).catch(error => {
        console.error('Error: ' + error.message);
        callback(null);
    });
}

getPDFPageCount(fullPDFPath, function (numPages) {
    if (numPages !== null) {
        numOfPapers = numPages;
        console.log('Number of pages:', numOfPapers);
        maxLocation = numOfPapers + 4;
    } else {
        console.log('Failed to load the PDF.');
    }
});

function renderPDFPageToImage(pdfDoc, pageNumber, container) {
    pdfDoc.getPage(pageNumber).then(page => {
        const viewport = page.getViewport({ scale: 1.0 });
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.height = viewport.height;
        canvas.width = viewport.width;

        const renderContext = {
            canvasContext: context,
            viewport: viewport
        };
        page.render(renderContext).promise.then(() => {
            const img = document.createElement('img');
            img.src = canvas.toDataURL();
            container.innerHTML = '';
            container.appendChild(img);
        });
    });
}

function loadPDFPage(pdfPath, pageNumber, container) {
    pdfjsLib.getDocument(pdfPath).promise.then(pdfDoc => {
        renderPDFPageToImage(pdfDoc, pageNumber, container);
    }).catch(error => {
        console.error('Error: ' + error.message);
    });
}

const firstPaper = document.querySelector("#first");
const paper2 = document.querySelector("#p2");
const paper3 = document.querySelector("#p3");
const lastPaper = document.querySelector("#last");

nextBtn.addEventListener("click", goNextPage);

function exitZoom() {
    prevBtn.classList.remove("open");
    nextBtn.classList.remove("open");
    container.classList.remove("book-open");
    book.classList.remove("open");
}

function openBook() {
    container.classList.add("book-open");
    book.classList.add("open");
    prevBtn.classList.add("open");
    nextBtn.classList.add("open");
    firstPaper.classList.add("flipped");
    firstPaper.style.zIndex = 1;
    book.style.transform = "translateX(50%)";
    prevBtn.style.transform = "translateX(-330px)";
    nextBtn.style.display = "block";
    prevBtn.style.display = "block";
    nextBtn.style.transform = "translateX(330px)";
}

function closeBook(isAtBeginning) {
    if (isAtBeginning) {
        book.style.transform = "translateX(0%)";
        prevBtn.style.display = "none";
        paper2.classList.remove("flipped");
        paper3.classList.remove("flipped");
        lastPaper.classList.remove("flipped");
    } else {
        paper2.classList.add("flipped");
        paper3.classList.add("flipped");
        lastPaper.classList.add("flipped");
        lastPaper.style.zIndex = 4;
        book.style.transform = "translateX(100%)";
        nextBtn.style.display = "none";
    }
    exitZoom();
    prevBtn.style.transform = "translateX(0px)";
    nextBtn.style.transform = "translateX(0px)";
}

let pointOfView = 1;
let view = 1;
let p1Position = 1;
let p2Position = 2;
let p3Position = 3;
let p4Position = 4;

function goNextPageUnderFivePage() {
    if (view === 1) {
        openBook();
        loadPDFPage(fullPDFPath, p1Position, paper2.querySelector('.front-content'));
        view += 1;
    } else if (view === 2 && numOfPapers === 1) {
        closeBook();
    } else if (view === 2 && numOfPapers === 2) {
        loadPDFPage(fullPDFPath, p2Position, paper2.querySelector('.back-content'));
        paper2.classList.add("flipped");
        paper3.classList.add("flipped");
        view += 1;
    } else if (view === 3 && numOfPapers === 2) {
        closeBook();
    } else if (view === 2 && numOfPapers > 2) {
        loadPDFPage(fullPDFPath, p2Position, paper2.querySelector('.back-content'));
        loadPDFPage(fullPDFPath, p3Position, paper3.querySelector('.front-content'));
        paper2.classList.add("flipped");
        view += 1;
    } else if (view === 3 && numOfPapers === 3) {
        closeBook();
    } else if (view === 3 && numOfPapers === 4) {
        loadPDFPage(fullPDFPath, p4Position, paper3.querySelector('.back-content'));
        paper3.classList.add("flipped");
        paper2.style.zIndex = 2;
        paper3.style.zIndex = 3;
        view += 1;
    } else {
        closeBook();
    }
}

function goNextPage() {
    if (pointOfView < 4 && numOfPapers > 4) {
        if (pointOfView === 1) {
            pointOfView += 1;
            openBook();
            loadPDFPage(fullPDFPath, p1Position, paper2.querySelector('.front-content'));
        } else if (pointOfView === 2) {
            if (p1Position === numOfPapers || p3Position === numOfPapers) {
                pointOfView += 1;
            }
            if (p2Position === numOfPapers) {
                loadPDFPage(fullPDFPath, p2Position, paper2.querySelector('.back-content'));
                paper2.classList.add("flipped");
                paper3.classList.add("flipped");
                paper2.style.zIndex = 3;
                paper3.style.zIndex = 2;
                paper2.querySelector(".front").style.transition = "transform 0.8s";
                paper2.querySelector(".back").style.transition = "transform 0.8s";
                pointOfView += 1;
            } else if (p4Position === numOfPapers) {
                loadPDFPage(fullPDFPath, p4Position, paper3.querySelector('.back-content'));
                paper2.classList.add("flipped");
                paper3.classList.add("flipped");
                paper3.querySelector(".front").style.transition = "transform 0.8s";
                paper3.querySelector(".back").style.transition = "transform 0.8s";
                paper2.style.zIndex = 2;
                paper3.style.zIndex = 3;
                pointOfView += 1;
            } else if (view === 2) {
                firstPaper.style.zIndex = 1;
                p1Position += 4;
                paper2.classList.add("flipped");
                loadPDFPage(fullPDFPath, p2Position, firstPaper.querySelector('.back-content'));
                loadPDFPage(fullPDFPath, p2Position, paper2.querySelector('.back-content'));
                loadPDFPage(fullPDFPath, p3Position, paper3.querySelector('.front-content'));
                loadPDFPage(fullPDFPath, p4Position, paper3.querySelector('.back-content'));
            } else if (view % 2 !== 0 && view !== 1) {
                p2Position += 4;
                p3Position += 4;
                loadPDFPage(fullPDFPath, p4Position, paper3.querySelector('.back-content'));
                loadPDFPage(fullPDFPath, p3Position, paper3.querySelector('.front-content'));
                loadPDFPage(fullPDFPath, p4Position, firstPaper.querySelector('.back-content'));
                loadPDFPage(fullPDFPath, p1Position, paper2.querySelector('.front-content'));
                paper3.classList.add("flipped");
                paper2.classList.remove("flipped");
                paper3.querySelector(".front").style.transition = "transform 0.8s";
                paper3.querySelector(".back").style.transition = "transform 0.8s";
                paper2.querySelector(".front").style.transition = "transform 0s";
                paper2.querySelector(".back").style.transition = "transform 0s";
            } else if (view % 2 === 0 && view !== 2) {
                p1Position += 4;
                p4Position += 4;
                loadPDFPage(fullPDFPath, p2Position, paper2.querySelector('.back-content'));
                loadPDFPage(fullPDFPath, p1Position, paper2.querySelector('.front-content'));
                loadPDFPage(fullPDFPath, p2Position, firstPaper.querySelector('.back-content'));
                loadPDFPage(fullPDFPath, p3Position, paper3.querySelector('.front-content'));
                paper2.classList.add("flipped");
                paper3.classList.remove("flipped");
                paper3.querySelector(".front").style.transition = "transform 0s";
                paper3.querySelector(".back").style.transition = "transform 0s";
                paper2.querySelector(".front").style.transition = "transform 0.8s";
                paper2.querySelector(".back").style.transition = "transform 0.8s";
            }
        } else if (pointOfView === 3) {
            closeBook();
            return;
        }
        view += 1;
        console.log(`view: ${view}, p1: ${p1Position}, p2: ${p2Position}, p3: ${p3Position}, p4: ${p4Position}, numOfPaper: ${numOfPapers}, pointOfView: ${pointOfView}`)
    } else if (numOfPapers <= 4) {
        goNextPageUnderFivePage();
    }
}