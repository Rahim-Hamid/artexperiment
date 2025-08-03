let distMouse = 30;
let blocks = [];
let rows;
let cols;
let size = 10;
let offset = 4;

function setup() {
  createCanvas(800, 800);
  rectMode(CENTER);
  angleMode(DEGREES);
  cols = width/size;
  rows = height/size;

  for (let i=0; i<cols; i++){
    blocks[i] = [];
    for (let j=0; j<rows;j++) {
      blocks[i][j] = new Block(size/2 + i*size, size/2 + j*size);
    }
  }

}

function draw() {
  background('black');
  for (let i=0; i<cols; i++){
    for (let j=0; j<rows;j++) {
      blocks[i][j].move();
      blocks[i][j].display();
    }
  }
  

}
