/* =========================================================
   AI DIGITAL TWIN DASHBOARD
========================================================= */


let dashboardData = null;


/* =========================================================
   START DASHBOARD
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    async function () {

        setupNavigation();

        setupLogout();

        setupSearch();

        await loadCurrentUser();

        await loadDashboard();

    }
);


/* =========================================================
   CURRENT USER
========================================================= */

async function loadCurrentUser() {

    try {

        const response = await fetch(
            "/api/me"
        );

        if (!response.ok) {

            window.location.href = "/";

            return;
        }

        const user = await response.json();

        document.getElementById(
            "userName"
        ).textContent = user.name;

        document.getElementById(
            "userRole"
        ).textContent = user.role;

        document.getElementById(
            "userAvatar"
        ).textContent =
            user.name.charAt(0).toUpperCase();

    } catch (error) {

        console.error(
            "User loading error:",
            error
        );

        window.location.href = "/";

    }
}


/* =========================================================
   LOAD DASHBOARD
========================================================= */

async function loadDashboard() {

    try {

        const response = await fetch(
            "/api/dashboard"
        );

        if (!response.ok) {

            if (response.status === 401) {

                window.location.href = "/";

                return;
            }

            throw new Error(
                "Dashboard request failed."
            );
        }

        dashboardData =
            await response.json();

        updateStatistics();

        renderTechnologyChart();

        renderActivity();

        renderTopTechnologies();

        renderSecurity();

        renderTechnologyCards();

        renderHiringTable();

        renderAITools();

        renderThreats();

        renderStartups();

        renderLeaderboard();

    } catch (error) {

        console.error(
            "Dashboard loading error:",
            error
        );

    }
}


/* =========================================================
   STATISTICS
========================================================= */

function updateStatistics() {

    document.getElementById(
        "technologyCount"
    ).textContent =
        dashboardData.technology_count;

    document.getElementById(
        "hiringCount"
    ).textContent =
        dashboardData.hiring_count;

    document.getElementById(
        "threatCount"
    ).textContent =
        dashboardData.threat_count;
}


/* =========================================================
   NAVIGATION
========================================================= */

function setupNavigation() {

    const navItems =
        document.querySelectorAll(
            ".nav-item"
        );

    navItems.forEach(
        function (item) {

            item.addEventListener(
                "click",
                function () {

                    const section =
                        item.dataset.section;

                    showSection(section);

                }
            );

        }
    );
}


function showSection(sectionName) {

    const sections =
        document.querySelectorAll(
            ".dashboard-section"
        );

    sections.forEach(
        function (section) {

            section.classList.remove(
                "active-section"
            );

        }
    );


    const selected =
        document.getElementById(
            "section-" + sectionName
        );

    if (selected) {

        selected.classList.add(
            "active-section"
        );

    }


    const navItems =
        document.querySelectorAll(
            ".nav-item"
        );

    navItems.forEach(
        function (item) {

            item.classList.remove(
                "active"
            );

            if (
                item.dataset.section ===
                sectionName
            ) {

                item.classList.add(
                    "active"
                );

            }

        }
    );


    const titles = {

        overview: "Overview",

        technologies:
            "Technology Trends",

        hiring:
            "Hiring Signals",

        "ai-tools":
            "AI Tools",

        threats:
            "Cyber Threat Monitor",

        startups:
            "Startup Radar",

        leaderboard:
            "Leaderboard"

    };


    document.getElementById(
        "pageTitle"
    ).textContent =
        titles[sectionName] || "Overview";


    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

}


/* =========================================================
   LOGOUT
========================================================= */

function setupLogout() {

    document
        .getElementById("logoutButton")
        .addEventListener(
            "click",
            async function () {

                await fetch(
                    "/api/logout",
                    {
                        method: "POST"
                    }
                );

                window.location.href = "/";

            }
        );
}


/* =========================================================
   TECHNOLOGY CHART
========================================================= */

function renderTechnologyChart() {

    const container =
        document.getElementById(
            "technologyChart"
        );

    container.innerHTML = "";


    const technologies =
        [...dashboardData.technologies]
            .sort(
                (a, b) =>
                    b.growth - a.growth
            )
            .slice(0, 7);


    const maxGrowth =
        Math.max(
            ...technologies.map(
                item => item.growth
            )
        );


    technologies.forEach(
        function (technology) {

            const column =
                document.createElement(
                    "div"
                );

            column.className =
                "chart-column";


            const value =
                document.createElement(
                    "div"
                );

            value.className =
                "chart-value";

            value.textContent =
                "+" +
                technology.growth.toFixed(1) +
                "%";


            const barContainer =
                document.createElement(
                    "div"
                );

            barContainer.className =
                "chart-bar-container";


            const bar =
                document.createElement(
                    "div"
                );

            bar.className =
                "chart-bar";


            const height =
                Math.max(
                    12,
                    (
                        technology.growth /
                        maxGrowth
                    ) * 100
                );


            bar.style.height =
                height + "%";


            const label =
                document.createElement(
                    "div"
                );

            label.className =
                "chart-label";

            label.textContent =
                technology.name;


            barContainer.appendChild(
                bar
            );

            column.appendChild(
                value
            );

            column.appendChild(
                barContainer
            );

            column.appendChild(
                label
            );

            container.appendChild(
                column
            );

        }
    );
}


