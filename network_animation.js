const canvas = document.getElementById('networkCanvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const particles = [];
const numParticles = 100;
let animationActive = false;

// Partikelklasse
class Particle {
    constructor() {
        this.pos = {
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height
        };
        this.vel = {
            x: (Math.random() - 0.5) * 2,
            y: (Math.random() - 0.5) * 2
        };
        this.size = 3;
    }

    update() {
        this.pos.x += this.vel.x;
        this.pos.y += this.vel.y;

        // Kollision mit den Rändern
        if (this.pos.x <= 0 || this.pos.x >= canvas.width) {
            this.vel.x *= -1;
        }
        if (this.pos.y <= 0 || this.pos.y >= canvas.height) {
            this.vel.y *= -1;
        }
    }

    draw() {
        ctx.beginPath();
        ctx.arc(this.pos.x, this.pos.y, this.size, 0, Math.PI * 2);
        ctx.fillStyle = 'white';
        ctx.fill();
    }
}

function initParticles() {
    for (let i = 0; i < numParticles; i++) {
        particles.push(new Particle());
    }
}

function connectParticles() {
    for (let i = 0; i < numParticles; i++) {
        for (let j = i + 1; j < numParticles; j++) {
            const dx = particles[i].pos.x - particles[j].pos.x;
            const dy = particles[i].pos.y - particles[j].pos.y;
            const dist = Math.hypot(dx, dy);
            if (dist < 100) {
                ctx.strokeStyle = `rgba(255, 255, 255, ${1 - dist / 100})`;
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(particles[i].pos.x, particles[i].pos.y);
                ctx.lineTo(particles[j].pos.x, particles[j].pos.y);
                ctx.stroke();
            }
        }
    }
}

function animate() {
    if (!animationActive) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let particle of particles) {
        particle.update();
        particle.draw();
    }
    connectParticles();
    requestAnimationFrame(animate);
}

// Button-Event für das Starten der Animation
document.getElementById('start-btn').addEventListener('click', () => {
    animationActive = true;
    initParticles();
    animate();
    document.getElementById('start-btn').style.display = 'none'; // Button ausblenden
});

// Größe des Canvas bei Fensteränderung anpassen
window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});
