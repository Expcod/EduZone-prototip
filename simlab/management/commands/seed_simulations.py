from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import Subject, Grade, Experiment
from simlab.models import SimulationType, Simulation, SimulationAsset
import random
import os
import json

class Command(BaseCommand):
    help = 'Seeds the database with initial simulation data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding simulation data...')
        
        # Create simulation types
        simulation_types_data = [
            {
                'name': 'Canvas 2D',
                'slug': 'canvas-2d',
                'icon': 'easel',
                'description': '2D simulations using HTML5 Canvas and JavaScript'
            },
            {
                'name': 'WebGL',
                'slug': 'webgl',
                'icon': 'gpu-card',
                'description': '3D simulations using WebGL and JavaScript'
            },
            {
                'name': 'Three.js',
                'slug': 'threejs',
                'icon': 'box',
                'description': '3D simulations using Three.js framework'
            },
            {
                'name': 'VPython',
                'slug': 'vpython',
                'icon': 'code-slash',
                'description': 'Python-based simulations using VPython'
            }
        ]
        
        sim_types = []
        for type_data in simulation_types_data:
            sim_type, created = SimulationType.objects.get_or_create(
                slug=type_data['slug'],
                defaults={
                    'name': type_data['name'],
                    'icon': type_data['icon'],
                    'description': type_data['description']
                }
            )
            sim_types.append(sim_type)
            if created:
                self.stdout.write(f'Created simulation type: {sim_type.name}')
        
        # Get subjects and experiments
        subjects = Subject.objects.all()
        if not subjects.exists():
            self.stdout.write('No subjects found. Please run seed_data command first.')
            return
        
        # Create simulations for each subject
        simulation_count = 0
        
        # Kimyo (Chemistry) simulations
        kimyo = subjects.filter(name='Kimyo').first()
        if kimyo:
            experiments = Experiment.objects.filter(subject=kimyo, grade__number=8)[:2]  # Get first 2 experiments for 8th grade
            for experiment in experiments:
                title = f"Virtual {experiment.title}"
                slug = slugify(title)
                
                # Choose simulation type based on experiment
                sim_type = random.choice(sim_types)
                code_js = "// Basic simulation code will be added here"
                code_python = "# Python simulation code will be added here"
                
                simulation, created = Simulation.objects.get_or_create(
                    slug=slug,
                    defaults={
                        'title': title,
                        'experiment': experiment,
                        'simulation_type': sim_type,
                        'description': f"Virtual simulation for {experiment.title}",
                        'instructions': "1. Read the theory\n2. Set up the parameters\n3. Run the simulation\n4. Observe the results\n5. Answer the questions",
                        'code_js': code_js,
                        'code_python': code_python,
                        'config': self._get_default_config(),
                        'is_active': True
                    }
                )
                if created:
                    simulation_count += 1
                    self.stdout.write(f'Created simulation: {simulation.title}')
        
        # Fizika (Physics) simulations
        fizika = subjects.filter(name='Fizika').first()
        if fizika:
            experiments = Experiment.objects.filter(subject=fizika, grade__number=8)[:2]  # Get first 2 experiments for 8th grade
            for experiment in experiments:
                title = f"Virtual {experiment.title}"
                slug = slugify(title)
                
                # Choose simulation type based on experiment
                sim_type = random.choice(sim_types)
                code_js = "// Basic simulation code will be added here"
                code_python = "# Python simulation code will be added here"
                
                simulation, created = Simulation.objects.get_or_create(
                    slug=slug,
                    defaults={
                        'title': title,
                        'experiment': experiment,
                        'simulation_type': sim_type,
                        'description': f"Virtual simulation for {experiment.title}",
                        'instructions': "1. Read the theory\n2. Set up the parameters\n3. Run the simulation\n4. Observe the results\n5. Answer the questions",
                        'code_js': code_js,
                        'code_python': code_python,
                        'config': self._get_default_config(),
                        'is_active': True
                    }
                )
                if created:
                    simulation_count += 1
                    self.stdout.write(f'Created simulation: {simulation.title}')
        
        self.stdout.write(f'Created {simulation_count} simulations')
        self.stdout.write('Successfully seeded simulation data')
    
    def _get_default_config(self):
        """Return default configuration for simulations"""
        return {
            "parameters": {
                "speed": 1.0,
                "gravity": 9.8,
                "temperature": 25,
                "showLabels": True,
                "showAxes": True
            },
            "ui": {
                "controls": ["play", "pause", "reset", "speed"],
                "panels": ["parameters", "results", "graph"]
            }
        }
    
    def _get_acid_base_simulation_js(self):
        """Return JavaScript code for acid-base simulation"""
        return """
// Acid-Base Reaction Simulation
const canvas = document.getElementById('simulation-canvas');
const ctx = canvas.getContext('2d');

// Configuration
let config = {
    width: canvas.width,
    height: canvas.height,
    acidColor: '#ff6666',
    baseColor: '#6666ff',
    neutralColor: '#66ff66',
    particleRadius: 8,
    particleSpeed: 2,
    acidConcentration: 0.5,
    baseConcentration: 0.5
};

// Particles
let particles = [];
let reactionProducts = [];

// Initialize simulation
function initSimulation() {
    particles = [];
    reactionProducts = [];
    
    // Create acid particles
    const acidCount = Math.floor(50 * config.acidConcentration);
    for (let i = 0; i < acidCount; i++) {
        particles.push({
            x: Math.random() * (config.width / 2 - 50) + 25,
            y: Math.random() * (config.height - 50) + 25,
            vx: (Math.random() - 0.5) * config.particleSpeed,
            vy: (Math.random() - 0.5) * config.particleSpeed,
            type: 'acid',
            color: config.acidColor,
            radius: config.particleRadius
        });
    }
    
    // Create base particles
    const baseCount = Math.floor(50 * config.baseConcentration);
    for (let i = 0; i < baseCount; i++) {
        particles.push({
            x: Math.random() * (config.width / 2 - 50) + config.width / 2 + 25,
            y: Math.random() * (config.height - 50) + 25,
            vx: (Math.random() - 0.5) * config.particleSpeed,
            vy: (Math.random() - 0.5) * config.particleSpeed,
            type: 'base',
            color: config.baseColor,
            radius: config.particleRadius
        });
    }
}

// Update simulation
function updateSimulation() {
    // Move particles
    for (let i = 0; i < particles.length; i++) {
        const p = particles[i];
        
        // Update position
        p.x += p.vx;
        p.y += p.vy;
        
        // Bounce off walls
        if (p.x < p.radius || p.x > config.width - p.radius) {
            p.vx = -p.vx;
            p.x = p.x < p.radius ? p.radius : config.width - p.radius;
        }
        if (p.y < p.radius || p.y > config.height - p.radius) {
            p.vy = -p.vy;
            p.y = p.y < p.radius ? p.radius : config.height - p.radius;
        }
    }
    
    // Check for collisions and reactions
    for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
            const p1 = particles[i];
            const p2 = particles[j];
            
            // Calculate distance
            const dx = p2.x - p1.x;
            const dy = p2.y - p1.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            // Check for collision
            if (distance < p1.radius + p2.radius) {
                // Handle collision
                const angle = Math.atan2(dy, dx);
                const sin = Math.sin(angle);
                const cos = Math.cos(angle);
                
                // Rotate velocities
                const vx1 = p1.vx * cos + p1.vy * sin;
                const vy1 = p1.vy * cos - p1.vx * sin;
                const vx2 = p2.vx * cos + p2.vy * sin;
                const vy2 = p2.vy * cos - p2.vx * sin;
                
                // Update velocities
                p1.vx = vx2 * cos - vy1 * sin;
                p1.vy = vy1 * cos + vx2 * sin;
                p2.vx = vx1 * cos - vy2 * sin;
                p2.vy = vy2 * cos + vx1 * sin;
                
                // Check for acid-base reaction
                if ((p1.type === 'acid' && p2.type === 'base') || 
                    (p1.type === 'base' && p2.type === 'acid')) {
                    // Create reaction product
                    reactionProducts.push({
                        x: (p1.x + p2.x) / 2,
                        y: (p1.y + p2.y) / 2,
                        radius: config.particleRadius,
                        color: config.neutralColor,
                        age: 0
                    });
                    
                    // Remove reacted particles
                    particles.splice(j, 1);
                    particles.splice(i, 1);
                    i--; // Adjust index
                    break;
                }
            }
        }
    }
    
    // Update reaction products
    for (let i = 0; i < reactionProducts.length; i++) {
        reactionProducts[i].age++;
    }
}

// Draw simulation
function drawSimulation() {
    // Clear canvas
    ctx.clearRect(0, 0, config.width, config.height);
    
    // Draw background
    ctx.fillStyle = '#f0f0f0';
    ctx.fillRect(0, 0, config.width, config.height);
    
    // Draw divider
    ctx.strokeStyle = '#cccccc';
    ctx.beginPath();
    ctx.moveTo(config.width / 2, 0);
    ctx.lineTo(config.width / 2, config.height);
    ctx.stroke();
    
    // Draw labels
    ctx.font = '16px Arial';
    ctx.fillStyle = '#000000';
    ctx.textAlign = 'center';
    ctx.fillText('Acid', config.width / 4, 30);
    ctx.fillText('Base', 3 * config.width / 4, 30);
    
    // Draw particles
    for (let i = 0; i < particles.length; i++) {
        const p = particles[i];
        ctx.fillStyle = p.color;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fill();
    }
    
    // Draw reaction products
    for (let i = 0; i < reactionProducts.length; i++) {
        const rp = reactionProducts[i];
        ctx.fillStyle = rp.color;
        ctx.beginPath();
        ctx.arc(rp.x, rp.y, rp.radius, 0, Math.PI * 2);
        ctx.fill();
    }
    
    // Draw pH indicator
    const acidCount = particles.filter(p => p.type === 'acid').length;
    const baseCount = particles.filter(p => p.type === 'base').length;
    let pH = 7;
    
    if (acidCount > baseCount) {
        pH = 7 - Math.min(7, Math.log10(acidCount / Math.max(1, baseCount)));
    } else if (baseCount > acidCount) {
        pH = 7 + Math.min(7, Math.log10(baseCount / Math.max(1, acidCount)));
    }
    
    // Draw pH scale
    const pHWidth = 200;
    const pHHeight = 30;
    const pHX = (config.width - pHWidth) / 2;
    const pHY = config.height - 50;
    
    // Draw pH background
    const gradient = ctx.createLinearGradient(pHX, pHY, pHX + pHWidth, pHY);
    gradient.addColorStop(0, '#ff0000');   // Red (acidic)
    gradient.addColorStop(0.5, '#00ff00'); // Green (neutral)
    gradient.addColorStop(1, '#0000ff');   // Blue (basic)
    
    ctx.fillStyle = gradient;
    ctx.fillRect(pHX, pHY, pHWidth, pHHeight);
    
    // Draw pH marker
    const markerX = pHX + (pH / 14) * pHWidth;
    ctx.fillStyle = '#000000';
    ctx.beginPath();
    ctx.moveTo(markerX, pHY - 5);
    ctx.lineTo(markerX - 5, pHY - 15);
    ctx.lineTo(markerX + 5, pHY - 15);
    ctx.closePath();
    ctx.fill();
    
    // Draw pH value
    ctx.fillStyle = '#000000';
    ctx.fillText(`pH: ${pH.toFixed(1)}`, config.width / 2, pHY - 20);
}

// Animation loop
let animationId;
function animate() {
    updateSimulation();
    drawSimulation();
    animationId = requestAnimationFrame(animate);
}

// Start simulation
function startSimulation() {
    if (animationId) {
        cancelAnimationFrame(animationId);
    }
    initSimulation();
    animate();
}

// Update parameters
function updateParameters(params) {
    config = { ...config, ...params };
    startSimulation();
}

// Initialize on load
window.addEventListener('load', startSimulation);

// Export functions for UI controls
window.simulationAPI = {
    start: startSimulation,
    stop: () => cancelAnimationFrame(animationId),
    updateParameters: updateParameters
};
"""
    
    def _get_electric_circuit_simulation_js(self):
        """Return JavaScript code for electric circuit simulation"""
        return """
// Electric Circuit Simulation
const canvas = document.getElementById('simulation-canvas');
const ctx = canvas.getContext('2d');

// Configuration
let config = {
    width: canvas.width,
    height: canvas.height,
    wireColor: '#333333',
    batteryColor: '#ff0000',
    resistorColor: '#8866cc',
    bulbColor: '#ffcc00',
    bulbGlowColor: '#ffffaa',
    electronColor: '#00aaff',
    electronRadius: 3,
    electronSpeed: 2,
    voltage: 9,
    resistance: 10
};

// Circuit components
let components = [];
let electrons = [];
let circuitPath = [];

// Initialize simulation
function initSimulation() {
    components = [];
    electrons = [];
    
    // Create circuit path (points that define the circuit)
    const margin = 50;
    const width = config.width - 2 * margin;
    const height = config.height - 2 * margin;
    
    circuitPath = [
        { x: margin, y: margin + height / 2 },                  // Left middle
        { x: margin + width / 4, y: margin + height / 2 },      // Left-center
        { x: margin + width / 4, y: margin },                   // Top left
        { x: margin + 3 * width / 4, y: margin },               // Top right
        { x: margin + 3 * width / 4, y: margin + height / 2 },  // Right-center
        { x: margin + width, y: margin + height / 2 },          // Right middle
        { x: margin + width, y: margin + height },              // Bottom right
        { x: margin, y: margin + height },                      // Bottom left
        { x: margin, y: margin + height / 2 }                   // Back to start
    ];
    
    // Create components
    components = [
        {
            type: 'battery',
            position: { x: margin + width / 8, y: margin + height / 2 },
            rotation: 0,
            voltage: config.voltage
        },
        {
            type: 'resistor',
            position: { x: margin + width / 2, y: margin },
            rotation: 0,
            resistance: config.resistance
        },
        {
            type: 'bulb',
            position: { x: margin + width, y: margin + 3 * height / 4 },
            rotation: Math.PI / 2,
            brightness: 0
        }
    ];
    
    // Create electrons
    const electronCount = Math.floor(config.voltage * 5);
    const pathLength = calculatePathLength(circuitPath);
    const spacing = pathLength / electronCount;
    
    for (let i = 0; i < electronCount; i++) {
        const position = getPositionOnPath(circuitPath, i * spacing);
        electrons.push({
            position: position,
            distance: i * spacing,
            speed: config.electronSpeed / (config.resistance / 10)
        });
    }
}

// Calculate total path length
function calculatePathLength(path) {
    let length = 0;
    for (let i = 1; i < path.length; i++) {
        const dx = path[i].x - path[i-1].x;
        const dy = path[i].y - path[i-1].y;
        length += Math.sqrt(dx * dx + dy * dy);
    }
    return length;
}

// Get position on path at a given distance
function getPositionOnPath(path, distance) {
    let currentDistance = 0;
    
    for (let i = 1; i < path.length; i++) {
        const p1 = path[i-1];
        const p2 = path[i];
        const dx = p2.x - p1.x;
        const dy = p2.y - p1.y;
        const segmentLength = Math.sqrt(dx * dx + dy * dy);
        
        if (currentDistance + segmentLength >= distance) {
            // Position is on this segment
            const t = (distance - currentDistance) / segmentLength;
            return {
                x: p1.x + t * dx,
                y: p1.y + t * dy
            };
        }
        
        currentDistance += segmentLength;
    }
    
    // If we get here, return the last point
    return { ...path[path.length - 1] };
}

// Update simulation
function updateSimulation() {
    // Calculate current based on voltage and resistance
    const current = config.voltage / Math.max(1, config.resistance);
    
    // Update electron positions
    const pathLength = calculatePathLength(circuitPath);
    
    for (let i = 0; i < electrons.length; i++) {
        const electron = electrons[i];
        
        // Update distance along path
        electron.distance += electron.speed * current;
        
        // Wrap around if needed
        if (electron.distance > pathLength) {
            electron.distance -= pathLength;
        }
        
        // Update position
        electron.position = getPositionOnPath(circuitPath, electron.distance);
    }
    
    // Update bulb brightness
    const bulb = components.find(c => c.type === 'bulb');
    if (bulb) {
        bulb.brightness = Math.min(1, current);
    }
}

// Draw simulation
function drawSimulation() {
    // Clear canvas
    ctx.clearRect(0, 0, config.width, config.height);
    
    // Draw background
    ctx.fillStyle = '#f0f0f0';
    ctx.fillRect(0, 0, config.width, config.height);
    
    // Draw circuit path
    ctx.strokeStyle = config.wireColor;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(circuitPath[0].x, circuitPath[0].y);
    
    for (let i = 1; i < circuitPath.length; i++) {
        ctx.lineTo(circuitPath[i].x, circuitPath[i].y);
    }
    
    ctx.stroke();
    
    // Draw components
    for (let i = 0; i < components.length; i++) {
        const component = components[i];
        
        switch (component.type) {
            case 'battery':
                drawBattery(component);
                break;
            case 'resistor':
                drawResistor(component);
                break;
            case 'bulb':
                drawBulb(component);
                break;
        }
    }
    
    // Draw electrons
    ctx.fillStyle = config.electronColor;
    for (let i = 0; i < electrons.length; i++) {
        const electron = electrons[i];
        ctx.beginPath();
        ctx.arc(electron.position.x, electron.position.y, config.electronRadius, 0, Math.PI * 2);
        ctx.fill();
    }
    
    // Draw voltage and current
    const current = config.voltage / Math.max(1, config.resistance);
    
    ctx.font = '16px Arial';
    ctx.fillStyle = '#000000';
    ctx.textAlign = 'left';
    ctx.fillText(`Voltage: ${config.voltage.toFixed(1)} V`, 20, 30);
    ctx.fillText(`Resistance: ${config.resistance.toFixed(1)} Ω`, 20, 55);
    ctx.fillText(`Current: ${current.toFixed(2)} A`, 20, 80);
}

// Draw battery
function drawBattery(battery) {
    const x = battery.position.x;
    const y = battery.position.y;
    
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(battery.rotation);
    
    // Draw battery
    ctx.strokeStyle = config.wireColor;
    ctx.fillStyle = config.batteryColor;
    ctx.lineWidth = 2;
    
    // Negative terminal
    ctx.beginPath();
    ctx.moveTo(-20, -10);
    ctx.lineTo(-20, 10);
    ctx.stroke();
    
    // Battery body
    ctx.fillRect(-15, -15, 30, 30);
    
    // Positive terminal
    ctx.beginPath();
    ctx.moveTo(20, -10);
    ctx.lineTo(20, 10);
    ctx.stroke();
    
    ctx.beginPath();
    ctx.moveTo(15, 0);
    ctx.lineTo(25, 0);
    ctx.stroke();
    
    // Label
    ctx.fillStyle = '#ffffff';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.font = '12px Arial';
    ctx.fillText(`${battery.voltage}V`, 0, 0);
    
    ctx.restore();
}

// Draw resistor
function drawResistor(resistor) {
    const x = resistor.position.x;
    const y = resistor.position.y;
    
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(resistor.rotation);
    
    // Draw resistor
    ctx.strokeStyle = config.wireColor;
    ctx.fillStyle = config.resistorColor;
    ctx.lineWidth = 2;
    
    // Resistor body
    ctx.fillRect(-25, -10, 50, 20);
    
    // Terminals
    ctx.beginPath();
    ctx.moveTo(-35, 0);
    ctx.lineTo(-25, 0);
    ctx.moveTo(25, 0);
    ctx.lineTo(35, 0);
    ctx.stroke();
    
    // Label
    ctx.fillStyle = '#ffffff';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.font = '12px Arial';
    ctx.fillText(`${resistor.resistance}Ω`, 0, 0);
    
    ctx.restore();
}

// Draw bulb
function drawBulb(bulb) {
    const x = bulb.position.x;
    const y = bulb.position.y;
    
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(bulb.rotation);
    
    // Draw bulb glow
    if (bulb.brightness > 0) {
        const glowRadius = 30 + bulb.brightness * 20;
        const gradient = ctx.createRadialGradient(0, 0, 10, 0, 0, glowRadius);
        gradient.addColorStop(0, `rgba(255, 255, 170, ${bulb.brightness})`);
        gradient.addColorStop(1, 'rgba(255, 255, 170, 0)');
        
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(0, 0, glowRadius, 0, Math.PI * 2);
        ctx.fill();
    }
    
    // Draw bulb
    ctx.strokeStyle = config.wireColor;
    ctx.fillStyle = config.bulbColor;
    ctx.lineWidth = 2;
    
    // Bulb base
    ctx.beginPath();
    ctx.moveTo(-10, 15);
    ctx.lineTo(10, 15);
    ctx.lineTo(5, 0);
    ctx.lineTo(-5, 0);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
    
    // Bulb glass
    ctx.beginPath();
    ctx.arc(0, 0, 10, 0, Math.PI, true);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
    
    // Terminals
    ctx.beginPath();
    ctx.moveTo(-5, 15);
    ctx.lineTo(-5, 25);
    ctx.moveTo(5, 15);
    ctx.lineTo(5, 25);
    ctx.stroke();
    
    ctx.restore();
}

// Animation loop
let animationId;
function animate() {
    updateSimulation();
    drawSimulation();
    animationId = requestAnimationFrame(animate);
}

// Start simulation
function startSimulation() {
    if (animationId) {
        cancelAnimationFrame(animationId);
    }
    initSimulation();
    animate();
}

// Update parameters
function updateParameters(params) {
    config = { ...config, ...params };
    
    // Update component properties
    const battery = components.find(c => c.type === 'battery');
    if (battery) {
        battery.voltage = config.voltage;
    }
    
    const resistor = components.find(c => c.type === 'resistor');
    if (resistor) {
        resistor.resistance = config.resistance;
    }
    
    // Update electron speeds
    const current = config.voltage / Math.max(1, config.resistance);
    for (let i = 0; i < electrons.length; i++) {
        electrons[i].speed = config.electronSpeed / (config.resistance / 10);
    }
}

// Initialize on load
window.addEventListener('load', startSimulation);

// Export functions for UI controls
window.simulationAPI = {
    start: startSimulation,
    stop: () => cancelAnimationFrame(animationId),
    updateParameters: updateParameters
};
"""
    
    def _get_molecule_simulation_js(self):
        """Return JavaScript code for molecule simulation using Three.js"""
        return """
// Molecule Visualization using Three.js
let scene, camera, renderer, controls;
let molecules = [];
let bonds = [];
let rotationSpeed = 0.005;
let isRotating = true;

// Initialize the scene
function initScene() {
    // Create scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf0f0f0);
    
    // Create camera
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 15;
    
    // Create renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.getElementById('simulation-container').appendChild(renderer.domElement);
    
    // Add orbit controls
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.damp  renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.25;
    
    // Add lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(1, 1, 1);
    scene.add(directionalLight);
    
    // Add axes helper
    const axesHelper = new THREE.AxesHelper(10);
    scene.add(axesHelper);
    
    // Handle window resize
    window.addEventListener('resize', onWindowResize);
}

// Handle window resize
function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

// Create a molecule
function createMolecule(moleculeData) {
    // Clear existing molecules
    molecules.forEach(atom => scene.remove(atom));
    bonds.forEach(bond => scene.remove(bond));
    molecules = [];
    bonds = [];
    
    // Create atoms
    moleculeData.atoms.forEach(atom => {
        const geometry = new THREE.SphereGeometry(atom.radius, 32, 32);
        const material = new THREE.MeshPhongMaterial({ color: atom.color });
        const sphere = new THREE.Mesh(geometry, material);
        
        sphere.position.set(atom.position.x, atom.position.y, atom.position.z);
        scene.add(sphere);
        molecules.push(sphere);
        
        // Add label if enabled
        if (moleculeData.showLabels) {
            const textGeometry = new THREE.TextGeometry(atom.element, {
                font: new THREE.Font(), // Font would need to be loaded
                size: 0.5,
                height: 0.1
            });
            const textMaterial = new THREE.MeshBasicMaterial({ color: 0x000000 });
            const text = new THREE.Mesh(textGeometry, textMaterial);
            text.position.set(
                atom.position.x + atom.radius + 0.2,
                atom.position.y + atom.radius + 0.2,
                atom.position.z
            );
            scene.add(text);
            molecules.push(text);
        }
    });
    
    // Create bonds
    moleculeData.bonds.forEach(bond => {
        const atom1 = moleculeData.atoms[bond.atom1];
        const atom2 = moleculeData.atoms[bond.atom2];
        
        const direction = new THREE.Vector3(
            atom2.position.x - atom1.position.x,
            atom2.position.y - atom1.position.y,
            atom2.position.z - atom1.position.z
        );
        
        const distance = direction.length();
        direction.normalize();
        
        const bondGeometry = new THREE.CylinderGeometry(0.1, 0.1, distance, 8);
        const bondMaterial = new THREE.MeshPhongMaterial({ color: 0xffffff });
        const bondMesh = new THREE.Mesh(bondGeometry, bondMaterial);
        
        // Position and rotate the bond
        bondMesh.position.copy(atom1.position);
        bondMesh.position.add(direction.multiplyScalar(distance / 2));
        
        // Align the cylinder with the direction vector
        const quaternion = new THREE.Quaternion();
        quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), direction.normalize());
        bondMesh.setRotationFromQuaternion(quaternion);
        
        scene.add(bondMesh);
        bonds.push(bondMesh);
    });
}

// Create water molecule (H2O)
function createWaterMolecule() {
    return {
        showLabels: true,
        atoms: [
            {
                element: 'O',
                radius: 0.8,
                color: 0xff0000,
                position: { x: 0, y: 0, z: 0 }
            },
            {
                element: 'H',
                radius: 0.5,
                color: 0xffffff,
                position: { x: 0.8, y: 0.6, z: 0 }
            },
            {
                element: 'H',
                radius: 0.5,
                color: 0xffffff,
                position: { x: -0.8, y: 0.6, z: 0 }
            }
        ],
        bonds: [
            { atom1: 0, atom2: 1 },
            { atom1: 0, atom2: 2 }
        ]
    };
}

// Create methane molecule (CH4)
function createMethaneMolecule() {
    return {
        showLabels: true,
        atoms: [
            {
                element: 'C',
                radius: 0.8,
                color: 0x808080,
                position: { x: 0, y: 0, z: 0 }
            },
            {
                element: 'H',
                radius: 0.5,
                color: 0xffffff,
                position: { x: 0.8, y: 0.8, z: 0.8 }
            },
            {
                element: 'H',
                radius: 0.5,
                color: 0xffffff,
                position: { x: -0.8, y: 0.8, z: -0.8 }
            },
            {
                element: 'H',
                radius: 0.5,
                color: 0xffffff,
                position: { x: 0.8, y: -0.8, z: -0.8 }
            },
            {
                element: 'H',
                radius: 0.5,
                color: 0xffffff,
                position: { x: -0.8, y: -0.8, z: 0.8 }
            }
        ],
        bonds: [
            { atom1: 0, atom2: 1 },
            { atom1: 0, atom2: 2 },
            { atom1: 0, atom2: 3 },
            { atom1: 0, atom2: 4 }
        ]
    };
}

// Create carbon dioxide molecule (CO2)
function createCarbonDioxideMolecule() {
    return {
        showLabels: true,
        atoms: [
            {
                element: 'C',
                radius: 0.8,
                color: 0x808080,
                position: { x: 0, y: 0, z: 0 }
            },
            {
                element: 'O',
                radius: 0.8,
                color: 0xff0000,
                position: { x: 1.5, y: 0, z: 0 }
            },
            {
                element: 'O',
                radius: 0.8,
                color: 0xff0000,
                position: { x: -1.5, y: 0, z: 0 }
            }
        ],
        bonds: [
            { atom1: 0, atom2: 1 },
            { atom1: 0, atom2: 2 }
        ]
    };
}

// Animation loop
function animate() {
    requestAnimationFrame(animate);
    
    // Rotate the molecule if enabled
    if (isRotating) {
        molecules.forEach(atom => {
            atom.rotation.y += rotationSpeed;
        });
        
        bonds.forEach(bond => {
            bond.rotation.y += rotationSpeed;
        });
    }
    
    controls.update();
    renderer.render(scene, camera);
}

// Initialize the simulation
function initSimulation() {
    initScene();
    createMolecule(createWaterMolecule());
    animate();
}

// Change molecule type
function changeMolecule(type) {
    let moleculeData;
    
    switch (type) {
        case 'water':
            moleculeData = createWaterMolecule();
            break;
        case 'methane':
            moleculeData = createMethaneMolecule();
            break;
        case 'carbon-dioxide':
            moleculeData = createCarbonDioxideMolecule();
            break;
        default:
            moleculeData = createWaterMolecule();
    }
    
    createMolecule(moleculeData);
}

// Toggle rotation
function toggleRotation() {
    isRotating = !isRotating;
}

// Set rotation speed
function setRotationSpeed(speed) {
    rotationSpeed = speed;
}

// Initialize on load
window.addEventListener('load', initSimulation);

// Export functions for UI controls
window.simulationAPI = {
    changeMolecule: changeMolecule,
    toggleRotation: toggleRotation,
    setRotationSpeed: setRotationSpeed
};
"""
    
    def _get_mechanics_simulation_python(self):
        """Return Python code for mechanics simulation using VPython"""
        return """
# Mechanics Simulation using VPython
from vpython import *
import numpy as np

# Configuration
config = {
    'g': 9.8,  # Gravity (m/s^2)
    'dt': 0.01,  # Time step (s)
    'duration': 10,  # Simulation duration (s)
    'trail_length': 100,  # Length of the trail
}

# Create the scene
scene = canvas(title='Projectile Motion Simulation',
               width=800, height=600,
               center=vector(0, 0, 0),
               background=color.white)

# Add a caption
scene.caption = "Projectile Motion Simulation\\nAdjust the initial velocity and angle to see how they affect the trajectory."

# Create the ground
ground = box(pos=vector(0, -0.1, 0),
             size=vector(20, 0.2, 4),
             color=color.green)

# Create axes
x_axis = arrow(pos=vector(0, 0, 0), axis=vector(5, 0, 0), color=color.red, shaftwidth=0.1)
y_axis = arrow(pos=vector(0, 0, 0), axis=vector(0, 5, 0), color=color.green, shaftwidth=0.1)
z_axis = arrow(pos=vector(0, 0, 0), axis=vector(0, 0, 5), color=color.blue, shaftwidth=0.1)

# Create labels for axes
x_label = label(pos=vector(5.5, 0, 0), text='X', color=color.red)
y_label = label(pos=vector(0, 5.5, 0), text='Y', color=color.green)
z_label = label(pos=vector(0, 0, 5.5), text='Z', color=color.blue)

# Create the projectile
projectile = sphere(pos=vector(0, 0, 0),
                    radius=0.2,
                    color=color.blue,
                    make_trail=True,
                    trail_type="points",
                    trail_color=color.blue,
                    trail_radius=0.05,
                    interval=5)

# Create velocity vector
velocity_arrow = arrow(pos=projectile.pos,
                       axis=vector(1, 1, 0),
                       color=color.yellow,
                       shaftwidth=0.1)

# Create UI controls
initial_velocity_slider = slider(min=1, max=20, step=1, value=10,
                                 bind=lambda: update_parameters())
initial_angle_slider = slider(min=0, max=90, step=1, value=45,
                              bind=lambda: update_parameters())

scene.append_to_caption('\\n\\nInitial Velocity (m/s): ')
scene.append_to_caption('\\n')
scene.append_to_caption(initial_velocity_slider)

scene.append_to_caption('\\n\\nInitial Angle (degrees): ')
scene.append_to_caption('\\n')
scene.append_to_caption(initial_angle_slider)

# Add buttons
scene.append_to_caption('\\n\\n')
button(text="Start", bind=lambda: start_simulation())
button(text="Reset", bind=lambda: reset_simulation())

# Variables to store simulation state
running = False
time = 0
position_data = []
velocity_data = []
acceleration_data = []

# Function to update parameters
def update_parameters():
    global initial_velocity, initial_angle, velocity, position
    
    initial_velocity = initial_velocity_slider.value
    initial_angle = initial_angle_slider.value
    
    # Convert angle to radians
    angle_rad = np.radians(initial_angle)
    
    # Set initial velocity components
    velocity = vector(initial_velocity * np.cos(angle_rad),
                      initial_velocity * np.sin(angle_rad),
                      0)
    
    # Update velocity arrow
    velocity_arrow.axis = velocity * 0.2  # Scale for visualization
    
    # Reset position
    position = vector(0, 0, 0)
    projectile.pos = position

# Function to reset the simulation
def reset_simulation():
    global running, time, position_data, velocity_data, acceleration_data
    
    running = False
    time = 0
    position_data = []
    velocity_data = []
    acceleration_data = []
    
    # Clear trail
    projectile.clear_trail()
    
    # Reset projectile position
    update_parameters()

# Function to start the simulation
def start_simulation():
    global running
    running = True
    
    # Start the animation loop
    animate()

# Function to animate the simulation
def animate():
    global running, time, position, velocity
    
    # Set up time step
    dt = config['dt']
    
    # Run the simulation until it's stopped or the projectile hits the ground
    while running and projectile.pos.y >= 0:
        # Set the animation rate
        rate(100)
        
        # Calculate acceleration (only gravity in y-direction)
        acceleration = vector(0, -config['g'], 0)
        
        # Update velocity
        velocity += acceleration * dt
        
        # Update position
        position += velocity * dt
        
        # Update projectile position
        projectile.pos = position
        
        # Update velocity arrow
        velocity_arrow.pos = position
        velocity_arrow.axis = velocity * 0.2  # Scale for visualization
        
        # Store data for analysis
        time += dt
        position_data.append(position)
        velocity_data.append(velocity)
        acceleration_data.append(acceleration)
        
        # Check if projectile hits the ground
        if position.y <= 0:
            running = False
            print("Projectile landed at x =", position.x, "meters")
            print("Total flight time:", time, "seconds")
            
            # Calculate maximum height
            max_height = max([p.y for p in position_data])
            print("Maximum height:", max_height, "meters")
            
            # Calculate range
            print("Range:", position.x, "meters")

# Initialize parameters
update_parameters()

# Display instructions
print("Adjust the sliders to change the initial velocity and angle.")
print("Click 'Start' to run the simulation and 'Reset' to start over.")
"""
