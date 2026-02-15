let matchChart = null;
let coverageChart = null;

function analyze(){

 const file = document.getElementById("cv").files[0];

 if(!file){
   alert("Upload CV first");
   return;
 }

 let fd = new FormData();
 fd.append("cv", file);

 fetch("/analyze",{method:"POST", body:fd})
 .then(res => res.json())
 .then(data => {

   const container = document.getElementById("results");
   container.innerHTML = "";

   // Prepare chart data
   let careers = [];
   let scores = [];
   let coverage = [];

   data.forEach(career => {

     careers.push(career.career);
     scores.push(career.match_score);
     coverage.push(career.coverage);

     let roadmapHTML = career.roadmap.map(r =>
       `<li>
         Step ${r.step}: Learn <b>${r.skill}</b> →
         <a href="${r.course}" target="_blank">Course</a>
       </li>`
     ).join("");

     container.innerHTML += `
       <div class="card p-3 mb-3">
         <h4>${career.career}</h4>
         <p>Match Score: ${career.match_score}</p>
         <p>Skill Coverage: ${career.coverage}%</p>

         <h6>Learning Roadmap</h6>
         <ul>${roadmapHTML}</ul>
       </div>
     `;
   });

   // Destroy old charts if exist
   if(matchChart) matchChart.destroy();
   if(coverageChart) coverageChart.destroy();

   // Match Score Bar Chart
   matchChart = new Chart(
     document.getElementById("matchChart"),
     {
       type: "bar",
       data: {
         labels: careers,
         datasets: [{
           label: "Match Score",
           data: scores
         }]
       },
       options: {
         responsive: true,
         scales: {
           y: { beginAtZero: true }
         }
       }
     }
   );

   // Skill Coverage Doughnut Chart
   coverageChart = new Chart(
     document.getElementById("coverageChart"),
     {
       type: "doughnut",
       data: {
         labels: careers,
         datasets: [{
           label: "Skill Coverage",
           data: coverage
         }]
       },
       options: {
         responsive: true
       }
     }
   );

 });

}
