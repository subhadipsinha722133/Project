

// Mobile Menu Toggle
const menuToggle = document.querySelector('.menu-toggle');
const navLinks = document.querySelector('.nav-links');

menuToggle.addEventListener('click', () => {
    navLinks.classList.toggle('active');
    menuToggle.innerHTML = navLinks.classList.contains('active') ? 
        '<i class="fas fa-times"></i>' : '<i class="fas fa-bars"></i>';
});






// Navbar Scroll Effect - Combined
const navbar = document.getElementById('navbar');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    const maxScroll = 500; // Adjust based on your page length
    
    if (currentScroll <= 0) {
        navbar.style.opacity = '1';
        navbar.style.transform = 'scale(1)';
        navbar.style.backdropFilter = 'blur(0px)';
        navbar.style.backgroundColor = 'rgba(15, 15, 20, 0.9)';
        navbar.classList.remove('scrolled');
        return;
    }
    
    const scrollPercent = Math.min(1, currentScroll / maxScroll);
    
    // Combined effects
    if (currentScroll > lastScroll) {
        // Scrolling down
        const opacity = 1 - (scrollPercent * 0.7); // Keep at least 30% opacity
        const scale = 1 - (scrollPercent * 0.1); // Scale down to 90%
        const blur = Math.min(8, scrollPercent * 15); // Max 8px blur
        
        navbar.style.opacity = opacity.toString();
        navbar.style.transform = `scale(${scale})`;
        navbar.style.backdropFilter = `blur(${blur}px)`;
    } else {
        // Scrolling up
        navbar.style.opacity = '1';
        navbar.style.transform = 'scale(1)';
        navbar.style.backdropFilter = 'blur(0px)';
    }
    
    // Color change
    const r = Math.floor(15 + (100 - 15) * scrollPercent);
    const g = Math.floor(15 + (100 - 15) * scrollPercent);
    const b = Math.floor(20 + (250 - 20) * scrollPercent);
    navbar.style.backgroundColor = `rgba(${r}, ${g}, ${b}, 0.9)`;
    
    if (currentScroll > 100) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
    
    lastScroll = currentScroll;
});




// 3D cube animation

// Create cursor trail elements



// Enhanced Typing Effect
const text = ["AIML Engineer...", "Web Developer...", "Creative Coder...", "Video Editor..."];
let i = 0, j = 0, currentText = "", isDeleting = false;
let typingPaused = false;

function typeEffect() {
    if (typingPaused) return;
    
    const typingElement = document.getElementById("typing");
    const currentString = text[i];
    
    // Dynamic typing speed based on character position
    const baseTypeSpeed = 100;
    const baseDeleteSpeed = 30;
    const typeSpeed = isDeleting ? 
        baseDeleteSpeed + Math.random() * 50 : 
        baseTypeSpeed - (j / currentString.length * 50);
    
    const pauseBetween = 1500;
    
    currentText = currentString.substring(0, j);
    typingElement.innerHTML = currentText + '<span class="typing-cursor"></span>';
    
    if (!isDeleting && j < currentString.length) {
        j++;
        setTimeout(typeEffect, typeSpeed);
    } 
    else if (!isDeleting && j === currentString.length) {
        isDeleting = true;
        setTimeout(typeEffect, pauseBetween);
    } 
    else if (isDeleting && j > 0) {
        j--;
        setTimeout(typeEffect, typeSpeed);
    } 
    else {
        isDeleting = false;
        i = (i + 1) % text.length;
        setTimeout(typeEffect, 500);
    }
}

// Pause typing animation when tab is not active
document.addEventListener('visibilitychange', function() {
    typingPaused = document.hidden;
    if (!typingPaused && !isDeleting) {
        typeEffect();
    }
});

// Three.js 3D Animation
const container = document.getElementById('canvas-container');

// Scene setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ 
    alpha: true, 
    antialias: true,
    powerPreference: "high-performance"
});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
container.appendChild(renderer.domElement);

// Particles with improved distribution
const particlesGeometry = new THREE.BufferGeometry();
const particleCount = 2000;

const posArray = new Float32Array(particleCount * 3);
const colorArray = new Float32Array(particleCount * 3);
const sizeArray = new Float32Array(particleCount);

