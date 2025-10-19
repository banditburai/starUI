/**
 * Constellation scroll-driven animation using Motion.js
 */

document.addEventListener('DOMContentLoaded', () => {
  // Respect prefers-reduced-motion
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Get all constellation components
  const components = document.querySelectorAll('[data-constellation-item]');

  if (prefersReducedMotion) {
    // Skip animations, just show components
    components.forEach(item => {
      item.style.opacity = '1';
      item.style.transform = 'translateY(0)';
    });
    return;
  }

  // Run normal animations if motion is allowed
  const { animate, scroll } = window.Motion;

  components.forEach(component => {
    const triggerPoint = parseFloat(component.dataset.scrollTrigger);
    const targetEl = component;

    // Initial state: hidden and shifted
    targetEl.style.opacity = '0';
    targetEl.style.transform = 'translateY(50px)';

    // Scroll-driven reveal animation
    scroll(
      animate(
        targetEl,
        {
          opacity: [0, 1],
          transform: ['translateY(50px)', 'translateY(0)']
        },
        {
          duration: 0.6,
          easing: 'ease-out'
        }
      ),
      {
        target: document.querySelector('#constellation-section'),
        offset: [`${triggerPoint * 100}%`, `${(triggerPoint * 100) + 10}%`]
      }
    );

    // Continuous float animation after reveal
    setTimeout(() => {
      animate(
        targetEl,
        {
          y: [-10, 10]
        },
        {
          duration: 3,
          repeat: Infinity,
          direction: 'alternate',
          easing: 'ease-in-out'
        }
      );
    }, (triggerPoint * 2000) + 600); // Start after reveal completes

    // Hover interactions
    targetEl.addEventListener('mouseenter', () => {
      animate(
        targetEl,
        { scale: 1.05 },
        { duration: 0.3, easing: 'ease-out' }
      );
      targetEl.classList.add('gradient-glow-intense');
    });

    targetEl.addEventListener('mouseleave', () => {
      animate(
        targetEl,
        { scale: 1 },
        { duration: 0.3, easing: 'ease-out' }
      );
      targetEl.classList.remove('gradient-glow-intense');
    });

    // Function to toggle component isolation
    const toggleIsolation = () => {
      const demoPanel = targetEl.querySelector('[data-demo-panel]');
      const allComponents = document.querySelectorAll('[data-constellation-item]');

      if (targetEl.classList.contains('isolated')) {
        // Return to constellation view
        allComponents.forEach(comp => {
          animate(comp, { opacity: 1, filter: 'blur(0px)' }, { duration: 0.3 });
        });
        animate(targetEl, { scale: 1 }, { duration: 0.3 });
        if (demoPanel) demoPanel.style.display = 'none';
        targetEl.classList.remove('isolated');
        targetEl.setAttribute('aria-expanded', 'false');
      } else {
        // Isolate this component
        allComponents.forEach(comp => {
          if (comp !== targetEl) {
            animate(comp, { opacity: 0.15, filter: 'blur(4px)' }, { duration: 0.3 });
          }
        });
        animate(targetEl, { scale: 1.3 }, { duration: 0.3 });
        if (demoPanel) demoPanel.style.display = 'block';
        targetEl.classList.add('isolated');
        targetEl.setAttribute('aria-expanded', 'true');
      }
    };

    // Click to isolate and demonstrate
    targetEl.addEventListener('click', toggleIsolation);

    // Keyboard support (Enter or Space)
    targetEl.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        toggleIsolation();
      }
    });
  });
});
