
var desiredIP = '192.168.1.4';
var offsetX = 0; // devrait etre autour de -8000 / 8000
var offsetY = 0; // devrait etre autour de -8000 / 8000
var scale = 1; // echelle

var EtherDream = require('./etherdream.js').EtherDream;

function sendframe(connection, data, callback) {
	console.log('send frame');
	connection.write(data, 30000, function() {
		console.log('frame written.');
		callback();
	});
}

console.log('Looking for EtherDream hosts...')
EtherDream.find(function(all) {
	if (all.length == 0) {
		console.log('Didn\'t find any EtherDream on the network.');
		return;
	}
	console.log('Found', all);	
	
	//find correct ip--------------------
	var laserIndex = -1;
	for (var i = 0; i < all.length; i++)
		if (all[i].ip == desiredIP)
			laserIndex = i;		
	//-----------------------------------

	EtherDream.connect(all[laserIndex].ip, all[laserIndex].port, function(conn) {

		console.log('Connected', conn);
		if (!conn) {
			return;
		}

		function blackPoint(framedata,x,y){
			x += offsetX;
			y += offsetY;
			x *= scale;
			y *= scale;
			for(var i=0; i<5 ; i++) {
				var pt = {};
				pt.x = x;
				pt.y = y;
				pt.r = 0;
				pt.g = 0;
				pt.b = 0;
				pt.control = 0;
				pt.i = 0;
				pt.u1 = 0;
				pt.u2 = 0;
				framedata.push(pt);
			}
		}

		function setPoint(framedata,x,y){
			x += offsetX;
			y += offsetY;
			x *= scale;
			y *= scale;

			for(var i=0; i<5 ; i++) {
				var pt = {};
				pt.x = x;
				pt.y = y;
				pt.r = 0;
				pt.g = 0;
				pt.b = 0;
				pt.control = 0;
				pt.i = 0;
				pt.u1 = 0;
				pt.u2 = 0;
				framedata.push(pt);
			}
			var pt = {};
			pt.x = x;
			pt.y = y;
			pt.r = 65000;
			pt.g = 20000;
			pt.b = 20000;
			pt.control = 0;
			pt.i = 0;
			pt.u1 = 0;
			pt.u2 = 0;
			framedata.push(pt);
			for(var i=0; i<5 ; i++) {
				var pt = {};
				pt.x = x;
				pt.y = y;
				pt.r = 0;
				pt.g = 0;
				pt.b = 0;
				pt.control = 0;
				pt.i = 0;
				pt.u1 = 0;
				pt.u2 = 0;
				framedata.push(pt);
			}
		}

		function drawline(framedata, x0,y0, x1,y1, r,g,b) {

			x0 += offsetX;
			y0 += offsetY;
			x0 *= scale;
			y0 *= scale;
			x1 += offsetX;
			y1 += offsetY;
			x1 *= scale;
			y1 *= scale;

			var dx = Math.abs(x1 - x0);
			var dy = Math.abs(y1 - y0);
			var d = Math.round(4 + (Math.sqrt(dx*dx + dy*dy) / 400));

			var jumpframes = 5;
			var stopframes = 5;
			var lineframes = d;

			for(var i=0; i<jumpframes; i++) {
				var pt = {};
				pt.x = x0;
				pt.y = y0;
				pt.r = 0;
				pt.g = 0;
				pt.b = 0;
				pt.control = 0;
				pt.i = 0;
				pt.u1 = 0;
				pt.u2 = 0;
				framedata.push(pt);
			}

			for(var i=0; i<lineframes; i++) {
				var pt = {};
				pt.x = (x0 + (x1 - x0) * (i / (lineframes - 1)));
				pt.y = (y0 + (y1 - y0) * (i / (lineframes - 1)));
				pt.r = r;
				pt.g = g;
				pt.b = b;
				pt.control = 0;
				pt.i = 0;
				pt.u1 = 0;
				pt.u2 = 0;
				framedata.push(pt);
			}

			for(var i=0; i<stopframes; i++) {
				var pt = {};
				pt.x = x1;
				pt.y = y1;
				pt.r = 0;
				pt.g = 0;
				pt.b = 0;
				pt.control = 0;
				pt.i = 0;
				pt.u1 = 0;
				pt.u2 = 0;
				framedata.push(pt);
			}
		}

		function drawTriangle(framedata, scale, rr, gg, bb){
			drawline(framedata,
					 -20000*scale,-20000*scale,
					 20000*scale,-20000*scale,
					 rr,
					 gg,
					 bb
			);
			drawline(framedata,
					 20000*scale,-20000*scale,
					 0,20000*scale,
					 rr,
					 gg,
					 bb
			);
			drawline(framedata,
					 0*scale,20000*scale,
					 -20000,-20000*scale,
					 rr,
					 gg,
					 bb
			);
		}

		// ANIMATION VARIABLES -----------------------------------------------

		var t = 0;

		var lastRadius = 0;
		var radiusRatio = 0;
		var nextRadius = 0;

		var startingAngle = 0.0;

		var nextLoops = 5;
		var loopsRatio = 0;
		var loopDelay = 2;
		var lastLoops = 0;

		var rr = 0;
		var gg = 0;
		var bb = 0;

		var lastRr = 0;
		var lastGg = 0;
		var lastBb = 0;

		var starPos = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];

		var lineRatio = 0.0;
		var linePosX;
		var linePosY;

		var line2Ratio = 0.0;
		var line2PosX;
		var line2PosY;

		var line3Ratio = 0.0;
		var line3PosX;
		var line3PosY;

		function renderframe(phase, callback) {

			var framedata = [];
			var shouldfill = conn.fullness < 1000;

			// radius change --------------------------
			radiusRatio += 0.01;

			var radius = 0;
			var r;
			var g;
			var b;

			if( radiusRatio > 1){
				radiusRatio = 0;
				radius = lastRadius = nextRadius;
				nextRadius = Math.random();
				r = lastRr = rr;
				g = lastGg = gg;
				b = lastBb = bb;
				rr = Math.random() * 65000;
				gg = Math.random() * 65000;
				bb = Math.random() * 65000;
			}else{
				radius = nextRadius*radiusRatio + lastRadius * (1-radiusRatio);
				r = lastRr*radiusRatio + rr * (1-radiusRatio);
				g = lastGg*radiusRatio + gg * (1-radiusRatio);
				b = lastBb*radiusRatio + bb * (1-radiusRatio);
			}

			// loop changes ----------------------------
			loopsRatio += 0.02;
			if (loopsRatio > loopDelay){
				loopsRatio = 0;
				nextLoops = Math.random()*6 + 2;
				loopDelay = Math.random() * 5 + 1;
			}
			var loops = lastLoops * loopsRatio + nextLoops * (1-loopsRatio);

			var angle = 0.0;
			var x1 = 0;
			var y1 = 0;

			// fait tourner l'ensemble--------
			startingAngle += 0.01;
			angle += startingAngle;

			x1 = Math.cos(angle) * 7000 + Math.cos(angle*loops) * 2000 * (radius-0.5) ;
			y1 = Math.sin(angle) * 7000 +  Math.sin(angle*loops) * -2000 * (radius-0.5);

			blackPoint(framedata,x1,y1);

			for(var i=0; i<80; i++) {
	
				x1 = Math.cos(angle) * 7000 + Math.cos(angle*loops) * 2000 * (radius-0.5) ;
				y1 = Math.sin(angle) * 7000 +  Math.sin(angle*loops) * -2000 * (radius-0.5);
				angle += 3.25 / 40;

				x1 += offsetX;
				y1 += offsetY;
				x1 *= scale;
				y1 *= scale;

				var pt = {};
				pt.x = x1;
				pt.y = y1;
				pt.r = r;
				pt.g = g;
				pt.b = b;
				pt.control = 0;
				pt.i = 0;
				pt.u1 = 0;
				pt.u2 = 0;
				framedata.push(pt);
			}

			blackPoint(framedata,x1,y1);

			x1 = Math.cos(angle) * 5500 * radius + Math.cos(angle*(loops+3)) * 2000 * (-radius+0.5) ;
			y1 = Math.sin(angle) * 5500 * radius +  Math.sin(angle*(loops+3)) * -2000 * (-radius+0.5) ;

			x1 += offsetX;
			y1 += offsetY;
			x1 *= scale;
			y1 *= scale;

			blackPoint(framedata,x1,y1);

			for(var i=0; i<80; i++) {

				x1 = Math.cos(angle) * 5500 * radius + Math.cos(angle*(loops+3)) * 2000 * (-radius+0.5) ;
				y1 = Math.sin(angle) * 5500 * radius +  Math.sin(angle*(loops+3)) * -2000 * (-radius+0.5) ;
				angle += 3.17 / 40;

				x1 += offsetX;
				y1 += offsetY;
				x1 *= scale;
				y1 *= scale;

				var pt = {};
				pt.x = x1;
				pt.y = y1;
				pt.r = 65000-r;
				pt.g = 65000-g;
				pt.b = 65000-b;
				pt.control = 0;
				pt.i = 0;
				pt.u1 = 0;
				pt.u2 = 0;
				framedata.push(pt);
			}

			blackPoint(framedata,x1,y1);

			blackPoint(framedata,x1,y1);

			var rS = 4000;
			drawline(framedata,
				Math.random()*rS-rS/2, Math.random()*rS-rS/2,
				Math.random()*rS-rS/2, Math.random()*rS-rS/2,
				65000,
				0,
				0
			);

			setPoint(framedata,0,0);

			for(var i=0; i<10; i++) {
				if(starPos[i*2] == 0 || Math.abs(starPos[i*2])> 12000 || Math.abs(starPos[i*2+1])> 12000 ){
					starPos[i*2] = Math.random()*1000-500;
					starPos[i*2+1] = Math.random()*1000-500;					
				}
				starPos[i*2] *= 1.2;
				starPos[i*2+1] *= 1.2;
				setPoint(framedata, starPos[i*2] , starPos[i*2+1] );
			}

			setPoint(framedata,0,0);

			// lignes de fuites ------------------------------------------------
			var maxLineSize = 8000;

			//01 ------
			if(lineRatio == 0){
				linePosX = Math.random()*50000-25000;
				linePosY = Math.random()*50000-25000;
			}
			lineRatio += 0.1;	
			if(Math.abs(linePosX * 0.5 * lineRatio) > maxLineSize || Math.abs(linePosY * 0.5 * lineRatio) > maxLineSize){
				lineRatio = 0;				
			}
			drawline(framedata,
				linePosX * 0.5 * lineRatio, linePosY * 0.5 * lineRatio,
				linePosX * lineRatio, linePosY * lineRatio,
				10000,30000,30000
			);

			//02 ------
			if(line2Ratio == 0){
				line2PosX = Math.random()*50000-25000;
				line3PosY = Math.random()*50000-25000;
			}
			line2Ratio += 0.1;	
			if(Math.abs(line2PosX * 0.5 * line2Ratio) > maxLineSize || Math.abs(line3PosY * 0.5 * line2Ratio) > maxLineSize){
				line2Ratio = 0;				
			}
			drawline(framedata,
				line2PosX * 0.5 * line2Ratio, line3PosY * 0.5 * line2Ratio,
				line2PosX * line2Ratio, line3PosY * line2Ratio,
				10000,30000,30000
			);

			//03 ------
			if(line3Ratio == 0){
				line3PosX = Math.random()*50000-25000;
				line3PosY = Math.random()*50000-25000;
			}
			line3Ratio += 0.1;	
			if(Math.abs(line3PosX * 0.5 * line3Ratio) > maxLineSize || Math.abs(line3PosY * 0.5 * line3Ratio) > maxLineSize){
				line3Ratio = 0;				
			}
			drawline(framedata,
				line3PosX * 0.5 * line3Ratio, line3PosY * 0.5 * line3Ratio,
				line3PosX * line3Ratio, line3PosY * line3Ratio,
				10000,30000,30000
			);

			//----------------------------------------------------------------

			blackPoint(framedata,0,0);

			callback(framedata);
		};

		var g_phase = 0;
		function frameProvider(callback) {
			g_phase += 1;
			renderframe(g_phase, callback);
		}

		conn.streamFrames(10000, frameProvider.bind(this));

	});
});