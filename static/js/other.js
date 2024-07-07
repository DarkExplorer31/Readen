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