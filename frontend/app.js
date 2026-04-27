const API =
"https://auditt.up.railway.app/report";

async function runAudit(){

const filename =
document.getElementById("filename").value;

const prediction =
document.getElementById("prediction").value;

const protectedCol =
document.getElementById("protected").value;

const url =
`${API}?filename=${filename}&prediction=${prediction}&protected=${protectedCol}`;

document.getElementById("output")
.innerText = "Running...";

const res = await fetch(url,{
method:"POST"
});

const data = await res.json();

document.getElementById("output")
.innerText =
JSON.stringify(data,null,2);

}