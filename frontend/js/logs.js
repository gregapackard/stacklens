// -------------------------
// Container Logs
// -------------------------

let logInterval = null

// -------------------------
// Show Node Panel
// -------------------------

function showNode(node){

selectedNode = node

// reset stat history
cpuHistory=[]
memHistory=[]
netHistory=[]
diskHistory=[]

let panelHTML = `
<h3>${node.label}</h3>

<div class='nodeStat'><b>Type:</b> ${node.type || "-"}</div>
<div class='nodeStat'><b>Status:</b> ${node.status || "-"}</div>
`

// -------------------------
// Container Metrics
// -------------------------

if(node.type==="container"){

panelHTML += `

<div class='nodeStat'><b>CPU:</b> <span id="nodeCPU">-</span></div>
<canvas id="cpuGraph"></canvas>

<div class='nodeStat'><b>Memory:</b> <span id="nodeMem">-</span></div>
<canvas id="memGraph"></canvas>

<div class='nodeStat'><b>Network:</b> <span id="nodeNet">-</span></div>
<canvas id="netGraph"></canvas>

<div class='nodeStat'><b>Disk:</b> <span id="nodeDisk">-</span></div>
<canvas id="diskGraph"></canvas>

`
}

document.getElementById("info").innerHTML = panelHTML

// -------------------------
// Controls
// -------------------------

let controls=""

if(node.type==="container"){

controls += `<button onclick="restartContainer('${node.label}')">Restart</button>`
controls += `<button onclick="stopContainer('${node.label}')">Stop</button>`
controls += `<button onclick="loadLogs('${node.label}')">Logs</button>`

}

document.getElementById("controls").innerHTML = controls

document.getElementById("logs").innerHTML=""

// start stat polling
startLiveStats()

}

// -------------------------
// Load Logs
// -------------------------

async function loadLogs(name){

if(logInterval){
clearInterval(logInterval)
}

async function fetchLogs(){

const data = await getLogs(name)

document.getElementById("logs").innerHTML =
"<h3>Logs</h3><pre>"+data.logs+"</pre>"

}

fetchLogs()

logInterval = setInterval(fetchLogs,2000)

}
