function setup() {
  createCanvas(2000,1600);
  noStroke();
}

function draw() {
  background('gray');

  let circleSize = 20;
  let spacing = 40;

  // Loop through rows
  for (let y = 0; y < height; y += spacing) {
    // Loop through columns
    for (let x = 0; x < width; x += spacing) {
      fill(random(255), random(255), random(255)); // Random color for each circle
      ellipse(x + circleSize / 2, y + circleSize / 2, circleSize, circleSize);
    }
  }
}