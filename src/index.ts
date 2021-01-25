// import * as Babylon from '@babylonjs/core'
import { Color3, StandardMaterial, FollowCamera, ArcRotateCamera, Engine, HemisphericLight, MeshBuilder, Scene, SceneLoader, Vector3, Material, Mesh, CubeTexture, Texture, float, AbstractMesh } from "@babylonjs/core";
import { StandardMaterialDefines } from "babylonjs";

const ALPHA = 0.3;
const BETA = 30;

class Fighter {
    speed: float;
    mesh: AbstractMesh;
    alpha: float;
    beta: float;

    constructor(mesh: AbstractMesh, speed: float) {
        this.mesh = mesh;
        this.speed = speed;
        this.alpha = ALPHA;
        this.beta = BETA;
    }

    pos = () => this.mesh.position;
    speedVec = () => new Vector3(this.speed, this.speed, this.speed);

    distance(other: Fighter) {
        return Vector3.Distance(this.pos(), other.pos());
    }

    advanceTowards(other: Fighter) {
        const normal = other.pos().subtract(this.pos()).normalize();
        this.mesh.rotation = normal;
        // this.mesh.rotation = normal.add(new Vector3(0, 0, 1));
        // this.pos().addInPlace(normal.multiply(this.speedVec()));
        this.pos().addInPlace(normal.multiply(this.speedVec()));

        // ???
        // this.mesh.lookAt(other.pos());
        // this.mesh.movePOV(0, 0, this.speed);
    }

    // TODO: predict where prey will be
}


const canvas: HTMLCanvasElement = document.getElementById("renderCanvas") as HTMLCanvasElement;
const engine = new Engine(canvas, true)


const createDemoScene = function () {
    const scene = new Scene(engine);

    // BABYLON.SceneLoader.ImportMeshAsync("meshbox", "https://assets.babylonjs.com/meshes/", "box.babylon");
    const box = MeshBuilder.CreateBox('box', { size: 3 }, scene);
    const sphere = MeshBuilder.CreateSphere('sphere', { segments: 10, diameter: 3 }, scene);
    const plane = MeshBuilder.CreatePlane('plane', { size: 2 }, scene)
    box.position = new Vector3(-3, -3, -3);
    sphere.position = new Vector3(3, 3, 3);
    plane.position = new Vector3(0, 0, 0);

    const light = new HemisphericLight("light", new Vector3(1, 1, 0), scene);

    // const camera = new BABYLON.FreeCamera('camera', new BABYLON.Vector3(0, 0, -5), scene);
    const camera = new ArcRotateCamera("camera", -Math.PI / 2, Math.PI / 2.5, 15, new Vector3(0, 0, 0), scene);
    camera.attachControl(canvas, true);

    return scene;
};

const createScene = function () {
    const scene = new Scene(engine);

    //! Skybox
    {
        const skybox = Mesh.CreateBox("skyBox", 100.0, scene);
        const skyboxMaterial = new StandardMaterial("skyBox", scene);
        skyboxMaterial.backFaceCulling = false;
        skyboxMaterial.disableLighting = true;
        skybox.material = skyboxMaterial;
        skybox.infiniteDistance = true;
        skyboxMaterial.reflectionTexture = new CubeTexture("textures/skybox", scene);
        skyboxMaterial.reflectionTexture.coordinatesMode = Texture.SKYBOX_MODE;
    }


    let stars: Mesh[] = [];

    for (let i = 0; i < 100; i++) {
        const star = MeshBuilder.CreateSphere('', { segments: 1, diameter: 1 }, scene);
        const starMat = new StandardMaterial('', scene);
        starMat.diffuseColor = new Color3(1, 1, 0);
        star.material = starMat;

        const rand = () => (0.5 - Math.random()) * 100;
        star.position = new Vector3(rand(), rand(), rand());
        stars.push()
    }

    //! Crafts
    const craft1 = MeshBuilder.CreateSphere('craft1', { segments: 1, diameter: 3 }, scene);
    const craft2 = MeshBuilder.CreateSphere('craft2', { segments: 1, diameter: 3 }, scene);
    // const craft1 = MeshBuilder.CreateCylinder('craft1', { diameterTop: 0 }, scene);
    // const craft2 = MeshBuilder.CreateCylinder('craft2', { diameterTop: 0 }, scene);

    craft1.position = new Vector3(50, 0, 0);
    craft2.position = new Vector3(0, 0, 0);


    const mat = new StandardMaterial('mat', scene);
    const mat2 = new StandardMaterial('mat2', scene);
    mat.diffuseColor = new Color3(0, 1, 1);
    mat2.diffuseColor = new Color3(1, 0, 0);
    craft1.material = mat;
    craft2.material = mat2;

    // const ufo = SceneLoader.ImportMeshAsync("ufo", "https://models.babylonjs.com/meshes/", "ufo.glb");
    // SceneLoader.ImportMesh("ufo", "./assets/models/", "skull.babylon", scene);
    // SceneLoader.ImportMesh("ufo2", "./assets/models/", "skull.babylon", scene);
    // const skull = scene.getMeshByName("skull");
    // const skull2 = scene.getMeshByName("skull2");
    // if (skull != null && skull2 != null) {
    //     skull.position = new Vector3(50, 0, 0);
    //     skull2.position = new Vector3(-50, 0, 0);
    // }

    //! Lights and Cameras
    const light = new HemisphericLight("light", new Vector3(1, 1, 0), scene);

    // const camera = new BABYLON.FreeCamera('camera', new BABYLON.Vector3(0, 0, -5), scene);
    // const camera = new ArcRotateCamera("camera", -Math.PI / 2, Math.PI / 2.5, 15, new Vector3(0, 0, -50), scene);
    const camera = new FollowCamera("camera", new Vector3(-1, -1, -1), scene, craft2);
    camera.fov = 80;
    // camera.attachControl(canvas, true);
    camera.attachControl();
    return scene;
};

// const scene = createDemoScene(); //Call the createScene function
const scene = createScene();

const prey = new Fighter(scene.getMeshByName('craft1') as AbstractMesh, .1);
const hunter = new Fighter(scene.getMeshByName('craft2') as AbstractMesh, .005);
// const camera = scene.getCameraByName('camera');
let fleeDir = new Vector3(1, 0, 0).normalize();
let i = 0;
// Register a render loop to repeatedly render the scene
engine.runRenderLoop(() => {
    const rand = () => (0.5 - Math.random()) * prey.speed;
    prey.pos().addInPlace(fleeDir.multiplyByFloats(prey.speed, prey.speed, prey.speed));

    i += 1;
    if (i >= 50) {
        fleeDir = new Vector3(rand(), rand(), rand()).normalize()
        i = 0;
    }

    hunter.advanceTowards(prey);

    console.log("dist: ", hunter.distance(prey));
    scene.render();
});
// Watch for browser/canvas resize events
window.addEventListener("resize", () => engine.resize());