/* =========================================================
   ACTIVITY
========================================================= */

function renderActivity() {

    const container =
        document.getElementById(
            "activityList"
        );

    container.innerHTML = "";


    dashboardData.activities
        .slice(0, 5)
        .forEach(
            function (activity) {

                const item =
                    document.createElement(
                        "div"
                    );

                item.className =
                    "activity-item";


                const icon =
                    document.createElement(
                        "div"
                    );

                icon.className =
                    "activity-icon";

                icon.textContent =
                    getActivityIcon(
                        activity.activity_type
                    );


                const content =
                    document.createElement(
                        "div"
                    );


                const title =
                    document.createElement(
                        "strong"
                    );

                title.textContent =
                    activity.title;


                const description =
                    document.createElement(
                        "p"
                    );

                description.textContent =
                    activity.description;


                const time =
                    document.createElement(
                        "small"
                    );

                time.textContent =
                    activity.created_at;


                content.appendChild(
                    title
                );

                content.appendChild(
                    description
                );

                content.appendChild(
                    time
                );


                item.appendChild(
                    icon
                );

                item.appendChild(
                    content
                );


                container.appendChild(
                    item
                );

            }
        );
}


function getActivityIcon(type) {

    const icons = {

        technology: "⌁",

        hiring: "▣",

        security: "!",

        startup: "↗",

        ai: "✦"

    };

    return icons[type] || "•";
}


/* =========================================================
   TOP TECHNOLOGIES
========================================================= */

function renderTopTechnologies() {

    const container =
        document.getElementById(
            "topTechnologyList"
        );

    container.innerHTML = "";


    const technologies =
        [...dashboardData.technologies]
            .sort(
                (a, b) =>
                    b.growth - a.growth
            )
            .slice(0, 6);


    technologies.forEach(
        function (technology) {

            const row =
                document.createElement(
                    "div"
                );

            row.className =
                "signal-row";


            const name =
                document.createElement(
                    "div"
                );

            name.className =
                "signal-name";

            name.textContent =
                technology.name;


            const progress =
                document.createElement(
                    "div"
                );

            progress.className =
                "signal-progress";


            const progressBar =
                document.createElement(
                    "span"
                );

            progressBar.style.width =
                technology.popularity +
                "%";


            progress.appendChild(
                progressBar
            );


            const growth =
                document.createElement(
                    "div"
                );

            growth.className =
                "signal-growth";

            growth.textContent =
                "+" +
                technology.growth.toFixed(1) +
                "%";


            row.appendChild(name);

            row.appendChild(progress);

            row.appendChild(growth);


            container.appendChild(row);

        }
    );
}


/* =========================================================
   SECURITY
========================================================= */

function renderSecurity() {

    const container =
        document.getElementById(
            "securityList"
        );

    container.innerHTML = "";


    dashboardData.threats
        .slice(0, 5)
        .forEach(
            function (threat) {

                const row =
                    document.createElement(
                        "div"
                    );

                row.className =
                    "security-row";


                const text =
                    document.createElement(
                        "div"
                    );


                const title =
                    document.createElement(
                        "strong"
                    );

                title.textContent =
                    threat.title;


                const activity =
                    document.createElement(
                        "small"
                    );

                activity.textContent =
                    threat.activity;


                text.appendChild(
                    title
                );

                text.appendChild(
                    activity
                );


                const severity =
                    document.createElement(
                        "span"
                    );

                severity.className =
                    "severity " +
                    threat.severity.toLowerCase();

                severity.textContent =
                    threat.severity;


                row.appendChild(
                    text
                );

                row.appendChild(
                    severity
                );


                container.appendChild(
                    row
                );

            }
        );
}


/* =========================================================
   TECHNOLOGY CARDS
========================================================= */

