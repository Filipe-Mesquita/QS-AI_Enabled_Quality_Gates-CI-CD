fetch("../data/metrics.json")
    .then(response => response.json())
    .then(data => {

        const total = data.length;

        const passes =
            data.filter(x => x.final_decision === "APPROVE").length;

        const fails =
            data.filter(x => x.final_decision === "REJECT").length;

        const reviews =
            data.filter(x => x.final_decision === "REVIEW").length;

        const overrides =
            data.filter(
                x => x.ai_decision !== x.human_decision
            ).length;

        const defectLeakage = data.reduce((count, item) => {

            if (
                item.final_decision === "REJECT" &&
                item.merge_final_decision === "GOOD"
            ) {
                return count + 1;
            }

            return count;

        }, 0);

        const avgScore =
            data.reduce((s, x) => s + x.score, 0) / total;

        const ai_approves =
            data.filter(x => x.ai_decision === "APPROVE").length;
        const ai_fails =
            data.filter(x => x.ai_decision === "REJECT").length;
        const ai_reviews =
            data.filter(x => x.ai_decision === "REVIEW").length;

        document.getElementById("totalMerges").innerText = total;

        document.getElementById("passRate").innerText =
            ((passes / total) * 100).toFixed(1) + "%";

        document.getElementById("failRate").innerText =
            ((fails / total) * 100).toFixed(1) + "%";

        document.getElementById("overrides").innerText =
            overrides;

        document.getElementById("avgScore").innerText =
            avgScore.toFixed(2);

        document.getElementById("defectLeakage").innerText =
            defectLeakage;

        new Chart(
            document.getElementById("decisionChart"),
            {
                type: "pie",
                data: {
                    labels: ["APPROVE", "REVIEW", "REJECT"],
                    datasets: [{
                        data: [ai_approves, ai_reviews, ai_fails]
                    }]
                }
            }
        );

        const aiCounts = {};
        const humanCounts = {};

        data.forEach(item => {

            aiCounts[item.ai_decision] =
                (aiCounts[item.ai_decision] || 0) + 1;

            humanCounts[item.human_decision] =
                (humanCounts[item.human_decision] || 0) + 1;
        });

        new Chart(
            document.getElementById("comparisonChart"),
            {
                type: "bar",
                data: {
                    labels: ["APPROVE", "REVIEW", "REJECT"],
                    datasets: [
                        {
                            label: "AI",
                            data: [
                                aiCounts.APPROVE || 0,
                                aiCounts.REVIEW || 0,
                                aiCounts.REJECT || 0
                            ]
                        },
                        {
                            label: "Human",
                            data: [
                                humanCounts.APPROVE || 0,
                                humanCounts.REVIEW || 0,
                                humanCounts.REJECT || 0
                            ]
                        }
                    ]
                }
            }
        );

        const systems = {};

        data.forEach(item => {

            if (!systems[item.system]) {
                systems[item.system] = {
                    pass_rate: [],
                    mutation: [],
                    fuzz: []
                };
            }

            systems[item.system].pass_rate.push(item.pass_rate);
            systems[item.system].mutation.push(item.mutation_score);
            systems[item.system].fuzz.push(item.fuzz_failures);
        });

        const labels = Object.keys(systems);

        const pass_rateData =
            labels.map(
                s =>
                    systems[s].pass_rate.reduce((a, b) => a + b, 0) /
                    systems[s].pass_rate.length
            );

        const fuzzData =
            labels.map(
                s =>
                    systems[s].fuzz.reduce((a, b) => a + b, 0) /
                    systems[s].fuzz.length
            );

        const mutationData =
            labels.map(
                s =>
                    systems[s].mutation.reduce((a, b) => a + b, 0) /
                    systems[s].mutation.length
            );

        new Chart(
            document.getElementById("systemChart"),
            {
                type: "bar",
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: "Pass Rate",
                            data: pass_rateData
                        },
                        {
                            label: "Fuzz Failures",
                            data: fuzzData
                        },
                        {
                            label: "Mutation Score",
                            data: mutationData
                        },
                    ]
                }
            }
        );

        const rq1 = {
            APPROVE: { APPROVE: 0, REVIEW: 0, REJECT: 0 },
            REVIEW: { APPROVE: 0, REVIEW: 0, REJECT: 0 },
            REJECT: { APPROVE: 0, REVIEW: 0, REJECT: 0 }
        };
        
        data.forEach(item => {

            let final = item.final_decision;

            // normalizar overrides
            if (final === "OVERRIDE_APPROVE") final = "APPROVE";
            if (final === "OVERRIDE_REJECT") final = "REJECT";

            rq1[item.ai_decision][final]++;

            console.log("AI decision:", item.ai_decision);
            console.log("FINAL decision (normalized):", final);
        });



        console.log("Approve approve:", rq1.APPROVE.APPROVE);
        console.log("approve review:", rq1.APPROVE.REVIEW);
        console.log("approve reject:", rq1.APPROVE.REJECT);
        console.log("review approve:", rq1.REVIEW.APPROVE);
        console.log("review review:", rq1.REVIEW.REVIEW);
        console.log("review reject:", rq1.REVIEW.REJECT);
        console.log("reject approve:", rq1.REJECT.APPROVE);
        console.log("reject reeview:", rq1.REJECT.REVIEW);
        console.log("reject reject:", rq1.REJECT.REJECT);

        new Chart(
            document.getElementById("rq1Chart"),
            {
                type: "bar",
                data: {
                    labels: ["AI: APPROVE", "AI: REVIEW", "AI: REJECT"],
                    datasets: [
                        {
                            label: "FINAL: APPROVE",
                            data: [
                                rq1.APPROVE.APPROVE || 0,
                                rq1.APPROVE.REVIEW || 0,
                                rq1.APPROVE.REJECT || 0
                            ]
                        },
                        {
                            label: "FINAL: REVIEW",
                            data: [
                                rq1.REVIEW.APPROVE || 0,
                                rq1.REVIEW.REVIEW || 0,
                                rq1.REVIEW.REJECT || 0
                            ]
                        },
                        {
                            label: "FINAL: REJECT",
                            data: [
                                rq1.REJECT.APPROVE || 0,
                                rq1.REJECT.REVIEW || 0,
                                rq1.REJECT.REJECT || 0
                            ]
                        }
                    ]
                }
            }
        );

        let overrideApprove = 0;
        let overrideReject = 0;
        let noOverride = 0;

        data.forEach(item => {

            if (item.ai_decision === item.final_decision) {
                noOverride++;
                return;
            }

            if (item.final_decision === "APPROVE") {
                overrideApprove++;
            }
            else {
                overrideReject++;
            }
        });
        new Chart(
            document.getElementById("overrideChart"),
            {
                type: "pie",
                data: {
                    labels: [
                        "OVERRIDE_TO_APPROVE",
                        "OVERRIDE_TO_REJECT",
                        "NO_OVERRIDE"
                    ],
                    datasets: [{
                        data: [
                            overrideApprove,
                            overrideReject,
                            noOverride
                        ]
                    }]
                }
            }
        );


        const riskRanges = {
            "0-20": 0,
            "21-40": 0,
            "41-60": 0,
            "61-80": 0,
            "81-100": 0
        };

        data.forEach(item => {

            const risk = 100 - item.score;

            if (risk <= 20)
                riskRanges["0-20"]++;

            else if (risk <= 40)
                riskRanges["21-40"]++;

            else if (risk <= 60)
                riskRanges["41-60"]++;

            else if (risk <= 80)
                riskRanges["61-80"]++;

            else
                riskRanges["81-100"]++;
        });

        new Chart(
            document.getElementById("riskChart"),
            {
                type: "bar",
                data: {
                    labels: Object.keys(riskRanges),
                    datasets: [{
                        label: "Number of Merges",
                        data: Object.values(riskRanges)
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            }
        );

        const falsePositive =
            data.filter(
                x =>
                    x.final_decision === "APPROVE"
                    &&
                    x.merge_final_decision === "BAD"
            ).length;

        const falseNegative =
            data.filter(
                x =>
                    x.final_decision === "REJECT"
                    &&
                    x.merge_final_decision === "GOOD"
            ).length;

        console.log("False Positive:", falsePositive);
        console.log("False Negative:", falseNegative);

        const noFalseCases =
            (falsePositive === 0 && falseNegative === 0) ? 100 : 0;

        new Chart(
            document.getElementById("falseDecisionChart"),
            {
                type: "doughnut",
                data: {
                    labels: [
                        "False Positive",
                        "False Negative",
                        "No False Cases"
                    ],
                    datasets: [{
                        data: [
                            falsePositive,
                            falseNegative,
                            noFalseCases
                        ]
                    }]
                }
            }
        );

        const tbody =
            document.querySelector("#summaryTable tbody");

        labels.forEach(system => {

            const entries =
                data.filter(x => x.system === system);

            const avgPassRate =
                entries.reduce((s, x) => s + x.pass_rate, 0)
                / entries.length;

            const avgMutation =
                entries.reduce((s, x) => s + x.mutation_score, 0)
                / entries.length;

            const avgFuzz =
                entries.reduce((s, x) => s + x.fuzz_failures, 0)
                / entries.length;

            const avgSystemScore =
                entries.reduce((s, x) => s + x.score, 0)
                / entries.length;

            tbody.innerHTML += `
        <tr>
            <td>${system}</td>
            <td>${avgPassRate.toFixed(2)}</td>
            <td>${avgMutation.toFixed(2)}</td>
            <td>${avgFuzz.toFixed(2)}</td>
            <td>${avgSystemScore.toFixed(2)}</td>
        </tr>`;
        });

    });