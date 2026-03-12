let network
let nodes
let edges


function iconFor(type){

if(type==="proxmox") return "/ui/icons/proxmox.svg"
if(type==="vm") return "/ui/icons/vm.svg"
if(type==="lxc") return "/ui/icons/docker.svg"
if(type==="docker") return "/ui/icons/docker.svg"
if(type==="container") return "/ui/icons/docker.svg"
if(type==="network") return "/ui/icons/network.svg"

return null

}


async function loadGraph(){

const r = await fetch("/graph")
const data = await r.json()

data.nodes.forEach(n=>{

// IMPORTANT
// If backend already sent an icon, keep it
if(n.image){

n.shape="image"
n.brokenImage="/ui/icons/docker.svg"

}else{

const icon = iconFor(n.type)

if(icon){
n.shape="image"
n.image=icon
n.brokenImage="/ui/icons/docker.svg"
}else{
n.shape="dot"
}

}

})

nodes = new vis.DataSet(data.nodes)
edges = new vis.DataSet(data.edges)

network = new vis.Network(
document.getElementById("graph"),
{nodes:nodes,edges:edges},
{

physics:{
enabled:true,
barnesHut:{
gravitationalConstant:-8000,
springLength:200
},
stabilization:{
enabled:true,
iterations:300
}
},

interaction:{
zoomView:true,
dragView:true
},

nodes:{
size:24,
font:{color:"white"}
},

edges:{
color:"#777",
smooth:true
}

}
)

network.on("click",params=>{

if(params.nodes.length===0) return

const node = nodes.get(params.nodes[0])

showNode(node)

})

}


function showNode(node){

document.getElementById("info").innerHTML=

"<h3>"+node.label+"</h3>"+

"<div class='nodeStat'><b>Type:</b> "+(node.type||"-")+"</div>"+

"<div class='nodeStat'><b>Status:</b> "+(node.status||"-")+"</div>"+

"<div class='nodeStat'><b>CPU:</b> "+(node.cpu||"-")+"</div>"+

"<div class='nodeStat'><b>Memory:</b> "+(node.mem||"-")+"</div>"

let controls=""

if(node.type==="container"){

controls+=
"<button onclick=\"restartContainer('"+node.label+"')\">Restart</button>"

controls+=
"<button onclick=\"stopContainer('"+node.label+"')\">Stop</button>"

controls+=
"<button onclick=\"loadLogs('"+node.label+"')\">Logs</button>"

}

document.getElementById("controls").innerHTML=controls
document.getElementById("logs").innerHTML=""

}


async function restartContainer(name){

await fetch("/docker/restart/"+name,{method:"POST"})

}


async function stopContainer(name){

await fetch("/docker/stop/"+name,{method:"POST"})

}


async function loadLogs(name){

const r = await fetch("/docker/logs/"+name)
const data = await r.json()

document.getElementById("logs").innerHTML =
"<h3>Logs</h3><pre>"+data.logs+"</pre>"

}


loadGraph()
