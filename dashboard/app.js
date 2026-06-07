fetch("../data/metrics.json")
.then(res => res.json())
.then(data => {

    const total = data.length;

    const pass = data.filter(d => d.final_decision === "PASS").length;
    const review = data.filter(d => d.final_decision === "REVIEW").length;
    const fail = data.filter(d => d.final_decision === "FAIL").length;

    const overrides = data.filter(d =>
        d.final_decision.includes("OVERRIDE")
    ).length;

    const leakage = data.filter(d =>
        d.final_decision === "FAIL" &&
        d.merge_final_decision === "GOOD"
    ).length;

    document.getElementById("total").innerHTML = "Total: " + total;
    document.getElementById("passRate").innerHTML = "PASS: " + pass;
    document.getElementById("leakage").innerHTML = "Leakage: " + leakage;
    document.getElementById("overrides").innerHTML = "Overrides: " + overrides;

    // -------------------------
    // Chart 1: Pipeline outcome
    // -------------------------
    new Chart(document.getElementById("pipelineChart"), {
        type: "pie",
        data: {
            labels: ["PASS", "REVIEW", "FAIL"],
            datasets: [{
                data: [pass, review, fail]
            }]
        }
    });

    // -------------------------
    // Chart 2: Risk proxy (simple)
    // -------------------------
    new Chart(document.getElementById("riskChart"), {
        type: "bar",
        data: {
            labels: data.map((_, i) => i),
            datasets: [{
                label: "Score",
                data: data.map(d => d.score)
            }]
        }
    });

    // -------------------------
    // Chart 3: Agreement
    // -------------------------
    const agree = data.filter(d =>
        (d.ai_decision === "PASS" && d.final_decision === "PASS") ||
        (d.ai_decision === "FAIL" && d.final_decision === "FAIL")
    ).length;

    new Chart(document.getElementById("agreementChart"), {
        type: "doughnut",
        data: {
            labels: ["Agreement", "Disagreement"],
            datasets: [{
                data: [agree, total - agree]
            }]
        }
    });

});