// -------------------------
// API Helpers
// -------------------------

async function getGraph(){

const r = await fetch("/graph")
return await r.json()

}

async function getDockerStats(name){

const r = await fetch("/docker/stats/"+name)
return await r.json()

}

async function getLogs(name){

const r = await fetch("/docker/logs/"+name)
return await r.json()

}
