import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.158/build/three.module.js";

export class RoDifArm {
    constructor(scene, bus, options = {}) {
        this.bus = bus;
        this.scene = scene;

        const beat = 1;
        const n_beats = 5;
        const tiempo = n_beats * beat;
        const d = 1;
        const R = 2.5;
        const omega = Math.PI / tiempo;
        const vel_lin = omega * R;

        this.sequences = {
            "ymca": [
                { v: 1, w: 0, alpha0: 0, time: 4 },
                { v: 0, w: -Math.PI / 4, alpha0: -Math.PI / 2, alpha1: 0, time: 2 },
                { v: vel_lin, w: omega, time: tiempo },
                {
                    v: 0,
                    w: 0,
                    alpha0: Math.PI / 2,
                    alpha1: (6 * Math.PI) / 16,
                    alpha2: -(6 * Math.PI) / 16,
                    time: 2,
                },
                { v: -vel_lin, w: omega, time: tiempo },
                /////////////////////////////////////////////////////////
                { v: 1, w: 0, alpha0: 0, time: 2 },
                {
                    v: 0,
                    w: -Math.PI / 4,
                    alpha0: Math.PI / 2,
                    alpha1: (6 * Math.PI) / 16,
                    alpha2: -(6 * Math.PI) / 16,
                    time: 2,
                },
                { v: -vel_lin, w: omega, time: tiempo },
                { v: 0, w: 0, alpha0: -Math.PI / 2, alpha1: 0, alpha2: 0, time: 2 },
                { v: vel_lin, w: omega, time: tiempo },
            ]
        };
        this.sequence = []// this.sequences["ymca"].map(step => ({...step}));

        this.state = {
            x: options.x ?? 0,
            y: options.y ?? 0,
            beta: options.beta ?? 0,
            alpha0: options.alpha0 ?? 0,
            alpha1: options.alpha1 ?? 0,
            alpha2: options.alpha2 ?? 0,
        };

        this.group = new THREE.Group();
        scene.add(this.group);
        scene.addAnimation(this);

        this._build();

        this.currentStep = null;
        this.timeLeft = 0;
        this.initialAngles = {};
        this.attachSubscriptions()
    }

    /* ============================================================
        NUEVO: Se llama desde el HTML cuando ya existe bus.prefix
       ============================================================ */
    attachSubscriptions() {
        // Estado del robot
        this.bus.sub_pre("RPi/state", (topic,msg) => {
            console.log('msg',msg)
            // this.state.beta = msg.w;
            // this.state.v += msg.v;
            // this.state.alpha0 = msg.alfa0;
            // this.state.alpha1 = msg.alfa1;
            // this.state.alpha2 = msg.alfa2;
        });

        // Secuencias
        this.bus.sub_pre("RPi/sequence", (topic,msg) => {
            if (msg.action === "create") {
                console.log('create')
                this.sequences[msg.sequence.name] = msg.sequence.states;
            }

            if (msg.action === "execute_now") {
                if (!msg.name) return;
                this.runSequence(msg.name);
            }
        });

        console.log("RoDifArm: suscripciones activadas para", this.bus.prefix);
    }


