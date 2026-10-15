/* ── Wisemonkey background: a drifting particle field ──
   Shared by /projects/wisemonkey/ and its docs page, so both pages animate
   identically.

   Each particle carries a heading and a speed, and wanders by perturbing the
   heading a little every frame. The speed is constant (it only breathes around
   its own base and spikes away from the cursor), so the field is never at rest.

   The previous implementation instead accumulated a velocity and damped it by
   0.999 every frame. That is a decay, not a drift: after a minute of sitting
   still a particle is down to ~2% of its starting speed and visibly frozen, and
   only the mouse repulsion could ever put energy back in. Hence "the particles
   are static when the mouse does not interact".
*/
(() => {
  const canvas = document.getElementById('bg-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  const PARTICLE_COUNT = 500;
  const CONNECTION_DIST = 150;
  const MOUSE_DIST = 100;
  const MAX_SPEED = 1.6;
  const WANDER = 0.12;          // radians of heading change per frame
  const MOUSE_PUSH = 1.5;       // px/frame added by a mouse at point-blank range

  let width = 0;
  let height = 0;
  let particles = [];
  const mouse = { x: -9999, y: -9999 };

  function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  }

  class Particle {
    constructor() {
      this.x = Math.random() * width;
      this.y = Math.random() * height;
      this.angle = Math.random() * Math.PI * 2;
      this.baseSpeed = 0.12 + Math.random() * 0.38;
      this.speed = this.baseSpeed;
      this.radius = Math.random() * 1.5 + 0.5;
      this.alpha = Math.random() * 0.5 + 0.15;
    }

    update() {
      // Random walk: the heading drifts, the pace breathes around its base.
      this.angle += (Math.random() - 0.5) * WANDER;
      this.speed += (this.baseSpeed - this.speed) * 0.02 + (Math.random() - 0.5) * 0.02;

      let vx = Math.cos(this.angle) * this.speed;
      let vy = Math.sin(this.angle) * this.speed;

      // Mouse repulsion: pushed away, and the heading turned outward, so the
      // particle leaves the cursor instead of drifting back through it.
      const dx = this.x - mouse.x;
      const dy = this.y - mouse.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist > 0.001 && dist < MOUSE_DIST) {
        const force = (MOUSE_DIST - dist) / MOUSE_DIST;
        vx += (dx / dist) * force * MOUSE_PUSH;
        vy += (dy / dist) * force * MOUSE_PUSH;
        this.angle = Math.atan2(vy, vx);
        this.speed = Math.min(MAX_SPEED, Math.sqrt(vx * vx + vy * vy));
      }

      this.x += vx;
      this.y += vy;

      // Reflect the heading off the edges, keeping the speed.
      if (this.x < 0) { this.x = 0; this.angle = Math.PI - this.angle; }
      else if (this.x > width) { this.x = width; this.angle = Math.PI - this.angle; }
      if (this.y < 0) { this.y = 0; this.angle = -this.angle; }
      else if (this.y > height) { this.y = height; this.angle = -this.angle; }
    }

    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(96, 250, 138, ${this.alpha})`;
      ctx.fill();
    }
  }

  function init() {
    resize();
    particles = [];
    for (let i = 0; i < PARTICLE_COUNT; i++) particles.push(new Particle());
  }

  function animate() {
    ctx.clearRect(0, 0, width, height);

    for (let i = 0; i < particles.length; i++) {
      const a = particles[i];
      a.update();
      a.draw();

      // Connections
      for (let j = i + 1; j < particles.length; j++) {
        const b = particles[j];
        const dx = a.x - b.x;
        const dy = a.y - b.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < CONNECTION_DIST) {
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.strokeStyle = `rgba(96, 250, 138, ${(1 - dist / CONNECTION_DIST) * 0.08})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }

    requestAnimationFrame(animate);
  }

  window.addEventListener('resize', resize);
  window.addEventListener('mousemove', (e) => { mouse.x = e.clientX; mouse.y = e.clientY; });
  window.addEventListener('mouseleave', () => { mouse.x = -9999; mouse.y = -9999; });

  init();
  animate();
})();
