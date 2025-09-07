const API_URL = "http://127.0.0.1:5000/api"
const COMPUTERS_CONTAINER = document.getElementById("machine")
const GETCOMPUTERS_FROM = document.getElementById("get_form") 
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
        const computers_elemants = document.createElement('option')
        computers_elemants.value = computer.name
        computers_elemants.innerHTML = `
        ${computer.name} ` ;
        COMPUTERS_CONTAINER.appendChild(computers_elemants) 
         
        
    })

}


document.addEventListener('DOMContentLoaded',()=> {
    fetch_computers();
    setupEventListeners();

})

function setupEventListeners(){
    GETCOMPUTERS_FROM.addEventListener('submit',get_computer_data)

}

function displayData(result) {
    console.log("📦 displayData קיבלה את:", result);

    const data = result.data;

    if (!data || !data.content) {
        console.warn("⚠ אין תוכן להצגה – data או data.content ריק/undefined");
        return;
    }

    document.getElementById("result").textContent = data.content;
}

async function get_computer_data(event){
    event.preventDefault();
    const NEW_REQUEST = {f_date:document.getElementById("f_date").value,
                        t_date:document.getElementById("t_date").value,
    machine : document.getElementById("machine").value};

    const RESULT = await get_data(NEW_REQUEST)

    if (RESULT && RESULT.success) {
    console.log("✔ נתונים שהתקבלו:", RESULT.data);
    displayData(RESULT);
    } else {        displayData({ data: { machine_name: "ERROR", content: "NO DATA" } });
    }

};



async function get_data(NEW_REQUEST){
    console.log(`${API_URL}/computers/${NEW_REQUEST.machine}?f_date=${NEW_REQUEST.f_date}&t_date=${NEW_REQUEST.t_date}`)
    try{
        const response = await fetch(`${API_URL}/computers/${NEW_REQUEST.machine}?f_date=${NEW_REQUEST.f_date}&t_date=${NEW_REQUEST.t_date}`,{
            method:'GET',
            headers: {
                'Content-type': 'application/json'
            }             
        });
        const result = await response.json();
        if (response.ok){
            return{success: true, data:result};
        }else{
            return {success:false,error:result.error}
        }
    } catch(error){
        console.error('error get computer data',error);
        return {success:false , error:'cant get data'}
    }
}