    _build() {
        const base = new THREE.Mesh(
            new THREE.BoxGeometry(2, 0.5, 2),
            new THREE.MeshBasicMaterial({ color: 0x0077ff })
        );
        base.position.y = 0.3;
        this.group.add(base);
        this.base = base;

        const wheelGeometry = new THREE.CylinderGeometry(0.4, 0.4, 0.5, 32);
        const wheelMaterial = new THREE.MeshBasicMaterial({ color: 0x222222 });

        const wheelOffsets = [
            [0.7, 0.4, 1.2],
            [0.7, 0.4, -1.2],
            [-0.7, 0.4, 1.2],
            [-0.7, 0.4, -1.2],
        ];

        wheelOffsets.forEach(([x, y, z]) => {
            const wheel = new THREE.Mesh(wheelGeometry, wheelMaterial);
            wheel.rotation.x = Math.PI / 2;
            wheel.position.set(x, y, z);
            this.group.add(wheel);
        });

        const color_brazo = 0x00fff0;
        const a1 = 0.5;
        const a2 = 1;
        const a3 = 1;

        let geometry = new THREE.BoxGeometry(0.5, a1, 0.5);
        let material = new THREE.MeshBasicMaterial({ color: color_brazo });
        const armBase = new THREE.Mesh(geometry, material);
        armBase.translateY(a1 / 2);
        armBase.translateX(0.6);
        base.add(armBase);
        this.armBase = armBase;

        let shoulder = new THREE.Object3D();
        shoulder.translateY(a1 / 2);
        armBase.add(shoulder);
        this.shoulder = shoulder;

        geometry = new THREE.BoxGeometry(a2, 0.2, 0.2);
        let lowerArm = new THREE.Mesh(geometry, material);
        lowerArm.translateX(a2 / 2);
        shoulder.add(lowerArm);

        let elbow = new THREE.Object3D();
        elbow.translateX(a2 / 2);
        lowerArm.add(elbow);
        this.elbow = elbow;

        geometry = new THREE.BoxGeometry(a3, 0.1, 0.1);
        let arm = new THREE.Mesh(geometry, material);
        arm.translateX(a3 / 2);
        elbow.add(arm);

        let wrist = new THREE.Object3D();
        wrist.translateX(a3 / 2);
        arm.add(wrist);

        geometry = new THREE.TorusGeometry(0.1, 0.01, 3, 9, 5.6);
        let hand = new THREE.Mesh(geometry, material);
        hand.rotation.y = Math.PI / 2;
        hand.rotation.x = Math.PI / 2;
        wrist.add(hand);
    }

    addSequence(name, sequence) {
        //console.log('addSequence')
        this.sequences[name] = sequence.map(step => ({...step}));
        this.runSequence(name);
    }

    runSequence(name) {
        //console.log('run-')
        this.currentStep = null;
        this.timeLeft = 0;
        this.sequence = this.sequences[name].map(step => ({...step}));
        //console.log('run-',this.sequence.length)
    }

    _startNextStep() {
        if (this.sequence.length === 0) {
            this.currentStep = null;
            return;
        }
        //console.log("_startNextStep 0",this.sequence.length,this.sequences['ymca'].length)
        this.currentStep = this.sequence.shift();
        //console.log("_startNextStep 1",this.sequence.length,this.sequences['ymca'].length)
        this.timeLeft = this.currentStep.time;

        this.initialAngles = {
            alpha0: this.state.alpha0,
            alpha1: this.state.alpha1,
            alpha2: this.state.alpha2,
        };
    }

    update(deltaTime) {
        //console.log("update",this.sequence.length,this.sequences['ymca'].length)
        if (!this.currentStep) {
            this._startNextStep();
            if (!this.currentStep) {
                this._render();
                return;
            }
        }

        const t = 1 - this.timeLeft / this.currentStep.time;

        this.state.x += this.currentStep.v * Math.cos(this.state.beta) * deltaTime;
        this.state.y -= this.currentStep.v * Math.sin(this.state.beta) * deltaTime;
        this.state.beta += (this.currentStep.w ?? 0) * deltaTime;

        ["alpha0", "alpha1", "alpha2"].forEach((key) => {
            if (this.currentStep[key] !== undefined) {
                const start = this.initialAngles[key];
                const end = this.currentStep[key];
                this.state[key] = start + (end - start) * t;
            }
        });

        this.timeLeft -= deltaTime;
        if (this.timeLeft <= 0) {
            this._startNextStep();
        }

        this._render();
    }

    _render() {
        this.group.position.set(this.state.x, 0, this.state.y);
        this.group.rotation.y = this.state.beta;

        this.armBase.rotation.y = this.state.alpha0;
        this.shoulder.rotation.z = this.state.alpha1;
        this.elbow.rotation.z = this.state.alpha2 - this.state.alpha1;
    }
}
