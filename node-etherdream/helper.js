/*
ES7 EtherDream helper
This use promise instead of callback


USAGE:
```
const STATIC_IP = '192.168.1.5';


function renderframe(phase, callback) {
	const framedata = [];
	// your code here
	callback(framedata);
}


(async () => {
	const helper = require('./helper');

	const laser = await helper.findLaser(STATIC_IP);
	const connection = await helper.connectToLaser(laser);

	var g_phase = 0;
	function frameProvider(callback) {
		g_phase += 1;
		renderframe(g_phase, callback);
	}

	connection.streamFrames(10000, frameProvider);
})();
```
*/


const EtherDream = require('./etherdream.js').EtherDream;



module.exports.findLaser = async function findLaser(static_ip) {
	const laserList = await new Promise(resolve => EtherDream.find(resolve));

	if (laserList.length === 0) {
		throw new Error(`Didn't find any EtherDream on the network.`);
	}

	let laser = laserList.filter(_laser => _laser.ip === static_ip);

	if (!laser) {
		console.log('Found', laserList);
		throw new Error(`The laser "${static_ip}" was't not found`);
	}

	return laser;
}



module.exports.connectToLaser = async function connectToLaser(laser) {
	const ip = laser[0].ip;
	const port = laser[0].port;

	const connection = new Promise(resolve => EtherDream.connect(ip, port, resolve));

	// console.log('Connected', connection);
	if (!connection) {
		throw new Error(`Can't connect tp ${ip}:${port}`);
	}

	return connection;
}
