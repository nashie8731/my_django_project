document.addEventListener('DOMContentLoaded', function () {
    const menuLinks = document.querySelectorAll('.result_count a');
    const backToTopButton = document.querySelector('.back-to-top');

    menuLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            const targetId = this.dataset.target;
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                scrollToElement(targetElement); // スクロール処理を関数化
            }
        });
    });

    backToTopButton.addEventListener('click', function () {
        scrollToElement(document.documentElement); // 最上部へスクロール
    });

    // スムーズスクロール関数 (共通化)
    function scrollToElement(targetElement) {
        const startPosition = window.pageYOffset;
        const targetPosition = targetElement.offsetTop;
        const distance = targetPosition - startPosition;
        const duration = 500;
        let start = null;

        function step(timestamp) {
            if (!start) start = timestamp;
            const progress = timestamp - start;
            window.scrollTo(0, easeInOutCubic(progress, startPosition, distance, duration));
            if (progress < duration) {
                window.requestAnimationFrame(step);
            }
        }

        function easeInOutCubic(t, b, c, d) {
            t /= d / 2;
            if (t < 1) return c / 2 * t * t * t + b;
            t -= 2;
            return c / 2 * (t * t * t + 2) + b;
        };

        window.requestAnimationFrame(step);
    }

    // 「TOPへ戻る」ボタンを表示/非表示
    window.addEventListener('scroll', function () {
        if (window.pageYOffset > 200) { // スクロール量
            backToTopButton.classList.add('show');
        } else {
            backToTopButton.classList.remove('show');
        }
    });
});