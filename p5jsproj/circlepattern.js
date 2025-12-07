function setup() {
  createCanvas(400, 400);
}

function draw() {
  final = 400;
  offset= 10;
  for (i = 0; i != final; i++) {
    circle(0 + offset, 0 + offset, 100);
    offset += 10;
  }
  
}