function renderTechnologyCards() {

    const container =
        document.getElementById(
            "technologyCards"
        );

    container.innerHTML = "";


    dashboardData.technologies
        .forEach(
            function (technology) {

                const card =
                    document.createElement(
                        "div"
                    );

                card.className =
                    "technology-card";


                card.innerHTML = `

                    <div class="card-top">

                        <div>

                            <span class="category-tag">
                                ${escapeHTML(technology.category)}
                            </span>

                            <h3>
                                ${escapeHTML(technology.name)}
                            </h3>

                            <p>
                                Internet popularity signal
                            </p>

                        </div>

                        <div class="score-number">
                            ${technology.score}
                        </div>

                    </div>

                    <div class="progress-track">

                        <span
                            style="width:${technology.score}%"
                        ></span>

                    </div>

                    <div class="card-bottom">

                        <span>
                            Popularity ${technology.popularity}%
                        </span>

                        <span class="positive">
                            +${technology.growth.toFixed(1)}%
                        </span>

                    </div>

                `;


                container.appendChild(
                    card
                );

            }
        );
}


/* =========================================================
   HIRING TABLE
========================================================= */

function renderHiringTable() {

    const table =
        document.getElementById(
            "hiringTable"
        );

    table.innerHTML = "";


    dashboardData.hiring.forEach(
        function (company) {

            const row =
                document.createElement(
                    "tr"
                );


            row.innerHTML = `

                <td>
                    <span class="company-name">
                        ${escapeHTML(company.company)}
                    </span>
                </td>

                <td>
                    ${escapeHTML(company.sector)}
                </td>

                <td>
                    ${company.openings.toLocaleString()}
                </td>

                <td class="positive">
                    +${company.growth.toFixed(1)}%
                </td>

                <td>
                    <span class="signal-pill">
                        ${escapeHTML(company.signal)}
                    </span>
                </td>

            `;


            table.appendChild(
                row
            );

        }
    );
}


/* =========================================================
   AI TOOLS
========================================================= */

function renderAITools() {

    const container =
        document.getElementById(
            "aiToolsGrid"
        );

    container.innerHTML = "";


    dashboardData.ai_tools.forEach(
        function (tool) {

            const card =
                document.createElement(
                    "div"
                );

            card.className =
                "ai-card";


            const initials =
                tool.name
                    .split(" ")
                    .map(
                        word =>
                            word.charAt(0)
                    )
                    .join("")
                    .slice(0, 2);


            card.innerHTML = `

                <div class="ai-logo">
                    ${escapeHTML(initials)}
                </div>

                <h3>
                    ${escapeHTML(tool.name)}
                </h3>

                <p>
                    ${escapeHTML(tool.category)}
                </p>

                <div class="progress-track">

                    <span
                        style="width:${tool.popularity}%"
                    ></span>

                </div>

                <div class="ai-card-footer">

                    <span>
                        Popularity ${tool.popularity}%
                    </span>

                    <span class="ai-growth">
                        +${tool.weekly_change.toFixed(1)}%
                    </span>

                </div>

            `;


            container.appendChild(
                card
            );

        }
    );
}


/* =========================================================
   THREATS
========================================================= */

function renderThreats() {

    const container =
        document.getElementById(
            "threatGrid"
        );

    container.innerHTML = "";


    dashboardData.threats.forEach(
        function (threat) {

            const card =
                document.createElement(
                    "div"
                );

            card.className =
                "threat-card";


            card.innerHTML = `

                <div class="threat-card-header">

                    <h3>
                        ${escapeHTML(threat.title)}
                    </h3>

                    <span
                        class="severity ${threat.severity.toLowerCase()}"
                    >
                        ${escapeHTML(threat.severity)}
                    </span>

                </div>

                <p>
                    The Digital Twin detected
                    ${escapeHTML(threat.category.toLowerCase())}
                    activity in the simulated environment.
                </p>

                <div class="threat-meta">

                    <span>
                        Category:
                        ${escapeHTML(threat.category)}
                    </span>

                    <span>
                        ${escapeHTML(threat.activity)}
                    </span>

                </div>

            `;


            container.appendChild(
                card
            );

        }
    );
}


/* =========================================================
   STARTUPS
========================================================= */

function renderStartups() {

    const container =
        document.getElementById(
            "startupGrid"
        );

    container.innerHTML = "";


    dashboardData.startups.forEach(
        function (startup) {

            const card =
                document.createElement(
                    "div"
                );

            card.className =
                "startup-card";


            card.innerHTML = `

                <div class="startup-icon">
                    ${escapeHTML(
                        startup.name
                            .charAt(0)
                            .toUpperCase()
                    )}
                </div>

                <h3>
                    ${escapeHTML(startup.name)}
                </h3>

                <div class="startup-sector">
                    ${escapeHTML(startup.sector)}
                </div>

                <div class="startup-details">

                    <div class="startup-detail">

                        <span>
                            Location
                        </span>

                        <strong>
                            ${escapeHTML(startup.location)}
                        </strong>

                    </div>

                    <div class="startup-detail">

                        <span>
                            Funding
                        </span>

                        <strong>
                            ${escapeHTML(startup.funding)}
                        </strong>

                    </div>

                </div>

                <div class="momentum">

                    <div class="momentum-head">

                        <span>
                            Momentum
                        </span>

                        <strong>
                            ${startup.momentum}%
                        </strong>

                    </div>

                    <div class="progress-track">

                        <span
                            style="width:${startup.momentum}%"
                        ></span>

                    </div>

                </div>

            `;


            container.appendChild(
                card
            );

        }
    );
}


