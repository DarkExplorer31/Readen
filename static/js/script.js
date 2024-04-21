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