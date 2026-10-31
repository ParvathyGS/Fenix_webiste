/* Animated "count up to final number" effect for stat/counter elements.
   Any element with class "fx-counter" and a data-target="123" attribute
   will count up from 0 to that number once it scrolls into view. */
(function () {
    function easeOutQuad(t) {
        return t * (2 - t);
    }

    function animateCounter(el) {
        var target = parseFloat(el.getAttribute('data-target')) || 0;
        var duration = 1500;
        var start = null;

        function step(timestamp) {
            if (start === null) start = timestamp;
            var progress = Math.min((timestamp - start) / duration, 1);
            var eased = easeOutQuad(progress);
            var current = Math.floor(eased * target);
            el.textContent = current.toLocaleString('en-IN');

            if (progress < 1) {
                window.requestAnimationFrame(step);
            } else {
                el.textContent = target.toLocaleString('en-IN');
            }
        }

        window.requestAnimationFrame(step);
    }

    document.addEventListener('DOMContentLoaded', function () {
        var counters = document.querySelectorAll('.fx-counter');
        if (!counters.length) return;

        if ('IntersectionObserver' in window) {
            var observer = new IntersectionObserver(function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        animateCounter(entry.target);
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.4 });

            counters.forEach(function (el) {
                observer.observe(el);
            });
        } else {
            counters.forEach(animateCounter);
        }
    });
})();
