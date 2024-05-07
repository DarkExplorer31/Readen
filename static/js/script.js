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
        } else {
            console.error('Elements not found on read_corner page.');
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
const prevBtn = document.querySelector("#prev-btn");
const nextBtn = document.querySelector("#next-btn");
const book = document.querySelector("#book");

const paper1 = document.querySelector("#p1");
const paper2 = document.querySelector("#p2");
const paper3 = document.querySelector("#p3");

// Event Listener about Book
prevBtn.addEventListener("click", goPrevPage);
nextBtn.addEventListener("click", goNextPage);

let currentLocation = 1;
let numOfPapers = 3;
let maxLocation = numOfPapers + 1;

function openBook() {
    book.style.transform = "translateX(50%)";
    prevBtn.style.transform = "translateX(-180px)";
    nextBtn.style.transform = "translateX(180px)";
}

function closeBook(isAtBeginning) {
    if (isAtBeginning) {
        book.style.transform = "translateX(0%)";
    } else {
        book.style.transform = "translateX(100%)";
    }
    prevBtn.style.transform = "translateX(0px)";
    nextBtn.style.transform = "translateX(0px)";
}

function goNextPage() {
    if (currentLocation < maxLocation) {
        switch (currentLocation) {
            case 1:
                openBook();
                paper1.classList.add("flipped");
                paper1.style.zIndex = 1;
                break;
            case 2:
                paper2.classList.add("flipped");
                paper2.style.zIndex = 2;
                break;
            case 3:
                paper3.classList.add("flipped");
                paper3.style.zIndex = 3;
                closeBook();
                break;
            default:
                throw new Error("unknow state");
        }
        currentLocation++;
    }
}

function goPrevPage() {
    if (currentLocation > 1) {
        switch (currentLocation) {
            case 2:
                closeBook(true);
                paper1.classList.remove("flipped");
                paper1.style.zIndex = 3;
                break;
            case 3:
                paper2.classList.remove("flipped");
                paper2.style.zIndex = 2;
                break;
            case 4:
                openBook();
                paper3.classList.remove("flipped");
                paper3.style.zIndex = 1;
                break;
            default:
                throw new Error("unknow state");
        }
        currentLocation--;
    }
}