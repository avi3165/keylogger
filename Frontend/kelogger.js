const API_URL = "http://127.0.0.1:5000/api"
const COMPUTERS_CONTAINER = document.getElementById("computer_list")
async function fetch_computers() {
    try {
        const response = await fetch(`${API_URL}/computers`);
        const computers = await response.json();
        renderComputers(computers);
    } catch (error) {
        showError("שגיאה בטעינת המחשבים");
    }
}

function renderComputers(computers) {
    COMPUTERS_CONTAINER.innerHTML = "";
    if (computers.length === 0) {
        COMPUTERS_CONTAINER.innerHTML = '<p class = "empty_state">"not found computers"</p>'
        return;
    }
    computers.forEach(computer => {
        const computers_elemants = document.createElement('li')
        computers_elemants.className = 'computer item'
        computers_elemants.innerHTML = `
        <div>${computer.name}</div>`    ``

    })

}
list = [{ "c_name": "111" }, { "c_name": "222" }]

document.addEventListener("computer", fetch_computers)
list.forEach(computer => {
     document.getElementById("computer").innerHTML = `<li><button id="${computer[c_name]}" value="${computer[c_name]}">${computer[c_name]}</button></li>` 
    })