for(let i = 0; i < particleCount * 3; i++) {
    // More organized particle distribution
    posArray[i] = (Math.random() - 0.5) * (10 + Math.random() * 5);
    
    // Add some color variation
    colorArray[i] = 0.5 + Math.random() * 0.5;
    
    // Random sizes
    if (i % 3 === 0) {
        sizeArray[i/3] = Math.random() * 0.05 + 0.01;
    }
}

particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
particlesGeometry.setAttribute('color', new THREE.BufferAttribute(colorArray, 3));
particlesGeometry.setAttribute('size', new THREE.BufferAttribute(sizeArray, 1));

const particlesMaterial = new THREE.PointsMaterial({
    size: 0.03,
    vertexColors: true,
    transparent: true,
    opacity: 0.8,
    blending: THREE.AdditiveBlending,
    sizeAttenuation: true
});

const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
scene.add(particlesMesh);

// Torus Knot with improved materials
const geometry = new THREE.TorusKnotGeometry(0.8, 0.3, 200, 32);
const material = new THREE.MeshStandardMaterial({ 
    color: 0x6c5ce7,
    wireframe: true,
    transparent: true,
    opacity: 0.8,
    emissive: 0x6c5ce7,
    emissiveIntensity: 0.3,
    metalness: 0.8,
    roughness: 0.2
});

const torusKnot = new THREE.Mesh(geometry, material);
scene.add(torusKnot);

// Add subtle lighting
const ambientLight = new THREE.AmbientLight(0x404040, 0.5);
scene.add(ambientLight);

const pointLight = new THREE.PointLight(0x5ce2e7, 0.8);
pointLight.position.set(5, 5, 5);
scene.add(pointLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
directionalLight.position.set(0, 1, 0);
scene.add(directionalLight);

camera.position.z = 3;

// Handle window resize
function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    
    const particleSize = Math.min(0.03, 0.015 + (window.innerWidth * 0.000015));
    particlesMaterial.size = particleSize;
}

window.addEventListener('resize', onWindowResize, false);

// Animation loop with smoother transitions
let time = 0;
function animate() {
    requestAnimationFrame(animate);
    
    time += 0.005;
    
    torusKnot.rotation.x = Math.sin(time * 0.5) * 0.2;
    torusKnot.rotation.y += 0.005;
    torusKnot.rotation.z = Math.cos(time * 0.3) * 0.1;
    torusKnot.position.y = Math.sin(time * 0.7) * 0.1;
    
    particlesMesh.rotation.y += 0.001;
    particlesMesh.rotation.x = Math.sin(time * 0.2) * 0.1;
    
    // Pulsing effect for the torus knot
    const scale = 1 + Math.sin(time * 2) * 0.05;
    torusKnot.scale.set(scale, scale, scale);
    
    renderer.render(scene, camera);
}

// Back to Top Button
const backToTopBtn = document.getElementById('backToTop');

window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        backToTopBtn.classList.add('active');
    } else {
        backToTopBtn.classList.remove('active');
    }
});

backToTopBtn.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// Intersection Observer for scroll animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.about-img, .about-text, .project-card, .book-card, .video-card, .contact-info, .contact-form').forEach(el => {
    observer.observe(el);
});

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    typeEffect();
    onWindowResize();
    animate();
    
    // Add hover effect to project cards
    document.querySelectorAll('.project-card').forEach(card => {
        VanillaTilt.init(card, {
            max: 5,
            speed: 300,
            glare: true,
            'max-glare': 0.1,
            scale: 1.02
        });
    });
    
    // Add hover effect to book cards
    document.querySelectorAll('.book-card').forEach(card => {
        VanillaTilt.init(card, {
            max: 5,
            speed: 300,
            glare: true,
            'max-glare': 0.1,
            scale: 1.02
        });
    });
    
    // Add hover effect to video cards
    document.querySelectorAll('.video-card').forEach(card => {
        VanillaTilt.init(card, {
            max: 5,
            speed: 300,
            glare: true,
            'max-glare': 0.1,
            scale: 1.02
        });
    });
});





// certificate 

document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.certificate-card');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    cards.forEach(card => observer.observe(card));
});









