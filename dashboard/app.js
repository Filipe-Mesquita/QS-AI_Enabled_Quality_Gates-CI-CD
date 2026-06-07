fetch("../data/metrics.json")
    .then(response => response.json())
    .then(data => {

        const total = data.length;

        const passes =
            data.filter(x => x.merge_final_decision === "GOOD").length;

        const fails =
            data.filter(x => x.merge_final_decision === "BAD").length;

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
                    coverage: [],
                    mutation: [],
                    fuzz: []
                };
            }

            systems[item.system].coverage.push(item.coverage);
            systems[item.system].mutation.push(item.mutation_score);
            systems[item.system].fuzz.push(item.fuzz_failures);
        });

        const labels = Object.keys(systems);

        const coverageData =
            labels.map(
                s =>
                    systems[s].coverage.reduce((a, b) => a + b, 0) /
                    systems[s].coverage.length
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
                            label: "Coverage",
                            data: coverageData
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

            rq1[item.ai_decision][item.final_decision]++;
        });
        new Chart(
            document.getElementById("rq1Chart"),
            {
                type: "bar",
                data: {
                    labels: ["APPROVE", "REVIEW", "REJECT"],
                    datasets: [
                        {
                            label: "AI APPROVE",
                            data: [
                                rq1.APPROVE.APPROVE,
                                rq1.APPROVE.REVIEW,
                                rq1.APPROVE.REJECT
                            ]
                        },
                        {
                            label: "AI REVIEW",
                            data: [
                                rq1.REVIEW.APPROVE,
                                rq1.REVIEW.REVIEW,
                                rq1.REVIEW.REJECT
                            ]
                        },
                        {
                            label: "AI REJECT",
                            data: [
                                rq1.REJECT.APPROVE,
                                rq1.REJECT.REVIEW,
                                rq1.REJECT.REJECT
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
                        "OVERRIDE_APPROVE",
                        "OVERRIDE_REJECT",
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

        new Chart(
            document.getElementById("falseDecisionChart"),
            {
                type: "doughnut",
                data: {
                    labels: [
                        "False Positive",
                        "False Negative"
                    ],
                    datasets: [{
                        data: [
                            falsePositive,
                            falseNegative
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

            const avgCoverage =
                entries.reduce((s, x) => s + x.coverage, 0)
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
            <td>${avgCoverage.toFixed(2)}</td>
            <td>${avgMutation.toFixed(2)}</td>
            <td>${avgFuzz.toFixed(2)}</td>
            <td>${avgSystemScore.toFixed(2)}</td>
        </tr>`;
        });

    });