/*
const RADIUS = 100;
const COLOR_ADJ = 50;

function drawRoulette(meal, colors) {
  let sum = meal.reduce((a, b) => a + b, 0);
  let angleSum = 0;
  push();
  colorMode(HSL, 255);
  for (let i = 0; i < meal.length; i++) {
    let probability = meal[i] / sum;
    let angle = probability * TWO_PI;
    fill(colors[i], 255 - COLOR_ADJ * colors[i], 128);
    arc(0, 0, RADIUS * 2, RADIUS * 2, angleSum, angleSum + angle);
    angleSum += angle;
  }
  pop();
}
*/