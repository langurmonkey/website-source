+++
categories = ["Projects"]
date = "2013-10-29"
tags = ["snake", "html5"]
title = "HTML5 Snake Game"
description = "Snake game and javascript source code"
showpagemeta = "false"
js = ["/js/snake.js", "/js/jquery.min.js"]
+++

<style>
input[type=checkbox], input[type=radio] {
	display: inline;
	opacity: 1;
	float: none;
	-webkit-appearance: radio;
	margin-right: 0;
}

input[type=text] {
    margin-top: 0.1em;
    margin-bottom: 0.1em;
    height: 1.5em;
    width: 15em;
    margin-right: 0px;
    margin-left: auto;
}

table td {
	padding: 0.1em;
}
</style>

This is my modification of the HTML5 snake game seen in [thecodeplayer.com](http://thecodeplayer.com/). You can change all the start parameters using the input form below, just remember to hit `r` to reload so that the new values take effect. It is very customizable, try it!

<!-- Lets make a simple snake game -->
<canvas id="snakecanvas" style="box-shadow: 0 0 8px 0 black;"></canvas>
<div class="snakehints">
	p - pause game&nbsp;&nbsp;&nbsp;&nbsp;r - restart game
</div>

<div id="form" style="min-height:140px;">
<h3>Options</h3>
<form id="snakeoptions">
<div><input type="radio" name="shape" value="square" checked="checked"> Square</div>
<input type="radio" name="shape" value="circle"> Circle
<div>
<table style="margin:0;width:100%">
<tr><td>Width (in blocks):</td><td><input type="text" name="canvaswidth" value="30" size="5"></input></td></tr>
<tr><td>Height (in blocks):</td><td><input type="text" name="canvasheight" value="30" size="5"></input></td></tr>
<tr><td>Size of blocks (px):</td><td><input type="text" name="size" value="10" size="5"></input></td></tr>
</table>
</div>

<div>
<table style="margin:0;width:100%">
<tr><td>Background colour:</td><td><input type="text" name="bgcol" value="#DDD" size="10"></input></td></tr>
<tr><td>Snake colour:</td><td><input type="text" name="snakecol" value="#3C7" size="10"></input></td></tr>
<tr><td>Food colour:</td><td><input type="text" name="foodcol" value="#A73" size="10"></input></td></tr>
</table>
</div>

<div>
<table style="margin:0;width:100%">
<tr><td>Velocity (higher is slower):</td><td><input type="text" name="velocity" value="150" size="5"></input></td></tr>
</table>
</div>

</form>
</div>

Below is the javascript code, if you need it. You can also get it [here](/js/snake.js). Of course you'll need [jQuery](http://jquery.com/) and some form input fields to get the initial values from in your html page, but this is not difficult to work out at all.

{{< highlight javascript "linenos=table" >}}
$(document).ready(
		function() {
			// GLOBAL VARIABLES
			// Canvas stuff
			canvas = $("#snakecanvas")[0];
			ctx = canvas.getContext("2d");


			// LOCAL VARIABLES
			var d, pause = false;
			var food;
			var score;
			var shape;
			// Snake array
			var snake_array;

			// Initialization function
			function init(interval) {
				d = "right";
				updateCanvasSize();
				// block size
				cw = parseInt($('#snakeoptions input:text[name="size"]').val());
				// block shape
				shape = $('#snakeoptions input:radio[name="shape"]:checked').val();
				bgcol = $('#snakeoptions input:text[name="bgcol"]').val();
				snakecol = $('#snakeoptions input:text[name="snakecol"]').val();
				foodcol = $('#snakeoptions input:text[name="foodcol"]').val();

				create_snake();
				create_food();
				score = 0;
				if (typeof game_loop != "undefined")
					clearInterval(game_loop);
				game_loop = setInterval(paint, interval);
			}
			init(parseInt($('#snakeoptions input:text[name="velocity"]').val()));

			function create_snake() {
				var length = 4; // Initial length of the snake
				snake_array = [];
				for ( var i = length - 1; i >= 0; i--) {
					// Create snake starting from top left
					snake_array.push({
						x : i,
						y : 0
					});
				}
			}

			function create_food() {
				food = {
					x : Math.round(Math.random() * (w - cw) / cw),
					y : Math.round(Math.random() * (h - cw) / cw),
				};
			}

			// Paint the snake
			function paint() {
				if (pause){
					writeText("Game paused", "white", 5, h-5, "15pt")
					return;
				}

				ctx.fillStyle = bgcol;
				ctx.fillRect(0, 0, w, h);
				ctx.strokeStyle = "black";
				ctx.strokeRect(0, 0, w, h);

				var nx = snake_array[0].x;
				var ny = snake_array[0].y;

				if (d == "right")
					nx++;
				else if (d == "left")
					nx--;
				else if (d == "up")
					ny--;
				else if (d == "down")
					ny++;

				// Lets add the game over clauses now
				if (nx == -1 || nx == w / cw || ny == -1 || ny == h / cw
						|| check_collision(nx, ny, snake_array)) {
					// restart game
					init(parseInt($('#snakeoptions input:text[name="velocity"]').val()));
					return;
				}

				// Lets write the code to make the snake eat the food
				if (nx == food.x && ny == food.y) {
					var tail = {
						x : nx,
						y : ny
					};
					score+=10;
					create_food();
				} else {
					var tail = snake_array.pop();
					tail.x = nx;
					tail.y = ny;
				}

				snake_array.unshift(tail);

				for ( var i = 0; i < snake_array.length; i++) {
					var c = snake_array[i];
					// Lets paint 10px wide cells
					paint_cell(c.x, c.y, snakecol);
				}

				// Lets paint the food
				paint_cell(food.x, food.y, foodcol);
				// Lets paint the score
				var score_text = "Score: " + score;
				writeText(score_text, "black", w-80, h-5, "10pt");

			}

			function writeText(text, color, px, py, fontSize){
				ctx.fillStyle = color;
				ctx.font = fontSize + " Calibri";
				ctx.fillText(text, px, py);
			}

			// Lets first create a generic function to paint cells
			function paint_cell(x, y, color, shp) {
				strokeStyle = "black"
				if (shape == "square") {
					ctx.fillStyle = color;
					ctx.fillRect(x * cw, y * cw, cw, cw);
					ctx.strokeStyle = strokeStyle;
					ctx.strokeRect(x * cw, y * cw, cw, cw);
				} else if (shape == "circle") {
					ctx.beginPath();
					ctx.arc(x * cw + cw / 2, y * cw + cw / 2, cw / 2, 0,
							2 * Math.PI, false);
					ctx.fillStyle = color;
					ctx.strokeStyle = strokeStyle;
					ctx.fill();
					ctx.stroke();
				}
			}

			function check_collision(x, y, array) {
				for ( var i = 0; i < array.length; i++) {
					if (array[i].x == x && array[i].y == y)
						return true;
				}
				return false;
			}

			// Lets add the keyboard controls now
			$(document).keydown(function(e) {
				var key = e.which;
				// We will add another clause to prevent reverse gear
				if (key == "37" && d != "right")
					d = "left";
				else if (key == "38" && d != "down")
					d = "up";
				else if (key == "39" && d != "left")
					d = "right";
				else if (key == "40" && d != "up")
					d = "down";

				// Key -> p - toggle pause
				if (key == "80")
					pause = !pause;

				// Key -> r - restart
				if(key == "82")
					init(parseInt($('#snakeoptions input:text[name="velocity"]').val()));
			})
});
function updateCanvasSize(){
	w = parseInt($('#snakeoptions input:text[name="canvaswidth"]').val()) 
       * parseInt($('#snakeoptions input:text[name="size"]').val());
	h = parseInt($('#snakeoptions input:text[name="canvasheight"]').val()) 
       * parseInt($('#snakeoptions input:text[name="size"]').val());
	canvas.width = w;
	canvas.height = h;
}
{{< /highlight >}}
