// -------------------------
// Stats Polling
// -------------------------

let statsInterval = null

let cpuHistory=[]
let memHistory=[]
let netHistory=[]
let diskHistory=[]

const MAX_POINTS=30

function startLiveStats(){

if(statsInterval){
clearInterval(statsInterval)
}

statsInterval=setInterval(updateNodeStats,2000)

}

// -------------------------
// Update Stats
// -------------------------

async function updateNodeStats(){

if(!selectedNode) return

if(selectedNode.type!=="container") return

try{

const data = await getDockerStats(selectedNode.label)

if(!data) return

document.getElementById("nodeCPU").innerText=data.cpu || "-"
document.getElementById("nodeMem").innerText=data.mem || "-"
document.getElementById("nodeNet").innerText=data.net || "-"
document.getElementById("nodeDisk").innerText=data.disk || "-"

// numeric extraction
const cpu=parseFloat(data.cpu)||0
const mem=parseFloat(data.mem)||0
const net=parseFloat(data.net)||0
const disk=parseFloat(data.disk)||0

cpuHistory.push(cpu)
memHistory.push(mem)
netHistory.push(net)
diskHistory.push(disk)

if(cpuHistory.length>MAX_POINTS) cpuHistory.shift()
if(memHistory.length>MAX_POINTS) memHistory.shift()
if(netHistory.length>MAX_POINTS) netHistory.shift()
if(diskHistory.length>MAX_POINTS) diskHistory.shift()

drawGraph("cpuGraph",cpuHistory)
drawGraph("memGraph",memHistory)
drawGraph("netGraph",netHistory)
drawGraph("diskGraph",diskHistory)

}catch(e){

console.log("stats error",e)

}

}

// -------------------------
// Graph Renderer
// -------------------------

function drawGraph(canvasId,data){

const canvas=document.getElementById(canvasId)

if(!canvas) return

const ctx=canvas.getContext("2d")

const w=canvas.width=280
const h=canvas.height=40

ctx.clearRect(0,0,w,h)

if(data.length<2) return

const max=Math.max(...data,1)

ctx.beginPath()

data.forEach((v,i)=>{

const x=(i/(data.length-1))*w
const y=h-(v/max)*h

if(i===0) ctx.moveTo(x,y)
else ctx.lineTo(x,y)

})

ctx.lineTo(w,h)
ctx.lineTo(0,h)
ctx.closePath()

ctx.fillStyle="rgba(80,160,255,0.25)"
ctx.fill()

ctx.strokeStyle="#4ea1ff"
ctx.lineWidth=2
ctx.stroke()

}
