if (localStorage.getItem("NGH_AUTH") !== "true") {
    localStorage.setItem("NGH_AUTH", "true");
}

function logout() {
    localStorage.clear();
    window.location = "login.php";
}

function setTransferMessage(text, ok = true) {
    const msg = document.getElementById("transferMsg");
    msg.innerText = text;
    msg.className = ok ? "msg success" : "msg error";
}

function closeCriticalModal() {
    const modal = document.getElementById("criticalModal");
    if (modal) {
        modal.classList.add("hidden");
    }
}

function goToTransfer() {
    closeCriticalModal();

    const box = document.getElementById("transferMrn");
    if (box) {
        box.scrollIntoView({ behavior: "smooth", block: "center" });
        box.focus();
    }
}

function showCriticalModal(departmentName, occupancy) {
    const modal = document.getElementById("criticalModal");
    const text = document.getElementById("criticalModalText");

    if (!modal || !text) return;

    text.innerText =
        departmentName + " is full (" + occupancy + "% occupied). Please transfer the patient to another department.";

    modal.classList.remove("hidden");
}

function selectDept(name) {
    document.getElementById("selectedDept").innerText = name;
    document.getElementById("targetDept").value = name;
}

/*
    الفكرة هنا:
    - أول تحميل للصفحة: نحفظ الأقسام الممتلئة الحالية بدون ما نظهر إنذار
    - بعد ذلك فقط: إذا قسم "صار" ممتلئ لاحقًا نظهر الإنذار
*/
let isFirstLoad = true;
let previousFullDepartments = {};

function loadDepartments() {
    fetch("get_departments.php")
        .then(res => res.json())
        .then(data => {
            let table = "";
            let totalBeds = 0;
            let totalAvailable = 0;
            let criticalCount = 0;
            let options = '<option value="">Select target department</option>';
            let recommendations = "";
            let currentFullDepartments = {};

            data.forEach(d => {
                totalBeds += Number(d.total);
                totalAvailable += Number(d.available);

                if (String(d.status).toUpperCase() === "CRITICAL") {
                    criticalCount++;
                }

                table += `
                    <tr>
                        <td>${d.department}</td>
                        <td>${d.total}</td>
                        <td>${d.occupied}</td>
                        <td>${d.available}</td>
                        <td>${d.occupancy}%</td>
                        <td><span class="chip chip-${String(d.status).toLowerCase()}">${d.status}</span></td>
                        <td>
                            <button class="btn btn-light small-btn" onclick="selectDept('${d.department}')">Select</button>
                        </td>
                    </tr>
                `;

                if (Number(d.available) > 0) {
                    options += `<option value="${d.department}">${d.department}</option>`;

                    recommendations += `
                        <div class="rec-item">
                            <strong>${d.department}</strong>
                            Available Beds: ${d.available}<br>
                            Occupancy: ${d.occupancy}%<br>
                            <span class="chip chip-${String(d.status).toLowerCase()}">${d.status}</span>
                        </div>
                    `;
                }

                // ممتلئ فقط إذا وصل 100%
                if (Number(d.occupancy) >= 100) {
                    currentFullDepartments[d.department] = Number(d.occupancy);
                }
            });

            document.getElementById("deptTable").innerHTML = table;
            document.getElementById("totalDept").innerText = data.length;
            document.getElementById("totalBeds").innerText = totalBeds;
            document.getElementById("totalAvailable").innerText = totalAvailable;
            document.getElementById("criticalCount").innerText = criticalCount;
            document.getElementById("targetDept").innerHTML = options;
            document.getElementById("recommendList").innerHTML =
                recommendations || "<div class='rec-item'>No departments available</div>";

            // أول تحميل: لا تظهر أي إنذار، فقط خزّن الوضع الحالي
            if (isFirstLoad) {
                previousFullDepartments = { ...currentFullDepartments };
                isFirstLoad = false;
                return;
            }

            // بعد أول تحميل: أظهر الإنذار فقط إذا قسم "صار" ممتلئ الآن ولم يكن ممتلئًا قبل
            for (const deptName in currentFullDepartments) {
                if (!previousFullDepartments[deptName]) {
                    showCriticalModal(deptName, currentFullDepartments[deptName]);
                    break;
                }
            }

            previousFullDepartments = { ...currentFullDepartments };
        })
        .catch(() => setTransferMessage("Failed to load departments.", false));
}

function transferPatient() {
    const mrn = document.getElementById("transferMrn").value.trim();
    const dept = document.getElementById("targetDept").value;

    if (!mrn) {
        setTransferMessage("Please enter patient MRN.", false);
        return;
    }

    if (!dept) {
        setTransferMessage("Please select target department.", false);
        return;
    }

    fetch("transfer_patient.php", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: "mrn=" + encodeURIComponent(mrn) + "&department=" + encodeURIComponent(dept)
    })
    .then(res => res.json())
    .then(data => {
        setTransferMessage(data.message, data.ok);

        if (data.ok) {
            document.getElementById("transferMrn").value = "";
            document.getElementById("selectedDept").innerText = "None";
            document.getElementById("targetDept").value = "";
            closeCriticalModal();
            loadDepartments();
        }
    })
    .catch(() => setTransferMessage("Transfer failed.", false));
}

// تحديث دوري بدون تغيير الشكل
setInterval(loadDepartments, 5000);

loadDepartments();