/* =========================================================
   LEADERBOARD
========================================================= */

function renderLeaderboard() {

    const container =
        document.getElementById(
            "leaderboard"
        );

    container.innerHTML = "";


    dashboardData.leaderboard.forEach(
        function (user, index) {

            const row =
                document.createElement(
                    "div"
                );

            row.className =
                "leader-row";


            const rank =
                document.createElement(
                    "div"
                );

            rank.className =
                "rank";

            rank.textContent =
                "#" + (index + 1);


            const userArea =
                document.createElement(
                    "div"
                );

            userArea.className =
                "leader-user";


            const avatar =
                document.createElement(
                    "div"
                );

            avatar.className =
                "leader-avatar";

            avatar.textContent =
                user.name
                    .charAt(0)
                    .toUpperCase();


            const details =
                document.createElement(
                    "div"
                );


            const name =
                document.createElement(
                    "strong"
                );

            name.textContent =
                user.name;


            const username =
                document.createElement(
                    "small"
                );

            username.textContent =
                "@" + user.username;


            details.appendChild(
                name
            );

            details.appendChild(
                username
            );


            userArea.appendChild(
                avatar
            );

            userArea.appendChild(
                details
            );


            const role =
                document.createElement(
                    "div"
                );

            role.className =
                "leader-role";

            role.textContent =
                user.role;


            const points =
                document.createElement(
                    "div"
                );

            points.className =
                "leader-points";

            points.textContent =
                user.points +
                " pts";


            row.appendChild(
                rank
            );

            row.appendChild(
                userArea
            );

            row.appendChild(
                role
            );

            row.appendChild(
                points
            );


            container.appendChild(
                row
            );

        }
    );
}


/* =========================================================
   SEARCH
========================================================= */

function setupSearch() {

    const input =
        document.getElementById(
            "searchInput"
        );

    const results =
        document.getElementById(
            "searchResults"
        );


    let timeout = null;


    input.addEventListener(
        "input",
        function () {

            clearTimeout(
                timeout
            );


            const query =
                input.value.trim();


            if (!query) {

                results.classList.add(
                    "hidden"
                );

                results.innerHTML = "";

                return;

            }


            timeout =
                setTimeout(
                    async function () {

                        try {

                            const response =
                                await fetch(
                                    "/api/search?q=" +
                                    encodeURIComponent(
                                        query
                                    )
                                );


                            if (!response.ok) {

                                return;

                            }


                            const data =
                                await response.json();


                            displaySearchResults(
                                data.results
                            );

                        } catch (error) {

                            console.error(
                                error
                            );

                        }

                    },
                    250
                );

        }
    );


    document.addEventListener(
        "click",
        function (event) {

            if (
                !event.target.closest(
                    ".search-box"
                ) &&
                !event.target.closest(
                    ".search-results"
                )
            ) {

                results.classList.add(
                    "hidden"
                );

            }

        }
    );
}


function displaySearchResults(
    results
) {

    const container =
        document.getElementById(
            "searchResults"
        );


    container.innerHTML = "";


    if (!results.length) {

        container.innerHTML = `

            <div class="search-result">

                <strong>
                    No results found
                </strong>

                <span>
                    Try another technology,
                    company or AI tool.
                </span>

            </div>

        `;

        container.classList.remove(
            "hidden"
        );

        return;
    }


    results.forEach(
        function (item) {

            const result =
                document.createElement(
                    "div"
                );

            result.className =
                "search-result";


            result.innerHTML = `

                <strong>

                    ${escapeHTML(item.name)}

                    <span class="search-type">
                        ${escapeHTML(item.type)}
                    </span>

                </strong>

                <span>
                    ${escapeHTML(item.details)}
                </span>

            `;


            container.appendChild(
                result
            );

        }
    );


    container.classList.remove(
        "hidden"
    );
}


/* =========================================================
   SECURITY HELPER
========================================================= */

function escapeHTML(value) {

    const div =
        document.createElement(
            "div"
        );

    div.textContent =
        value ?? "";

    return div.innerHTML;
}