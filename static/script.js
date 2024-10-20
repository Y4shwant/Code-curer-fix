document.addEventListener('DOMContentLoaded', () => {
    const starsContainer = document.querySelector('.stars');

    // Function to generate a random number between min and max
    function getRandom(min, max) {
        return Math.random() * (max - min) + min;
    }

    // Create 50 floating stars
    for (let i = 0; i < 50; i++) {
        const star = document.createElement('div');
        star.classList.add('star');

        // Random position for each star
        star.style.left = `${getRandom(0, 100)}vw`;
        star.style.top = `${getRandom(0, 100)}vh`;

        // Random animation duration and delay
        star.style.animationDuration = `${getRandom(2, 5)}s`;
        star.style.animationDelay = `${getRandom(0, 5)}s`;

        starsContainer.appendChild(star);
    }

    // Create 50 twinkling stars
    for (let i = 0; i < 50; i++) {
        const twinkleStar = document.createElement('div');
        twinkleStar.classList.add('twinkle-star');

        // Random position for each star
        twinkleStar.style.left = `${getRandom(0, 100)}vw`;
        twinkleStar.style.top = `${getRandom(0, 100)}vh`;

        // Random animation duration and delay
        twinkleStar.style.animationDuration = `${getRandom(1, 3)}s`;
        twinkleStar.style.animationDelay = `${getRandom(0, 2)}s`;

        starsContainer.appendChild(twinkleStar);
    }
});